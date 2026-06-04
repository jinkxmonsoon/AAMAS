"""Validators for the Journal-v1 full ordered trace schema."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from cctdiag.schema.errors import ValidationError
from cctdiag.schema.full_trace_contracts import (
    DATASET_VERSION,
    FORBIDDEN_FULL_TRACE_TOP_LEVEL_FIELDS,
    MIN_AGENTS_PER_TRACE,
    MIN_NON_GOLD_CANDIDATE_AGENTS,
    MIN_NON_GOLD_CANDIDATE_STEPS,
    MIN_STEPS_PER_TRACE,
    PERTURBATION_TYPES,
    REQUIRED_FULL_TRACE_FIELDS,
    REQUIRED_PRIVATE_LABEL_FIELDS,
    REQUIRED_PROVENANCE_FIELDS,
    REQUIRED_STEP_FIELDS,
    SCENARIO_GROUPS,
)


def _is_none_like(value: Any) -> bool:
    return value is None or value == "" or str(value).lower() == "none"


def _require_mapping(value: Any, label: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise ValidationError(f"{label} must be an object")
    return value


def _require_non_empty_text(value: Any, label: str) -> None:
    if value is None or str(value).strip() == "":
        raise ValidationError(f"{label} must be present")


def validate_full_trace_schema(record: Mapping[str, Any]) -> None:
    """Validate one full ordered multi-step trace record."""

    missing = REQUIRED_FULL_TRACE_FIELDS - set(record)
    if missing:
        raise ValidationError(f"Missing required full-trace fields: {sorted(missing)}")

    forbidden = FORBIDDEN_FULL_TRACE_TOP_LEVEL_FIELDS & set(record)
    if forbidden:
        raise ValidationError(f"Top-level failure-centered fields are forbidden: {sorted(forbidden)}")

    if record.get("dataset_version") != DATASET_VERSION:
        raise ValidationError("dataset_version must be BRACIS-Journal-v1")
    if record.get("scenario_group") not in SCENARIO_GROUPS:
        raise ValidationError("Invalid scenario_group")
    if record.get("perturbation_type") not in PERTURBATION_TYPES:
        raise ValidationError("Invalid perturbation_type")
    if record.get("perturbation_type") == "none" and not _is_none_like(record.get("perturbation_intensity")):
        raise ValidationError("perturbation_intensity must be none/null when perturbation_type is none")
    if record.get("perturbation_type") != "none" and _is_none_like(record.get("perturbation_intensity")):
        raise ValidationError("perturbation_intensity required when perturbation_type != none")

    steps = record.get("steps")
    if not isinstance(steps, list) or not steps:
        raise ValidationError("steps must be an ordered non-empty list")
    if len(steps) < MIN_STEPS_PER_TRACE:
        raise ValidationError(f"full trace must contain at least {MIN_STEPS_PER_TRACE} ordered steps")

    step_ids: list[Any] = []
    agent_ids: list[Any] = []
    for index, step in enumerate(steps):
        step_obj = _require_mapping(step, f"steps[{index}]")
        missing_step_fields = REQUIRED_STEP_FIELDS - set(step_obj)
        if missing_step_fields:
            raise ValidationError(f"steps[{index}] missing required fields: {sorted(missing_step_fields)}")
        _require_non_empty_text(step_obj.get("step_id"), f"steps[{index}].step_id")
        _require_non_empty_text(step_obj.get("agent_id"), f"steps[{index}].agent_id")
        if not isinstance(step_obj.get("evidence_items"), list):
            raise ValidationError(f"steps[{index}].evidence_items must be a list")
        if not isinstance(step_obj.get("evidence_used"), list):
            raise ValidationError(f"steps[{index}].evidence_used must be a list")
        step_ids.append(step_obj.get("step_id"))
        agent_ids.append(step_obj.get("agent_id"))

    if len(set(step_ids)) != len(step_ids):
        raise ValidationError("step_id values must be unique within a full trace")
    if len(set(agent_ids)) < MIN_AGENTS_PER_TRACE:
        raise ValidationError(f"full trace must contain at least {MIN_AGENTS_PER_TRACE} distinct agents")

    private_labels = _require_mapping(record.get("private_labels"), "private_labels")
    missing_private_fields = REQUIRED_PRIVATE_LABEL_FIELDS - set(private_labels)
    if missing_private_fields:
        raise ValidationError(f"private_labels missing required fields: {sorted(missing_private_fields)}")

    gold_step = private_labels.get("gold_failure_step")
    gold_agent = private_labels.get("gold_failure_agent")
    if gold_step not in set(step_ids):
        raise ValidationError("gold_failure_step must exist among steps")
    if gold_agent not in set(agent_ids):
        raise ValidationError("gold_failure_agent must appear among steps")
    non_gold_steps = set(step_ids) - {gold_step}
    if len(non_gold_steps) < MIN_NON_GOLD_CANDIDATE_STEPS:
        raise ValidationError(
            f"full trace must contain at least {MIN_NON_GOLD_CANDIDATE_STEPS} plausible non-gold candidate steps"
        )
    non_gold_agents = set(agent_ids) - {gold_agent}
    if len(non_gold_agents) < MIN_NON_GOLD_CANDIDATE_AGENTS:
        raise ValidationError(
            f"full trace must contain at least {MIN_NON_GOLD_CANDIDATE_AGENTS} plausible non-gold candidate agent"
        )

    conf = private_labels.get("label_confidence")
    if not isinstance(conf, int | float) or conf < 0 or conf > 1:
        raise ValidationError("private_labels.label_confidence must be numeric in [0,1]")

    provenance = _require_mapping(record.get("provenance"), "provenance")
    missing_provenance = REQUIRED_PROVENANCE_FIELDS - set(provenance)
    if missing_provenance:
        raise ValidationError(f"provenance missing required fields: {sorted(missing_provenance)}")
