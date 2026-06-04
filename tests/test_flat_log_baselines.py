"""Tests for transparent flat-log diagnostic baselines."""

import pytest

from cctdiag.baselines.flat_log import flat_log_keyword_agent, flat_log_keyword_step, flat_log_role_agent
from cctdiag.io.views import make_prediction_view
from cctdiag.metrics.attribution import agent_accuracy, step_accuracy


RAW_RECORDS = [
    {
        "input_message": "phase=evidence-integration; event=evidence integration retained a contradiction",
        "output_message": "Integrated bundle preserved incompatible observations",
        "tool_call": "lookup_context",
        "tool_output": "evidence-merge retained conflict",
        "terminal_outcome": "failed_execution",
        "agent_id": "a2",
        "agent_role": "coordinator",
        "agent_catalog": ["a1", "a2", "a3"],
        "step_id": "s3",
        "step_catalog": ["s1", "s2", "s3", "s4"],
        "gold_failure_step": "s3",
        "gold_failure_agent": "a2",
    },
    {
        "input_message": "phase=final-adjudication; terminal decision ignored late correction",
        "output_message": "Final adjudication kept the degraded answer",
        "tool_call": "final_check",
        "tool_output": "terminal issue remained",
        "terminal_outcome": "degraded_execution",
        "agent_id": "a5",
        "agent_role": "reviewer",
        "agent_catalog": ["a4", "a5"],
        "step_id": "s5",
        "step_catalog": ["s1", "s2", "s3", "s4", "s5"],
        "gold_failure_step": "s5",
        "gold_failure_agent": "a5",
    },
]

VIEWS = [make_prediction_view(record) for record in RAW_RECORDS]


def test_flat_log_keyword_step_is_deterministic_on_prediction_views():
    predictions = flat_log_keyword_step(VIEWS)
    assert predictions == [{"predicted_failure_step": "s3"}, {"predicted_failure_step": "s5"}]
    assert step_accuracy(RAW_RECORDS, predictions) == 1.0


def test_flat_log_keyword_agent_uses_sanitized_candidates_not_raw_agent_id():
    predictions = flat_log_keyword_agent(VIEWS)
    assert predictions == [{"predicted_failure_agent": "a1"}, {"predicted_failure_agent": "a4"}]
    assert agent_accuracy(RAW_RECORDS, predictions) == 0.0


def test_flat_log_role_agent_uses_role_catalog_preference_on_prediction_views():
    predictions = flat_log_role_agent(VIEWS)
    assert predictions == [{"predicted_failure_agent": "a2"}, {"predicted_failure_agent": "a5"}]
    assert agent_accuracy(RAW_RECORDS, predictions) == 1.0


def test_flat_log_baselines_reject_raw_records_with_gold_fields():
    with pytest.raises(ValueError):
        flat_log_keyword_step(RAW_RECORDS)
