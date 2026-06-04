#!/usr/bin/env python3
"""Audit full-trace CCT structural feature variance without scoring.

This script computes descriptive diagnostics only. It does not compute CCT
predictions, compare against gold labels, rank candidate steps, learn weights,
calibrate outputs, run refinements, run ablations, test hypotheses, or produce
paper-ready result tables.
"""

from __future__ import annotations

import json
import math
import sys
from collections import Counter, defaultdict
from pathlib import Path
from statistics import mean
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
FEATURES_PATH = ROOT / "data/interim/journal_v1_full_trace_cct/cct_features.jsonl"
GRAPHS_PATH = ROOT / "data/interim/journal_v1_full_trace_cct/cct_graphs.jsonl"
CORPUS_PATH = ROOT / "data/processed/journal_v1_full_trace/main_full_trace_all.jsonl"
REPORT_DIR = ROOT / "results/reports/journal_v1_full_trace_cct"

FORBIDDEN_PRIVATE_FIELDS = {
    "private_labels",
    "provenance",
    "gold_failure_step",
    "gold_failure_agent",
    "gold_irreversibility",
    "gold_propagation",
    "gold_recoverability",
    "label_rationale",
    "label_confidence",
    "label_source",
    "propagation_evidence",
    "irreversibility_evidence",
    "recovery_opportunity",
    "primary_labeler",
    "secondary_labeler",
    "adjudicator",
    "disagreement_type",
    "adjudication_decision",
    "manual_audit_status",
    "synthetic_control_rule",
    "annotator_or_generator",
    "provenance_notes",
}

IDENTIFIER_FIELDS = {"feature_schema_version", "trace_id", "step_id"}
AUDIT_METADATA_FIELDS = {"scenario_group", "perturbation_type"}


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    with path.open(encoding="utf-8") as handle:
        return [json.loads(line) for line in handle if line.strip()]


def _stable_value(value: Any) -> str:
    return json.dumps(value, sort_keys=True)


def find_forbidden_paths(value: Any, path: str = "") -> list[str]:
    found: list[str] = []
    if isinstance(value, dict):
        for key, nested in value.items():
            nested_path = f"{path}.{key}" if path else str(key)
            if key in FORBIDDEN_PRIVATE_FIELDS:
                found.append(nested_path)
            found.extend(find_forbidden_paths(nested, nested_path))
    elif isinstance(value, list):
        for index, item in enumerate(value):
            found.extend(find_forbidden_paths(item, f"{path}[{index}]"))
    return found


def _feature_names(rows: list[dict[str, Any]]) -> list[str]:
    names: set[str] = set()
    for row in rows:
        names.update(row)
    return sorted(names)


def _is_numeric(value: Any) -> bool:
    return isinstance(value, int | float | bool) and not isinstance(value, str)


def _numeric_summary(values: list[Any]) -> dict[str, float] | None:
    numeric_values = [float(value) for value in values if value is not None and _is_numeric(value)]
    non_missing = [value for value in values if value is not None]
    if len(numeric_values) != len(non_missing) or not numeric_values:
        return None
    return {
        "min": min(numeric_values),
        "max": max(numeric_values),
        "mean": mean(numeric_values),
    }


def _scenario_metadata() -> dict[str, dict[str, str]]:
    metadata = {}
    for record in read_jsonl(CORPUS_PATH):
        metadata[record["trace_id"]] = {
            "scenario_group": record.get("scenario_group", "missing"),
            "perturbation_type": record.get("perturbation_type", "missing"),
        }
    return metadata


def _group_variation(rows: list[dict[str, Any]], names: list[str], group_field: str) -> dict[str, dict[str, int]]:
    by_feature: dict[str, dict[str, int]] = {}
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        grouped[str(row.get(group_field, "missing"))].append(row)
    for name in names:
        if name in AUDIT_METADATA_FIELDS:
            continue
        group_counts = {group: len({_stable_value(row.get(name)) for row in group_rows}) for group, group_rows in grouped.items()}
        if len(set(group_counts.values())) > 1 or any(count > 1 for count in group_counts.values()):
            by_feature[name] = group_counts
    return by_feature


