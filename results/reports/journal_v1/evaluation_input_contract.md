# Journal-v1 Evaluation Input Contract

## Status

This contract is binding for all future baseline and CCT evaluation code. It defines the model-visible prediction input separately from private labels and diagnostic metadata.

## Prediction input MAY include

- `trace_id` as an identifier only; predictors must not parse embedded scenario or perturbation substrings from it.
- `case_variant` only when it is non-informative for the target.
- Candidate step IDs as `candidate_steps`.
- Candidate agent IDs as `candidate_agents`.
- Ordered multi-step trace content once the corpus schema is revised to support full traces.
- Visible agent roles for each step in a full trace.
- Visible messages, tool calls, tool outputs, and terminal outcome fields for each step in a full trace.
- Model-visible evidence item identifiers/content that do not state private labels or rationales.

## Prediction input MUST NOT include

- `gold_failure_step`.
- `gold_failure_agent`.
- `gold_irreversibility`.
- `gold_propagation`.
- `gold_recoverability`.
- `label_rationale`.
- `label_source`.
- `label_confidence`.
- `synthetic_control_rule`.
- `adjudication_decision`.
- `annotator_or_generator`.
- `provenance_notes`.
- `generation_seed`.
- `propagation_evidence` when it directly states the gold dependency.
- `irreversibility_evidence` when it directly states the gold outcome.
- `recovery_opportunity` when it directly states recoverability.
- Top-level `step_id` or `agent_id` when those fields identify the failure point rather than enumerate full trace steps.
- `handoff_to` or `handoff_from` as top-level fields in the current failure-centered schema because `handoff_to` identifies the failure agent in this corpus.

## Current Task 12A prediction view

`src/cctdiag/io/views.py` implements `make_prediction_view(record)` with these top-level keys:

- `view_version`;
- `trace_id`;
- `case_variant`;
- `candidate_steps`;
- `candidate_agents`;
- `observed_step_content` containing only sanitized visible fields;
- `model_visible_evidence_items`;
- `representation_warning`.

The current view still contains only failure-centered single-record visible content because the corpus does not yet provide full ordered multi-step traces. Therefore, this contract prevents direct private-field leakage but does not clear the corpus for CCT evaluation.

## Required enforcement

- Baselines and future CCT code must call `make_prediction_view(record)` before prediction.
- Baselines and future CCT code must reject raw records with `assert_no_gold_leakage(prediction_view)` or equivalent enforcement.
- Evaluation metrics may access private labels only after predictions are produced.
- No parent gold-label propagation is allowed.
