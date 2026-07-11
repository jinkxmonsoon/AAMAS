"""Representation-only redesigned CCT graph builder.

Task 24 integrates only the three authorized strong causal-flow edge types into
prediction-view-safe graph artifacts. This module does not score, rank,
calibrate, compare to gold/H6 labels, or produce evaluation results.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any

from cctdiag.cct.causal_edges import extract_causal_edges_from_prediction_view

STRONG_CAUSAL_EDGE_TYPES = {
    "downstream_dependency_edge",
    "tool_alignment_edge",
    "cross_agent_dependency_edge",
}
BASE_EDGE_TYPES = {"sequence_edge", "visible_handoff_edge"}
GRAPH_VERSION = "cct_redesigned_graph_v0_representation_only"


def build_redesigned_cct_graph(prediction_view: Mapping[str, Any]) -> dict[str, Any]:
    """Build a redesigned representation graph from a prediction view only."""

    trace_id = str(prediction_view["trace_id"])
    steps = list(prediction_view["steps"])
    nodes = _build_step_nodes(trace_id, steps)
    base_edges = _build_base_edges(trace_id, steps)
    causal_edges = extract_causal_edges_from_prediction_view(prediction_view, edge_types=STRONG_CAUSAL_EDGE_TYPES)
    graph_edges = base_edges + [_graph_edge_from_causal_edge(edge) for edge in causal_edges]
    return {
        "graph_version": GRAPH_VERSION,
        "trace_id": trace_id,
        "construction_scope": "representation_only_no_scoring_no_gold_comparison",
        "nodes": nodes,
        "edges": graph_edges,
        "edge_type_counts": _edge_type_counts(graph_edges),
        "node_count": len(nodes),
        "base_edge_count": len(base_edges),
        "causal_flow_edge_count": len(causal_edges),
        "total_edge_count": len(graph_edges),
        "causal_edge_types_included": sorted(STRONG_CAUSAL_EDGE_TYPES),
        "causal_edge_types_excluded": [
            "constraint_shift_edge",
            "semantic_collision_edge",
            "evidence_conflict_edge",
            "evidence_omission_edge",
            "correction_opportunity_edge",
            "correction_attempt_edge",
            "unresolved_caveat_edge",
        ],
    }


def base_graph_signature(graph: Mapping[str, Any]) -> str:
    """Return a coarse base-graph signature before causal-flow augmentation."""

    edge_counts = graph["edge_type_counts"]
    return "|".join(
        [
            f"nodes={graph['node_count']}",
            f"sequence_edge={edge_counts.get('sequence_edge', 0)}",
            f"visible_handoff_edge={edge_counts.get('visible_handoff_edge', 0)}",
        ]
    )


def redesigned_graph_signature(graph: Mapping[str, Any]) -> str:
    """Return a representation signature including strong causal-flow edges."""

    edge_counts = graph["edge_type_counts"]
    causal_deltas = []
    for edge in graph["edges"]:
        if edge["edge_type"] in STRONG_CAUSAL_EDGE_TYPES:
            causal_deltas.append(str(edge.get("step_delta")))
    return "|".join(
        [
            base_graph_signature(graph),
            f"downstream_dependency_edge={edge_counts.get('downstream_dependency_edge', 0)}",
            f"tool_alignment_edge={edge_counts.get('tool_alignment_edge', 0)}",
            f"cross_agent_dependency_edge={edge_counts.get('cross_agent_dependency_edge', 0)}",
            "deltas=" + ",".join(sorted(causal_deltas)),
        ]
    )


def _build_step_nodes(trace_id: str, steps: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    nodes = []
    for step in steps:
        nodes.append(
            {
                "node_id": _step_node_id(trace_id, step),
                "node_type": "step",
                "step_id": step["step_id"],
                "visible_fields_present": sorted(key for key, value in step.items() if value not in (None, "", [], {})),
            }
        )
    return nodes


def _build_base_edges(trace_id: str, steps: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    edges: list[dict[str, Any]] = []
    for index, source in enumerate(steps[:-1], start=1):
        target = steps[index]
        edges.append(
            _base_edge(
                trace_id=trace_id,
                edge_index=len(edges) + 1,
                edge_type="sequence_edge",
                source=source,
                target=target,
                visible_fields_used=["step_id"],
                extraction_rule_id="visible_step_order_sequence_v0",
            )
        )
        if source.get("handoff_to") or target.get("handoff_from"):
            edges.append(
                _base_edge(
                    trace_id=trace_id,
                    edge_index=len(edges) + 1,
                    edge_type="visible_handoff_edge",
                    source=source,
                    target=target,
                    visible_fields_used=["handoff_from", "handoff_to"],
                    extraction_rule_id="visible_handoff_adjacency_v0",
                )
            )
    return edges


def _base_edge(
    *,
    trace_id: str,
    edge_index: int,
    edge_type: str,
    source: Mapping[str, Any],
    target: Mapping[str, Any],
    visible_fields_used: list[str],
    extraction_rule_id: str,
) -> dict[str, Any]:
    return {
        "edge_id": f"{trace_id}:base_edge:{edge_index:03d}",
        "edge_type": edge_type,
        "source_node_id": _step_node_id(trace_id, source),
        "target_node_id": _step_node_id(trace_id, target),
        "source_step_id": source["step_id"],
        "target_step_id": target["step_id"],
        "visible_fields_used": visible_fields_used,
        "extraction_rule_id": extraction_rule_id,
        "step_delta": _step_delta(source["step_id"], target["step_id"]),
        "representation_only": True,
    }


def _graph_edge_from_causal_edge(edge: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "edge_id": edge["edge_id"],
        "edge_type": edge["edge_type"],
        "source_node_id": edge["source_node_id"],
        "target_node_id": edge["target_node_id"],
        "source_step_id": edge["source_step_id"],
        "target_step_id": edge["target_step_id"],
        "visible_fields_used": list(edge["visible_fields_used"]),
        "extraction_rule_id": edge["extraction_rule_id"],
        "extraction_notes": edge["extraction_notes"],
        "extraction_version": edge["extraction_version"],
        "step_delta": _step_delta(edge.get("source_step_id"), edge.get("target_step_id")),
        "representation_only": True,
    }


def _edge_type_counts(edges: Sequence[Mapping[str, Any]]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for edge in edges:
        edge_type = str(edge["edge_type"])
        counts[edge_type] = counts.get(edge_type, 0) + 1
    return dict(sorted(counts.items()))


def _step_node_id(trace_id: str, step: Mapping[str, Any]) -> str:
    return f"trace:{trace_id}:step:{step['step_id']}"


def _step_delta(source_step_id: Any, target_step_id: Any) -> int | None:
    try:
        return int(str(target_step_id).lstrip("s")) - int(str(source_step_id).lstrip("s"))
    except ValueError:
        return None
