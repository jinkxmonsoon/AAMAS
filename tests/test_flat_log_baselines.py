"""Tests for transparent flat-log diagnostic baselines."""

from cctdiag.baselines.flat_log import flat_log_keyword_agent, flat_log_keyword_step, flat_log_role_agent
from cctdiag.metrics.attribution import agent_accuracy, step_accuracy


RECORDS = [
    {
        "input_message": "phase=evidence-integration; event=evidence integration retained a contradiction",
        "output_message": "Integrated bundle preserved incompatible observations",
        "tool_call": "lookup_context",
        "tool_output": "evidence-merge retained conflict",
        "terminal_outcome": "failed_execution",
        "agent_id": "a2",
        "agent_role": "coordinator",
        "agent_catalog": ["a1", "a2", "a3"],
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
        "step_catalog": ["s1", "s2", "s3", "s4", "s5"],
        "gold_failure_step": "s5",
        "gold_failure_agent": "a5",
    },
]


def test_flat_log_keyword_step_is_deterministic_and_text_only():
    predictions = flat_log_keyword_step(RECORDS)
    assert predictions == [{"predicted_failure_step": "s3"}, {"predicted_failure_step": "s5"}]
    assert step_accuracy(RECORDS, predictions) == 1.0


def test_flat_log_keyword_agent_uses_active_log_metadata_not_gold_labels():
    predictions = flat_log_keyword_agent(RECORDS)
    assert predictions == [{"predicted_failure_agent": "a2"}, {"predicted_failure_agent": "a5"}]
    assert agent_accuracy(RECORDS, predictions) == 1.0


def test_flat_log_role_agent_uses_role_catalog_preference():
    predictions = flat_log_role_agent(RECORDS)
    assert predictions == [{"predicted_failure_agent": "a2"}, {"predicted_failure_agent": "a5"}]
    assert agent_accuracy(RECORDS, predictions) == 1.0
