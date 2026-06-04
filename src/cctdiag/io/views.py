"""Prediction/private view helpers for Journal-v1 records.

The prediction view is the only object that diagnostic baselines and future
models may inspect. It intentionally removes private labels, rationales,
provenance, target-equivalent top-level failure pointers, and H6 evidence fields
that state label outcomes.
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

Record = Mapping[str, Any]

PREDICTION_VIEW_VERSION = "journal_v1_prediction_view_v1"
PRIVATE_LABEL_VIEW_VERSION = "journal_v1_private_label_view_v1"

GOLD_FIELDS = {
    "gold_failure_step",
    "gold_failure_agent",
    "gold_irreversibility",
    "gold_propagation",
    "gold_recoverability",
}

PRIVATE_METADATA_FIELDS = {
    "label_rationale",
    "label_source",
    "label_confidence",
    "primary_labeler",
    "secondary_labeler",
    "adjudication_decision",
    "adjudicator",
    "manual_audit_status",
    "annotator_or_generator",
    "provenance_notes",
    "synthetic_control_rule",
    "generation_seed",
}

PRIVATE_H6_EVIDENCE_FIELDS = {
    "propagation_evidence",
    "irreversibility_evidence",
    "recovery_opportunity",
}

TARGET_EQUIVALENT_TOP_LEVEL_FIELDS = {
    "step_id",
    "agent_id",
    "handoff_from",
    "handoff_to",
}

FORBIDDEN_PREDICTION_FIELDS = (
    GOLD_FIELDS | PRIVATE_METADATA_FIELDS | PRIVATE_H6_EVIDENCE_FIELDS | TARGET_EQUIVALENT_TOP_LEVEL_FIELDS
)

VISIBLE_TRACE_FIELDS = (
    "input_message",
    "output_message",
    "tool_call",
    "tool_output",
    "terminal_outcome",
    "agent_role",
)


def make_prediction_view(record: Record) -> dict[str, Any]:
    """Return a sanitized model-visible prediction view for one raw record."""

    observed_step = {field: record.get(field) for field in VISIBLE_TRACE_FIELDS if field in record}
    view: dict[str, Any] = {
        "view_version": PREDICTION_VIEW_VERSION,
        "trace_id": record.get("trace_id"),
        "case_variant": record.get("case_variant"),
        "candidate_steps": list(record.get("step_catalog") or []),
        "candidate_agents": list(record.get("agent_catalog") or []),
        "observed_step_content": observed_step,
        "model_visible_evidence_items": list(record.get("evidence_items") or []),
        "representation_warning": (
            "failure_centered_single_record_without_full_ordered_multistep_trace"
        ),
    }
    assert_no_gold_leakage(view)
    return view


def make_private_label_view(record: Record) -> dict[str, Any]:
    """Return private gold labels and private diagnostic metadata for evaluation only."""

    fields = GOLD_FIELDS | PRIVATE_METADATA_FIELDS | PRIVATE_H6_EVIDENCE_FIELDS | TARGET_EQUIVALENT_TOP_LEVEL_FIELDS
    return {
        "view_version": PRIVATE_LABEL_VIEW_VERSION,
        "trace_id": record.get("trace_id"),
        **{field: record.get(field) for field in sorted(fields) if field in record},
    }


def assert_no_gold_leakage(prediction_view: Mapping[str, Any]) -> None:
    """Raise if a prediction view exposes forbidden target/private fields."""

    leaked_paths: list[str] = []

    def visit(value: Any, path: str) -> None:
        if isinstance(value, Mapping):
            for key, nested in value.items():
                key_text = str(key)
                nested_path = f"{path}.{key_text}" if path else key_text
                if key_text in FORBIDDEN_PREDICTION_FIELDS:
                    leaked_paths.append(nested_path)
                visit(nested, nested_path)
        elif isinstance(value, list | tuple):
            for index, item in enumerate(value):
                visit(item, f"{path}[{index}]")

    visit(prediction_view, "")
    if leaked_paths:
        raise ValueError("prediction view exposes forbidden fields: " + ", ".join(sorted(leaked_paths)))
