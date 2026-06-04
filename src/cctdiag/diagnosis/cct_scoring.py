"""Frozen uncalibrated CCT diagnostic scoring.

This module implements the Task 17 fixed weighted-sum protocol only. It does
not learn weights, calibrate scores, run grid search, run LOSO, refine outputs,
run ablations, perform statistical tests, or produce paper-ready result tables.
Gold/private labels must not be passed to these scoring functions.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any

PRIVATE_OR_GOLD_FIELDS = {
    "private_labels",
    "gold_failure_step",
    "gold_failure_agent",
    "gold_irreversibility",
    "gold_propagation",
    "gold_recoverability",
    "label_rationale",
    "label_confidence",
    "label_source",
    "propagation_evidence",
    "irreversibility_evidence",
    "recovery_opportunity",
    "provenance",
    "annotator_or_generator",
    "provenance_notes",
    "synthetic_control_rule",
    "scenario_group",
    "perturbation_type",
    "case_id",
}


def assert_no_scoring_private_fields(row: Mapping[str, Any]) -> None:
    """Reject feature rows that expose private/gold or audit-only fields."""

    leaked = sorted(PRIVATE_OR_GOLD_FIELDS & set(row))
    if leaked:
        raise ValueError("CCT scoring row exposes forbidden fields: " + ", ".join(leaked))


def score_feature_row(row: Mapping[str, Any], weights: Mapping[str, float]) -> float:
    """Score a single visible feature row with fixed weights."""

    assert_no_scoring_private_fields(row)
    total = 0.0
    for feature, weight in weights.items():
        value = row.get(feature, 0)
        if isinstance(value, bool):
            numeric = 1.0 if value else 0.0
        elif isinstance(value, int | float):
            numeric = float(value)
        elif value is None:
            numeric = 0.0
        else:
            raise TypeError(f"feature {feature} must be numeric/bool for scoring")
        total += float(weight) * numeric
    return total


def score_variant_rows(rows: Sequence[Mapping[str, Any]], variant: Mapping[str, Any]) -> list[dict[str, Any]]:
    """Return diagnostic candidate scores for a frozen config variant."""

    weights = variant.get("features", {})
    if not isinstance(weights, Mapping) or not weights:
        raise ValueError("variant must define fixed feature weights")

    scored = []
    for row in rows:
        scored.append(
            {
                "trace_id": row["trace_id"],
                "step_id": row["step_id"],
                "agent_id": row["agent_id"],
                "score": score_feature_row(row, weights),
            }
        )
    return scored
