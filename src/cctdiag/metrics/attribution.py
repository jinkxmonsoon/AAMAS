"""Attribution metric interfaces for diagnostic Journal-v1 evaluations.

These helpers compute simple accuracy-style interfaces only. They do not
implement CCT scoring, calibration, refinement variants, ablations, or result
-table generation.
"""

from __future__ import annotations

from collections import defaultdict
from collections.abc import Callable, Mapping, Sequence
from typing import Any

NA = None

Record = Mapping[str, Any]
Prediction = Mapping[str, Any]


def _as_list(items: Sequence[Mapping[str, Any]]) -> list[Mapping[str, Any]]:
    return list(items)


def _prediction_value(prediction: Prediction, names: tuple[str, ...]) -> Any:
    for name in names:
        if name in prediction:
            return prediction[name]
    return NA


def _accuracy(
    records: Sequence[Record],
    predictions: Sequence[Prediction],
    *,
    gold_field: str,
    prediction_fields: tuple[str, ...],
) -> float | None:
    rows = _as_list(records)
    preds = _as_list(predictions)
    if len(rows) != len(preds):
        raise ValueError(f"records/predictions length mismatch: {len(rows)} != {len(preds)}")

    computable = 0
    correct = 0
    for row, pred in zip(rows, preds, strict=True):
        predicted = _prediction_value(pred, prediction_fields)
        if predicted is NA:
            continue
        computable += 1
        if predicted == row.get(gold_field):
            correct += 1

    if computable == 0:
        return NA
    return correct / computable


def step_accuracy(records: Sequence[Record], predictions: Sequence[Prediction]) -> float | None:
    """Return accuracy for `gold_failure_step` against predicted step labels."""

    return _accuracy(
        records,
        predictions,
        gold_field="gold_failure_step",
        prediction_fields=("predicted_failure_step", "failure_step", "step"),
    )


def agent_accuracy(records: Sequence[Record], predictions: Sequence[Prediction]) -> float | None:
    """Return accuracy for `gold_failure_agent` against predicted agent labels."""

    return _accuracy(
        records,
        predictions,
        gold_field="gold_failure_agent",
        prediction_fields=("predicted_failure_agent", "failure_agent", "agent"),
    )


def tuple_accuracy_step_agent(records: Sequence[Record], predictions: Sequence[Prediction]) -> float | None:
    """Return joint accuracy requiring both failure step and failure agent to match."""

    rows = _as_list(records)
    preds = _as_list(predictions)
    if len(rows) != len(preds):
        raise ValueError(f"records/predictions length mismatch: {len(rows)} != {len(preds)}")

    computable = 0
    correct = 0
    for row, pred in zip(rows, preds, strict=True):
        predicted_step = _prediction_value(pred, ("predicted_failure_step", "failure_step", "step"))
        predicted_agent = _prediction_value(pred, ("predicted_failure_agent", "failure_agent", "agent"))
        if predicted_step is NA or predicted_agent is NA:
            continue
        computable += 1
        if predicted_step == row.get("gold_failure_step") and predicted_agent == row.get("gold_failure_agent"):
            correct += 1

    if computable == 0:
        return NA
    return correct / computable


def irreversibility_accuracy(records: Sequence[Record], predictions: Sequence[Prediction]) -> float | None:
    """Return H6 irreversibility-label accuracy, or NA when predictions are absent."""

    return _accuracy(
        records,
        predictions,
        gold_field="gold_irreversibility",
        prediction_fields=("predicted_irreversibility", "irreversibility"),
    )


def propagation_accuracy(records: Sequence[Record], predictions: Sequence[Prediction]) -> float | None:
    """Return H6 propagation-label accuracy, or NA when predictions are absent."""

    return _accuracy(
        records,
        predictions,
        gold_field="gold_propagation",
        prediction_fields=("predicted_propagation", "propagation"),
    )


def recoverability_accuracy(records: Sequence[Record], predictions: Sequence[Prediction]) -> float | None:
    """Return H6 recoverability-label accuracy, or NA when predictions are absent."""

    return _accuracy(
        records,
        predictions,
        gold_field="gold_recoverability",
        prediction_fields=("predicted_recoverability", "recoverability"),
    )


def macro_accuracy_by_field(
    records: Sequence[Record],
    predictions: Sequence[Prediction],
    *,
    group_field: str,
    metric: Callable[[Sequence[Record], Sequence[Prediction]], float | None] = step_accuracy,
) -> dict[str, Any]:
    """Return equal-weighted per-group accuracy summary for a metric."""

    rows = _as_list(records)
    preds = _as_list(predictions)
    if len(rows) != len(preds):
        raise ValueError(f"records/predictions length mismatch: {len(rows)} != {len(preds)}")

    grouped_rows: dict[str, list[Record]] = defaultdict(list)
    grouped_preds: dict[str, list[Prediction]] = defaultdict(list)
    for row, pred in zip(rows, preds, strict=True):
        group = str(row.get(group_field, "<missing>"))
        grouped_rows[group].append(row)
        grouped_preds[group].append(pred)

    per_group = {
        group: {"accuracy": metric(grouped_rows[group], grouped_preds[group]), "n": len(grouped_rows[group])}
        for group in sorted(grouped_rows)
    }
    values = [entry["accuracy"] for entry in per_group.values() if entry["accuracy"] is not NA]
    macro = (sum(values) / len(values)) if values else NA
    return {"macro_accuracy": macro, "per_group": per_group}


def macro_accuracy_by_scenario(
    records: Sequence[Record],
    predictions: Sequence[Prediction],
    metric: Callable[[Sequence[Record], Sequence[Prediction]], float | None] = step_accuracy,
) -> dict[str, Any]:
    """Return equal-weighted macro accuracy grouped by `scenario_group`."""

    return macro_accuracy_by_field(records, predictions, group_field="scenario_group", metric=metric)


def macro_accuracy_by_perturbation(
    records: Sequence[Record],
    predictions: Sequence[Prediction],
    metric: Callable[[Sequence[Record], Sequence[Prediction]], float | None] = step_accuracy,
) -> dict[str, Any]:
    """Return equal-weighted macro accuracy grouped by `perturbation_type`."""

    return macro_accuracy_by_field(records, predictions, group_field="perturbation_type", metric=metric)
