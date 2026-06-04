"""Transparent flat-log diagnostic baselines for Journal-v1 prediction views.

The rules in this module intentionally inspect only sanitized prediction-view
fields. They are deterministic shortcut diagnostics, not CCT scoring,
calibration, learned models, refinement variants, or paper-ready baselines.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any

from cctdiag.io.views import assert_no_gold_leakage

Record = Mapping[str, Any]
Prediction = dict[str, Any]

TEXT_FIELDS = (
    "input_message",
    "output_message",
    "tool_call",
    "tool_output",
    "terminal_outcome",
    "agent_role",
)

STEP_KEYWORDS = (
    ("s5", ("final-adjudication", "final adjudication", "terminal", "completion", "completion-check")),
    ("s4", ("verification-transfer", "verification transfer", "verification", "transfer", "audit")),
    ("s3", ("evidence-integration", "evidence integration", "evidence", "integrated", "merge", "observations")),
    ("s2", ("handoff-intake", "handoff intake", "handoff", "intake", "constraint")),
)

ROLE_AGENT_PREFERENCE = {
    "analyst": 0,
    "planner": 0,
    "coordinator": 1,
    "executor": -1,
    "reviewer": -1,
}


def _observed_step(row: Record) -> Mapping[str, Any]:
    observed = row.get("observed_step_content")
    return observed if isinstance(observed, Mapping) else row


def _text(row: Record) -> str:
    assert_no_gold_leakage(row)
    observed = _observed_step(row)
    return " ".join(str(observed.get(field) or "") for field in TEXT_FIELDS).lower()


def _catalog(row: Record, field: str) -> list[Any]:
    if field == "step_catalog":
        return list(row.get("candidate_steps") or [])
    if field == "agent_catalog":
        return list(row.get("candidate_agents") or [])
    return list(row.get(field) or [])


def _fallback_step(row: Record) -> Any:
    catalog = _catalog(row, "step_catalog")
    return catalog[0] if catalog else None


def _fallback_agent(row: Record) -> Any:
    catalog = _catalog(row, "agent_catalog")
    return catalog[0] if catalog else None


def flat_log_keyword_step(records: Sequence[Record]) -> list[Prediction]:
    """Predict failure step from transparent flat text keyword matches."""

    predictions = []
    for row in records:
        text = _text(row)
        predicted = None
        for step, keywords in STEP_KEYWORDS:
            if any(keyword in text for keyword in keywords):
                predicted = step
                break
        predictions.append({"predicted_failure_step": predicted or _fallback_step(row)})
    return predictions


def flat_log_keyword_agent(records: Sequence[Record]) -> list[Prediction]:
    """Predict failure agent from sanitized candidate-agent metadata only."""

    predictions = []
    for row in records:
        assert_no_gold_leakage(row)
        predictions.append({"predicted_failure_agent": _fallback_agent(row)})
    return predictions


def flat_log_role_agent(records: Sequence[Record]) -> list[Prediction]:
    """Predict failure agent from active role plus candidate-agent position."""

    predictions = []
    for row in records:
        assert_no_gold_leakage(row)
        catalog = _catalog(row, "agent_catalog")
        role = str(_observed_step(row).get("agent_role") or "").lower()
        if not catalog:
            predictions.append({"predicted_failure_agent": None})
            continue
        index = ROLE_AGENT_PREFERENCE.get(role, 0)
        predictions.append({"predicted_failure_agent": catalog[index]})
    return predictions
