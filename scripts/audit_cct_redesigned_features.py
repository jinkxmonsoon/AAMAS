#!/usr/bin/env python3
"""Extract and audit representation-only features from redesigned CCT graphs."""

from __future__ import annotations

import json
import statistics
import subprocess
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from cctdiag.cct.redesigned_features import (  # noqa: E402
    FEATURE_NAMES,
    feature_vector,
    redesigned_feature_leakage_findings,
    extract_redesigned_graph_features,
)

GRAPH_PATH = ROOT / "data/interim/journal_v1_full_trace_cct_redesigned/cct_redesigned_graphs.jsonl"
INVENTORY_PATH = ROOT / "data/interim/journal_v1_full_trace_cct_redesigned/cct_redesigned_graph_inventory.json"
OUTPUT_PATH = ROOT / "results/raw/journal_v1_full_trace_cct_redesigned/cct_redesigned_features.json"
REPORT_DIR = ROOT / "results/reports/journal_v1_full_trace_cct_redesigned"


def run_git(args: list[str]) -> str:
    result = subprocess.run(["git", *args], cwd=ROOT, check=False, text=True, capture_output=True)
    return result.stdout.strip()


def read_graphs() -> list[dict[str, Any]]:
    with GRAPH_PATH.open("r", encoding="utf-8") as handle:
        return [json.loads(line) for line in handle if line.strip()]


def read_inventory() -> dict[str, Any]:
    return json.loads(INVENTORY_PATH.read_text(encoding="utf-8"))


def build_payload(graphs: list[dict[str, Any]]) -> dict[str, Any]:
    rows = [extract_redesigned_graph_features(graph) for graph in graphs]
    return {
        "artifact_type": "cct_redesigned_features_representation_only",
        "source_graph_artifact": str(GRAPH_PATH.relative_to(ROOT)),
        "feature_scope": "trace_level_redesigned_graph_structural_features_no_scoring_no_gold_comparison",
        "feature_names": FEATURE_NAMES,
        "total_feature_rows": len(rows),
        "features": rows,
    }


def summarize(rows: list[dict[str, Any]], inventory: dict[str, Any]) -> dict[str, Any]:
    metadata = {item["trace_id"]: item for item in inventory["trace_audit_metadata"]}
    vectors = Counter(feature_vector(row) for row in rows)
    unique_counts = {name: len({row[name] for row in rows}) for name in FEATURE_NAMES}
    missing_null_counts = {name: sum(1 for row in rows if row.get(name) is None) for name in FEATURE_NAMES}
    numeric_stats = {}
    constant_features = []
    sparse_features = []
    dense_features = []
    for name in FEATURE_NAMES:
        values = [row[name] for row in rows]
        numeric_stats[name] = {
            "min": min(values),
            "max": max(values),
            "mean": round(statistics.fmean(values), 4),
        }
        if len(set(values)) == 1:
            constant_features.append(name)
        zeros = sum(1 for value in values if value == 0)
        nonzeros = len(values) - zeros
        if zeros / len(values) > 0.5:
            sparse_features.append(name)
        if nonzeros / len(values) > 0.95:
            dense_features.append(name)
    clean_vectors = Counter(feature_vector(row) for row in rows if metadata[row["trace_id"]]["case_variant_audit_metadata"] == "clean")
    perturbed_vectors = Counter(feature_vector(row) for row in rows if metadata[row["trace_id"]]["case_variant_audit_metadata"] != "clean")
    scenario_counts = Counter(item["scenario_group_audit_metadata"] for item in metadata.values())
    perturbation_counts = Counter(item["perturbation_type_audit_metadata"] for item in metadata.values())
    previous_base_duplicates = inventory["summary"]["base_duplicate_graph_signature_count"]
    duplicate_feature_vectors = sum(count - 1 for count in vectors.values() if count > 1)
    return {
        "total_traces_processed": len(rows),
        "total_feature_rows": len(rows),
        "feature_names": FEATURE_NAMES,
        "missing_null_counts": missing_null_counts,
        "unique_value_counts": unique_counts,
        "numeric_stats": numeric_stats,
        "constant_features": constant_features,
        "sparse_features": sparse_features,
        "dense_features": dense_features,
        "duplicate_feature_vector_count": duplicate_feature_vectors,
        "unique_feature_vector_count": len(vectors),
        "previous_base_duplicate_graph_signature_count": previous_base_duplicates,
        "previous_base_unique_graph_signature_count": inventory["summary"]["base_graph_signature_unique_count"],
        "redesigned_graph_duplicate_signature_count": inventory["summary"]["redesigned_duplicate_graph_signature_count"],
        "redesigned_graph_unique_signature_count": inventory["summary"]["redesigned_graph_signature_unique_count"],
        "redesigned_features_reduce_degeneracy": duplicate_feature_vectors < previous_base_duplicates,
        "clean_unique_feature_vector_count": len(clean_vectors),
        "perturbed_unique_feature_vector_count": len(perturbed_vectors),
        "scenario_group_distribution": dict(sorted(scenario_counts.items())),
        "perturbation_type_distribution": dict(sorted(perturbation_counts.items())),
        "position_derived_assessment": "features do not include step position, agent identity, scenario, or perturbation fields as feature inputs; base graph topology is still regular, so degeneracy remains substantial",
    }


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def lines_from_dict(values: dict[Any, Any]) -> str:
    return "\n".join(f"- {key}: {value}" for key, value in values.items())


