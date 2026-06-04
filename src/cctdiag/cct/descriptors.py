"""Sample-only causal-flow descriptor prototypes for full-trace CCT records.

These descriptors consume sanitized full-trace prediction views only. They are
not scoring features in the frozen protocol, do not access private labels, and
must not be compared with gold labels in this prototype task.
"""

from __future__ import annotations

import re
from collections.abc import Mapping
from typing import Any

DESCRIPTOR_EXTRACTION_VERSION = "journal_v1_cct_descriptor_sample_v1"
DESCRIPTOR_NAMES = [
    "handoff_constraint_shift_indicator",
    "evidence_ignored_indicator",
    "downstream_reference_to_prior_output",
]
FORBIDDEN_INPUT_FIELDS = {
    "private_labels",
    "provenance",
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
    "scenario_group",
    "perturbation_type",
    "case_id",
}
CONSTRAINT_CUES = {
    "budget cap",
    "privacy flag",
    "time window",
    "format rule",
    "access limit",
    "priority tier",
    "required",
    "condition",
    "constraint",
    "date",
    "source",
    "authorization",
    "confidence",
    "estimate",
}
STRONG_MODALITY = {"required", "must", "enforce", "condition", "authorized", "verified", "confirmed"}
WEAK_MODALITY = {"optional", "background", "preference", "may", "softened", "omits", "misses", "weak"}
STOPWORDS = {
    "the", "and", "with", "that", "this", "from", "into", "case", "step", "note", "notes", "output",
    "input", "visible", "context", "relevant", "downstream", "candidate", "records", "perform", "including",
    "one", "for", "but", "not", "while", "through", "received", "packet", "detail", "details",
}


def assert_prediction_view_safe(payload: Mapping[str, Any]) -> None:
    """Reject raw/private payloads before descriptor extraction."""

    leaked: list[str] = []

    def visit(value: Any, path: str = "") -> None:
        if isinstance(value, Mapping):
            for key, nested in value.items():
                key_text = str(key)
                nested_path = f"{path}.{key_text}" if path else key_text
                if key_text in FORBIDDEN_INPUT_FIELDS:
                    leaked.append(nested_path)
                visit(nested, nested_path)
        elif isinstance(value, list | tuple):
            for index, item in enumerate(value):
                visit(item, f"{path}[{index}]")

    visit(payload)
    if leaked:
        raise ValueError("descriptor input contains forbidden/private fields: " + ", ".join(sorted(leaked)))
    if "steps" not in payload or "view_version" not in payload:
        raise ValueError("descriptor extraction requires a sanitized full-trace prediction view")


def _text(*values: Any) -> str:
    return " ".join(str(value or "") for value in values).lower()


def _tokens(value: str) -> set[str]:
    return {token for token in re.findall(r"[a-z][a-z0-9_]+", value.lower()) if token not in STOPWORDS and len(token) > 3}


def _constraint_hits(value: str) -> set[str]:
    lowered = value.lower()
    return {cue for cue in CONSTRAINT_CUES if cue in lowered}


def _has_any(value: str, terms: set[str]) -> bool:
    lowered = value.lower()
    return any(term in lowered for term in terms)


def _record(trace_id: str, step_id: str, descriptor_name: str, value: bool, fields: list[str], notes: str) -> dict[str, Any]:
    return {
        "trace_id": trace_id,
        "step_id": step_id,
        "descriptor_name": descriptor_name,
        "descriptor_value": bool(value),
        "visible_fields_used": fields,
        "extraction_notes": notes,
        "extraction_version": DESCRIPTOR_EXTRACTION_VERSION,
    }


def extract_descriptor_rows(prediction_view: Mapping[str, Any]) -> list[dict[str, Any]]:
    """Extract sample-only descriptor rows from a prediction view."""

    assert_prediction_view_safe(prediction_view)
    trace_id = str(prediction_view["trace_id"])
    steps = list(prediction_view["steps"])
    rows: list[dict[str, Any]] = []

    prior_outputs: list[str] = []
    for index, step in enumerate(steps):
        step_id = str(step["step_id"])
        current_output = _text(step.get("output_message"), step.get("visible_step_notes"))
        current_input = _text(step.get("input_message"))
        current_tool = _text(step.get("tool_output"), " ".join(step.get("evidence_items") or []), " ".join(step.get("evidence_used") or []))
        prior_text = _text(*prior_outputs)
        combined_current = _text(current_input, current_output, current_tool)

        prior_constraints = _constraint_hits(prior_text)
        current_constraints = _constraint_hits(combined_current)
        shared_constraints = prior_constraints & current_constraints
        shift = bool(shared_constraints and _has_any(prior_text, STRONG_MODALITY) and _has_any(current_output, WEAK_MODALITY))
        rows.append(
            _record(
                trace_id,
                step_id,
                "handoff_constraint_shift_indicator",
                shift,
                ["steps.output_message", "steps.input_message", "steps.handoff_from", "steps.handoff_to", "steps.visible_step_notes"],
                "shared constraint cue with strong prior modality and weak/optional current output" if shift else "no deterministic strong-to-weak handoff modality shift detected",
            )
        )

        tool_constraints = _constraint_hits(current_tool)
        output_constraints = _constraint_hits(current_output)
        ignored = bool(tool_constraints - output_constraints) or bool(_has_any(current_tool, STRONG_MODALITY) and _has_any(current_output, WEAK_MODALITY))
        rows.append(
            _record(
                trace_id,
                step_id,
                "evidence_ignored_indicator",
                ignored,
                ["steps.tool_output", "steps.evidence_items", "steps.evidence_used", "steps.output_message", "steps.visible_step_notes"],
                "visible tool/evidence cue absent from or weakened in step output" if ignored else "tool/evidence cues appear carried or no explicit cue detected",
            )
        )

        output_tokens = _tokens(current_output)
        downstream_text = _text(*[_text(s.get("input_message"), s.get("output_message"), s.get("visible_step_notes")) for s in steps[index + 1 :]])
        downstream_tokens = _tokens(downstream_text)
        overlap = output_tokens & downstream_tokens
        reference = len(overlap) >= 2
        rows.append(
            _record(
                trace_id,
                step_id,
                "downstream_reference_to_prior_output",
                reference,
                ["steps.output_message", "later_steps.input_message", "later_steps.output_message", "later_steps.visible_step_notes"],
                f"downstream overlap tokens: {', '.join(sorted(overlap)[:8])}" if reference else "insufficient downstream lexical carryover detected",
            )
        )
        prior_outputs.append(current_output)

    return rows
