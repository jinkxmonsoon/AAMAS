#!/usr/bin/env python3
"""Run shortcut baseline and semantic diversity diagnostics on full-trace pilot.

Diagnostic only: no CCT graph construction/scoring, calibration, refinement,
ablations, paper claims, or paper-ready result tables.
"""

from __future__ import annotations

import json
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Callable

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from cctdiag.io.full_trace_views import make_full_trace_prediction_view  # noqa: E402
from cctdiag.metrics.attribution import (  # noqa: E402
    agent_accuracy,
    macro_accuracy_by_perturbation,
    macro_accuracy_by_scenario,
    step_accuracy,
    tuple_accuracy_step_agent,
)

PILOT_PATH = ROOT / "data/interim/journal_v1_full_trace_pilot/full_trace_pilot_all.jsonl"
REPORT_DIR = ROOT / "results/reports/journal_v1_full_trace_pilot"
SHORTCUT_REPORT = REPORT_DIR / "full_trace_pilot_shortcut_baseline_report.md"
DIVERSITY_REPORT = REPORT_DIR / "full_trace_pilot_semantic_diversity_report.md"
READINESS_REPORT = REPORT_DIR / "full_trace_pilot_readiness_gate.md"
REVIEW_THRESHOLD = 0.70
BLOCK_THRESHOLD = 0.85
LEAKAGE_TERMS = (
    "gold",
    "label",
    "failure marker",
    "failing step",
    "root cause",
    "ground truth",
    "known failure",
    "decisive error",
    "culprit",
    "target step",
)

