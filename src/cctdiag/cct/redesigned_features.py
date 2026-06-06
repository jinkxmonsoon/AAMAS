"""Representation-only features for redesigned CCT graphs.

Task 24A extracts structural features from redesigned graph artifacts. These
features are for audit only and are not scores, ranks, calibrated values, or
paper-ready results.
"""

from __future__ import annotations

from collections import Counter
from collections.abc import Mapping, Sequence
from typing import Any

STRONG_CAUSAL_EDGE_TYPES = {
    "downstream_dependency_edge",
    "tool_alignment_edge",
    "cross_agent_dependency_edge",
}
FEATURE_NAMES = [
    "causal_flow_edge_count_total",
    "downstream_dependency_edge_count",
    "tool_alignment_edge_count",
    "cross_agent_dependency_edge_count",
    "incoming_causal_flow_edge_count",
    "outgoing_causal_flow_edge_count",
    "non_adjacent_dependency_count",
    "cross_agent_dependency_count",
    "tool_alignment_relation_count",
    "causal_flow_degree",
    "causal_flow_in_degree",
    "causal_flow_out_degree",
    "causal_flow_edge_type_diversity",
]
FORBIDDEN_FEATURE_FIELDS = {
    "private_labels",
    "gold_failure_step",
    "gold_failure_agent",
    "gold_irreversibility",
    "gold_propagation",
    "gold_recoverability",
    "label_rationale",
    "provenance",
    "correctness",
    "correct",
    "incorrect",
    "score",
    "rank",
    "scenario_group",
    "perturbation_type",
}


def extract_redesigned_graph_features(graph: Mapping[str, Any]) -> dict[str, Any]:
    """Extract one representation-only feature row from a redesigned graph."""

    causal_edges = [edge for edge in graph.get("edges", []) if edge.get("edge_type") in STRONG_CAUSAL_EDGE_TYPES]
    edge_counts = Counter(edge["edge_type"] for edge in causal_edges)
    incoming = Counter(edge.get("target_step_id") for edge in causal_edges)
    outgoing = Counter(edge.get("source_step_id") for edge in causal_edges)
    non_adjacent = sum(1 for edge in causal_edges if edge.get("step_delta") not in {None, 0, 1})
    row = {
        "trace_id": graph["trace_id"],
        "causal_flow_edge_count_total": len(causal_edges),
        "downstream_dependency_edge_count": edge_counts.get("downstream_dependency_edge", 0),
        "tool_alignment_edge_count": edge_counts.get("tool_alignment_edge", 0),
        "cross_agent_dependency_edge_count": edge_counts.get("cross_agent_dependency_edge", 0),
        "incoming_causal_flow_edge_count": sum(incoming.values()),
        "outgoing_causal_flow_edge_count": sum(outgoing.values()),
        "non_adjacent_dependency_count": non_adjacent,
        "cross_agent_dependency_count": edge_counts.get("cross_agent_dependency_edge", 0),
        "tool_alignment_relation_count": edge_counts.get("tool_alignment_edge", 0),
        "causal_flow_degree": sum(incoming.values()) + sum(outgoing.values()),
        "causal_flow_in_degree": max(incoming.values(), default=0),
        "causal_flow_out_degree": max(outgoing.values(), default=0),
        "causal_flow_edge_type_diversity": len(edge_counts),
    }
    validate_redesigned_feature_row(row)
    return row


def feature_vector(row: Mapping[str, Any]) -> tuple[Any, ...]:
    """Return the comparable feature-vector portion of a feature row."""

    return tuple(row[name] for name in FEATURE_NAMES)


def validate_redesigned_feature_row(row: Mapping[str, Any]) -> None:
    forbidden = sorted(set(row) & FORBIDDEN_FEATURE_FIELDS)
    if forbidden:
        raise ValueError("redesigned feature row contains forbidden field(s): " + ", ".join(forbidden))
    missing = [name for name in FEATURE_NAMES if name not in row]
    if missing:
        raise ValueError("redesigned feature row missing required feature(s): " + ", ".join(missing))


def redesigned_feature_leakage_findings(rows: Sequence[Mapping[str, Any]]) -> list[str]:
    findings: list[str] = []
    for row_index, row in enumerate(rows):
        for key in row:
            if key in FORBIDDEN_FEATURE_FIELDS:
                findings.append(f"row[{row_index}].{key}")
    return findings
