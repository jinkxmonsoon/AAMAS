#!/usr/bin/env python3
"""Run frozen uncalibrated CCT diagnostic scoring.

This script executes the Task 17 fixed-weight diagnostic variants. It does not
calibrate, tune, grid search, run LOSO, refine outputs, run ablations, perform
statistical tests, or produce paper-ready result tables.
"""

from __future__ import annotations

import hashlib
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from cctdiag.diagnosis.cct_ranking import rank_trace_candidates, top_ranked_by_trace  # noqa: E402
from cctdiag.diagnosis.cct_scoring import score_variant_rows  # noqa: E402

CONFIG_PATH = ROOT / "configs/cct_scoring.yaml"
FEATURES_PATH = ROOT / "data/interim/journal_v1_full_trace_cct/cct_features.jsonl"
CORPUS_PATH = ROOT / "data/processed/journal_v1_full_trace/main_full_trace_all.jsonl"
TASK15_BASELINE_PATH = ROOT / "results/raw/journal_v1_full_trace/main_full_trace_baseline_sanity.json"
RAW_OUT = ROOT / "results/raw/journal_v1_full_trace_cct/cct_uncalibrated_diagnostics.json"
REPORT_DIR = ROOT / "results/reports/journal_v1_full_trace_cct"
REPORT_PATH = REPORT_DIR / "cct_uncalibrated_diagnostics_report.md"
SHORTCUT_PATH = REPORT_DIR / "cct_uncalibrated_shortcut_interpretation.md"


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    with path.open(encoding="utf-8") as handle:
        return [json.loads(line) for line in handle if line.strip()]


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _accuracy(correct: int, total: int) -> float | None:
    return None if total == 0 else correct / total


def _macro(records: list[dict[str, Any]], group_field: str, correct_field: str) -> dict[str, Any]:
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for record in records:
        grouped[str(record[group_field])].append(record)
    per_group = {}
    for group, rows in sorted(grouped.items()):
        per_group[group] = {
            "accuracy": _accuracy(sum(1 for row in rows if row[correct_field]), len(rows)),
            "n": len(rows),
        }
    values = [group["accuracy"] for group in per_group.values() if group["accuracy"] is not None]
    return {"macro_accuracy": sum(values) / len(values) if values else None, "per_group": per_group}


def _evaluate_predictions(predictions: dict[str, dict[str, Any]], labels: dict[str, dict[str, Any]]) -> dict[str, Any]:
    rows = []
    for trace_id, label in labels.items():
        pred = predictions[trace_id]
        step_correct = pred["step_id"] == label["gold_step"]
        agent_correct = pred["agent_id"] == label["gold_agent"]
        rows.append(
            {
                "trace_id": trace_id,
                "scenario_group": label["scenario_group"],
                "perturbation_type": label["perturbation_type"],
                "case_variant_group": "clean" if label["case_variant"] == "clean" else "perturbed",
                "step_correct": step_correct,
                "agent_correct": agent_correct,
                "tuple_correct": step_correct and agent_correct,
                "top_score_tie_count": pred.get("top_score_tie_count", 1),
            }
        )
    return {
        "step_accuracy": _accuracy(sum(1 for row in rows if row["step_correct"]), len(rows)),
        "agent_accuracy": _accuracy(sum(1 for row in rows if row["agent_correct"]), len(rows)),
        "tuple_step_agent_accuracy": _accuracy(sum(1 for row in rows if row["tuple_correct"]), len(rows)),
        "macro_by_scenario": _macro(rows, "scenario_group", "step_correct"),
        "macro_by_perturbation": _macro(rows, "perturbation_type", "step_correct"),
        "clean_vs_perturbed": _macro(rows, "case_variant_group", "step_correct"),
        "mean_top_score_tie_count": sum(row["top_score_tie_count"] for row in rows) / len(rows) if rows else None,
    }


def _labels_and_step_agents(corpus_rows: list[dict[str, Any]]) -> tuple[dict[str, dict[str, Any]], dict[str, dict[str, str]]]:
    labels: dict[str, dict[str, Any]] = {}
    step_agents: dict[str, dict[str, str]] = {}
    for record in corpus_rows:
        trace_id = record["trace_id"]
        labels[trace_id] = {
            "gold_step": record["private_labels"]["gold_failure_step"],
            "gold_agent": record["private_labels"]["gold_failure_agent"],
            "scenario_group": record["scenario_group"],
            "perturbation_type": record["perturbation_type"],
            "case_variant": record["case_variant"],
        }
        step_agents[trace_id] = {step["step_id"]: step["agent_id"] for step in record["steps"]}
    return labels, step_agents


