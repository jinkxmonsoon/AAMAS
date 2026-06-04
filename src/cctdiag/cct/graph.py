"""Full-trace CCT graph construction and feature extraction.

This module builds model-visible graph artifacts only. It does not implement
CCT scoring, ranking, calibration, refinement variants, ablations, empirical
hypothesis tests, or paper-ready result tables.
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from cctdiag.io.full_trace_views import make_full_trace_prediction_view

GRAPH_SCHEMA_VERSION = "journal_v1_full_trace_cct_graph_v1"
FEATURE_SCHEMA_VERSION = "journal_v1_full_trace_cct_features_v1"


def _text_len(value: Any) -> int:
    return len(str(value or ""))


def _token_count(value: Any) -> int:
    return len(str(value or "").split())


def build_cct_graph(record: Mapping[str, Any]) -> dict[str, Any]:
    """Build a visible full-trace graph for one record.

    The graph uses only the full-trace prediction view. Private labels and
    provenance are intentionally unavailable to this function after view
    construction.
    """

    view = make_full_trace_prediction_view(record)
    steps = view["steps"]
    nodes = []
    edges = []

    for index, step in enumerate(steps):
        node_id = step["step_id"]
        nodes.append(
            {
                "node_id": node_id,
                "node_type": "trace_step",
                "order_index": index,
                "agent_id": step["agent_id"],
                "agent_role": step["agent_role"],
                "input_token_count": _token_count(step.get("input_message")),
                "output_token_count": _token_count(step.get("output_message")),
                "tool_output_token_count": _token_count(step.get("tool_output")),
                "evidence_item_count": len(step.get("evidence_items") or []),
                "evidence_used_count": len(step.get("evidence_used") or []),
                "has_tool_call": bool(step.get("tool_call")),
                "has_handoff_from": bool(step.get("handoff_from")),
                "has_handoff_to": bool(step.get("handoff_to")),
            }
        )
        if index > 0:
            edges.append(
                {
                    "source": steps[index - 1]["step_id"],
                    "target": node_id,
                    "edge_type": "temporal_next",
                }
            )
        if step.get("handoff_from"):
            edges.append(
                {
                    "source": str(step["handoff_from"]),
                    "target": node_id,
                    "edge_type": "handoff_from_agent",
                }
            )
        if step.get("handoff_to"):
            edges.append(
                {
                    "source": node_id,
                    "target": str(step["handoff_to"]),
                    "edge_type": "handoff_to_agent",
                }
            )

    return {
        "graph_schema_version": GRAPH_SCHEMA_VERSION,
        "trace_id": view["trace_id"],
        "candidate_steps": view["candidate_steps"],
        "candidate_agents": view["candidate_agents"],
        "nodes": nodes,
        "edges": edges,
    }


def extract_cct_feature_rows(graph: Mapping[str, Any]) -> list[dict[str, Any]]:
    """Extract one compact feature row per step node without scoring."""

    in_degree: dict[str, int] = {}
    out_degree: dict[str, int] = {}
    for edge in graph["edges"]:
        source = str(edge["source"])
        target = str(edge["target"])
        out_degree[source] = out_degree.get(source, 0) + 1
        in_degree[target] = in_degree.get(target, 0) + 1

    rows = []
    for node in graph["nodes"]:
        node_id = node["node_id"]
        rows.append(
            {
                "feature_schema_version": FEATURE_SCHEMA_VERSION,
                "trace_id": graph["trace_id"],
                "step_id": node_id,
                "agent_id": node["agent_id"],
                "agent_role": node["agent_role"],
                "order_index": node["order_index"],
                "in_degree": in_degree.get(node_id, 0),
                "out_degree": out_degree.get(node_id, 0),
                "input_token_count": node["input_token_count"],
                "output_token_count": node["output_token_count"],
                "tool_output_token_count": node["tool_output_token_count"],
                "evidence_item_count": node["evidence_item_count"],
                "evidence_used_count": node["evidence_used_count"],
                "has_tool_call": node["has_tool_call"],
                "has_handoff_from": node["has_handoff_from"],
                "has_handoff_to": node["has_handoff_to"],
            }
        )
    return rows
