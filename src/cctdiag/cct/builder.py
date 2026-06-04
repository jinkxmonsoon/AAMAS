"""Visible-only full-trace CCT graph builder.

This module constructs graph artifacts from sanitized full-trace prediction
views only. It does not implement CCT scoring, ranking, calibration,
refinement variants, ablations, empirical hypothesis tests, or paper-ready
result tables.
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from cctdiag.io.full_trace_views import make_full_trace_prediction_view

GRAPH_SCHEMA_VERSION = "journal_v1_full_trace_cct_graph_v1"


def _token_count(value: Any) -> int:
    return len(str(value or "").split())


def build_cct_graph(record: Mapping[str, Any]) -> dict[str, Any]:
    """Build a visible full-trace graph for one record."""

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
