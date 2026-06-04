"""Unit tests for diagnostic attribution metric interfaces."""

import pytest

from cctdiag.metrics.attribution import (
    agent_accuracy,
    irreversibility_accuracy,
    macro_accuracy_by_perturbation,
    macro_accuracy_by_scenario,
    propagation_accuracy,
    recoverability_accuracy,
    step_accuracy,
    tuple_accuracy_step_agent,
)


RECORDS = [
    {
        "gold_failure_step": "s2",
        "gold_failure_agent": "a1",
        "gold_irreversibility": True,
        "gold_propagation": False,
        "gold_recoverability": True,
        "scenario_group": "alpha",
        "perturbation_type": "none",
    },
    {
        "gold_failure_step": "s3",
        "gold_failure_agent": "a2",
        "gold_irreversibility": False,
        "gold_propagation": True,
        "gold_recoverability": False,
        "scenario_group": "alpha",
        "perturbation_type": "paraphrase",
    },
    {
        "gold_failure_step": "s3",
        "gold_failure_agent": "a3",
        "gold_irreversibility": True,
        "gold_propagation": True,
        "gold_recoverability": False,
        "scenario_group": "beta",
        "perturbation_type": "paraphrase",
    },
]


PREDICTIONS = [
    {
        "predicted_failure_step": "s2",
        "predicted_failure_agent": "a1",
        "predicted_irreversibility": True,
        "predicted_propagation": False,
        "predicted_recoverability": False,
    },
    {
        "predicted_failure_step": "s2",
        "predicted_failure_agent": "a2",
        "predicted_irreversibility": True,
        "predicted_propagation": True,
        "predicted_recoverability": False,
    },
    {
        "predicted_failure_step": "s3",
        "predicted_failure_agent": "a1",
        "predicted_irreversibility": True,
        "predicted_propagation": False,
        "predicted_recoverability": False,
    },
]


def test_core_attribution_accuracies():
    assert step_accuracy(RECORDS, PREDICTIONS) == pytest.approx(2 / 3)
    assert agent_accuracy(RECORDS, PREDICTIONS) == pytest.approx(2 / 3)
    assert tuple_accuracy_step_agent(RECORDS, PREDICTIONS) == pytest.approx(1 / 3)


def test_h6_accuracies_and_na_when_missing():
    assert irreversibility_accuracy(RECORDS, PREDICTIONS) == pytest.approx(2 / 3)
    assert propagation_accuracy(RECORDS, PREDICTIONS) == pytest.approx(2 / 3)
    assert recoverability_accuracy(RECORDS, PREDICTIONS) == pytest.approx(2 / 3)
    assert irreversibility_accuracy(RECORDS, [{}, {}, {}]) is None


def test_macro_accuracy_by_scenario_and_perturbation():
    by_scenario = macro_accuracy_by_scenario(RECORDS, PREDICTIONS)
    assert by_scenario["per_group"]["alpha"]["accuracy"] == pytest.approx(0.5)
    assert by_scenario["per_group"]["beta"]["accuracy"] == pytest.approx(1.0)
    assert by_scenario["macro_accuracy"] == pytest.approx(0.75)

    by_perturbation = macro_accuracy_by_perturbation(RECORDS, PREDICTIONS)
    assert by_perturbation["per_group"]["none"]["accuracy"] == pytest.approx(1.0)
    assert by_perturbation["per_group"]["paraphrase"]["accuracy"] == pytest.approx(0.5)
    assert by_perturbation["macro_accuracy"] == pytest.approx(0.75)


def test_length_mismatch_raises():
    with pytest.raises(ValueError):
        step_accuracy(RECORDS, PREDICTIONS[:1])
