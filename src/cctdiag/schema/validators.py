"""Schema and label validators for Journal-v1 corpus records."""

from __future__ import annotations
from .contracts import *
from .errors import ValidationError


def _is_none_like(v):
    return v is None or v == "" or str(v).lower() == "none"


def validate_record_schema(record: dict) -> None:
    missing = REQUIRED_FIELDS - set(record)
    if missing:
        raise ValidationError(f"Missing required fields: {sorted(missing)}")
    if record["dataset_version"] != DATASET_VERSION:
        raise ValidationError("dataset_version must be BRACIS-Journal-v1")
    if record["scenario_group"] not in SCENARIO_GROUPS:
        raise ValidationError("Invalid scenario_group")
    if record["perturbation_type"] not in PERTURBATION_TYPES:
        raise ValidationError("Invalid perturbation_type")
    if record["perturbation_type"] == "none":
        if not _is_none_like(record["perturbation_intensity"]):
            raise ValidationError("perturbation_intensity must be none/null when perturbation_type is none")
    else:
        if _is_none_like(record["perturbation_intensity"]):
            raise ValidationError("perturbation_intensity required when perturbation_type != none")
        if _is_none_like(record.get("clean_parent_trace_id")):
            raise ValidationError("clean_parent_trace_id required for perturbation variants")
    if _is_none_like(record["step_id"]):
        raise ValidationError("step_id must be present")
    conf = record["label_confidence"]
    if not isinstance(conf, (int, float)) or conf < 0 or conf > 1:
        raise ValidationError("label_confidence must be numeric in [0,1]")
    if _is_none_like(record["label_source"]):
        raise ValidationError("label_source required")
    for p in PROVENANCE_FIELDS:
        if _is_none_like(record.get(p)):
            raise ValidationError(f"Missing provenance field: {p}")
    if "bracis_v0" in str(record.get("provenance_notes", "")).lower() and "historical" not in str(record.get("provenance_notes", "")).lower():
        raise ValidationError("BRACIS v0 cannot be used as empirical source")


def validate_label_consistency(record: dict, trace_steps: list[dict]) -> None:
    step_ids = {s.get("step_id") for s in trace_steps}
    agent_ids = {s.get("agent_id") for s in trace_steps}
    if record.get("gold_failure_step") not in step_ids:
        raise ValidationError("gold_failure_step must exist in trace")
    if record.get("gold_failure_agent") not in agent_ids:
        raise ValidationError("gold_failure_agent must appear in trace")
    for key in ["gold_irreversibility", "gold_propagation", "gold_recoverability"]:
        if record.get(key) not in BOOL_ENUM:
            raise ValidationError(f"{key} must be boolean/controlled enum")
    if record.get("perturbation_type") != "none" and _is_none_like(record.get("clean_parent_trace_id")):
        raise ValidationError("perturbation variant must contain clean_parent_trace_id")
    if record.get("perturbation_type") != "none" and record.get("case_variant") == "clean":
        raise ValidationError("perturbation variants must not overwrite clean cases")
