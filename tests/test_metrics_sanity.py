"""Unit tests for trivial baselines and shortcut-risk interpretation."""

from cctdiag.baselines.trivial import (
    always_s2,
    first_active_agent,
    last_active_agent,
    majority_agent,
    majority_step,
    random_agent_seeded,
    random_step_seeded,
    same_as_parent_for_perturbations,
)
from cctdiag.metrics.attribution import agent_accuracy, step_accuracy, tuple_accuracy_step_agent
from cctdiag.metrics.sanity import interpret_shortcut_risk


RECORDS = [
    {
        "trace_id": "clean-1",
        "gold_failure_step": "s2",
        "gold_failure_agent": "a1",
        "gold_irreversibility": True,
        "gold_propagation": False,
        "gold_recoverability": True,
        "step_catalog": ["s1", "s2", "s3"],
        "agent_catalog": ["a1", "a2"],
    },
    {
        "trace_id": "clean-2",
        "gold_failure_step": "s3",
        "gold_failure_agent": "a2",
        "gold_irreversibility": False,
        "gold_propagation": True,
        "gold_recoverability": False,
        "step_catalog": ["s1", "s2", "s3"],
        "agent_catalog": ["a1", "a2"],
    },
    {
        "trace_id": "pert-2",
        "clean_parent_trace_id": "clean-2",
        "gold_failure_step": "s3",
        "gold_failure_agent": "a2",
        "gold_irreversibility": False,
        "gold_propagation": True,
        "gold_recoverability": False,
        "step_catalog": ["s1", "s2", "s3"],
        "agent_catalog": ["a1", "a2"],
    },
]


def test_allowed_trivial_baseline_predictions():
    assert step_accuracy(RECORDS, majority_step(RECORDS)) == 2 / 3
    assert agent_accuracy(RECORDS, majority_agent(RECORDS)) == 2 / 3
    assert step_accuracy(RECORDS, always_s2(RECORDS)) == 1 / 3
    assert len(random_step_seeded(RECORDS, seed=7)) == len(RECORDS)
    assert len(random_agent_seeded(RECORDS, seed=8)) == len(RECORDS)
    assert first_active_agent(RECORDS) == [
        {"predicted_failure_agent": "a1"},
        {"predicted_failure_agent": "a1"},
        {"predicted_failure_agent": "a1"},
    ]
    assert last_active_agent(RECORDS) == [
        {"predicted_failure_agent": "a2"},
        {"predicted_failure_agent": "a2"},
        {"predicted_failure_agent": "a2"},
    ]


def test_same_as_parent_for_perturbations_uses_predictions_not_gold_labels():
    assert same_as_parent_for_perturbations(RECORDS) == [{}, {}, {}]

    predictions = same_as_parent_for_perturbations(
        RECORDS,
        parent_predictions={
            "clean-2": {"predicted_failure_step": "s3", "predicted_failure_agent": "a2"}
        },
    )
    assert predictions[0] == {}
    assert predictions[1] == {}
    assert predictions[2]["predicted_failure_step"] == "s3"
    assert predictions[2]["predicted_failure_agent"] == "a2"
    assert step_accuracy(RECORDS, predictions) == 1.0
    assert agent_accuracy(RECORDS, predictions) == 1.0
    assert tuple_accuracy_step_agent(RECORDS, predictions) == 1.0


def test_shortcut_risk_interpretation_blocks_and_passes():
    blocked = interpret_shortcut_risk(
        {
            "majority_step": {"step_accuracy": 0.51, "agent_accuracy": None},
            "majority_agent": {"step_accuracy": None, "agent_accuracy": 0.51},
        }
    )
    assert blocked["status"] == "blocked"
    assert len(blocked["blockers"]) == 2

    passed = interpret_shortcut_risk(
        {
            "majority_step": {"step_accuracy": 0.25, "agent_accuracy": None},
            "majority_agent": {"step_accuracy": None, "agent_accuracy": 0.25},
        }
    )
    assert passed == {"status": "passed", "blockers": [], "review_flags": []}
