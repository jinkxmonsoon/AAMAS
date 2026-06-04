#!/usr/bin/env python3
"""Run flat-log and spectrum-inspired non-CCT baseline diagnostics.

This diagnostic layer checks whether transparent non-CCT heuristics already
solve BRACIS-Journal-v1. It does not implement CCT graph construction, CCT
scoring, calibration, refinement variants, ablations, or paper-ready tables.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from cctdiag.baselines.flat_log import flat_log_keyword_agent, flat_log_keyword_step, flat_log_role_agent  # noqa: E402
from cctdiag.baselines.spectrum import spectrum_inspired_agent, spectrum_inspired_step  # noqa: E402
from cctdiag.io.loaders import load_jsonl  # noqa: E402
from cctdiag.io.views import make_prediction_view  # noqa: E402
from cctdiag.metrics.attribution import (  # noqa: E402
    agent_accuracy,
    irreversibility_accuracy,
    macro_accuracy_by_perturbation,
    macro_accuracy_by_scenario,
    propagation_accuracy,
    recoverability_accuracy,
    step_accuracy,
    tuple_accuracy_step_agent,
)

CORPUS = ROOT / "data/processed/journal_v1/main_all_traces.jsonl"
RAW_OUTPUT = ROOT / "results/raw/journal_v1/non_cct_baseline_diagnostics.json"
REPORT_OUTPUT = ROOT / "results/reports/journal_v1/non_cct_baseline_diagnostics_report.md"
REVIEW_THRESHOLD = 0.70
BLOCK_THRESHOLD = 0.85


def pct(value: float | None) -> str:
    if value is None:
        return "NA"
    return f"{value * 100.0:.2f}%"


def merge_predictions(*prediction_sets: list[dict[str, Any]]) -> list[dict[str, Any]]:
    if not prediction_sets:
        return []
    n = len(prediction_sets[0])
    if any(len(predictions) != n for predictions in prediction_sets):
        raise ValueError("prediction sets must have the same length")
    merged = []
    for index in range(n):
        row_prediction: dict[str, Any] = {}
        for predictions in prediction_sets:
            row_prediction.update(predictions[index])
        merged.append(row_prediction)
    return merged


def metric_block(records: list[dict[str, Any]], predictions: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "step_accuracy": step_accuracy(records, predictions),
        "agent_accuracy": agent_accuracy(records, predictions),
        "tuple_accuracy_step_agent": tuple_accuracy_step_agent(records, predictions),
        "irreversibility_accuracy": irreversibility_accuracy(records, predictions),
        "propagation_accuracy": propagation_accuracy(records, predictions),
        "recoverability_accuracy": recoverability_accuracy(records, predictions),
        "macro_by_scenario": macro_accuracy_by_scenario(records, predictions),
        "macro_by_perturbation": macro_accuracy_by_perturbation(records, predictions),
    }


def interpret_non_cct_risk(results: dict[str, dict[str, Any]]) -> dict[str, Any]:
    blockers: list[str] = []
    review_flags: list[str] = []
    for baseline_name, metrics in results.items():
        for metric_name in ("step_accuracy", "agent_accuracy"):
            value = metrics.get(metric_name)
            if not isinstance(value, int | float):
                continue
            label = f"{baseline_name}.{metric_name}={value:.4f}"
            if value > BLOCK_THRESHOLD:
                blockers.append(f"{label} exceeds block threshold {BLOCK_THRESHOLD:.2f}")
            elif value > REVIEW_THRESHOLD:
                review_flags.append(f"{label} exceeds review threshold {REVIEW_THRESHOLD:.2f}")
    status = "blocked" if blockers else ("review" if review_flags else "passed")
    return {"status": status, "blockers": blockers, "review_flags": review_flags}


def macro_text(macro: dict[str, Any]) -> str:
    return pct(macro.get("macro_accuracy"))


def format_macro_details(macro: dict[str, Any]) -> list[str]:
    lines = ["| group | n | step accuracy |", "|---|---:|---:|"]
    for group, entry in macro.get("per_group", {}).items():
        lines.append(f"| {group} | {entry.get('n')} | {pct(entry.get('accuracy'))} |")
    return lines


def main() -> int:
    records = load_jsonl(str(CORPUS))
    prediction_views = [make_prediction_view(record) for record in records]
    RAW_OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    REPORT_OUTPUT.parent.mkdir(parents=True, exist_ok=True)

    flat_step = flat_log_keyword_step(prediction_views)
    flat_agent = flat_log_keyword_agent(prediction_views)
    flat_role_agent = flat_log_role_agent(prediction_views)
    spectrum_step = spectrum_inspired_step(prediction_views)
    spectrum_agent = spectrum_inspired_agent(prediction_views)

    baseline_predictions = {
        "flat_log_keyword_step": flat_step,
        "flat_log_keyword_agent": flat_agent,
        "flat_log_role_agent": flat_role_agent,
        "flat_log_keyword_step_agent": merge_predictions(flat_step, flat_agent),
        "spectrum_inspired_step": spectrum_step,
        "spectrum_inspired_agent": spectrum_agent,
        "spectrum_inspired_step_agent": merge_predictions(spectrum_step, spectrum_agent),
    }
    results = {name: metric_block(records, predictions) for name, predictions in baseline_predictions.items()}
    interpretation = interpret_non_cct_risk(results)

    payload = {
        "scope": {
            "corpus": str(CORPUS.relative_to(ROOT)),
            "diagnostic_baseline_layer_only": True,
            "not_cct_evaluation": True,
            "not_calibrated": True,
            "not_final_paper_result_table": True,
            "simple_non_cct_shortcut_detection": True,
            "uses_prediction_view_only": True,
            "cct_graph_construction_implemented": False,
            "cct_scoring_implemented": False,
            "calibration_implemented": False,
            "refinement_variant_implemented": False,
            "ablation_implemented": False,
        },
        "thresholds": {"review": REVIEW_THRESHOLD, "block": BLOCK_THRESHOLD},
        "n_records": len(records),
        "baseline_results": results,
        "diagnostic_interpretation": interpretation,
        "example_raw_record": records[0] if records else None,
        "example_prediction_view": prediction_views[0] if prediction_views else None,
    }
    RAW_OUTPUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    lines = [
        "# Journal-v1 Non-CCT Baseline Diagnostics Report",
        "",
        "## Scope and prohibitions",
        f"- Corpus: `{CORPUS.relative_to(ROOT)}`.",
        f"- Total records: {len(records)}.",
        "- This is a **diagnostic baseline layer only**.",
        "- This is **not CCT evaluation**.",
        "- This is **not calibrated**.",
        "- This is **not a final paper result table**.",
        "- This is intended to detect whether simple non-CCT heuristics already solve the corpus.",
        "- Baselines operate on `make_prediction_view(record)` outputs only, not raw records.",
        "- No CCT graph construction, CCT scoring, calibration, refinement variant, ablation, or paper-ready result table was implemented.",
        "",
        "## Diagnostic interpretation rules",
        f"- Accuracy greater than {REVIEW_THRESHOLD:.0%} on step or agent attribution flags corpus/baseline review.",
        f"- Accuracy greater than {BLOCK_THRESHOLD:.0%} on step or agent attribution blocks evaluation pending investigation.",
        "- If non-CCT baselines remain moderate, CCT implementation may proceed only in a later approved task.",
        "",
        "## Baseline summary",
        "| baseline | step accuracy | agent accuracy | tuple step-agent accuracy | irreversibility | propagation | recoverability | macro scenario | macro perturbation |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for baseline_name, metrics in results.items():
        lines.append(
            "| "
            + " | ".join(
                [
                    baseline_name,
                    pct(metrics["step_accuracy"]),
                    pct(metrics["agent_accuracy"]),
                    pct(metrics["tuple_accuracy_step_agent"]),
                    pct(metrics["irreversibility_accuracy"]),
                    pct(metrics["propagation_accuracy"]),
                    pct(metrics["recoverability_accuracy"]),
                    macro_text(metrics["macro_by_scenario"]),
                    macro_text(metrics["macro_by_perturbation"]),
                ]
            )
            + " |"
        )

    lines.extend(["", "## Macro-by-scenario details (step accuracy)"])
    for baseline_name, metrics in results.items():
        lines.extend(["", f"### {baseline_name}", *format_macro_details(metrics["macro_by_scenario"])])

    lines.extend(["", "## Macro-by-perturbation details (step accuracy)"])
    for baseline_name, metrics in results.items():
        lines.extend(["", f"### {baseline_name}", *format_macro_details(metrics["macro_by_perturbation"])])

    lines.extend(
        [
            "",
            "## Diagnostic interpretation",
            f"- Gate status: **{interpretation['status'].upper()}**.",
            "- Blockers: " + ("; ".join(interpretation["blockers"]) if interpretation["blockers"] else "none."),
            "- Review flags: "
            + ("; ".join(interpretation["review_flags"]) if interpretation["review_flags"] else "none."),
            f"- Raw JSON output: `{RAW_OUTPUT.relative_to(ROOT)}`.",
            "",
            "## Example sanitized prediction view",
            "",
            "```json",
            json.dumps(prediction_views[0] if prediction_views else {}, indent=2, sort_keys=True),
            "```",
        ]
    )
    REPORT_OUTPUT.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print("=== Non-CCT Baseline Diagnostics ===")
    print(f"records: {len(records)}")
    print(f"raw: {RAW_OUTPUT.relative_to(ROOT)}")
    print(f"report: {REPORT_OUTPUT.relative_to(ROOT)}")
    print(f"gate: {interpretation['status'].upper()}")
    if interpretation["blockers"]:
        print("blockers:")
        for blocker in interpretation["blockers"]:
            print(f"  - {blocker}")
    if interpretation["review_flags"]:
        print("review flags:")
        for flag in interpretation["review_flags"]:
            print(f"  - {flag}")
    print("FINAL: DIAGNOSTIC_COMPLETE")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
