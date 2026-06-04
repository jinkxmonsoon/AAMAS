"""Prediction/private view helpers for full ordered trace records."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from cctdiag.schema.full_trace_contracts import PRIVATE_PREDICTION_FORBIDDEN_FIELDS, REQUIRED_STEP_FIELDS
from cctdiag.schema.full_trace_validators import validate_full_trace_schema

FULL_TRACE_PREDICTION_VIEW_VERSION = "journal_v1_full_trace_prediction_view_v1"
FULL_TRACE_PRIVATE_LABEL_VIEW_VERSION = "journal_v1_full_trace_private_label_view_v1"

VISIBLE_STEP_FIELDS = REQUIRED_STEP_FIELDS


def make_full_trace_prediction_view(record: Mapping[str, Any]) -> dict[str, Any]:
    """Return model-visible full-trace prediction input for one valid record."""

    validate_full_trace_schema(record)
    visible_steps = []
    for step in record["steps"]:
        visible_steps.append({field: step.get(field) for field in sorted(VISIBLE_STEP_FIELDS)})

    view = {
        "view_version": FULL_TRACE_PREDICTION_VIEW_VERSION,
        "trace_id": record.get("trace_id"),
        "candidate_steps": [step["step_id"] for step in visible_steps],
        "candidate_agents": sorted({step["agent_id"] for step in visible_steps}),
        "steps": visible_steps,
    }
    assert_no_full_trace_private_leakage(view)
    return view


def make_full_trace_private_label_view(record: Mapping[str, Any]) -> dict[str, Any]:
    """Return private labels/provenance for evaluation after predictions are produced."""

    validate_full_trace_schema(record)
    return {
        "view_version": FULL_TRACE_PRIVATE_LABEL_VIEW_VERSION,
        "trace_id": record.get("trace_id"),
        "private_labels": dict(record["private_labels"]),
        "provenance": dict(record["provenance"]),
    }


def assert_no_full_trace_private_leakage(prediction_view: Mapping[str, Any]) -> None:
    """Raise if a full-trace prediction view exposes private/gold fields."""

    leaked_paths: list[str] = []

    def visit(value: Any, path: str) -> None:
        if isinstance(value, Mapping):
            for key, nested in value.items():
                key_text = str(key)
                nested_path = f"{path}.{key_text}" if path else key_text
                if key_text in PRIVATE_PREDICTION_FORBIDDEN_FIELDS:
                    leaked_paths.append(nested_path)
                if path == "" and key_text in {"step_id", "agent_id"}:
                    leaked_paths.append(nested_path)
                visit(nested, nested_path)
        elif isinstance(value, list | tuple):
            for index, item in enumerate(value):
                visit(item, f"{path}[{index}]")

    visit(prediction_view, "")
    if leaked_paths:
        raise ValueError("full-trace prediction view exposes private fields: " + ", ".join(sorted(leaked_paths)))
