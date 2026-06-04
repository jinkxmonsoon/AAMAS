"""Tests for full ordered trace prediction views."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from cctdiag.io.full_trace_views import (
    assert_no_full_trace_private_leakage,
    make_full_trace_prediction_view,
    make_full_trace_private_label_view,
)

FIXTURE_DIR = Path(__file__).parent / "fixtures/full_trace"


def load_valid_fixture() -> dict:
    return json.loads((FIXTURE_DIR / "minimal_valid_full_trace.json").read_text(encoding="utf-8"))


def test_full_trace_prediction_view_preserves_ordered_visible_steps_and_candidates():
    record = load_valid_fixture()
    view = make_full_trace_prediction_view(record)
    assert view["trace_id"] == record["trace_id"]
    assert view["candidate_steps"] == ["s1", "s2", "s3", "s4"]
    assert view["candidate_agents"] == ["a1", "a2", "a3", "a4"]
    assert [step["step_id"] for step in view["steps"]] == ["s1", "s2", "s3", "s4"]
    assert view["steps"][1]["agent_id"] == "a2"
    assert view["steps"][1]["input_message"]
    assert view["steps"][1]["evidence_items"] == ["ev2", "ev3"]


def test_full_trace_prediction_view_excludes_private_labels_and_provenance():
    view = make_full_trace_prediction_view(load_valid_fixture())
    assert "private_labels" not in view
    assert "provenance" not in view
    assert "gold_failure_step" not in json.dumps(view)
    assert "label_rationale" not in json.dumps(view)
    assert "propagation_evidence" not in json.dumps(view)
    assert_no_full_trace_private_leakage(view)


def test_full_trace_prediction_view_excludes_top_level_failure_centered_fields():
    view = make_full_trace_prediction_view(load_valid_fixture())
    assert "step_id" not in view
    assert "agent_id" not in view
    assert all("step_id" in step for step in view["steps"])
    assert all("agent_id" in step for step in view["steps"])


def test_full_trace_private_label_view_keeps_private_data_for_evaluation_only():
    private_view = make_full_trace_private_label_view(load_valid_fixture())
    assert private_view["private_labels"]["gold_failure_step"] == "s2"
    assert private_view["private_labels"]["gold_failure_agent"] == "a2"
    assert private_view["provenance"]["synthetic_control_rule"] == "task13_full_trace_fixture"


def test_full_trace_leakage_assertion_rejects_nested_private_fields():
    with pytest.raises(ValueError, match="private_labels"):
        assert_no_full_trace_private_leakage({"steps": [{"private_labels": {"gold_failure_step": "s2"}}]})
