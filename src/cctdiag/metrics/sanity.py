"""Diagnostic trivial-baseline sanity metric helpers."""

from __future__ import annotations

from typing import Any, Mapping

STEP_BLOCKER_THRESHOLD = 0.50
AGENT_BLOCKER_THRESHOLD = 0.50
UNEXPECTED_AGENT_REVIEW_THRESHOLD = 0.50


def interpret_shortcut_risk(results: Mapping[str, Mapping[str, Any]]) -> dict[str, Any]:
    """Interpret trivial-baseline diagnostic results against blocker thresholds.

    The thresholds are sanity gates only. They are not CCT comparisons and do
    not establish paper-ready results.
    """

    blockers: list[str] = []
    review_flags: list[str] = []

    for baseline_name, metrics in results.items():
        step_acc = metrics.get("step_accuracy")
        agent_acc = metrics.get("agent_accuracy")
        if isinstance(step_acc, int | float) and step_acc > STEP_BLOCKER_THRESHOLD:
            blockers.append(
                f"{baseline_name}.step_accuracy={step_acc:.4f} exceeds {STEP_BLOCKER_THRESHOLD:.2f}"
            )
        if (
            baseline_name == "majority_agent"
            and isinstance(agent_acc, int | float)
            and agent_acc > AGENT_BLOCKER_THRESHOLD
        ):
            blockers.append(
                f"majority_agent.agent_accuracy={agent_acc:.4f} exceeds {AGENT_BLOCKER_THRESHOLD:.2f}"
            )
        if baseline_name in {
            "random_step_seeded",
            "random_agent_seeded",
            "first_active_agent",
            "last_active_agent",
        }:
            if isinstance(agent_acc, int | float) and agent_acc > UNEXPECTED_AGENT_REVIEW_THRESHOLD:
                review_flags.append(
                    f"{baseline_name}.agent_accuracy={agent_acc:.4f} exceeds review threshold {UNEXPECTED_AGENT_REVIEW_THRESHOLD:.2f}"
                )
            if isinstance(step_acc, int | float) and step_acc > STEP_BLOCKER_THRESHOLD:
                review_flags.append(
                    f"{baseline_name}.step_accuracy={step_acc:.4f} exceeds review threshold {STEP_BLOCKER_THRESHOLD:.2f}"
                )

    status = "blocked" if blockers else ("review" if review_flags else "passed")
    return {"status": status, "blockers": blockers, "review_flags": review_flags}
