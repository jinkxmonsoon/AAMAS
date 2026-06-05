"""Sample-only deterministic CCT causal-flow edge prototype.

Task 20A scope: prototype selected non-position causal-flow edges on compact
prediction-view samples only. This module does not score, rank, calibrate,
compare to gold labels, or process full-corpus artifacts.
"""

from __future__ import annotations

import re
from collections.abc import Mapping, Sequence
from typing import Any

EXTRACTION_VERSION = "cct_causal_edge_sample_v0"
IMPLEMENTED_EDGE_TYPES = {
    "constraint_shift_edge",
    "downstream_dependency_edge",
    "tool_alignment_edge",
    "cross_agent_dependency_edge",
    "semantic_collision_edge",
}
FORBIDDEN_OUTPUT_FIELDS = {
    "private_labels",
    "provenance",
    "gold_failure_step",
    "gold_failure_agent",
    "gold_irreversibility",
    "gold_propagation",
    "gold_recoverability",
    "label_rationale",
    "propagation_evidence",
    "irreversibility_evidence",
    "recovery_opportunity",
    "scenario_group",
    "perturbation_type",
    "correctness",
    "correct",
    "incorrect",
    "score",
    "rank",
}
FORBIDDEN_NOTE_TERMS = {"gold", "label", "correct", "incorrect", "score", "rank"}
VISIBLE_STEP_TEXT_FIELDS = ("input_message", "output_message", "tool_output", "visible_step_notes")

_STOPWORDS = {
    "a", "an", "and", "are", "as", "at", "be", "but", "by", "for", "from", "in", "into", "is",
    "it", "of", "on", "or", "rather", "the", "this", "to", "with", "while", "where", "that", "one",
    "step", "case", "variant", "perform", "review", "candidate", "neutral", "visible", "notes", "note",
    "context", "detail", "details", "relevant", "downstream", "upstream", "message", "output", "tool",
}
_HARD_TERMS = {"required", "mandatory", "must", "condition", "constraint", "cap", "authorized", "stronger"}
_SOFT_TERMS = {"optional", "preference", "background", "broad", "weak", "weaker", "softened"}
_DEPENDENCY_MARKERS = {"received", "forwarded", "follows", "based", "using", "through", "aligns", "selected", "delivers", "references", "depends"}
_SEMANTIC_MARKERS = {"alternate", "alternative", "interpretation", "reading", "broad", "narrower", "rather", "instead", "selected"}
_TOKEN_RE = re.compile(r"[a-z0-9_]+")


def assert_prediction_view_safe(prediction_view: Mapping[str, Any]) -> None:
    """Reject non-prediction-view or private/scoring-bearing input."""

    leaked: list[str] = []

    def visit(value: Any, path: str = "") -> None:
        if isinstance(value, Mapping):
            for key, nested in value.items():
                key_text = str(key)
                nested_path = f"{path}.{key_text}" if path else key_text
                if key_text in FORBIDDEN_OUTPUT_FIELDS:
                    leaked.append(nested_path)
                visit(nested, nested_path)
        elif isinstance(value, list | tuple):
            for index, item in enumerate(value):
                visit(item, f"{path}[{index}]")

    visit(prediction_view)
    if leaked:
        raise ValueError("causal edge extraction input is not prediction-view safe: " + ", ".join(sorted(leaked)))
    if "steps" not in prediction_view or "trace_id" not in prediction_view:
        raise ValueError("causal edge extraction requires a full-trace prediction view")


def audit_edges_for_private_leakage(edges: Sequence[Mapping[str, Any]]) -> list[str]:
    """Return leakage findings for edge artifacts."""

    findings: list[str] = []
    for edge_index, edge in enumerate(edges):
        for key in edge:
            if key in FORBIDDEN_OUTPUT_FIELDS:
                findings.append(f"edge[{edge_index}].{key}")
        notes = str(edge.get("extraction_notes", "")).lower()
        for term in FORBIDDEN_NOTE_TERMS:
            if term in notes:
                findings.append(f"edge[{edge_index}].extraction_notes:{term}")
    return findings


def extract_causal_edges_from_prediction_view(prediction_view: Mapping[str, Any]) -> list[dict[str, Any]]:
    """Extract sample-only deterministic causal-flow edges from one prediction view."""

    assert_prediction_view_safe(prediction_view)
    trace_id = str(prediction_view["trace_id"])
    steps = list(prediction_view["steps"])
    edges: list[dict[str, Any]] = []

    _add_constraint_shift_edges(trace_id, steps, edges)
    _add_downstream_dependency_edges(trace_id, steps, edges)
    _add_tool_alignment_edges(trace_id, steps, edges)
    _add_cross_agent_dependency_edges(trace_id, steps, edges)
    _add_semantic_collision_edges(trace_id, steps, edges)

    for index, edge in enumerate(edges, start=1):
        edge["edge_id"] = f"{trace_id}:edge:{index:03d}"
    findings = audit_edges_for_private_leakage(edges)
    if findings:
        raise ValueError("causal edge output leakage findings: " + ", ".join(findings))
    return edges


def _add_edge(
    edges: list[dict[str, Any]],
    *,
    trace_id: str,
    edge_type: str,
    source_step: Mapping[str, Any],
    target_step: Mapping[str, Any],
    source_node_id: str,
    target_node_id: str,
    visible_fields_used: list[str],
    extraction_rule_id: str,
    extraction_notes: str,
) -> None:
    edges.append(
        {
            "trace_id": trace_id,
            "edge_id": "pending",
            "edge_type": edge_type,
            "source_node_id": source_node_id,
            "target_node_id": target_node_id,
            "source_step_id": source_step.get("step_id"),
            "target_step_id": target_step.get("step_id"),
            "visible_fields_used": visible_fields_used,
            "extraction_rule_id": extraction_rule_id,
            "extraction_notes": extraction_notes,
            "extraction_version": EXTRACTION_VERSION,
        }
    )


