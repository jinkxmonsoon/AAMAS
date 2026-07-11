#!/usr/bin/env python3
"""Run non-scoring rescue candidate-step feature readiness dry run."""

from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from cctdiag.io.full_trace_views import make_full_trace_prediction_view
from cctdiag.rescue.candidate_step_features import (
    FEATURE_NAMES,
    audit_candidate_step_rows_for_private_leakage,
    extract_candidate_step_feature_rows,
    position_identity_risk_summary,
    summarize_feature_rows,
)

CORPUS_PATH = ROOT / "data/processed/journal_v1_full_trace/main_full_trace_all.jsonl"
RAW_OUTPUT = ROOT / "results/raw/journal_v1_rescue/rescue_candidate_step_features.json"
REPORT_DIR = ROOT / "results/reports/journal_v1_rescue"
INVENTORY_REPORT = REPORT_DIR / "rescue_candidate_step_feature_inventory.md"
LEAKAGE_REPORT = REPORT_DIR / "rescue_candidate_step_feature_leakage_audit.md"
DEGENERACY_REPORT = REPORT_DIR / "rescue_candidate_step_feature_degeneracy_report.md"
POSITION_REPORT = REPORT_DIR / "rescue_candidate_step_position_identity_risk_report.md"
READINESS_REPORT = REPORT_DIR / "rescue_candidate_step_feature_readiness_gate.md"
EXPECTED_TRACES = 420
EXPECTED_ROWS = 2100


def load_records() -> list[dict[str, Any]]:
    return [json.loads(line) for line in CORPUS_PATH.read_text().splitlines() if line.strip()]


def main() -> None:
    records = load_records()
    if len(records) != EXPECTED_TRACES:
        raise SystemExit(f"expected {EXPECTED_TRACES} traces, found {len(records)}")

    raw_rejection_passed = False
    try:
        extract_candidate_step_feature_rows(records[0])
    except ValueError:
        raw_rejection_passed = True
    if not raw_rejection_passed:
        raise SystemExit("raw record was not rejected by candidate-step feature extractor")

    rows: list[dict[str, Any]] = []
    scenario_counts: Counter[str] = Counter()
    perturbation_counts: Counter[str] = Counter()
    for record in records:
        scenario_counts[str(record.get("scenario_group"))] += 1
        perturbation_counts[str(record.get("perturbation_type"))] += 1
        prediction_view = make_full_trace_prediction_view(record)
        rows.extend(extract_candidate_step_feature_rows(prediction_view))

    if len(rows) != EXPECTED_ROWS:
        raise SystemExit(f"expected {EXPECTED_ROWS} candidate-step rows, found {len(rows)}")

    findings = audit_candidate_step_rows_for_private_leakage(rows)
    summary = summarize_feature_rows(rows)
    position_summary = position_identity_risk_summary(rows)
    constant_over_95 = summary["feature_families_over_95_percent_constant"]
    readiness = (
        not findings
        and raw_rejection_passed
        and not summary["duplicate_threshold_exceeded"]
        and not constant_over_95
    )
    blockers: list[str] = []
    if findings:
        blockers.append("leakage findings present")
    if not raw_rejection_passed:
        blockers.append("raw records are not rejected")
    if summary["duplicate_threshold_exceeded"]:
        blockers.append("duplicate candidate-step feature vectors exceed 50%")
    if constant_over_95:
        blockers.append("feature families exceed 95% constant threshold: " + ", ".join(constant_over_95))

    RAW_OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    RAW_OUTPUT.write_text("[\n" + ",\n".join(json.dumps(row, sort_keys=True) for row in rows) + "\n]\n")

    INVENTORY_REPORT.write_text(_inventory_markdown(rows, summary, scenario_counts, perturbation_counts))
    LEAKAGE_REPORT.write_text(_leakage_markdown(findings, raw_rejection_passed))
    DEGENERACY_REPORT.write_text(_degeneracy_markdown(summary))
    POSITION_REPORT.write_text(_position_markdown(position_summary))
    READINESS_REPORT.write_text(_readiness_markdown(readiness, blockers, summary, findings))

    print(
        "rescue_candidate_step_feature_readiness "
        f"rows={len(rows)} leakage={'PASS' if not findings and raw_rejection_passed else 'FAIL'} "
        f"duplicate_pct={summary['duplicate_feature_vector_percentage']:.3f} "
        f"ready_for_scoring={'yes' if readiness else 'no'}"
    )


def _inventory_markdown(
    rows: list[dict[str, Any]],
    summary: dict[str, Any],
    scenario_counts: Counter[str],
    perturbation_counts: Counter[str],
) -> str:
    lines = [
        "# Rescue Candidate-Step Feature Inventory",
        "",
        "## Scope",
        "- Non-scoring candidate-step feature-readiness dry run for `rescue_experiment_v1`.",
        "- One row per candidate step per trace; no gold/H6 comparison is performed.",
        "",
        "## Counts",
        f"- Total candidate-step rows: {len(rows)}",
        f"- Expected candidate-step rows: {EXPECTED_ROWS}",
        f"- Feature count: {len(FEATURE_NAMES)}",
        "",
        "## Feature names",
    ]
    lines.extend(f"- `{name}`" for name in FEATURE_NAMES)
    lines.extend([
        "",
        "## Missing/null counts",
    ])
    lines.extend(f"- {name}: {count}" for name, count in summary["missing_null_counts"].items())
    lines.extend([
        "",
        "## Audit-only scenario distribution",
    ])
    lines.extend(f"- {key}: {scenario_counts[key]}" for key in sorted(scenario_counts))
    lines.extend([
        "",
        "## Audit-only perturbation distribution",
    ])
    lines.extend(f"- {key}: {perturbation_counts[key]}" for key in sorted(perturbation_counts))
    return "\n".join(lines) + "\n"


