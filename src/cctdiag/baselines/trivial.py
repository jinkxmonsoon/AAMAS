"""Allowed trivial baselines for Journal-v1 diagnostic sanity checks.

These functions intentionally implement only shortcut-risk diagnostics. They do
not implement CCT scoring, calibration, refinement variants, ablations, or
paper-ready result tables.
"""

from __future__ import annotations

from collections import Counter
from collections.abc import Sequence
from random import Random
from typing import Any, Mapping

Record = Mapping[str, Any]
Prediction = dict[str, Any]


def _most_common(rows: Sequence[Record], field: str) -> Any:
    counts = Counter(row.get(field) for row in rows)
    if not counts:
        return None
    return sorted(counts.items(), key=lambda item: (-item[1], str(item[0])))[0][0]


def majority_step(records: Sequence[Record]) -> list[Prediction]:
    label = _most_common(records, "gold_failure_step")
    return [{"predicted_failure_step": label} for _ in records]


def majority_agent(records: Sequence[Record]) -> list[Prediction]:
    label = _most_common(records, "gold_failure_agent")
    return [{"predicted_failure_agent": label} for _ in records]


def always_s2(records: Sequence[Record]) -> list[Prediction]:
    return [{"predicted_failure_step": "s2"} for _ in records]


def random_step_seeded(records: Sequence[Record], *, seed: int = 11011) -> list[Prediction]:
    rng = Random(seed)
    global_steps = sorted(
        {row.get("gold_failure_step") for row in records if row.get("gold_failure_step") is not None}
    )
    predictions = []
    for row in records:
        catalog = list(row.get("step_catalog") or global_steps)
        predictions.append({"predicted_failure_step": rng.choice(catalog) if catalog else None})
    return predictions


def random_agent_seeded(records: Sequence[Record], *, seed: int = 11012) -> list[Prediction]:
    rng = Random(seed)
    global_agents = sorted(
        {row.get("gold_failure_agent") for row in records if row.get("gold_failure_agent") is not None}
    )
    predictions = []
    for row in records:
        catalog = list(row.get("agent_catalog") or global_agents)
        predictions.append({"predicted_failure_agent": rng.choice(catalog) if catalog else None})
    return predictions


def first_active_agent(records: Sequence[Record]) -> list[Prediction]:
    predictions = []
    for row in records:
        catalog = list(row.get("agent_catalog") or [])
        predictions.append({"predicted_failure_agent": catalog[0] if catalog else None})
    return predictions


def last_active_agent(records: Sequence[Record]) -> list[Prediction]:
    predictions = []
    for row in records:
        catalog = list(row.get("agent_catalog") or [])
        predictions.append({"predicted_failure_agent": catalog[-1] if catalog else None})
    return predictions


def same_as_parent_for_perturbations(
    records: Sequence[Record], parent_predictions: Mapping[str, Prediction] | None = None
) -> list[Prediction]:
    """Propagate available clean-parent predictions to perturbed rows.

    This diagnostic never reads parent gold labels. When no external parent
    predictions are supplied, all rows receive NA predictions, which keeps the
    standalone sanity script from introducing gold-label leakage.
    """

    parent_predictions = parent_predictions or {}
    predictions = []
    for row in records:
        parent_id = row.get("clean_parent_trace_id")
        parent_prediction = parent_predictions.get(parent_id)
        predictions.append(dict(parent_prediction) if parent_prediction is not None else {})
    return predictions


TRIVIAL_BASELINES = {
    "majority_step": majority_step,
    "majority_agent": majority_agent,
    "always_s2": always_s2,
    "random_step_seeded": random_step_seeded,
    "random_agent_seeded": random_agent_seeded,
    "first_active_agent": first_active_agent,
    "last_active_agent": last_active_agent,
    "same_as_parent_for_perturbations": same_as_parent_for_perturbations,
}
