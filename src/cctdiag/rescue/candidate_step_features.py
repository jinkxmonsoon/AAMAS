"""Candidate-step CCT rescue feature readiness extraction.

This module implements a non-scoring dry-run feature matrix for the Task 28
rescue protocol. It derives candidate-step rows from prediction-view-safe full
trace records only. It does not score, rank, calibrate, compare to gold labels,
or use private/provenance fields.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from collections.abc import Mapping, Sequence
from typing import Any

from cctdiag.cct.causal_edges import extract_causal_edges_from_prediction_view

RESCUE_FEATURE_VERSION = "rescue_candidate_step_features_v1"
STRONG_EDGE_TYPES = {
    "downstream_dependency_edge",
    "tool_alignment_edge",
    "cross_agent_dependency_edge",
}
IDENTIFIER_FIELDS = {"trace_id", "candidate_step_id", "feature_version"}
FORBIDDEN_FEATURE_FIELDS = {
    "private_labels",
    "gold_failure_step",
    "gold_failure_agent",
    "gold_irreversibility",
    "gold_propagation",
    "gold_recoverability",
    "label_rationale",
    "propagation_evidence",
    "irreversibility_evidence",
    "recovery_opportunity",
    "provenance",
    "scenario_group",
    "perturbation_type",
    "case_id",
    "case_variant",
    "correctness",
    "score",
    "rank",
}
FEATURE_NAMES = [
    "incoming_strong_edge_count",
    "outgoing_strong_edge_count",
    "downstream_dependency_incoming_count",
    "downstream_dependency_outgoing_count",
    "tool_alignment_incoming_count",
    "tool_alignment_outgoing_count",
    "cross_agent_dependency_incoming_count",
    "cross_agent_dependency_outgoing_count",
    "non_adjacent_dependency_involvement_count",
    "relation_type_diversity_count",
    "visible_tool_output_alignment_indicator",
    "visible_dependency_carryover_indicator",
    "causal_flow_total_degree",
    "has_visible_tool_call",
    "has_visible_tool_output",
    "has_visible_handoff_from",
    "has_visible_handoff_to",
    "has_visible_step_notes",
]


def assert_rescue_prediction_view_safe(prediction_view: Mapping[str, Any]) -> None:
    """Reject raw records or prediction views carrying forbidden fields."""

    leaked: list[str] = []

    def visit(value: Any, path: str = "") -> None:
        if isinstance(value, Mapping):
            for key, nested in value.items():
                key_text = str(key)
                nested_path = f"{path}.{key_text}" if path else key_text
                if key_text in FORBIDDEN_FEATURE_FIELDS:
                    leaked.append(nested_path)
                visit(nested, nested_path)
        elif isinstance(value, list | tuple):
            for index, item in enumerate(value):
                visit(item, f"{path}[{index}]")

    visit(prediction_view)
    if leaked:
        raise ValueError("rescue candidate-step feature input is not prediction-view safe: " + ", ".join(sorted(leaked)))
    if "steps" not in prediction_view or "trace_id" not in prediction_view:
        raise ValueError("rescue candidate-step feature extraction requires a full-trace prediction view")


def extract_candidate_step_feature_rows(prediction_view: Mapping[str, Any]) -> list[dict[str, Any]]:
    """Return one non-scoring feature row per candidate step."""

    assert_rescue_prediction_view_safe(prediction_view)
    trace_id = str(prediction_view["trace_id"])
    steps = list(prediction_view["steps"])
    edges = extract_causal_edges_from_prediction_view(prediction_view, STRONG_EDGE_TYPES)

    per_step: dict[str, Counter[str]] = {str(step["step_id"]): Counter() for step in steps}
    relation_types: dict[str, set[str]] = {str(step["step_id"]): set() for step in steps}

    for edge in edges:
        edge_type = str(edge["edge_type"])
        source_step_id = str(edge.get("source_step_id"))
        target_step_id = str(edge.get("target_step_id"))
        source_counter = per_step[source_step_id]
        target_counter = per_step[target_step_id]
        source_counter["outgoing_strong_edge_count"] += 1
        target_counter["incoming_strong_edge_count"] += 1
        prefix = _edge_feature_prefix(edge_type)
        source_counter[f"{prefix}_outgoing_count"] += 1
        target_counter[f"{prefix}_incoming_count"] += 1
        relation_types[source_step_id].add(edge_type)
        relation_types[target_step_id].add(edge_type)

        if source_step_id != target_step_id:
            try:
                distance = abs(_step_number(target_step_id) - _step_number(source_step_id))
            except ValueError:
                distance = 0
            if distance > 1:
                source_counter["non_adjacent_dependency_involvement_count"] += 1
                target_counter["non_adjacent_dependency_involvement_count"] += 1

        if edge_type == "tool_alignment_edge":
            source_counter["visible_tool_output_alignment_indicator"] = 1
            target_counter["visible_tool_output_alignment_indicator"] = 1
        if edge_type == "downstream_dependency_edge":
            source_counter["visible_dependency_carryover_indicator"] = 1
            target_counter["visible_dependency_carryover_indicator"] = 1

    rows: list[dict[str, Any]] = []
    for step in steps:
        step_id = str(step["step_id"])
        counter = per_step[step_id]
        row: dict[str, Any] = {
            "trace_id": trace_id,
            "candidate_step_id": step_id,
            "feature_version": RESCUE_FEATURE_VERSION,
        }
        for feature_name in FEATURE_NAMES:
            row[feature_name] = int(counter.get(feature_name, 0))
        row["causal_flow_total_degree"] = int(
            row["incoming_strong_edge_count"] + row["outgoing_strong_edge_count"]
        )
        row["relation_type_diversity_count"] = len(relation_types[step_id])
        row["has_visible_tool_call"] = _presence(step.get("tool_call"))
        row["has_visible_tool_output"] = _presence(step.get("tool_output"))
        row["has_visible_handoff_from"] = _presence(step.get("handoff_from"))
        row["has_visible_handoff_to"] = _presence(step.get("handoff_to"))
        row["has_visible_step_notes"] = _presence(step.get("visible_step_notes"))
        rows.append(row)

    findings = audit_candidate_step_rows_for_private_leakage(rows)
    if findings:
        raise ValueError("rescue candidate-step feature leakage findings: " + ", ".join(findings))
    return rows


def audit_candidate_step_rows_for_private_leakage(rows: Sequence[Mapping[str, Any]]) -> list[str]:
    """Return forbidden-field findings for candidate-step feature rows."""

    findings: list[str] = []
    for row_index, row in enumerate(rows):
        for key in row:
            if key in FORBIDDEN_FEATURE_FIELDS:
                findings.append(f"row[{row_index}].{key}")
    return findings


def feature_vector(row: Mapping[str, Any]) -> tuple[Any, ...]:
    """Return the non-identifier feature vector for duplicate analysis."""

    return tuple(row[name] for name in FEATURE_NAMES)


def summarize_feature_rows(rows: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    """Summarize non-scoring readiness properties of feature rows."""

    total_rows = len(rows)
    feature_names = list(FEATURE_NAMES)
    missing_null_counts = {
        name: sum(1 for row in rows if name not in row or row.get(name) is None) for name in feature_names
    }
    unique_values = {name: len({row.get(name) for row in rows}) for name in feature_names}
    constant_features = [name for name, count in unique_values.items() if count <= 1]
    vectors = [feature_vector(row) for row in rows]
    unique_vector_count = len(set(vectors))
    duplicate_vector_count = total_rows - unique_vector_count
    duplicate_vector_percentage = duplicate_vector_count / total_rows if total_rows else 0.0

    rows_by_trace: dict[str, list[Mapping[str, Any]]] = defaultdict(list)
    for row in rows:
        rows_by_trace[str(row["trace_id"])].append(row)
    within_trace_duplicate_rows = 0
    traces_with_within_trace_duplicates = 0
    for trace_rows in rows_by_trace.values():
        trace_vectors = [feature_vector(row) for row in trace_rows]
        duplicate_rows = len(trace_vectors) - len(set(trace_vectors))
        within_trace_duplicate_rows += duplicate_rows
        if duplicate_rows:
            traces_with_within_trace_duplicates += 1

    values_by_step: dict[str, Counter[tuple[Any, ...]]] = defaultdict(Counter)
    for row in rows:
        values_by_step[str(row["candidate_step_id"])][feature_vector(row)] += 1
    deterministic_by_step = {
        step_id: len(counter) == 1 for step_id, counter in sorted(values_by_step.items())
    }

    return {
        "total_rows": total_rows,
        "feature_names": feature_names,
        "missing_null_counts": missing_null_counts,
        "unique_values_per_feature": unique_values,
        "constant_features": constant_features,
        "unique_feature_vector_count": unique_vector_count,
        "duplicate_feature_vector_count": duplicate_vector_count,
        "duplicate_feature_vector_percentage": duplicate_vector_percentage,
        "duplicate_threshold_exceeded": duplicate_vector_percentage > 0.50,
        "within_trace_duplicate_candidate_step_rows": within_trace_duplicate_rows,
        "traces_with_within_trace_duplicates": traces_with_within_trace_duplicates,
        "feature_families_over_95_percent_constant": _features_over_threshold(rows, 0.95),
        "deterministic_vector_by_step_id": deterministic_by_step,
        "all_step_ids_single_vector": all(deterministic_by_step.values()) if deterministic_by_step else False,
    }


def position_identity_risk_summary(rows: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    """Summarize position/identity shortcut risk without using agent identities."""

    distribution_by_step: dict[str, dict[str, Counter[Any]]] = defaultdict(lambda: defaultdict(Counter))
    for row in rows:
        step_id = str(row["candidate_step_id"])
        for name in FEATURE_NAMES:
            distribution_by_step[step_id][name][row[name]] += 1

    step_unique_vectors = {
        step_id: len({feature_vector(row) for row in rows if str(row["candidate_step_id"]) == step_id})
        for step_id in sorted({str(row["candidate_step_id"]) for row in rows})
    }
    feature_means_by_step = {
        step_id: {
            name: round(sum(counter_value * count for counter_value, count in counts.items()) / sum(counts.values()), 4)
            for name, counts in feature_counts.items()
        }
        for step_id, feature_counts in sorted(distribution_by_step.items())
    }
    return {
        "features_include_step_position_column": False,
        "features_include_agent_identity_column": False,
        "features_usable_without_position_or_agent_fields": True,
        "step_ids_present_as_row_identifiers_only": sorted(step_unique_vectors),
        "unique_vectors_by_candidate_step_id": step_unique_vectors,
        "feature_means_by_candidate_step_id": feature_means_by_step,
        "position_shortcut_risk": "review" if len(set(step_unique_vectors.values())) > 1 else "low",
        "agent_identity_shortcut_risk": "low",
    }


def _features_over_threshold(rows: Sequence[Mapping[str, Any]], threshold: float) -> list[str]:
    flagged: list[str] = []
    for name in FEATURE_NAMES:
        counts = Counter(row.get(name) for row in rows)
        if not counts:
            continue
        most_common_count = counts.most_common(1)[0][1]
        if most_common_count / len(rows) > threshold:
            flagged.append(name)
    return flagged


def _presence(value: Any) -> int:
    if value is None:
        return 0
    if isinstance(value, str):
        stripped = value.strip().lower()
        return int(bool(stripped) and stripped not in {"none", "n/a", "null"})
    return int(bool(value))


def _step_number(step_id: str) -> int:
    if len(step_id) >= 2 and step_id[0].lower() == "s" and step_id[1:].isdigit():
        return int(step_id[1:])
    raise ValueError(f"unsupported step id for adjacency audit: {step_id}")


def _edge_feature_prefix(edge_type: str) -> str:
    return {
        "downstream_dependency_edge": "downstream_dependency",
        "tool_alignment_edge": "tool_alignment",
        "cross_agent_dependency_edge": "cross_agent_dependency",
    }[edge_type]