def _prediction(trace_id: str, step_id: str, step_agents: dict[str, dict[str, str]], score: float = 0.0) -> dict[str, Any]:
    return {
        "trace_id": trace_id,
        "step_id": step_id,
        "agent_id": step_agents[trace_id][step_id],
        "score": score,
        "top_score_tie_count": 1,
    }


def _baseline_predictions(
    baseline_name: str,
    labels: dict[str, dict[str, Any]],
    step_agents: dict[str, dict[str, str]],
    feature_rows: list[dict[str, Any]],
) -> dict[str, dict[str, Any]]:
    trace_ids = sorted(labels)
    by_trace_features: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in feature_rows:
        by_trace_features[row["trace_id"]].append(row)

    if baseline_name == "majority_step":
        step = sorted(Counter(label["gold_step"] for label in labels.values()).items(), key=lambda item: (-item[1], item[0]))[0][0]
        return {trace_id: _prediction(trace_id, step, step_agents) for trace_id in trace_ids}
    if baseline_name == "majority_agent":
        agent = sorted(Counter(label["gold_agent"] for label in labels.values()).items(), key=lambda item: (-item[1], item[0]))[0][0]
        return {
            trace_id: _prediction(trace_id, next(step for step, step_agent in step_agents[trace_id].items() if step_agent == agent), step_agents)
            for trace_id in trace_ids
        }
    if baseline_name == "always_s2":
        return {trace_id: _prediction(trace_id, "s2", step_agents) for trace_id in trace_ids}
    if baseline_name == "first_step":
        return {trace_id: _prediction(trace_id, sorted(step_agents[trace_id])[0], step_agents) for trace_id in trace_ids}
    if baseline_name == "last_step":
        return {trace_id: _prediction(trace_id, sorted(step_agents[trace_id])[-1], step_agents) for trace_id in trace_ids}
    if baseline_name == "most_detailed_step":
        return {
            trace_id: _prediction(
                trace_id,
                max(by_trace_features[trace_id], key=lambda row: (row["input_token_count"] + row["output_token_count"] + row["tool_output_token_count"], -row["order_index"]))["step_id"],
                step_agents,
            )
            for trace_id in trace_ids
        }
    if baseline_name == "simple_spectrum_visible_step":
        return {
            trace_id: _prediction(
                trace_id,
                max(by_trace_features[trace_id], key=lambda row: (row["evidence_used_count"] + row["has_tool_call"] + row["out_degree"], -row["order_index"]))["step_id"],
                step_agents,
            )
            for trace_id in trace_ids
        }
    if baseline_name == "simple_spectrum_visible_agent":
        return {
            trace_id: _prediction(
                trace_id,
                max(by_trace_features[trace_id], key=lambda row: (row["evidence_used_count"] + row["has_tool_call"] + row["out_degree"], -row["order_index"]))["step_id"],
                step_agents,
            )
            for trace_id in trace_ids
        }
    raise ValueError(f"unknown baseline {baseline_name}")


def _run_variants(config: dict[str, Any], features: list[dict[str, Any]], labels: dict[str, dict[str, Any]]) -> dict[str, Any]:
    outputs = {}
    for variant_name, variant in config["variants"].items():
        scored = score_variant_rows(features, variant)
        ranked = rank_trace_candidates(scored)
        top = top_ranked_by_trace(ranked)
        outputs[variant_name] = {
            "variant_status": variant["status"],
            "uses_position_or_identity_features": variant["uses_position_or_identity_features"],
            "metrics": _evaluate_predictions(top, labels),
            "prediction_count": len(top),
        }
    return outputs


def _run_baselines(labels: dict[str, dict[str, Any]], step_agents: dict[str, dict[str, str]], features: list[dict[str, Any]]) -> dict[str, Any]:
    names = [
        "majority_step",
        "majority_agent",
        "always_s2",
        "first_step",
        "last_step",
        "most_detailed_step",
        "simple_spectrum_visible_step",
        "simple_spectrum_visible_agent",
    ]
    return {name: {"metrics": _evaluate_predictions(_baseline_predictions(name, labels, step_agents, features), labels)} for name in names}


