"""Contracts for the Journal-v1 full ordered trace schema.

Task 13 defines validation infrastructure only. It does not regenerate corpus
files, implement CCT scoring, calibration, refinement variants, ablations, or
paper-ready result tables.
"""

from __future__ import annotations

DATASET_VERSION = "BRACIS-Journal-v1"

SCENARIO_GROUPS = {
    "clean_broken_handoff",
    "tool_evidence_usage",
    "same_agent_continuation",
    "cross_agent_propagation",
    "recoverable_irreversible_failure",
    "semantic_collision",
    "complex_collaboration",
}

PERTURBATION_TYPES = {
    "none",
    "paraphrase",
    "tool_output_truncation",
    "partial_observability",
    "non_causal_textual_distraction",
    "evidence_order_shuffle",
    "irrelevant_tool_noise",
    "handoff_ambiguity",
}

REQUIRED_FULL_TRACE_FIELDS = {
    "trace_id",
    "dataset_version",
    "scenario_group",
    "case_id",
    "case_variant",
    "perturbation_type",
    "perturbation_intensity",
    "steps",
    "terminal_outcome",
    "private_labels",
    "provenance",
}

REQUIRED_STEP_FIELDS = {
    "step_id",
    "agent_id",
    "agent_role",
    "input_message",
    "output_message",
    "tool_call",
    "tool_output",
    "handoff_from",
    "handoff_to",
    "evidence_items",
    "evidence_used",
    "visible_step_notes",
}

REQUIRED_PRIVATE_LABEL_FIELDS = {
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
    "primary_labeler",
    "secondary_labeler",
    "adjudicator",
    "disagreement_type",
    "adjudication_decision",
    "manual_audit_status",
}

REQUIRED_PROVENANCE_FIELDS = {
    "annotator_or_generator",
    "provenance_notes",
    "synthetic_control_rule",
}

FORBIDDEN_FULL_TRACE_TOP_LEVEL_FIELDS = {
    "step_id",
    "agent_id",
    "agent_role",
    "input_message",
    "output_message",
    "tool_call",
    "tool_output",
    "handoff_from",
    "handoff_to",
    "evidence_items",
    "evidence_used",
    "gold_failure_step",
    "gold_failure_agent",
    "gold_irreversibility",
    "gold_propagation",
    "gold_recoverability",
    "label_rationale",
    "label_confidence",
    "label_source",
}

PRIVATE_PREDICTION_FORBIDDEN_FIELDS = REQUIRED_PRIVATE_LABEL_FIELDS | REQUIRED_PROVENANCE_FIELDS | {
    "private_labels",
    "provenance",
    "generation_seed",
    "label_rationale",
    "label_confidence",
    "label_source",
    "propagation_evidence",
    "irreversibility_evidence",
    "recovery_opportunity",
    "gold_failure_step",
    "gold_failure_agent",
    "gold_irreversibility",
    "gold_propagation",
    "gold_recoverability",
}

MIN_STEPS_PER_TRACE = 4
MIN_AGENTS_PER_TRACE = 2
MIN_NON_GOLD_CANDIDATE_STEPS = 2
MIN_NON_GOLD_CANDIDATE_AGENTS = 1
