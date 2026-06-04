#!/usr/bin/env python3
"""Run diagnostic-only trivial baseline sanity checks for Journal-v1.

This script is not a paper-result generator and does not compare against CCT.
It exists only to detect remaining obvious shortcut risks before future method
implementation.
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

from cctdiag.baselines.trivial import TRIVIAL_BASELINES  # noqa: E402
from cctdiag.io.loaders import load_jsonl  # noqa: E402
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
from cctdiag.metrics.sanity import interpret_shortcut_risk  # noqa: E402

CORPUS = ROOT / "data/processed/journal_v1/main_all_traces.jsonl"
RAW_OUTPUT = ROOT / "results/raw/journal_v1/trivial_baseline_sanity.json"
REPORT_OUTPUT = ROOT / "results/reports/journal_v1/trivial_baseline_sanity_report.md"


def pct(value: float | None) -> str:
    if value is None:
        return "NA"
    return f"{value * 100.0:.2f}%"


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


def summarize_macro(macro: dict[str, Any]) -> str:
    return pct(macro.get("macro_accuracy"))


def format_macro_details(macro: dict[str, Any]) -> list[str]:
    lines = ["| group | n | step accuracy |", "|---|---:|---:|"]
    for group, entry in macro.get("per_group", {}).items():
        lines.append(f"| {group} | {entry.get('n')} | {pct(entry.get('accuracy'))} |")
    return lines


def main() -> int:
    records = load_jsonl(str(CORPUS))
    RAW_OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    REPORT_OUTPUT.parent.mkdir(parents=True, exist_ok=True)

    results = {}
    for baseline_name, baseline_fn in TRIVIAL_BASELINES.items():
        predictions = baseline_fn(records)
        results[baseline_name] = metric_block(records, predictions)

    gate = interpret_shortcut_risk(results)
    payload = {
        "scope": {
            "corpus": str(CORPUS.relative_to(ROOT)),
            "diagnostic_sanity_check_only": True,
            "not_paper_result_table": True,
            "not_cct_comparison": True,
            "not_evidence_for_h1": True,
            "shortcut_detection_only": True,
            "cct_scoring_implemented": False,
            "calibration_implemented": False,
            "refinement_variant_implemented": False,
            "ablation_implemented": False,
        },
        "n_records": len(records),
        "baseline_results": results,
        "shortcut_risk_interpretation": gate,
    }
    RAW_OUTPUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    lines = [
        "# Journal-v1 Trivial Baseline Sanity Report",
        "",
        "## Scope and prohibitions",
        f"- Corpus: `{CORPUS.relative_to(ROOT)}`.",
        f"- Total records: {len(records)}.",
        "- This is a **diagnostic sanity check only**.",
        "- This is **not a paper result table**.",
        "- This is **not a comparison against CCT**.",
        "- This is **not evidence for H1**.",
        "- These values are used only to detect remaining obvious shortcuts before future approved method work.",
        "- No CCT scoring, calibration, refinement variant, ablation, or paper-ready result table was implemented.",
        "",
        "## Shortcut-risk gate rules",
        "- If any trivial baseline step accuracy is greater than 50%, evaluation remains blocked.",
        "- If `majority_agent` agent accuracy is greater than 50%, evaluation remains blocked.",
        "- If random or first/last active agent performance is unexpectedly high, flag for review.",
        "- Otherwise, mark the trivial-baseline gate as passed.",
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
                    summarize_macro(metrics["macro_by_scenario"]),
                    summarize_macro(metrics["macro_by_perturbation"]),
                ]
            )
            + " |"
        )

    lines.extend(
        [
            "",
            "## Macro-by-scenario details (step accuracy)",
        ]
    )
    for baseline_name, metrics in results.items():
        lines.extend(["", f"### {baseline_name}", *format_macro_details(metrics["macro_by_scenario"])])

    lines.extend(["", "## Macro-by-perturbation details (step accuracy)"])
    for baseline_name, metrics in results.items():
        lines.extend(["", f"### {baseline_name}", *format_macro_details(metrics["macro_by_perturbation"])])

    lines.extend(
        [
            "",
            "## Shortcut-risk interpretation",
            f"- Gate status: **{gate['status'].upper()}**.",
            "- Blockers: " + ("; ".join(gate["blockers"]) if gate["blockers"] else "none."),
            "- Review flags: " + ("; ".join(gate["review_flags"]) if gate["review_flags"] else "none."),
            f"- Raw JSON output: `{RAW_OUTPUT.relative_to(ROOT)}`.",
        ]
    )
    REPORT_OUTPUT.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print("=== Trivial Baseline Sanity ===")
    print(f"records: {len(records)}")
    print(f"raw: {RAW_OUTPUT.relative_to(ROOT)}")
    print(f"report: {REPORT_OUTPUT.relative_to(ROOT)}")
    print(f"gate: {gate['status'].upper()}")
    if gate["blockers"]:
        print("blockers:")
        for blocker in gate["blockers"]:
            print(f"  - {blocker}")
    if gate["review_flags"]:
        print("review flags:")
        for flag in gate["review_flags"]:
            print(f"  - {flag}")
    print("FINAL: PASS" if gate["status"] == "passed" else "FINAL: REVIEW" if gate["status"] == "review" else "FINAL: BLOCKED")
    return 0 if gate["status"] in {"passed", "review"} else 1


if __name__ == "__main__":
    raise SystemExit(main())