def _leakage_markdown(findings: list[str], raw_rejection_passed: bool) -> str:
    status = "PASS" if not findings and raw_rejection_passed else "FAIL"
    lines = [
        "# Rescue Candidate-Step Feature Leakage Audit",
        "",
        f"- Leakage status: {status}",
        "- Extraction input: `make_full_trace_prediction_view(record)` only.",
        f"- Raw-record rejection check passed: {'yes' if raw_rejection_passed else 'no'}",
        "- Output contains no private/gold/H6/provenance/scoring fields: " + ("yes" if not findings else "no"),
        "- Gold/H6 comparison performed: no",
        "- Scenario/perturbation/case metadata used as feature input: no",
        f"- Findings: {len(findings)}",
    ]
    lines.extend(f"  - {finding}" for finding in findings)
    return "\n".join(lines) + "\n"


def _degeneracy_markdown(summary: dict[str, Any]) -> str:
    lines = [
        "# Rescue Candidate-Step Feature Degeneracy Report",
        "",
        f"- Total rows: {summary['total_rows']}",
        f"- Unique feature-vector count: {summary['unique_feature_vector_count']}",
        f"- Duplicate candidate-step feature-vector count: {summary['duplicate_feature_vector_count']}",
        f"- Duplicate candidate-step feature-vector percentage: {summary['duplicate_feature_vector_percentage']:.2%}",
        f"- Duplicate threshold (>50%) exceeded: {'yes' if summary['duplicate_threshold_exceeded'] else 'no'}",
        f"- Within-trace duplicate candidate-step rows: {summary['within_trace_duplicate_candidate_step_rows']}",
        f"- Traces with within-trace duplicates: {summary['traces_with_within_trace_duplicates']}",
        "",
        "## Unique values per feature",
    ]
    lines.extend(f"- {name}: {count}" for name, count in summary["unique_values_per_feature"].items())
    lines.extend([
        "",
        "## Constant features",
    ])
    if summary["constant_features"]:
        lines.extend(f"- {name}" for name in summary["constant_features"])
    else:
        lines.append("- none")
    lines.extend([
        "",
        "## Feature families over 95% constant threshold",
    ])
    over = summary["feature_families_over_95_percent_constant"]
    if over:
        lines.extend(f"- {name}" for name in over)
    else:
        lines.append("- none")
    return "\n".join(lines) + "\n"


def _position_markdown(position_summary: dict[str, Any]) -> str:
    lines = [
        "# Rescue Candidate-Step Position/Identity Risk Report",
        "",
        f"- Features include step position column: {'yes' if position_summary['features_include_step_position_column'] else 'no'}",
        f"- Features include agent identity column: {'yes' if position_summary['features_include_agent_identity_column'] else 'no'}",
        f"- Features usable without position or agent fields: {'yes' if position_summary['features_usable_without_position_or_agent_fields'] else 'no'}",
        f"- Position shortcut risk: {position_summary['position_shortcut_risk']}",
        f"- Agent identity shortcut risk: {position_summary['agent_identity_shortcut_risk']}",
        "",
        "## Unique vectors by candidate step id (identifier-only audit)",
    ]
    for step_id, count in position_summary["unique_vectors_by_candidate_step_id"].items():
        lines.append(f"- {step_id}: {count}")
    lines.extend([
        "",
        "## Feature means by candidate step id (identifier-only audit)",
    ])
    for step_id, means in position_summary["feature_means_by_candidate_step_id"].items():
        compact = ", ".join(f"{name}={value}" for name, value in means.items())
        lines.append(f"- {step_id}: {compact}")
    return "\n".join(lines) + "\n"


def _readiness_markdown(
    readiness: bool, blockers: list[str], summary: dict[str, Any], findings: list[str]
) -> str:
    lines = [
        "# Rescue Candidate-Step Feature Readiness Gate",
        "",
        f"- RESCUE_CANDIDATE_STEP_FEATURES_READY_FOR_SCORING = {'yes' if readiness else 'no'}",
        "- Authorized next action if yes: one future minimal scoring task under `configs/rescue_experiment_v1.yaml` only.",
        "- Recommended next action if no: redesign candidate-step features once, then rerun this dry-run gate before scoring.",
        f"- Total candidate-step rows: {summary['total_rows']}",
        f"- Leakage status: {'PASS' if not findings else 'FAIL'}",
        f"- Duplicate candidate-step feature-vector percentage: {summary['duplicate_feature_vector_percentage']:.2%}",
        f"- Feature families over 95% constant threshold: {len(summary['feature_families_over_95_percent_constant'])}",
        "",
        "## Blockers",
    ]
    if blockers:
        lines.extend(f"- {blocker}" for blocker in blockers)
    else:
        lines.append("- none")
    lines.extend([
        "",
        "## Non-action confirmation",
        "- No scoring, ranking, gold/H6 comparison, calibration, tuning, grid search, LOSO, ablation, statistical test, corpus/gold-label change, scoring-config restoration, or paper-ready result table was produced.",
    ])
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    main()
