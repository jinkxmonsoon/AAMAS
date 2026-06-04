"""Structural CCT feature extraction from visible graph artifacts.

Feature rows are descriptive preprocessing artifacts. They are not predictions,
scores, rankings, calibration outputs, refinement outputs, ablation outputs,
empirical hypothesis tests, or paper-ready result tables.
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

FEATURE_SCHEMA_VERSION = "journal_v1_full_trace_cct_features_v1"


def extract_cct_feature_rows(graph: Mapping[str, Any]) -> list[dict[str, Any]]:
    """Extract one compact structural feature row per step node without scoring."""

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
