# 15 — CCT Causal-Flow Descriptor Sample Prototype Specification

## Status

Task 18C defines and prototypes sample-only causal-flow descriptors. This task does not revise scoring, modify `configs/cct_scoring.yaml`, compute CCT predictions, rank candidate steps, compare descriptor values to gold labels, calibrate, grid search, run LOSO, refine, ablate, run statistical tests, or produce paper-ready result tables.

## Input boundary

Descriptor extraction must consume `make_full_trace_prediction_view(record)` outputs only. Raw records containing `private_labels`, gold fields, label rationales, H6 private evidence, or provenance fields must be rejected by descriptor extraction helpers.

## Sample boundary

The prototype uses a fixed documented sample: first clean trace and first perturbed trace per scenario group, capped at 20 traces. This keeps the task reviewable and avoids full-corpus feature revision before descriptor leakage/variance behavior is understood.

## Descriptor definitions

### `handoff_constraint_shift_indicator`

- Rule: detect a shared visible constraint cue where earlier visible context uses strong modality (`required`, `must`, `enforce`, `condition`, `authorized`, `verified`, `confirmed`) and the current step output uses weak modality (`optional`, `background`, `preference`, `may`, `softened`, `omits`, `misses`, `weak`).
- Visible fields used: ordered step `input_message`, `output_message`, `handoff_from`, `handoff_to`, and `visible_step_notes`.
- Forbidden fields not used: gold labels, `private_labels`, label rationales, H6 private evidence, provenance, `scenario_group`, `perturbation_type`, `trace_id` as a descriptor value, and `case_id`.
- Output type: boolean descriptor row per step.
- Future status: candidate for future primary scoring only after full-corpus leakage/variance/shortcut audit.

### `evidence_ignored_indicator`

- Rule: detect when visible tool/evidence text contains constraint cues absent from the current output, or when strong tool/evidence modality is weakened in the output.
- Visible fields used: `tool_output`, `evidence_items`, `evidence_used`, `output_message`, and `visible_step_notes`.
- Forbidden fields not used: private/gold/provenance fields and audit metadata.
- Output type: boolean descriptor row per step.
- Future status: candidate for future primary scoring if deterministic extraction remains stable after full audit.

### `downstream_reference_to_prior_output`

- Rule: detect whether later visible steps lexically carry at least two non-stopword tokens introduced in the current step output/visible notes.
- Visible fields used: current `output_message`/`visible_step_notes` and later `input_message`, `output_message`, and `visible_step_notes`.
- Forbidden fields not used: private/gold/provenance fields and audit metadata.
- Output type: boolean descriptor row per step.
- Future status: candidate for future primary scoring after variance and position-shortcut audit.

## Review and risk requirements

Each descriptor must report positive/negative counts, missing/null counts, whether it is constant in the sample, whether positives appear limited to one scenario template, leakage risks, lexical shortcut risks, and readiness for full-corpus audit. `DESCRIPTOR_READY_FOR_SCORING` defaults to `no`.
