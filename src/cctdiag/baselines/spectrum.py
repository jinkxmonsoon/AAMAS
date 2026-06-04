"""Spectrum-inspired non-CCT diagnostics for sanitized prediction views.

These heuristics assign simple suspiciousness scores to prediction-view-visible
components. They do not build CCT graphs, calibrate scores, learn weights, call
LLMs, or use gold labels for prediction.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any

from cctdiag.io.views import assert_no_gold_leakage

Record = Mapping[str, Any]
Prediction = dict[str, Any]

STEP_RANK = {"s1": 1, "s2": 2, "s3": 3, "s4": 4, "s5": 5}


def _observed_step(row: Record) -> Mapping[str, Any]:
    observed = row.get("observed_step_content")
    return observed if isinstance(observed, Mapping) else row


def _text(row: Record) -> str:
    observed = _observed_step(row)
    return " ".join(
        str(observed.get(field) or "")
        for field in ("input_message", "output_message", "tool_call", "tool_output", "terminal_outcome")
    ).lower()


def _step_score(step: Any, row: Record) -> tuple[int, int]:
    step_text = str(step)
    text = _text(row)
    score = 0
    if step_text and step_text in text:
        score += 4
    phase_patterns = {
        "s2": ("handoff", "intake", "constraint"),
        "s3": ("evidence", "integration", "merge", "observation"),
        "s4": ("verification", "transfer", "audit"),
        "s5": ("final", "adjudication", "terminal", "completion"),
    }
    score += sum(1 for token in phase_patterns.get(step_text, ()) if token in text)
    return score, STEP_RANK.get(step_text, 0)


def _agent_score(agent: Any, row: Record) -> tuple[int, str]:
    agent_text = str(agent)
    observed = _observed_step(row)
    text = " ".join(str(observed.get(field) or "") for field in ("input_message", "output_message", "tool_call", "tool_output")).lower()
    score = 0
    if agent_text and agent_text.lower() in text:
        score += 1
    return score, agent_text


def spectrum_inspired_step(records: Sequence[Record]) -> list[Prediction]:
    """Predict the highest-suspiciousness step from sanitized flat component scores."""

    predictions = []
    for row in records:
        assert_no_gold_leakage(row)
        catalog = list(row.get("candidate_steps") or [])
        if not catalog:
            predictions.append({"predicted_failure_step": None})
            continue
        predicted = max(catalog, key=lambda step: _step_score(step, row))
        predictions.append({"predicted_failure_step": predicted})
    return predictions


def spectrum_inspired_agent(records: Sequence[Record]) -> list[Prediction]:
    """Predict the highest-suspiciousness agent from sanitized flat component scores."""

    predictions = []
    for row in records:
        assert_no_gold_leakage(row)
        catalog = list(row.get("candidate_agents") or [])
        if not catalog:
            predictions.append({"predicted_failure_agent": None})
            continue
        predicted = max(catalog, key=lambda agent: _agent_score(agent, row))
        predictions.append({"predicted_failure_agent": predicted})
    return predictions
