#!/usr/bin/env python3
"""Validate reproducible full-trace CCT graph artifacts without scoring."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

FORBIDDEN_KEYS = {
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
}
INPUT_PATH = ROOT / "data/processed/journal_v1_full_trace/main_full_trace_all.jsonl"
OUT_DIR = ROOT / "data/interim/journal_v1_full_trace_cct"
GRAPHS_PATH = OUT_DIR / "cct_graphs.jsonl"
FEATURES_PATH = OUT_DIR / "cct_features.jsonl"
SAMPLE_GRAPHS_PATH = OUT_DIR / "sample_cct_graphs.jsonl"
SAMPLE_FEATURES_PATH = OUT_DIR / "sample_cct_features.jsonl"


def _read_jsonl(path: Path) -> list[dict[str, Any]]:
    with path.open(encoding="utf-8") as handle:
        return [json.loads(line) for line in handle if line.strip()]


def _find_forbidden(value: Any, path: str = "") -> list[str]:
    found: list[str] = []
    if isinstance(value, dict):
        for key, nested in value.items():
            nested_path = f"{path}.{key}" if path else str(key)
            if key in FORBIDDEN_KEYS:
                found.append(nested_path)
            found.extend(_find_forbidden(nested, nested_path))
    elif isinstance(value, list):
        for index, item in enumerate(value):
            found.extend(_find_forbidden(item, f"{path}[{index}]"))
    return found


def _require(condition: bool, message: str, failures: list[str]) -> None:
    if not condition:
        failures.append(message)


def main() -> int:
    failures: list[str] = []
    for path in [GRAPHS_PATH, FEATURES_PATH, SAMPLE_GRAPHS_PATH, SAMPLE_FEATURES_PATH]:
        _require(path.is_file(), f"missing artifact: {path.relative_to(ROOT)}", failures)
    if failures:
        for failure in failures:
            print(f"FAIL: {failure}")
        return 1

    records = _read_jsonl(INPUT_PATH)
    graphs = _read_jsonl(GRAPHS_PATH)
    features = _read_jsonl(FEATURES_PATH)
    sample_graphs = _read_jsonl(SAMPLE_GRAPHS_PATH)
    sample_features = _read_jsonl(SAMPLE_FEATURES_PATH)
    expected_feature_rows = sum(len(record["steps"]) for record in records)

    _require(len(graphs) == len(records), f"expected {len(records)} graphs, found {len(graphs)}", failures)
    _require(len(features) == expected_feature_rows, f"expected {expected_feature_rows} feature rows, found {len(features)}", failures)
    _require(len(sample_graphs) >= 2, "sample must contain at least two graphs", failures)
    _require(len(sample_features) >= 2, "sample must contain corresponding feature rows", failures)

    variants = {record["trace_id"]: record.get("case_variant") for record in records}
    sample_variants = {variants.get(graph["trace_id"]) for graph in sample_graphs}
    _require("clean" in sample_variants, "sample missing clean trace graph", failures)
    _require(any(variant != "clean" for variant in sample_variants), "sample missing perturbed trace graph", failures)

    graph_ids = {graph["trace_id"] for graph in graphs}
    sample_graph_ids = {graph["trace_id"] for graph in sample_graphs}
    sample_feature_ids = {row["trace_id"] for row in sample_features}
    _require(sample_feature_ids == sample_graph_ids, "sample feature rows do not correspond to sample graphs", failures)
    _require({row["trace_id"] for row in features}.issubset(graph_ids), "feature trace IDs are not a subset of graph IDs", failures)

    for artifact_name, rows in [("graphs", graphs), ("features", features), ("sample_graphs", sample_graphs), ("sample_features", sample_features)]:
        leaked = []
        for index, row in enumerate(rows):
            leaked.extend(f"{artifact_name}[{index}].{path}" for path in _find_forbidden(row))
        _require(not leaked, "private-field leakage detected: " + ", ".join(leaked[:10]), failures)

    print("=== Full-Trace CCT Graph Validation ===")
    print(f"Input traces: {len(records)}")
    print(f"Graphs: {len(graphs)}")
    print(f"Feature rows: {len(features)}")
    print(f"Sample graphs: {len(sample_graphs)}")
    print(f"Sample feature rows: {len(sample_features)}")
    if failures:
        for failure in failures:
            print(f"FAIL: {failure}")
        print("FINAL: FAIL")
        return 1
    print("FINAL: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
