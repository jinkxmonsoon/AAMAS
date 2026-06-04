"""Tests for sanitized prediction/private view contracts."""

import pytest

from cctdiag.io.views import assert_no_gold_leakage, make_prediction_view, make_private_label_view


RAW_RECORD = {
    "trace_id": "JV1_example",
    "case_id": "SG_EX_C001",
    "case_variant": "clean",
    "scenario_group": "clean_broken_handoff",
    "perturbation_type": "none",
    "step_id": "s2",
    "agent_id": "a5",
    "agent_role": "analyst",
    "agent_catalog": ["a3", "a5", "a9"],
    "step_catalog": ["s1", "s2", "s3", "s4"],
    "input_message": "phase=handoff-intake; unresolved constraint mismatch",
    "output_message": "Intake summary moved forward with unresolved gap",
    "tool_call": "query_incident_log",
    "tool_output": "handoff-audit: mismatch open",
    "terminal_outcome": "degraded_execution",
    "handoff_from": "a3",
    "handoff_to": "a5",
    "evidence_items": ["ev1", "ev2"],
    "evidence_used": ["ev1"],
    "gold_failure_step": "s2",
    "gold_failure_agent": "a5",
    "gold_irreversibility": True,
    "gold_propagation": True,
    "gold_recoverability": False,
    "label_rationale": "non-visible rationale: s2/a5 anchors the fault",
    "label_source": "journal_v1_main_controlled",
    "label_confidence": 0.9,
    "propagation_evidence": "dependent agent reused unresolved output from s2",
    "irreversibility_evidence": "mitigation after s2 was insufficient",
    "recovery_opportunity": "not_applicable_or_unavailable",
    "provenance_notes": "seed=10001",
    "synthetic_control_rule": "task10_main_controlled",
    "adjudication_decision": "auto_rule",
}


def test_prediction_view_removes_gold_labels_and_private_metadata():
    view = make_prediction_view(RAW_RECORD)
    forbidden = {
        "gold_failure_step",
        "gold_failure_agent",
        "gold_irreversibility",
        "gold_propagation",
        "gold_recoverability",
        "label_rationale",
        "label_source",
        "label_confidence",
        "synthetic_control_rule",
        "adjudication_decision",
        "provenance_notes",
    }
    assert forbidden.isdisjoint(view)
    assert forbidden.isdisjoint(view["observed_step_content"])
    assert_no_gold_leakage(view)


def test_prediction_view_removes_h6_evidence_and_target_equivalent_top_level_fields():
    view = make_prediction_view(RAW_RECORD)
    forbidden = {
        "propagation_evidence",
        "irreversibility_evidence",
        "recovery_opportunity",
        "step_id",
        "agent_id",
        "handoff_from",
        "handoff_to",
    }
    assert forbidden.isdisjoint(view)
    assert forbidden.isdisjoint(view["observed_step_content"])


def test_prediction_view_retains_minimal_trace_content_for_attribution():
    view = make_prediction_view(RAW_RECORD)
    assert view["trace_id"] == "JV1_example"
    assert view["candidate_steps"] == ["s1", "s2", "s3", "s4"]
    assert view["candidate_agents"] == ["a3", "a5", "a9"]
    assert view["observed_step_content"]["input_message"]
    assert view["observed_step_content"]["output_message"]
    assert view["observed_step_content"]["tool_output"]
    assert view["model_visible_evidence_items"] == ["ev1", "ev2"]


def test_private_label_view_contains_gold_fields_for_evaluation_only():
    private = make_private_label_view(RAW_RECORD)
    assert private["gold_failure_step"] == "s2"
    assert private["gold_failure_agent"] == "a5"
    assert private["step_id"] == "s2"
    assert private["agent_id"] == "a5"


def test_assert_no_gold_leakage_rejects_nested_forbidden_fields():
    with pytest.raises(ValueError, match="gold_failure_step"):
        assert_no_gold_leakage({"observed_step_content": {"gold_failure_step": "s2"}})
