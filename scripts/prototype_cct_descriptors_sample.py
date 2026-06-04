#!/usr/bin/env python3
"""Prototype sample-only CCT causal-flow descriptors.

This script extracts three deterministic descriptors on a fixed sample only. It
never scores, ranks, calibrates, grid searches, runs LOSO, refines, ablates,
runs statistical tests, or compares descriptor values to gold labels.
"""

from __future__ import annotations

import json
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from cctdiag.cct.descriptors import DESCRIPTOR_NAMES, extract_descriptor_rows  # noqa: E402
from cctdiag.io.full_trace_views import make_full_trace_prediction_view  # noqa: E402

CORPUS_PATH = ROOT / "data/processed/journal_v1_full_trace/main_full_trace_all.jsonl"
RAW_OUT = ROOT / "results/raw/journal_v1_full_trace_cct/cct_descriptor_sample_prototype.json"
REPORT_DIR = ROOT / "results/reports/journal_v1_full_trace_cct"
PROTOTYPE_REPORT = REPORT_DIR / "cct_descriptor_sample_prototype_report.md"
LEAKAGE_REPORT = REPORT_DIR / "cct_descriptor_leakage_risk_report.md"
VARIANCE_REPORT = REPORT_DIR / "cct_descriptor_variance_preview.md"
READINESS_REPORT = REPORT_DIR / "cct_descriptor_readiness_gate.md"
FORBIDDEN_OUTPUT_FIELDS = {
    "gold_failure_step",
    "gold_failure_agent",
    "private_labels",
    "label_rationale",
    "gold_irreversibility",
    "gold_propagation",
    "gold_recoverability",
    "propagation_evidence",
    "irreversibility_evidence",
    "recovery_opportunity",
    "provenance",
    "annotator_or_generator",
    "provenance_notes",
    "synthetic_control_rule",
}


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    with path.open(encoding="utf-8") as handle:
        return [json.loads(line) for line in handle if line.strip()]


