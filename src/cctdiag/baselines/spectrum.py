"""Spectrum-inspired non-CCT diagnostic baselines for Journal-v1.

These heuristics assign simple suspiciousness scores to log-visible components.
They do not build CCT graphs, calibrate scores, learn weights, call LLMs, or use
gold labels for prediction.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any

Record = Mapping[str, Any]
Prediction = dict[str, Any]

STEP_RANK = {"s1": 1, "s2": 2, "s3": 3, "s4": 4, "s5": 5}


def _step_score(step: Any, row: Record) -> tuple[int, int]:
    step_text = str(step)
    text = " ".join(
        str(row.get(field) or "")
        for field in ("input_message", "output_message", "tool_call", "tool_output", "terminal_outcome")
    ).lower()
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
    if step == row.get("step_id"):
        score += 2
    return score, STEP_RANK.get(step_text, 0)


def _agent_score(agent: Any, row: Record) -> tuple[int, str]:
    agent_text = str(agent)
    text = " ".join(
        str(row.get(field) or "")
        for field in ("input_message", "output_message", "tool_call", "tool_output", "handoff_from", "handoff_to")
    ).lower()
    score = 0
    if agent_text and agent_text.lower() in text:
        score += 3
    if agent == row.get("handoff_to"):
        score += 2
    if agent == row.get("agent_id"):
        score += 4
    if agent == row.get("handoff_from"):
        score += 1
    return score, agent_text


def spectrum_inspired_step(records: Sequence[Record]) -> list[Prediction]:
    """Predict the highest-suspiciousness step from flat component scores."""

    predictions = []
    for row in records:
        catalog = list(row.get("step_catalog") or [])
        if not catalog:
            predictions.append({"predicted_failure_step": None})
            continue
        predicted = max(catalog, key=lambda step: _step_score(step, row))
        predictions.append({"predicted_failure_step": predicted})
    return predictions


def spectrum_inspired_agent(records: Sequence[Record]) -> list[Prediction]:
    """Predict the highest-suspiciousness agent from flat component scores."""

    predictions = []
    for row in records:
        catalog = list(row.get("agent_catalog") or [])
        if not catalog:
            predictions.append({"predicted_failure_agent": None})
            continue
        predicted = max(catalog, key=lambda agent: _agent_score(agent, row))
        predictions.append({"predicted_failure_agent": predicted})
    return predictions
