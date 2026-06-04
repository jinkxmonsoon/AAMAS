"""Tests for spectrum-inspired non-CCT diagnostic baselines."""

import pytest

from cctdiag.baselines.spectrum import spectrum_inspired_agent, spectrum_inspired_step
from cctdiag.io.views import make_prediction_view
from cctdiag.metrics.attribution import agent_accuracy, step_accuracy


RAW_RECORDS = [
    {
        "input_message": "handoff packet omitted critical constraints",
        "output_message": "Intake summary moved forward with unresolved constraint gap",
        "tool_call": "query_incident_log",
        "tool_output": "handoff-audit: constraint mismatch remained open",
        "terminal_outcome": "degraded_execution",
        "handoff_from": "a1",
        "handoff_to": "a2",
        "agent_id": "a2",
        "agent_role": "analyst",
        "step_id": "s2",
        "agent_catalog": ["a1", "a2", "a3"],
        "step_catalog": ["s1", "s2", "s3", "s4"],
        "gold_failure_step": "s2",
        "gold_failure_agent": "a2",
    },
    {
        "input_message": "verification transfer let an audit issue pass",
        "output_message": "Transfer preserved unverified claim",
        "tool_call": "verify_claim",
        "tool_output": "audit warning remained unresolved",
        "terminal_outcome": "failed_execution",
        "handoff_from": "a3",
        "handoff_to": "a4",
        "agent_id": "a4",
        "agent_role": "coordinator",
        "step_id": "s4",
        "agent_catalog": ["a3", "a4", "a5"],
        "step_catalog": ["s1", "s2", "s3", "s4", "s5"],
        "gold_failure_step": "s4",
        "gold_failure_agent": "a4",
    },
]

VIEWS = [make_prediction_view(record) for record in RAW_RECORDS]


def test_spectrum_inspired_step_scores_prediction_view_components():
    predictions = spectrum_inspired_step(VIEWS)
    assert predictions == [{"predicted_failure_step": "s2"}, {"predicted_failure_step": "s4"}]
    assert step_accuracy(RAW_RECORDS, predictions) == 1.0


def test_spectrum_inspired_agent_cannot_use_removed_raw_agent_or_handoff_fields():
    predictions = spectrum_inspired_agent(VIEWS)
    assert predictions == [{"predicted_failure_agent": "a3"}, {"predicted_failure_agent": "a5"}]
    assert agent_accuracy(RAW_RECORDS, predictions) == 0.0


def test_spectrum_baselines_reject_raw_records_with_gold_fields():
    with pytest.raises(ValueError):
        spectrum_inspired_step(RAW_RECORDS)