def select_sample(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Select two traces per scenario: first clean and first perturbed."""

    selected: list[dict[str, Any]] = []
    by_scenario: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for record in records:
        by_scenario[record["scenario_group"]].append(record)
    for scenario in sorted(by_scenario):
        rows = by_scenario[scenario]
        clean = next(row for row in rows if row["case_variant"] == "clean")
        perturbed = next(row for row in rows if row["case_variant"] != "clean")
        selected.extend([clean, perturbed])
    return selected[:20]


def _forbidden_paths(value: Any, path: str = "") -> list[str]:
    found: list[str] = []
    if isinstance(value, dict):
        for key, nested in value.items():
            nested_path = f"{path}.{key}" if path else str(key)
            if key in FORBIDDEN_OUTPUT_FIELDS:
                found.append(nested_path)
            found.extend(_forbidden_paths(nested, nested_path))
    elif isinstance(value, list):
        for index, item in enumerate(value):
            found.extend(_forbidden_paths(item, f"{path}[{index}]"))
    return found


def _descriptor_counts(rows: list[dict[str, Any]]) -> dict[str, dict[str, int]]:
    counts = {}
    for name in DESCRIPTOR_NAMES:
        values = [row["descriptor_value"] for row in rows if row["descriptor_name"] == name]
        counts[name] = {
            "positive": sum(1 for value in values if value is True),
            "negative": sum(1 for value in values if value is False),
            "missing_or_null": sum(1 for value in values if value is None),
            "total": len(values),
            "unique_values": len(set(values)),
        }
    return counts


def _scenario_template_flags(rows: list[dict[str, Any]], metadata: dict[str, dict[str, str]]) -> dict[str, Any]:
    flags = {}
    for name in DESCRIPTOR_NAMES:
        positive_trace_ids = {row["trace_id"] for row in rows if row["descriptor_name"] == name and row["descriptor_value"] is True}
        scenarios = sorted({metadata[trace_id]["scenario_group"] for trace_id in positive_trace_ids})
        perturbations = sorted({metadata[trace_id]["perturbation_type"] for trace_id in positive_trace_ids})
        flags[name] = {
            "positive_scenario_groups": scenarios,
            "positive_perturbation_types": perturbations,
            "fires_only_one_scenario_template": len(scenarios) == 1,
            "appears_overly_sparse": len(positive_trace_ids) <= 1,
            "appears_overly_dense": len(positive_trace_ids) == len(set(metadata)),
        }
    return flags


def _example(rows: list[dict[str, Any]], name: str, value: bool) -> dict[str, Any] | None:
    return next((row for row in rows if row["descriptor_name"] == name and row["descriptor_value"] is value), None)


def write_reports(sample: list[dict[str, Any]], descriptor_rows: list[dict[str, Any]], metadata: dict[str, dict[str, str]], leakage_paths: list[str]) -> None:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    counts = _descriptor_counts(descriptor_rows)
    flags = _scenario_template_flags(descriptor_rows, metadata)
    sampled_step_count = sum(len(record["steps"]) for record in sample)

    prototype_lines = [
        "# Journal-v1 Full-Trace CCT Descriptor Sample Prototype Report",
        "",
        "Scope: sample-only deterministic descriptor extraction. No scoring, ranking, calibration, grid search, LOSO, refinement, ablation, statistical test, descriptor-to-gold comparison, or paper-ready result table was produced.",
        "",
        f"- Sampled traces: {len(sample)}",
        f"- Sampled step rows: {sampled_step_count}",
        "- Sample rule: first clean trace and first perturbed trace per scenario group, capped at 20 traces.",
        "- Descriptor subset: `handoff_constraint_shift_indicator`, `evidence_ignored_indicator`, `downstream_reference_to_prior_output`.",
        "",
        "## Examples",
    ]
    for name in DESCRIPTOR_NAMES:
        pos = _example(descriptor_rows, name, True)
        neg = _example(descriptor_rows, name, False)
        prototype_lines.append(f"- `{name}` positive example: `{pos}`" if pos else f"- `{name}` positive example: none in sample")
        prototype_lines.append(f"- `{name}` negative example: `{neg}`" if neg else f"- `{name}` negative example: none in sample")
    PROTOTYPE_REPORT.write_text("\n".join(prototype_lines) + "\n", encoding="utf-8")

    leakage_lines = [
        "# Journal-v1 Full-Trace CCT Descriptor Leakage Risk Report",
        "",
        "Descriptor extraction consumes `make_full_trace_prediction_view(record)` and the extractor rejects payloads containing private/gold/provenance fields.",
        f"- Forbidden output fields detected: {'none' if not leakage_paths else ', '.join(leakage_paths[:20])}",
        "- Private labels used: no.",
        "- Gold labels used: no.",
        "- Scenario/perturbation used as descriptor value: no; metadata is used only for sample audit summaries.",
        "- Leakage status: PASS." if not leakage_paths else "- Leakage status: FAIL.",
    ]
    LEAKAGE_REPORT.write_text("\n".join(leakage_lines) + "\n", encoding="utf-8")

    variance_lines = [
        "# Journal-v1 Full-Trace CCT Descriptor Variance Preview",
        "",
        f"- Sampled traces: {len(sample)}",
        f"- Sampled step rows: {sampled_step_count}",
        "",
        "| Descriptor | Positive | Negative | Missing/null | Constant in sample | Fires only one scenario template | Overly sparse | Overly dense |",
        "|---|---:|---:|---:|---|---|---|---|",
    ]
    for name in DESCRIPTOR_NAMES:
        constant = counts[name]["unique_values"] <= 1
        variance_lines.append(
            f"| `{name}` | {counts[name]['positive']} | {counts[name]['negative']} | {counts[name]['missing_or_null']} | {str(constant).lower()} | {str(flags[name]['fires_only_one_scenario_template']).lower()} | {str(flags[name]['appears_overly_sparse']).lower()} | {str(flags[name]['appears_overly_dense']).lower()} |"
        )
    VARIANCE_REPORT.write_text("\n".join(variance_lines) + "\n", encoding="utf-8")

    ready_for_full = not leakage_paths and any(counts[name]["positive"] > 0 and counts[name]["negative"] > 0 for name in DESCRIPTOR_NAMES)
    readiness_lines = [
        "# Journal-v1 Full-Trace CCT Descriptor Readiness Gate",
        "",
        f"- `DESCRIPTOR_PROTOTYPE_READY_FOR_FULL_AUDIT = {'yes' if ready_for_full else 'no'}`",
        "- `DESCRIPTOR_READY_FOR_SCORING = no`",
        "- Authorized next step if ready: future full-corpus descriptor extraction and leakage/variance/shortcut audit only, not scoring.",
        "- No descriptor values were compared to gold labels.",
        "- No scoring, ranking, calibration, grid search, LOSO, refinement, ablation, statistical test, or paper-ready result table was produced.",
    ]
    READINESS_REPORT.write_text("\n".join(readiness_lines) + "\n", encoding="utf-8")


def main() -> int:
    records = read_jsonl(CORPUS_PATH)
    sample = select_sample(records)
    metadata = {
        record["trace_id"]: {
            "scenario_group": record["scenario_group"],
            "perturbation_type": record["perturbation_type"],
        }
        for record in sample
    }
    descriptor_rows: list[dict[str, Any]] = []
    for record in sample:
        prediction_view = make_full_trace_prediction_view(record)
        descriptor_rows.extend(extract_descriptor_rows(prediction_view))

    leakage_paths = _forbidden_paths(descriptor_rows)
    RAW_OUT.parent.mkdir(parents=True, exist_ok=True)
    RAW_OUT.write_text(json.dumps(descriptor_rows, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    write_reports(sample, descriptor_rows, metadata, leakage_paths)

    counts = _descriptor_counts(descriptor_rows)
    print("=== CCT Descriptor Sample Prototype ===")
    print(f"Sampled traces: {len(sample)}")
    print(f"Sampled step rows: {sum(len(record['steps']) for record in sample)}")
    for name in DESCRIPTOR_NAMES:
        print(f"{name}: positive={counts[name]['positive']} negative={counts[name]['negative']}")
    print(f"Leakage status: {'PASS' if not leakage_paths else 'FAIL'}")
    print("FINAL: PASS" if not leakage_paths else "FINAL: FAIL")
    return 0 if not leakage_paths else 1


if __name__ == "__main__":
    raise SystemExit(main())
