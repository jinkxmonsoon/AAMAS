# 13 — Full Ordered Trace Schema Migration Plan

## Status and scope

Task 12B freezes the migration plan from the current failure-centered single-record representation to a full ordered multi-step trace representation for **BRACIS-Journal-v1**.

This is a protocol/schema correction task only:

- no corpus regeneration is performed;
- no gold labels are changed;
- no perturbation definitions are changed;
- no CCT graph construction or CCT scoring is implemented;
- no calibration, refinement variants, ablations, or paper-ready result tables are implemented.

## Diagnosis: why the current corpus is failure-centered

The current `data/processed/journal_v1/main_all_traces.jsonl` representation stores one JSONL record per trace, but that record is centered on the failure event rather than on the full trace. The top-level fields describe the failure point directly:

- `step_id` equals the failure step in the current records;
- `agent_id` equals the failure agent in the current records;
- `handoff_to` is target-equivalent for the failure agent in the current records;
- `input_message`, `output_message`, `tool_call`, and `tool_output` describe the failure-point event rather than all candidate events;
- phase and event strings in the failure-point text make step attribution trivial even after gold/private fields are removed;
- private fields such as `label_rationale`, `propagation_evidence`, `irreversibility_evidence`, `recovery_opportunity`, `provenance_notes`, and `synthetic_control_rule` are present in raw records and must stay outside model-visible prediction inputs.

Therefore, the current 420-record corpus is **not evaluation-ready**. It remains useful only as a diagnostic artifact and migration source candidate.

## New required unit of evaluation

The new unit of evaluation is:

> **one record = one complete ordered multi-step trace**

Each record must contain an ordered `steps` array. Each element of `steps` must represent a model-visible trace step and include:

- `step_id`;
- `agent_id`;
- `agent_role`;
- `input_message`;
- `output_message`;
- `tool_call`;
- `tool_output`;
- `handoff_from`;
- `handoff_to`;
- `evidence_items`;
- `evidence_used`;
- `visible_step_notes`, if needed.

Top-level `step_id` and top-level `agent_id` are prohibited in the full-trace schema because they identify a single event and recreate the failure-centered view. Step and agent identifiers belong inside `steps` where they enumerate all candidate events.

## Private label fields outside model-visible steps

The following fields remain top-level private/evaluation-only fields outside the model-visible `steps` array:

- `gold_failure_step`;
- `gold_failure_agent`;
- `gold_irreversibility`;
- `gold_propagation`;
- `gold_recoverability`;
- `label_rationale`;
- `label_confidence`;
- `label_source`;
- H6 evidence fields, including `propagation_evidence`, `irreversibility_evidence`, and `recovery_opportunity`;
- adjudication/provenance fields, including `primary_labeler`, `secondary_labeler`, `adjudicator`, `disagreement_type`, `adjudication_decision`, `manual_audit_status`, `annotator_or_generator`, `provenance_notes`, `synthetic_control_rule`, and generation metadata.

Private fields may be used by validators and metric evaluation after predictions are produced. They must not be passed to prediction code.

## Full-trace prediction-view contract

Prediction view may include:

- `trace_id` as an identifier only;
- ordered visible `steps`;
- visible `agent_id` and `agent_role` per step;
- visible `input_message`, `output_message`, `tool_call`, `tool_output`, handoff fields, and evidence fields per step;
- all candidate step IDs and candidate agent IDs derived from the ordered `steps` array.

Prediction view must not include:

- any gold label;
- label rationale;
- private H6 evidence fields;
- top-level failure-centered `step_id` or `agent_id`;
- any field that directly identifies the failure step or failure agent;
- provenance/control fields that encode generation rules or label provenance;
- scenario or perturbation strings if they directly reveal labels or target construction.

## Migration implications

- The current 420-record corpus is not evaluation-ready.
- Current trivial and non-CCT baseline outputs are diagnostic-only shortcut/leakage checks.
- No result from the failure-centered corpus may be used in the paper.
- Existing records may be converted into full traces only if enough non-failure step information exists to reconstruct realistic, ordered, model-visible candidate events without fabricating evidence.
- If existing records do not contain enough information, the corpus must be regenerated from `scripts/build_main_corpus.py` or a successor builder under the full-trace schema.
- Because the current JSONL records store only one failure-centered event, the default expected path is **regeneration from the builder under the full-trace schema**, not silent conversion.

## Acceptance criteria for a future full-trace corpus

A future full-trace Journal-v1 corpus is accepted for evaluation preparation only if all of the following hold:

- each trace has at least 4 ordered steps;
- each trace has at least 2 agents;
- `gold_failure_step` appears among `steps[*].step_id`;
- `gold_failure_agent` appears among `steps[*].agent_id`;
- at least 2 plausible non-gold candidate steps exist per trace;
- at least 1 plausible non-gold candidate agent exists per trace;
- prediction view contains all candidate steps, not only the failing step;
- prediction view contains all candidate agents, not only the failing agent;
- private labels, rationales, H6 evidence, and provenance fields are excluded from prediction view;
- non-CCT baselines are rerun after migration;
- `spectrum_inspired_step` must no longer trivially reach 100% unless the run is explicitly justified and blocked for review;
- schema, label consistency, leakage, integrity, and prediction-view audits all pass.

## Validator updates required in a future task

Future validator work must add or update:

- schema validator checks for a top-level ordered `steps` array;
- schema validator checks for the required per-step fields;
- schema validator rejection of top-level failure-centered `step_id` and `agent_id` in evaluation-ready records;
- label consistency checks that gold labels appear in the `steps` array;
- label consistency checks that plausible non-gold candidate steps/agents exist;
- leakage audit scans over visible `steps` only;
- leakage audit rejection of private label/rationale/provenance/H6 fields in prediction view;
- integrity audit validation of parent-child perturbed traces under the full-trace schema;
- prediction-view tests that all candidate steps and agents are preserved.

## Builder updates required in a future task

Future builder work must update `scripts/build_main_corpus.py` or its successor so that:

- it generates full ordered traces;
- failure step varies across `s2`, `s3`, `s4`, and `s5`;
- non-failure steps are realistic and plausible;
- evidence structures span multiple steps;
- handoff structures span multiple steps;
- perturbed traces preserve parent trace structure unless the perturbation explicitly changes observability;
- private labels/rationales/evidence/provenance are separated from model-visible step content;
- full-trace manifests and audits are regenerated after approved corpus regeneration.

## Explicit blocked status

Until full-trace schema migration is implemented and audited:

- evaluation is blocked;
- CCT graph construction is blocked;
- CCT scoring is blocked;
- calibration is blocked;
- V2 refinement is blocked;
- ablations are blocked;
- paper-ready result tables are blocked.
