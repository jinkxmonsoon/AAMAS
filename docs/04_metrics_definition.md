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