def audit_feature_variance() -> dict[str, Any]:
    features = read_jsonl(FEATURES_PATH)
    graphs = read_jsonl(GRAPHS_PATH)
    metadata = _scenario_metadata()
    rows = [{**row, **metadata.get(row.get("trace_id"), {})} for row in features]
    names = _feature_names(features)
    audit_names = _feature_names(rows)

    missing_counts = {name: sum(1 for row in features if row.get(name) is None) for name in names}
    unique_counts = {name: len({_stable_value(row.get(name)) for row in features}) for name in names}
    numeric_stats = {
        name: summary
        for name in names
        if (summary := _numeric_summary([row.get(name) for row in features])) is not None
    }
    constant_features = [name for name, count in unique_counts.items() if count == 1]

    by_position: dict[Any, list[dict[str, Any]]] = defaultdict(list)
    for row in features:
        by_position[row.get("order_index")].append(row)
    vary_only_by_position = []
    for name in names:
        if unique_counts[name] <= 1:
            continue
        if all(len({_stable_value(row.get(name)) for row in position_rows}) == 1 for position_rows in by_position.values()):
            vary_only_by_position.append(name)

    perfectly_determines_position = []
    for name in names:
        value_positions: dict[str, set[Any]] = defaultdict(set)
        for row in features:
            value_positions[_stable_value(row.get(name))].add(row.get("order_index"))
        if unique_counts[name] > 1 and all(len(positions) == 1 for positions in value_positions.values()):
            perfectly_determines_position.append(name)

    structural_vector_fields = [name for name in names if name not in IDENTIFIER_FIELDS]
    vector_counts = Counter(
        tuple((name, _stable_value(row.get(name))) for name in structural_vector_fields)
        for row in features
    )
    max_identical_vector_count = max(vector_counts.values()) if vector_counts else 0
    duplicate_vector_threshold = max(25, math.ceil(len(features) * 0.05))
    duplicate_vector_warning = max_identical_vector_count >= duplicate_vector_threshold

    node_counts = [len(graph.get("nodes", [])) for graph in graphs]
    edge_counts = [len(graph.get("edges", [])) for graph in graphs]
    graph_count_summary = {
        "graph_count": len(graphs),
        "node_count_min": min(node_counts) if node_counts else 0,
        "node_count_max": max(node_counts) if node_counts else 0,
        "node_count_unique": sorted(set(node_counts)),
        "edge_count_min": min(edge_counts) if edge_counts else 0,
        "edge_count_max": max(edge_counts) if edge_counts else 0,
        "edge_count_unique": sorted(set(edge_counts)),
    }

    forbidden_feature_paths = []
    for index, row in enumerate(features):
        forbidden_feature_paths.extend(f"features[{index}].{path}" for path in find_forbidden_paths(row))
    forbidden_graph_paths = []
    for index, graph in enumerate(graphs):
        forbidden_graph_paths.extend(f"graphs[{index}].{path}" for path in find_forbidden_paths(graph))

    high_variance_features = [
        name
        for name, count in sorted(unique_counts.items(), key=lambda item: (-item[1], item[0]))
        if count >= 10 and name not in IDENTIFIER_FIELDS
    ]
    scenario_variation = _group_variation(rows, audit_names, "scenario_group")
    perturbation_variation = _group_variation(rows, audit_names, "perturbation_type")

    blocker_reasons = []
    if forbidden_feature_paths or forbidden_graph_paths:
        blocker_reasons.append("private/gold field leakage detected in graph or feature payloads")
    if not features:
        blocker_reasons.append("no feature rows available")
    if not graphs:
        blocker_reasons.append("no graph rows available")
    if not high_variance_features:
        blocker_reasons.append("no high-variance feature fields detected")

    warnings = []
    if perfectly_determines_position:
        warnings.append("single-feature position shortcuts exist")
    if duplicate_vector_warning:
        warnings.append("many identical structural feature vectors exist")
    if len(set(node_counts)) == 1 and len(set(edge_counts)) == 1:
        warnings.append("graph node and edge counts are constant across all traces")
    if vary_only_by_position:
        warnings.append("some features vary only by step position")

    return {
        "feature_row_count": len(features),
        "feature_names": names,
        "missing_counts": missing_counts,
        "unique_counts": unique_counts,
        "numeric_stats": numeric_stats,
        "constant_features": constant_features,
        "high_variance_features": high_variance_features,
        "vary_only_by_position": sorted(vary_only_by_position),
        "perfectly_determines_position": sorted(perfectly_determines_position),
        "scenario_variation": scenario_variation,
        "perturbation_variation": perturbation_variation,
        "graph_count_summary": graph_count_summary,
        "forbidden_feature_paths": forbidden_feature_paths,
        "forbidden_graph_paths": forbidden_graph_paths,
        "structural_vector_fields": structural_vector_fields,
        "max_identical_vector_count": max_identical_vector_count,
        "duplicate_vector_threshold": duplicate_vector_threshold,
        "warnings": warnings,
        "blocker_reasons": blocker_reasons,
        "readiness_decision": "ready_with_shortcut_warnings" if not blocker_reasons else "blocked",
    }