def _interpret(variant_results: dict[str, Any], baseline_results: dict[str, Any]) -> dict[str, Any]:
    primary = variant_results["cct_primary_no_position"]["metrics"]
    primary_step = primary["step_accuracy"]
    position_step = variant_results["cct_with_position_features"]["metrics"]["step_accuracy"]
    flow_step = variant_results["cct_flow_only"]["metrics"]["step_accuracy"]
    context_step = variant_results["cct_context_only"]["metrics"]["step_accuracy"]
    baseline_best = max(result["metrics"]["step_accuracy"] for result in baseline_results.values())
    clean = primary["clean_vs_perturbed"]["per_group"].get("clean", {}).get("accuracy")
    perturbed = primary["clean_vs_perturbed"]["per_group"].get("perturbed", {}).get("accuracy")

    warnings = []
    h1_status = "diagnostic_weakened"
    h2_status = "diagnostic_weakened"
    if primary_step is not None and primary_step <= 0.30:
        warnings.append("primary CCT is near random/plausible-candidate baseline; H1 remains unsupported")
        h1_status = "unsupported_in_this_diagnostic_run"
    if position_step is not None and primary_step is not None and position_step > primary_step:
        warnings.append("high-risk position diagnostic exceeds primary CCT; structural claim is at risk")
    if flow_step is not None and flow_step <= 0.30:
        warnings.append("flow-only diagnostic is near random; handoff/propagation claims are weakened")
    if context_step is not None and primary_step is not None and context_step > primary_step:
        warnings.append("context-only diagnostic exceeds primary CCT; signal may be lexical/contextual")
    if baseline_best is not None and primary_step is not None and baseline_best >= primary_step:
        warnings.append("one or more diagnostic non-CCT/trivial baselines match or exceed primary CCT; H2 is not supported")
        h2_status = "unsupported_in_this_diagnostic_run"
    if clean is not None and perturbed is not None and clean - perturbed >= 0.15:
        warnings.append("clean performance is much higher than perturbed performance; robustness claims remain blocked")

    if h1_status != "unsupported_in_this_diagnostic_run" and primary_step is not None and primary_step > 0.30:
        h1_status = "diagnostic_supported_with_shortcut_warnings"
    if h2_status != "unsupported_in_this_diagnostic_run" and primary_step is not None and baseline_best is not None and primary_step > baseline_best:
        h2_status = "diagnostic_supported_with_shortcut_warnings"

    return {
        "warnings": warnings,
        "h1_status": h1_status,
        "h2_status": h2_status,
        "h6_status": "future_structural_analysis_only_no_h6_scoring_in_this_run",
        "best_diagnostic_baseline_step_accuracy": baseline_best,
        "non_actions": [
            "no calibration",
            "no grid search",
            "no LOSO",
            "no refinement",
            "no ablation",
            "no statistical test",
            "no paper-ready result table",
        ],
    }