PredictionFn = Callable[[list[dict[str, Any]], list[dict[str, Any]]], list[dict[str, Any]]]


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def eval_records(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    records = []
    for row in rows:
        labels = row["private_labels"]
        records.append(
            {
                "trace_id": row["trace_id"],
                "scenario_group": row["scenario_group"],
                "perturbation_type": row["perturbation_type"],
                "gold_failure_step": labels["gold_failure_step"],
                "gold_failure_agent": labels["gold_failure_agent"],
            }
        )
    return records


def pct(value: float | None) -> str:
    return "NA" if value is None else f"{value * 100:.2f}%"


def step_text(step: dict[str, Any]) -> str:
    return " ".join(
        str(step.get(field) or "")
        for field in ("input_message", "output_message", "tool_call", "tool_output", "visible_step_notes")
    )


def step_len(step: dict[str, Any]) -> int:
    return len(step_text(step))


def first_step(views, _records):
    return [{"predicted_failure_step": view["candidate_steps"][0]} for view in views]


def last_step(views, _records):
    return [{"predicted_failure_step": view["candidate_steps"][-1]} for view in views]


def first_agent(views, _records):
    return [{"predicted_failure_agent": view["candidate_agents"][0]} for view in views]


def last_agent(views, _records):
    return [{"predicted_failure_agent": view["candidate_agents"][-1]} for view in views]


def always_s2(views, _records):
    return [{"predicted_failure_step": "s2"} for _ in views]


def majority_step(views, records):
    value = Counter(record["gold_failure_step"] for record in records).most_common(1)[0][0]
    return [{"predicted_failure_step": value} for _ in views]


def majority_agent(views, records):
    value = Counter(record["gold_failure_agent"] for record in records).most_common(1)[0][0]
    return [{"predicted_failure_agent": value} for _ in views]


def tool_presence_step(views, _records):
    predictions = []
    for view in views:
        candidates = [step for step in view["steps"] if step.get("tool_call") or step.get("tool_output")]
        predictions.append({"predicted_failure_step": (candidates[0] if candidates else view["steps"][0])["step_id"]})
    return predictions


def most_detailed_step(views, _records):
    return [{"predicted_failure_step": max(view["steps"], key=step_len)["step_id"]} for view in views]


def keyword_degradation_step(views, _records):
    keywords = ("degraded", "ambiguity", "unresolved", "constraint", "warning", "repair", "incomplete")
    predictions = []
    for view in views:
        def score(step):
            text = step_text(step).lower()
            return sum(text.count(keyword) for keyword in keywords), -int(step["step_id"].lstrip("s"))
        predictions.append({"predicted_failure_step": max(view["steps"], key=score)["step_id"]})
    return predictions


def simple_spectrum_visible_step(views, _records):
    predictions = []
    for view in views:
        def score(step):
            text = step_text(step).lower()
            return (
                int(bool(step.get("tool_call")))
                + len(step.get("evidence_items") or [])
                + len(step.get("evidence_used") or [])
                + text.count("ambiguity")
                + text.count("cross-check"),
                -int(step["step_id"].lstrip("s")),
            )
        predictions.append({"predicted_failure_step": max(view["steps"], key=score)["step_id"]})
    return predictions


def simple_spectrum_visible_agent(views, _records):
    predictions = []
    for view in views:
        scores = Counter()
        for step in view["steps"]:
            scores[step["agent_id"]] += int(bool(step.get("tool_call"))) + len(step.get("evidence_used") or [])
        best = sorted(scores.items(), key=lambda item: (-item[1], item[0]))[0][0]
        predictions.append({"predicted_failure_agent": best})
    return predictions


BASELINES: dict[str, PredictionFn] = {
    "majority_step": majority_step,
    "majority_agent": majority_agent,
    "always_s2": always_s2,
    "first_step": first_step,
    "last_step": last_step,
    "first_agent": first_agent,
    "last_agent": last_agent,
    "tool_presence_step": tool_presence_step,
    "most_detailed_step": most_detailed_step,
    "keyword_degradation_step": keyword_degradation_step,
    "simple_spectrum_visible_step": simple_spectrum_visible_step,
    "simple_spectrum_visible_agent": simple_spectrum_visible_agent,
}


def metric_block(records, predictions):
    return {
        "step_accuracy": step_accuracy(records, predictions),
        "agent_accuracy": agent_accuracy(records, predictions),
        "tuple_accuracy_step_agent": tuple_accuracy_step_agent(records, predictions),
        "macro_by_scenario": macro_accuracy_by_scenario(records, predictions),
        "macro_by_perturbation": macro_accuracy_by_perturbation(records, predictions),
    }


def interpret(results):
    blockers = []
    review = []
    for name, metrics in results.items():
        for metric_name in ("step_accuracy", "agent_accuracy"):
            value = metrics[metric_name]
            if value is None:
                continue
            label = f"{name}.{metric_name}={value:.4f}"
            if value > BLOCK_THRESHOLD:
                blockers.append(f"{label} exceeds pilot block threshold {BLOCK_THRESHOLD:.2f}")
            elif value > REVIEW_THRESHOLD:
                review.append(f"{label} exceeds pilot review threshold {REVIEW_THRESHOLD:.2f}")
    return {"status": "blocked" if blockers else ("review" if review else "passed"), "blockers": blockers, "review_flags": review}


def semantic_diversity(rows, views):
    leakage_hits = []
    step_counts = []
    agent_counts = []
    gold_tool = non_gold_tool = 0
    gold_evidence = non_gold_evidence = 0
    gold_lengths = []
    non_gold_lengths = []
    gold_only_tool = []
    by_trace = []
    for row, view in zip(rows, views, strict=True):
        gold_step = row["private_labels"]["gold_failure_step"]
        step_counts.append(len(view["steps"]))
        agent_counts.append(len(view["candidate_agents"]))
        trace_gold_lengths = []
        trace_non_gold_lengths = []
        for step in view["steps"]:
            text_lower = step_text(step).lower()
            for term in LEAKAGE_TERMS:
                if term in text_lower:
                    leakage_hits.append({"trace_id": view["trace_id"], "step_id": step["step_id"], "term": term})
            has_tool = bool(step.get("tool_call") or step.get("tool_output"))
            has_evidence = bool(step.get("evidence_items") or step.get("evidence_used"))
            length = step_len(step)
            if step["step_id"] == gold_step:
                gold_tool += int(has_tool)
                gold_evidence += int(has_evidence)
                gold_lengths.append(length)
                trace_gold_lengths.append(length)
            else:
                non_gold_tool += int(has_tool)
                non_gold_evidence += int(has_evidence)
                non_gold_lengths.append(length)
                trace_non_gold_lengths.append(length)
        if gold_tool and not any(
            (step["step_id"] != gold_step and (step.get("tool_call") or step.get("tool_output"))) for step in view["steps"]
        ):
            gold_only_tool.append(view["trace_id"])
        gold_len = trace_gold_lengths[0]
        avg_non_gold = sum(trace_non_gold_lengths) / len(trace_non_gold_lengths)
        by_trace.append({"trace_id": view["trace_id"], "gold_length": gold_len, "avg_non_gold_length": avg_non_gold})
    avg_gold = sum(gold_lengths) / len(gold_lengths)
    avg_non_gold = sum(non_gold_lengths) / len(non_gold_lengths)
    ratio = avg_gold / avg_non_gold if avg_non_gold else 0
    systematic = ratio > 1.25
    return {
        "steps_per_trace": {"min": min(step_counts), "max": max(step_counts), "avg": sum(step_counts) / len(step_counts)},
        "agents_per_trace": {"min": min(agent_counts), "max": max(agent_counts), "avg": sum(agent_counts) / len(agent_counts)},
        "tool_call_distribution": {"gold_steps_with_tool": gold_tool, "non_gold_steps_with_tool": non_gold_tool},
        "evidence_distribution": {"gold_steps_with_evidence": gold_evidence, "non_gold_steps_with_evidence": non_gold_evidence},
        "visible_text_length": {"avg_gold_step": avg_gold, "avg_non_gold_step": avg_non_gold, "gold_to_non_gold_ratio": ratio},
        "gold_steps_systematically_more_detailed": systematic,
        "gold_only_tool_traces": gold_only_tool,
        "leakage_hits": leakage_hits,
        "per_trace_lengths": by_trace,
    }


def table(results):
    lines = [
        "| baseline | step accuracy | agent accuracy | tuple accuracy | macro scenario | macro perturbation |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for name, metrics in results.items():
        lines.append(
            f"| {name} | {pct(metrics['step_accuracy'])} | {pct(metrics['agent_accuracy'])} | "
            f"{pct(metrics['tuple_accuracy_step_agent'])} | {pct(metrics['macro_by_scenario']['macro_accuracy'])} | "
            f"{pct(metrics['macro_by_perturbation']['macro_accuracy'])} |"
        )
    return lines


def write_reports(results, interpretation, diversity, readiness):
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    SHORTCUT_REPORT.write_text(
        "\n".join(
            [
                "# Full-Trace Pilot Shortcut Baseline Report",
                "",
                "## Scope",
                "- Diagnostic pilot baselines only; not CCT evaluation and not paper evidence.",
                "- Baselines operate only on sanitized full-trace prediction views.",
                "- Pilot thresholds are diagnostic and interpreted cautiously for n=14.",
                "",
                "## Thresholds",
                f"- review if step/agent accuracy > {REVIEW_THRESHOLD:.0%}.",
                f"- block if step/agent accuracy > {BLOCK_THRESHOLD:.0%}.",
                "",
                "## Baseline results",
                *table(results),
                "",
                "## Interpretation",
                f"- status: {interpretation['status'].upper()}",
                "- blockers: " + ("; ".join(interpretation["blockers"]) if interpretation["blockers"] else "none."),
                "- review flags: " + ("; ".join(interpretation["review_flags"]) if interpretation["review_flags"] else "none."),
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    DIVERSITY_REPORT.write_text(
        "\n".join(
            [
                "# Full-Trace Pilot Semantic Diversity Report",
                "",
                "## Scope",
                "- Diagnostic semantic diversity audit for the non-final pilot.",
                "",
                "## Step and agent counts",
                f"- steps per trace: min={diversity['steps_per_trace']['min']}, max={diversity['steps_per_trace']['max']}, avg={diversity['steps_per_trace']['avg']:.2f}.",
                f"- agents per trace: min={diversity['agents_per_trace']['min']}, max={diversity['agents_per_trace']['max']}, avg={diversity['agents_per_trace']['avg']:.2f}.",
                "",
                "## Tool and evidence distribution",
                f"- gold steps with tool calls: {diversity['tool_call_distribution']['gold_steps_with_tool']}.",
                f"- non-gold steps with tool calls: {diversity['tool_call_distribution']['non_gold_steps_with_tool']}.",
                f"- gold steps with evidence: {diversity['evidence_distribution']['gold_steps_with_evidence']}.",
                f"- non-gold steps with evidence: {diversity['evidence_distribution']['non_gold_steps_with_evidence']}.",
                "",
                "## Visible text length",
                f"- average gold step visible length: {diversity['visible_text_length']['avg_gold_step']:.2f}.",
                f"- average non-gold step visible length: {diversity['visible_text_length']['avg_non_gold_step']:.2f}.",
                f"- gold/non-gold length ratio: {diversity['visible_text_length']['gold_to_non_gold_ratio']:.3f}.",
                f"- gold steps systematically more detailed: {'yes' if diversity['gold_steps_systematically_more_detailed'] else 'no'}.",
                "",
                "## Leakage terms",
                "- hits: " + (json.dumps(diversity["leakage_hits"], sort_keys=True) if diversity["leakage_hits"] else "none."),
                "",
                "## Gold-only tool-call traces",
                "- traces: " + (", ".join(diversity["gold_only_tool_traces"]) if diversity["gold_only_tool_traces"] else "none."),
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    READINESS_REPORT.write_text(
        "\n".join(
            [
                "# Full-Trace Pilot Readiness Gate",
                "",
                "## Decision",
                f"- FULL_TRACE_PILOT_READY_FOR_MAIN_CORPUS = {'yes' if readiness['ready'] else 'no'}",
                "- This permits only a future explicitly approved full-trace main corpus builder task if yes.",
                "- The old failure-centered corpus remains blocked regardless of this pilot decision.",
                "",
                "## Blockers",
                *( ["- none."] if not readiness["blockers"] else [f"- {blocker}" for blocker in readiness["blockers"]] ),
                "",
                "## Scope prohibitions",
                "- No full 420-trace corpus was generated.",
                "- No CCT scoring, calibration, refinement, ablation, or paper-ready result table was produced.",
            ]
        )
        + "\n",
        encoding="utf-8",
    )


def main() -> int:
    rows = load_jsonl(PILOT_PATH)
    views = [make_full_trace_prediction_view(row) for row in rows]
    records = eval_records(rows)
    predictions = {name: fn(views, records) for name, fn in BASELINES.items()}
    results = {name: metric_block(records, pred) for name, pred in predictions.items()}
    interpretation = interpret(results)
    diversity = semantic_diversity(rows, views)
    blockers = list(interpretation["blockers"])
    if diversity["leakage_hits"]:
        blockers.append("visible-step lexical leakage terms detected")
    if diversity["gold_steps_systematically_more_detailed"]:
        blockers.append("gold steps are systematically more detailed than non-gold steps")
    if diversity["gold_only_tool_traces"]:
        blockers.append("some gold steps are the only steps with tool calls")
    readiness = {"ready": not blockers, "blockers": blockers}
    write_reports(results, interpretation, diversity, readiness)
    print("=== Full-Trace Pilot Baseline Sanity ===")
    for name, metrics in results.items():
        print(
            f"{name}: step={pct(metrics['step_accuracy'])} agent={pct(metrics['agent_accuracy'])} "
            f"tuple={pct(metrics['tuple_accuracy_step_agent'])}"
        )
    print(f"leakage_hits: {len(diversity['leakage_hits'])}")
    print(f"gold_steps_systematically_more_detailed: {diversity['gold_steps_systematically_more_detailed']}")
    print(f"FULL_TRACE_PILOT_READY_FOR_MAIN_CORPUS: {'yes' if readiness['ready'] else 'no'}")
    print("FINAL:", "PASS" if readiness["ready"] else "FAIL")
    return 0 if readiness["ready"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
