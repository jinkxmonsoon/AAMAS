"""Operational contract constants for BRACIS-Journal-v1."""

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

BOOL_ENUM = {True, False, "true", "false", "yes", "no", "unknown"}

REQUIRED_FIELDS = {
    "trace_id", "dataset_version", "scenario_group", "case_id", "case_variant",
    "perturbation_type", "perturbation_intensity", "step_id", "agent_id", "agent_role",
    "input_message", "output_message", "tool_call", "tool_output", "handoff_from", "handoff_to",
    "evidence_items", "evidence_used", "terminal_outcome", "gold_failure_step", "gold_failure_agent",
    "gold_irreversibility", "gold_propagation", "gold_recoverability", "label_source", "label_confidence",
    "annotator_or_generator", "provenance_notes",
}

PROVENANCE_FIELDS = {"annotator_or_generator", "provenance_notes"}