def _write_reports(result: dict[str, Any]) -> None:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    variants = result["variant_results"]
    baselines = result["diagnostic_baselines"]
    primary = variants["cct_primary_no_position"]["metrics"]

    lines = [
        "# Journal-v1 Full-Trace CCT Uncalibrated Diagnostics Report",
        "",
        "Scope: controlled initial diagnostic run of the Task 17 frozen uncalibrated scoring protocol. This is not a paper-ready result table and does not include calibration, LOSO, grid search, refinement, ablation, or statistical testing.",
        "",
        f"- Branch: `{result['provenance']['branch']}`",
        f"- Execution HEAD: `{result['provenance']['head']}`",
        f"- `configs/cct_scoring.yaml` SHA256 before execution: `{result['provenance']['config_sha256_before_execution']}`",
        "",
        "## Variant metrics",
        "",
        "| Variant | Step accuracy | Agent accuracy | Tuple step-agent accuracy | Clean step accuracy | Perturbed step accuracy |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for name, payload in variants.items():
        metrics = payload["metrics"]
        clean = metrics["clean_vs_perturbed"]["per_group"].get("clean", {}).get("accuracy")
        perturbed = metrics["clean_vs_perturbed"]["per_group"].get("perturbed", {}).get("accuracy")
        lines.append(
            f"| `{name}` | {metrics['step_accuracy']:.6f} | {metrics['agent_accuracy']:.6f} | {metrics['tuple_step_agent_accuracy']:.6f} | {clean:.6f} | {perturbed:.6f} |"
        )
    lines.extend(
        [
            "",
            "## Primary macro by scenario",
            "",
            "| Scenario | Step accuracy | n |",
            "|---|---:|---:|",
        ]
    )
    for scenario, payload in primary["macro_by_scenario"]["per_group"].items():
        lines.append(f"| `{scenario}` | {payload['accuracy']:.6f} | {payload['n']} |")
    lines.extend(["", "## Primary macro by perturbation", "", "| Perturbation | Step accuracy | n |", "|---|---:|---:|"])
    for perturbation, payload in primary["macro_by_perturbation"]["per_group"].items():
        lines.append(f"| `{perturbation}` | {payload['accuracy']:.6f} | {payload['n']} |")
    lines.extend(["", "## Diagnostic baseline comparison", "", "| Baseline | Step accuracy | Agent accuracy | Tuple step-agent accuracy |", "|---|---:|---:|---:|"])
    for name, payload in baselines.items():
        metrics = payload["metrics"]
        step = "n/a" if metrics["step_accuracy"] is None else f"{metrics['step_accuracy']:.6f}"
        agent = "n/a" if metrics["agent_accuracy"] is None else f"{metrics['agent_accuracy']:.6f}"
        tuple_acc = "n/a" if metrics["tuple_step_agent_accuracy"] is None else f"{metrics['tuple_step_agent_accuracy']:.6f}"
        lines.append(f"| `{name}` | {step} | {agent} | {tuple_acc} |")
    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            f"- H1 diagnostic status: `{result['interpretation']['h1_status']}`",
            f"- H2 diagnostic status: `{result['interpretation']['h2_status']}`",
            f"- H6 status: `{result['interpretation']['h6_status']}`",
            f"- Warnings: {'; '.join(result['interpretation']['warnings']) if result['interpretation']['warnings'] else 'none'}",
            "- Non-actions: no calibration, grid search, LOSO, refinement, ablation, statistical test, or paper-ready result table was produced.",
        ]
    )
    REPORT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")

    shortcut_lines = [
        "# Journal-v1 Full-Trace CCT Uncalibrated Shortcut Interpretation",
        "",
        "This interpretation applies only to the controlled diagnostic run and is not final journal-grade evidence.",
        "",
        f"- Primary step accuracy: {primary['step_accuracy']:.6f}",
        f"- Flow-only step accuracy: {variants['cct_flow_only']['metrics']['step_accuracy']:.6f}",
        f"- Context-only step accuracy: {variants['cct_context_only']['metrics']['step_accuracy']:.6f}",
        f"- With-position step accuracy: {variants['cct_with_position_features']['metrics']['step_accuracy']:.6f}",
        f"- Best diagnostic baseline step accuracy: {result['interpretation']['best_diagnostic_baseline_step_accuracy']:.6f}",
        "",
        "## Shortcut warnings",
    ]
    shortcut_lines.extend(f"- {warning}" for warning in result["interpretation"]["warnings"])
    shortcut_lines.append("- No calibration, grid search, refinement, ablation, statistical test, or paper-ready result table was produced.")
    SHORTCUT_PATH.write_text("\n".join(shortcut_lines) + "\n", encoding="utf-8")


def main() -> int:
    config_hash = sha256(CONFIG_PATH)
    config = read_json(CONFIG_PATH)
    features = read_jsonl(FEATURES_PATH)
    corpus = read_jsonl(CORPUS_PATH)
    labels, step_agents = _labels_and_step_agents(corpus)
    variant_results = _run_variants(config, features, labels)
    baseline_results = _run_baselines(labels, step_agents, features)
    existing_task15 = read_json(TASK15_BASELINE_PATH) if TASK15_BASELINE_PATH.exists() else None
    interpretation = _interpret(variant_results, baseline_results)

    result = {
        "provenance": {
            "branch": "work",
            "head": __import__("subprocess").check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
            "config_path": str(CONFIG_PATH.relative_to(ROOT)),
            "config_sha256_before_execution": config_hash,
            "protocol_version": config["protocol_version"],
        },
        "variant_results": variant_results,
        "diagnostic_baselines": baseline_results,
        "existing_task15_baseline_sanity": existing_task15,
        "interpretation": interpretation,
    }
    RAW_OUT.parent.mkdir(parents=True, exist_ok=True)
    RAW_OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    _write_reports(result)

    primary = variant_results["cct_primary_no_position"]["metrics"]
    print("=== Frozen Uncalibrated CCT Diagnostics ===")
    print(f"Config SHA256 before execution: {config_hash}")
    print(f"Primary step accuracy: {primary['step_accuracy']:.6f}")
    print(f"Primary agent accuracy: {primary['agent_accuracy']:.6f}")
    print(f"Primary tuple accuracy: {primary['tuple_step_agent_accuracy']:.6f}")
    for name in config["variants"]:
        print(f"{name} step accuracy: {variant_results[name]['metrics']['step_accuracy']:.6f}")
    print(f"H1 status: {interpretation['h1_status']}")
    print(f"H2 status: {interpretation['h2_status']}")
    print("FINAL: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
