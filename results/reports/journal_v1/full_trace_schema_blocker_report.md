# Journal-v1 Full-Trace Schema Blocker Report

## Blocker status

**Evaluation is blocked.** The current Journal-v1 corpus is failure-centered and lacks a full ordered multi-step trace representation.

## Evidence

Task 12A found that direct leakage through raw fields could be corrected with `make_prediction_view(record)`, but sanitized non-CCT diagnostics still left `spectrum_inspired_step` at 100% step accuracy. The remaining source is corpus representation: each record exposes the visible content of the failure-point event rather than a full candidate trace.

## Failure-centered fields

The current records include top-level fields that behave as target-equivalent or failure-centered fields:

- `step_id` identifies the failure step;
- `agent_id` identifies the failure agent;
- `handoff_to` identifies the failure agent in the current corpus;
- `input_message`, `output_message`, `tool_call`, and `tool_output` describe the failure event rather than all events;
- `label_rationale`, `propagation_evidence`, `irreversibility_evidence`, `recovery_opportunity`, `provenance_notes`, and `synthetic_control_rule` are private/non-visible and must not be exposed to prediction code.

## Required schema replacement

The next corpus schema must use one record per complete trace and include an ordered `steps` array. Each step must include:

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

Private labels and adjudication/provenance fields must remain outside model-visible steps.

## Migration decision

The current 420-record corpus is not evaluation-ready and no result from it may be used in the paper. Because the current records store a single failure-centered event rather than full ordered traces, migration should default to regeneration from an approved full-trace builder unless a future audit proves enough raw information exists for lossless conversion without fabricating non-failure steps.

## Blocked work

Until full-trace schema migration is implemented and audited, all of the following remain blocked:

- evaluation;
- CCT graph construction;
- CCT scoring;
- calibration;
- refinement variants;
- ablations;
- paper-ready result tables.
