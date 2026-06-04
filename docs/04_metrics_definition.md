# 04 — Metrics Definition

## Task 11 diagnostic metric interfaces

Task 11 authorizes implementation of basic metric interfaces for diagnostic
sanity checks on the corrected BRACIS-Journal-v1 corpus. These interfaces are
limited to accuracy-style comparisons between gold labels and supplied
predictions:

- `step_accuracy`
- `agent_accuracy`
- `tuple_accuracy_step_agent`
- `irreversibility_accuracy`
- `propagation_accuracy`
- `recoverability_accuracy`
- `macro_accuracy_by_scenario`
- `macro_accuracy_by_perturbation`

## Scope limits

- These interfaces do **not** implement CCT scoring.
- These interfaces do **not** implement calibration.
- These interfaces do **not** implement refinement variants.
- These interfaces do **not** implement ablations.
- Diagnostic trivial-baseline outputs are not paper-ready result tables and may
  be used only as shortcut-risk checks before future approved method work.
- H6 metrics must be reported as `NA` when a baseline does not produce the
  corresponding prediction rather than as zero.

## Shortcut-risk sanity thresholds

For the Task 11 diagnostic gate:

- If any standalone trivial baseline step accuracy is greater than 50%,
  evaluation remains blocked.
- If `majority_agent` agent accuracy is greater than 50%, evaluation remains
  blocked.
- If random or first/last active agent accuracy is unexpectedly high, the corpus
  must be flagged for review.
- Otherwise, the trivial-baseline sanity gate may be marked as passed.

## Task 12 non-CCT baseline diagnostic layer

Task 12 authorizes transparent deterministic flat-log and spectrum-inspired
baseline diagnostics before any CCT implementation. These diagnostics may use
non-gold log text and metadata, but they must not use gold labels for
prediction, parent gold labels, CCT graph construction, calibration, learned
weights, LLM calls, refinement variants, ablations, or paper-ready result-table
formatting.

Task 12 diagnostics use the existing metric interfaces from Task 11:

- step accuracy;
- agent accuracy;
- tuple step-agent accuracy when both predictions exist;
- macro step accuracy by scenario;
- macro step accuracy by perturbation;
- H6 accuracies only when a baseline explicitly predicts H6 labels, otherwise
  `NA`.

Diagnostic interpretation thresholds:

- Any non-CCT baseline above 70% step or agent accuracy flags corpus/baseline
  review.
- Any non-CCT baseline above 85% step or agent accuracy blocks evaluation
  pending investigation.
- Moderate non-CCT results would permit CCT implementation only in a later
  explicitly approved task.
