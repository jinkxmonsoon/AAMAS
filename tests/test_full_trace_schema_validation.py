"""Tests for full ordered trace schema validation."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from cctdiag.schema.errors import ValidationError
from cctdiag.schema.full_trace_contracts import REQUIRED_FULL_TRACE_FIELDS, REQUIRED_PRIVATE_LABEL_FIELDS, REQUIRED_STEP_FIELDS
from cctdiag.schema.full_trace_validators import validate_full_trace_schema

FIXTURE_DIR = Path(__file__).parent / "fixtures/full_trace"


def load_fixture(name: str) -> dict:
    return json.loads((FIXTURE_DIR / name).read_text(encoding="utf-8"))


def test_full_trace_contract_field_sets_include_required_schema_fields():
    assert {
        "trace_id",
        "dataset_version",
        "scenario_group",
        "case_id",
        "case_variant",
        "perturbation_type",
        "perturbation_intensity",
        "steps",
        "terminal_outcome",
        "private_labels",
        "provenance",
    }.issubset(REQUIRED_FULL_TRACE_FIELDS)
    assert {
        "step_id",
        "agent_id",
        "agent_role",
        "input_message",
        "output_message",
        "tool_call",
        "tool_output",
        "handoff_from",
        "handoff_to",
        "evidence_items",
        "evidence_used",
        "visible_step_notes",
    }.issubset(REQUIRED_STEP_FIELDS)
    assert {
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
    }.issubset(REQUIRED_PRIVATE_LABEL_FIELDS)


def test_minimal_valid_full_trace_fixture_passes():
    validate_full_trace_schema(load_fixture("minimal_valid_full_trace.json"))


@pytest.mark.parametrize(
    ("fixture_name", "expected_message"),
    [
        ("invalid_missing_steps.json", "Missing required full-trace fields"),
        ("invalid_gold_step_not_in_steps.json", "gold_failure_step must exist among steps"),
        ("invalid_failure_centered_top_level.json", "Top-level failure-centered fields are forbidden"),
        ("invalid_single_candidate_trace.json", "at least 2 distinct agents"),
    ],
)
def test_invalid_full_trace_fixtures_fail_for_expected_reasons(fixture_name: str, expected_message: str):
    with pytest.raises(ValidationError, match=expected_message):
        validate_full_trace_schema(load_fixture(fixture_name))