def _text(step: Mapping[str, Any], fields: Sequence[str] = VISIBLE_STEP_TEXT_FIELDS) -> str:
    return " ".join(str(step.get(field) or "") for field in fields).lower()


def _tokens(text: str) -> set[str]:
    return {tok for tok in _TOKEN_RE.findall(text.lower()) if len(tok) >= 4 and tok not in _STOPWORDS}


def _content_overlap(a: Mapping[str, Any], b: Mapping[str, Any]) -> set[str]:
    return _tokens(_text(a)) & _tokens(_text(b))


def _pairs(steps: Sequence[Mapping[str, Any]]):
    for source_index, source in enumerate(steps):
        for target in steps[source_index + 1 :]:
            yield source, target


def _add_constraint_shift_edges(trace_id: str, steps: Sequence[Mapping[str, Any]], edges: list[dict[str, Any]]) -> None:
    added = 0
    for source, target in _pairs(steps):
        source_text = _text(source)
        target_text = _text(target)
        shared = _content_overlap(source, target)
        if (_HARD_TERMS & _tokens(source_text)) and (_SOFT_TERMS & _tokens(target_text)) and shared:
            _add_edge(
                edges,
                trace_id=trace_id,
                edge_type="constraint_shift_edge",
                source_step=source,
                target_step=target,
                source_node_id=f"step:{source['step_id']}:constraint_context",
                target_node_id=f"step:{target['step_id']}:shifted_constraint",
                visible_fields_used=["input_message", "output_message", "tool_output", "visible_step_notes"],
                extraction_rule_id="constraint_modal_shift_v0",
                extraction_notes="hard_to_soft_visible_constraint_shift",
            )
            added += 1
            if added >= 1:
                return


def _add_downstream_dependency_edges(trace_id: str, steps: Sequence[Mapping[str, Any]], edges: list[dict[str, Any]]) -> None:
    added = 0
    for source, target in _pairs(steps):
        target_tokens = _tokens(_text(target))
        shared = _content_overlap(source, target)
        if len(shared) >= 2 and (_DEPENDENCY_MARKERS & target_tokens):
            _add_edge(
                edges,
                trace_id=trace_id,
                edge_type="downstream_dependency_edge",
                source_step=source,
                target_step=target,
                source_node_id=f"step:{source['step_id']}:visible_content",
                target_node_id=f"step:{target['step_id']}:dependent_action",
                visible_fields_used=["input_message", "output_message", "tool_output"],
                extraction_rule_id="visible_content_dependency_v0",
                extraction_notes="later_step_reuses_visible_content",
            )
            added += 1
            if added >= 2:
                return


def _add_tool_alignment_edges(trace_id: str, steps: Sequence[Mapping[str, Any]], edges: list[dict[str, Any]]) -> None:
    added = 0
    for step in steps:
        tool_tokens = _tokens(str(step.get("tool_output") or ""))
        output_tokens = _tokens(str(step.get("output_message") or ""))
        if not tool_tokens:
            continue
        overlap = tool_tokens & output_tokens
        relation = "align" if len(overlap) >= 2 else "ignore"
        if relation == "ignore" and len(tool_tokens) < 4:
            continue
        _add_edge(
            edges,
            trace_id=trace_id,
            edge_type="tool_alignment_edge",
            source_step=step,
            target_step=step,
            source_node_id=f"step:{step['step_id']}:tool_output",
            target_node_id=f"step:{step['step_id']}:step_output",
            visible_fields_used=["tool_call", "tool_output", "output_message"],
            extraction_rule_id="tool_output_to_step_output_overlap_v0",
            extraction_notes=f"tool_output_relation_{relation}",
        )
        added += 1
        if added >= 2:
            return


def _add_cross_agent_dependency_edges(trace_id: str, steps: Sequence[Mapping[str, Any]], edges: list[dict[str, Any]]) -> None:
    added = 0
    for source, target in _pairs(steps):
        if source.get("agent_id") == target.get("agent_id"):
            continue
        shared = _content_overlap(source, target)
        if len(shared) >= 2:
            _add_edge(
                edges,
                trace_id=trace_id,
                edge_type="cross_agent_dependency_edge",
                source_step=source,
                target_step=target,
                source_node_id=f"step:{source['step_id']}:cross_agent_content",
                target_node_id=f"step:{target['step_id']}:cross_agent_use",
                visible_fields_used=["handoff_from", "handoff_to", "input_message", "output_message", "tool_output"],
                extraction_rule_id="cross_agent_content_overlap_v0",
                extraction_notes="visible_content_crosses_agent_boundary",
            )
            added += 1
            if added >= 2:
                return


def _add_semantic_collision_edges(trace_id: str, steps: Sequence[Mapping[str, Any]], edges: list[dict[str, Any]]) -> None:
    added = 0
    for source, target in _pairs(steps):
        source_tokens = _tokens(_text(source))
        target_tokens = _tokens(_text(target))
        if (_SEMANTIC_MARKERS & source_tokens) and ({"selected", "delivers", "aligns"} & target_tokens):
            _add_edge(
                edges,
                trace_id=trace_id,
                edge_type="semantic_collision_edge",
                source_step=source,
                target_step=target,
                source_node_id=f"step:{source['step_id']}:semantic_alternatives",
                target_node_id=f"step:{target['step_id']}:selected_interpretation",
                visible_fields_used=["input_message", "output_message", "tool_output", "visible_step_notes"],
                extraction_rule_id="semantic_alternative_selection_v0",
                extraction_notes="visible_alternative_selected_downstream",
            )
            added += 1
            if added >= 2:
                return