def _format_float(value: float) -> str:
    return f"{value:.3f}".rstrip("0").rstrip(".")


def _write_variance_report(audit: dict[str, Any]) -> None:
    lines = [
        "# Journal-v1 Full-Trace CCT Feature Variance Report",
        "",
        "Scope: descriptive structural feature diagnostics only. This report does not compute predictions, compare to gold labels, rank candidates, learn weights, calibrate outputs, run refinements, run ablations, test hypotheses, or produce paper-ready result tables.",
        "",
        f"- Feature rows audited: {audit['feature_row_count']}",
        f"- Feature names: {', '.join(audit['feature_names'])}",
        f"- Constant features: {', '.join(audit['constant_features']) if audit['constant_features'] else 'none'}",
        f"- High-variance features (>=10 unique values): {', '.join(audit['high_variance_features']) if audit['high_variance_features'] else 'none'}",
        "",
        "## Feature diagnostics",
        "",
        "| Feature | Missing/null | Unique values | Numeric min | Numeric max | Numeric mean |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for name in audit["feature_names"]:
        stats = audit["numeric_stats"].get(name)
        if stats:
            stat_cells = [_format_float(stats["min"]), _format_float(stats["max"]), _format_float(stats["mean"])]
        else:
            stat_cells = ["n/a", "n/a", "n/a"]
        lines.append(
            f"| `{name}` | {audit['missing_counts'][name]} | {audit['unique_counts'][name]} | {stat_cells[0]} | {stat_cells[1]} | {stat_cells[2]} |"
        )
    lines.extend(
        [
            "",
            "## Audit metadata variation",
            "",
            "`scenario_group` and `perturbation_type` are joined from the public full-trace corpus record for audit stratification only. They are not added to the feature payload and are not scoring inputs.",
            "",
            f"- Features varying within/by scenario-group audit strata: {', '.join(sorted(audit['scenario_variation'])) if audit['scenario_variation'] else 'none'}",
            f"- Features varying within/by perturbation-type audit strata: {', '.join(sorted(audit['perturbation_variation'])) if audit['perturbation_variation'] else 'none'}",
        ]
    )
    (REPORT_DIR / "cct_feature_variance_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def _write_shortcut_report(audit: dict[str, Any]) -> None:
    graph = audit["graph_count_summary"]
    lines = [
        "# Journal-v1 Full-Trace CCT Structural Shortcut Risk Report",
        "",
        "Scope: structural shortcut diagnostics only; no gold-label performance comparison is performed.",
        "",
        "## Position and template shortcut checks",
        "",
        f"- Single features that perfectly determine step position: {', '.join(audit['perfectly_determines_position']) if audit['perfectly_determines_position'] else 'none'}",
        f"- Features that vary only by step position: {', '.join(audit['vary_only_by_position']) if audit['vary_only_by_position'] else 'none'}",
        f"- Maximum identical structural feature-vector count: {audit['max_identical_vector_count']} rows (warning threshold: {audit['duplicate_vector_threshold']}).",
        f"- Identical-vector warning: {'yes' if 'many identical structural feature vectors exist' in audit['warnings'] else 'no'}.",
        "",
        "## Graph-size constancy",
        "",
        f"- Graphs audited: {graph['graph_count']}",
        f"- Node-count unique values: {graph['node_count_unique']}",
        f"- Edge-count unique values: {graph['edge_count_unique']}",
        "- Interpretation: constant graph node/edge counts are expected for the current five-step linear full-trace corpus, but future scoring must not treat graph size alone as diagnostic evidence.",
        "",
        "## Private-field shortcut checks",
        "",
        f"- Forbidden private/gold fields in feature payloads: {'none' if not audit['forbidden_feature_paths'] else ', '.join(audit['forbidden_feature_paths'][:10])}",
        f"- Forbidden private/gold fields in graph payloads: {'none' if not audit['forbidden_graph_paths'] else ', '.join(audit['forbidden_graph_paths'][:10])}",
        f"- Structural shortcut warnings: {', '.join(audit['warnings']) if audit['warnings'] else 'none'}",
    ]
    (REPORT_DIR / "cct_structural_shortcut_risk_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def _write_readiness_gate(audit: dict[str, Any]) -> None:
    lines = [
        "# Journal-v1 Full-Trace CCT Feature Readiness Gate",
        "",
        f"Decision: `{audit['readiness_decision']}`.",
        "",
        "Future scoring may proceed only in a separately authorized task and only if this feature-layer audit has no unresolved blocker. Current warnings must be acknowledged in any future scoring protocol.",
        "",
        f"- Blockers: {', '.join(audit['blocker_reasons']) if audit['blocker_reasons'] else 'none'}",
        f"- Warnings: {', '.join(audit['warnings']) if audit['warnings'] else 'none'}",
        "- Private leakage status: pass; no forbidden private/gold fields were detected in graph or feature payloads." if not audit["forbidden_feature_paths"] and not audit["forbidden_graph_paths"] else "- Private leakage status: fail; forbidden fields were detected.",
        "- Non-actions: no scoring, ranking, evaluation, calibration, refinement, ablation, empirical hypothesis test, or paper-ready result table was produced.",
    ]
    (REPORT_DIR / "cct_feature_readiness_gate.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_reports(audit: dict[str, Any]) -> None:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    _write_variance_report(audit)
    _write_shortcut_report(audit)
    _write_readiness_gate(audit)


def main() -> int:
    audit = audit_feature_variance()
    write_reports(audit)
    print("=== CCT Feature Variance Audit ===")
    print(f"Feature rows audited: {audit['feature_row_count']}")
    print(f"Feature names: {', '.join(audit['feature_names'])}")
    print(f"Constant features: {', '.join(audit['constant_features']) if audit['constant_features'] else 'none'}")
    print(f"High-variance features: {', '.join(audit['high_variance_features']) if audit['high_variance_features'] else 'none'}")
    print(f"Graph node-count unique values: {audit['graph_count_summary']['node_count_unique']}")
    print(f"Graph edge-count unique values: {audit['graph_count_summary']['edge_count_unique']}")
    print(f"Warnings: {', '.join(audit['warnings']) if audit['warnings'] else 'none'}")
    print(f"Private leakage: {'PASS' if not audit['forbidden_feature_paths'] and not audit['forbidden_graph_paths'] else 'FAIL'}")
    print(f"Readiness decision: {audit['readiness_decision']}")
    if audit["blocker_reasons"]:
        print("FINAL: FAIL")
        return 1
    print("FINAL: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
