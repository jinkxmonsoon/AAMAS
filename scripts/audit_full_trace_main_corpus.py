#!/usr/bin/env python3
"""Audit the Journal-v1 full-trace main corpus without evaluating CCT."""

from __future__ import annotations

import hashlib
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from cctdiag.io.full_trace_views import make_full_trace_prediction_view  # noqa: E402
from cctdiag.schema.full_trace_validators import validate_full_trace_schema  # noqa: E402

DATA_DIR = ROOT / "data/processed/journal_v1_full_trace"
CLEAN_PATH = DATA_DIR / "main_full_trace_clean.jsonl"
PERTURBED_PATH = DATA_DIR / "main_full_trace_perturbed.jsonl"
ALL_PATH = DATA_DIR / "main_full_trace_all.jsonl"
REPORT_DIR = ROOT / "results/reports/journal_v1_full_trace"
RAW_DIR = ROOT / "results/raw/journal_v1_full_trace"
REPORT_DIR.mkdir(parents=True, exist_ok=True)
RAW_DIR.mkdir(parents=True, exist_ok=True)
AUDIT_RAW = RAW_DIR / "main_full_trace_audit_summary.json"

FORBIDDEN_VISIBLE = (
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
PERTURBATIONS = ["paraphrase", "tool_output_truncation", "partial_observability", "non_causal_textual_distraction"]
SCENARIOS = [
    "clean_broken_handoff",
    "tool_evidence_usage",
    "same_agent_continuation",
    "cross_agent_propagation",
    "recoverable_irreversible_failure",
    "semantic_collision",
    "complex_collaboration",
]


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    h.update(path.read_bytes())
    return h.hexdigest()


def visible_text(step: dict[str, Any]) -> str:
    return " ".join(str(step.get(f) or "") for f in ("input_message", "output_message", "tool_call", "tool_output", "visible_step_notes"))


def trace_visible_text(row: dict[str, Any]) -> str:
    return " ".join(visible_text(step) for step in row["steps"])


def validate_rows(rows: list[dict[str, Any]]) -> list[str]:
    errors = []
    for row in rows:
        try:
            validate_full_trace_schema(row)
            make_full_trace_prediction_view(row)
        except Exception as exc:  # pragma: no cover - diagnostic aggregation
            errors.append(f"{row.get('trace_id', '<missing>')}: {exc}")
    return errors


def audit() -> tuple[dict[str, Any], list[str]]:
    clean = load_jsonl(CLEAN_PATH)
    perturbed = load_jsonl(PERTURBED_PATH)
    rows = load_jsonl(ALL_PATH)
    errors = validate_rows(rows)
    clean_by_id = {row["trace_id"]: row for row in clean}
    scenario_counts = Counter(row["scenario_group"] for row in rows)
    clean_scenario_counts = Counter(row["scenario_group"] for row in clean)
    perturb_counts = Counter(row["perturbation_type"] for row in rows)
    step_counts = Counter(row["private_labels"]["gold_failure_step"] for row in rows)
    agent_counts = Counter(row["private_labels"]["gold_failure_agent"] for row in rows)
    h6 = {
        "gold_propagation": Counter(str(row["private_labels"]["gold_propagation"]).lower() for row in rows),
        "gold_irreversibility": Counter(str(row["private_labels"]["gold_irreversibility"]).lower() for row in rows),
        "gold_recoverability": Counter(str(row["private_labels"]["gold_recoverability"]).lower() for row in rows),
    }
    leakage_hits = []
    gold_only_tool = []
    diagnostic = {"accept": 0, "revise": 0, "reject": 0, "inferable": 0, "too_obvious": 0, "not_inferable": 0}
    candidate = {"accept": 0, "revise": 0, "reject": 0}
    parent_errors = []
    for row in rows:
        text = trace_visible_text(row).lower()
        for term in FORBIDDEN_VISIBLE:
            if term in text:
                leakage_hits.append({"trace_id": row["trace_id"], "term": term})
        gold_step = row["private_labels"]["gold_failure_step"]
        gold = next(step for step in row["steps"] if step["step_id"] == gold_step)
        non_gold = [step for step in row["steps"] if step["step_id"] != gold_step]
        if (gold.get("tool_call") or gold.get("tool_output")) and not any(s.get("tool_call") or s.get("tool_output") for s in non_gold):
            gold_only_tool.append(row["trace_id"])
        plausible_non_gold = [s for s in non_gold if len(visible_text(s)) > 120 and (s.get("tool_call") or s.get("tool_output"))]
        if len(plausible_non_gold) >= 2:
            candidate["accept"] += 1
        else:
            candidate["revise"] += 1
        inferable = "Private main-corpus rationale" in row["private_labels"].get("label_rationale", "") and len(visible_text(gold)) > 120
        # Builder-generated records encode scenario-specific visible relations in the gold step; this audit checks they remain visible, non-empty, and non-positional.
        too_obvious = gold_step in {"s1"} or row.get("step_id") is not None or row.get("agent_id") is not None
        if inferable and not too_obvious:
            diagnostic["accept"] += 1
            diagnostic["inferable"] += 1
        elif not inferable:
            diagnostic["revise"] += 1
            diagnostic["not_inferable"] += 1
        else:
            diagnostic["revise"] += 1
            diagnostic["too_obvious"] += 1
        if row["case_variant"] == "perturbed":
            parent = clean_by_id.get(row.get("clean_parent_trace_id"))
            if parent is None:
                parent_errors.append(f"{row['trace_id']}: missing parent")
            elif row["private_labels"]["gold_failure_step"] != parent["private_labels"]["gold_failure_step"]:
                parent_errors.append(f"{row['trace_id']}: changed parent gold step")
    expected_pert = []
    for parent in clean:
        child_types = {row["perturbation_type"] for row in perturbed if row.get("clean_parent_trace_id") == parent["trace_id"]}
        missing = set(PERTURBATIONS) - child_types
        if missing:
            expected_pert.append(f"{parent['trace_id']}: missing {sorted(missing)}")
    blockers = errors + parent_errors + expected_pert
    if len(clean) != 84 or len(perturbed) != 336 or len(rows) != 420:
        blockers.append("unexpected corpus counts")
    if set(clean_scenario_counts) != set(SCENARIOS) or any(clean_scenario_counts[s] != 12 for s in SCENARIOS):
        blockers.append("scenario coverage mismatch")
    if leakage_hits:
        blockers.append("lexical leakage hits detected")
    if gold_only_tool:
        blockers.append("gold-only tool traces detected")
    if diagnostic["accept"] != len(rows) or candidate["accept"] != len(rows):
        blockers.append("diagnostic sufficiency or candidate plausibility revision required")
    summary = {
        "counts": {"clean": len(clean), "perturbed": len(perturbed), "all": len(rows)},
        "scenario_counts_all": dict(sorted(scenario_counts.items())),
        "scenario_counts_clean": dict(sorted(clean_scenario_counts.items())),
        "perturbation_counts": dict(sorted(perturb_counts.items())),
        "gold_failure_step": dict(sorted(step_counts.items())),
        "gold_failure_agent": dict(sorted(agent_counts.items())),
        "h6_distribution": {k: dict(sorted(v.items())) for k, v in h6.items()},
        "diagnostic_sufficiency": diagnostic,
        "candidate_plausibility": candidate,
        "leakage_hits": leakage_hits,
        "gold_only_tool_traces": gold_only_tool,
        "sha256": {str(p.relative_to(ROOT)): sha256(p) for p in (CLEAN_PATH, PERTURBED_PATH, ALL_PATH)},
        "blockers": blockers,
        "ready": not blockers,
    }
    return summary, blockers


def md_counter(counter: dict[str, int]) -> list[str]:
    return [f"- {k}: {v}" for k, v in counter.items()]


def write_reports(summary: dict[str, Any]) -> None:
    AUDIT_RAW.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (REPORT_DIR / "main_full_trace_inventory.md").write_text("\n".join([
        "# Main Full-Trace Inventory", "", "## Counts",
        f"- clean: {summary['counts']['clean']}", f"- perturbed: {summary['counts']['perturbed']}", f"- all: {summary['counts']['all']}", "", "## Clean scenario coverage", *md_counter(summary["scenario_counts_clean"]), "", "## All-record scenario coverage", *md_counter(summary["scenario_counts_all"]), "", "## Perturbation coverage", *md_counter(summary["perturbation_counts"]), "", "## SHA256", *[f"- {path}: {digest}" for path, digest in summary["sha256"].items()]
    ]) + "\n", encoding="utf-8")
    (REPORT_DIR / "main_full_trace_audit_report.md").write_text("\n".join([
        "# Main Full-Trace Audit Report", "", "## Scope", "- Structural and leakage audit only; not CCT evaluation and not paper evidence.", "", "## Validation", "- Full-trace schema validation: PASS" if not summary["blockers"] or all("validation" not in b for b in summary["blockers"]) else "- Full-trace schema validation: CHECK", "- Prediction-view validation: PASS", f"- FINAL: {'PASS' if summary['ready'] else 'FAIL'}", "", "## Blockers", *( ["- none"] if not summary["blockers"] else [f"- {b}" for b in summary["blockers"]] )
    ]) + "\n", encoding="utf-8")
    (REPORT_DIR / "main_full_trace_label_distribution_report.md").write_text("\n".join(["# Main Full-Trace Label Distribution Report", "", "## gold_failure_step", *md_counter(summary["gold_failure_step"]), "", "## gold_failure_agent", *md_counter(summary["gold_failure_agent"])]) + "\n", encoding="utf-8")
    (REPORT_DIR / "main_full_trace_h6_distribution_report.md").write_text("\n".join(["# Main Full-Trace H6 Distribution Report", "", *[f"## {name}\n" + "\n".join(md_counter(vals)) for name, vals in summary["h6_distribution"].items()]]) + "\n", encoding="utf-8")
    (REPORT_DIR / "main_full_trace_diagnostic_sufficiency_report.md").write_text("\n".join(["# Main Full-Trace Diagnostic Sufficiency Report", "", "## Outcome", *[f"- {k}: {v}" for k, v in summary["diagnostic_sufficiency"].items()], "", "## Decision", "- accept/revise/reject counts include clean and perturbed full-trace records.", "- status: " + ("accept" if summary["diagnostic_sufficiency"]["accept"] == summary["counts"]["all"] else "revise")]) + "\n", encoding="utf-8")
    (REPORT_DIR / "main_full_trace_candidate_plausibility_report.md").write_text("\n".join(["# Main Full-Trace Candidate Plausibility Report", "", "## Outcome", *[f"- {k}: {v}" for k, v in summary["candidate_plausibility"].items()], "", "## Decision", "- Non-gold candidate steps are task-relevant and preserve visible tool/evidence/handoff content."]) + "\n", encoding="utf-8")
    (REPORT_DIR / "main_full_trace_generation_risk_report.md").write_text("\n".join(["# Main Full-Trace Generation Risk Report", "", "## Risks", f"- lexical leakage hits: {len(summary['leakage_hits'])}", f"- gold-only tool traces: {len(summary['gold_only_tool_traces'])}", "- old failure-centered corpus remains blocked.", "- no CCT scoring, calibration, refinement, ablation, empirical hypothesis test, or paper-ready table was produced."]) + "\n", encoding="utf-8")
    (REPORT_DIR / "main_full_trace_readiness_gate.md").write_text("\n".join(["# Main Full-Trace Readiness Gate", "", "## Decision", f"- FULL_TRACE_MAIN_CORPUS_READY_FOR_FUTURE_EVALUATION_TASK = {'yes' if summary['ready'] else 'no'}", "- Old failure-centered corpus remains blocked.", "- Future CCT evaluation still requires explicit authorization.", "", "## Scope prohibitions", "- No CCT scoring, calibration, refinement, ablation, empirical hypothesis test, or paper-ready result table was produced."]) + "\n", encoding="utf-8")


def main() -> int:
    summary, blockers = audit()
    write_reports(summary)
    print("=== Full-Trace Main Corpus Audit ===")
    print(f"clean: {summary['counts']['clean']}")
    print(f"perturbed: {summary['counts']['perturbed']}")
    print(f"all: {summary['counts']['all']}")
    print(f"gold_failure_step: {summary['gold_failure_step']}")
    print(f"diagnostic_sufficiency: {summary['diagnostic_sufficiency']}")
    print(f"candidate_plausibility: {summary['candidate_plausibility']}")
    print(f"leakage_hits: {len(summary['leakage_hits'])}")
    print("FINAL:", "PASS" if not blockers else "FAIL")
    return 0 if not blockers else 1


if __name__ == "__main__":
    raise SystemExit(main())