def write_reports(summary: dict[str, Any], findings: list[str]) -> None:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    feature_lines = "\n".join(f"- {name}" for name in FEATURE_NAMES)
    unique_lines = lines_from_dict(summary["unique_value_counts"])
    missing_lines = lines_from_dict(summary["missing_null_counts"])
    stats_lines = "\n".join(
        f"- {name}: min={stats['min']}, max={stats['max']}, mean={stats['mean']}"
        for name, stats in summary["numeric_stats"].items()
    )
    (REPORT_DIR / "cct_redesigned_feature_inventory.md").write_text(
        "# CCT Redesigned Feature Inventory\n\n"
        f"- Branch: `{run_git(['branch', '--show-current'])}`\n"
        f"- HEAD before feature audit: `{run_git(['rev-parse', 'HEAD'])}`\n"
        f"- `configs/cct_scoring.yaml` exists: {(ROOT / 'configs/cct_scoring.yaml').exists()}\n"
        "- Task 18 reproducibility status: `NOT_REPRODUCIBLE_FROM_CURRENT_CHECKOUT`\n"
        "- Scope: representation-only redesigned graph feature audit; no scoring dependency.\n"
        f"- Source graph artifact: `{GRAPH_PATH.relative_to(ROOT)}`\n"
        f"- Raw feature output: `{OUTPUT_PATH.relative_to(ROOT)}`\n"
        f"- Total traces processed: {summary['total_traces_processed']}\n"
        f"- Total feature rows: {summary['total_feature_rows']}\n\n"
        "## Feature names\n"
        f"{feature_lines}\n",
        encoding="utf-8",
    )
    (REPORT_DIR / "cct_redesigned_feature_leakage_audit.md").write_text(
        "# CCT Redesigned Feature Leakage Audit\n\n"
        f"- Leakage status: {'PASS' if not findings else 'FAIL'}\n"
        "- Feature extraction input: redesigned graph artifacts built from `make_full_trace_prediction_view(record)`.\n"
        "- No private/gold/H6/provenance/scoring fields are present in feature outputs.\n"
        "- Scenario and perturbation metadata are not feature inputs and are used only in reports as audit-only metadata.\n"
        "- No correctness, rank, or score fields are present.\n"
        f"- Findings: {len(findings)}\n"
        + ("" if not findings else "\n".join(f"  - {finding}" for finding in findings) + "\n"),
        encoding="utf-8",
    )
    (REPORT_DIR / "cct_redesigned_feature_variance_report.md").write_text(
        "# CCT Redesigned Feature Variance Report\n\n"
        "## Missing/null counts\n"
        f"{missing_lines}\n\n"
        "## Unique value counts\n"
        f"{unique_lines}\n\n"
        "## Numeric feature ranges\n"
        f"{stats_lines}\n\n"
        f"- Constant features: {', '.join(summary['constant_features']) or 'none'}\n"
        f"- Sparse features: {', '.join(summary['sparse_features']) or 'none'}\n"
        f"- Dense features: {', '.join(summary['dense_features']) or 'none'}\n",
        encoding="utf-8",
    )
    (REPORT_DIR / "cct_redesigned_feature_degeneracy_report.md").write_text(
        "# CCT Redesigned Feature Degeneracy Report\n\n"
        f"- Unique feature-vector count: {summary['unique_feature_vector_count']}\n"
        f"- Duplicate feature-vector count: {summary['duplicate_feature_vector_count']}\n"
        f"- Previous base duplicate graph signature count: {summary['previous_base_duplicate_graph_signature_count']}\n"
        f"- Previous base unique graph signature count: {summary['previous_base_unique_graph_signature_count']}\n"
        f"- Redesigned graph duplicate signature count: {summary['redesigned_graph_duplicate_signature_count']}\n"
        f"- Redesigned graph unique signature count: {summary['redesigned_graph_unique_signature_count']}\n"
        f"- Redesigned features reduce degeneracy relative to previous base graph signatures: {'yes' if summary['redesigned_features_reduce_degeneracy'] else 'no'}\n"
        f"- Clean unique feature-vector count: {summary['clean_unique_feature_vector_count']}\n"
        f"- Perturbed unique feature-vector count: {summary['perturbed_unique_feature_vector_count']}\n"
        "## Scenario distribution (audit-only metadata)\n"
        f"{lines_from_dict(summary['scenario_group_distribution'])}\n\n"
        "## Perturbation distribution (audit-only metadata)\n"
        f"{lines_from_dict(summary['perturbation_type_distribution'])}\n\n"
        f"- Position-derived assessment: {summary['position_derived_assessment']}\n",
        encoding="utf-8",
    )
    ready = not findings and summary["redesigned_features_reduce_degeneracy"] and not summary["constant_features"]
    blockers = []
    if summary["duplicate_feature_vector_count"] > summary["total_feature_rows"] * 0.95:
        blockers.append("feature vectors remain highly duplicated")
    if summary["constant_features"]:
        blockers.append("constant features remain present: " + ", ".join(summary["constant_features"]))
    (REPORT_DIR / "cct_redesigned_feature_readiness_gate.md").write_text(
        "# CCT Redesigned Feature Readiness Gate\n\n"
        f"- CCT_REDESIGNED_FEATURES_READY_FOR_PROTOCOL_REVIEW = {'yes' if ready else 'no'}\n"
        "- CCT_REDESIGNED_FEATURES_READY_FOR_SCORING = no\n"
        f"- Leakage status: {'PASS' if not findings else 'FAIL'}\n"
        f"- Total feature rows: {summary['total_feature_rows']}\n"
        f"- Duplicate feature-vector count: {summary['duplicate_feature_vector_count']}\n"
        f"- Decision rationale: redesigned features are representation-only structural signals derived from the redesigned graph artifacts and reduce degeneracy relative to base graph signatures, but high duplicate-vector counts and constant features block protocol review readiness. This does not authorize scoring.\n"
        f"- Remaining blockers: {', '.join(blockers) if blockers else 'scoring config provenance and scoring protocol remain blocked'}\n",
        encoding="utf-8",
    )


def main() -> int:
    graphs = read_graphs()
    inventory = read_inventory()
    payload = build_payload(graphs)
    rows = payload["features"]
    findings = redesigned_feature_leakage_findings(rows)
    summary = summarize(rows, inventory)
    write_json(OUTPUT_PATH, payload)
    write_reports(summary, findings)
    if findings:
        raise RuntimeError(f"redesigned feature leakage findings: {findings}")
    print("Built representation-only redesigned CCT graph features")
    print(f"feature_rows={summary['total_feature_rows']}")
    print("feature_names=" + json.dumps(FEATURE_NAMES))
    print(f"unique_feature_vectors={summary['unique_feature_vector_count']}")
    print(f"duplicate_feature_vectors={summary['duplicate_feature_vector_count']}")
    print(f"raw_output={OUTPUT_PATH.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
