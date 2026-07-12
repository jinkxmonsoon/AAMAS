# CCT Representation-Only Status After Scoring-Config Blocker

## Scope

Task 21 continues only representation-level causal-edge auditing after the Task 20F scoring-config hash adjudication. It does not restore or recreate `configs/cct_scoring.yaml`, run scoring, rank candidate steps, compare edges to gold/H6 labels, calibrate, grid search, run LOSO, refine scoring, ablate, perform statistical tests, change corpus/gold labels, or produce paper-ready result tables.

## Current status

- Branch inspected: `work`
- HEAD inspected before Task 21 changes: `43141e72f9de7d7e59f7948524eb523804d0b421`
- `configs/cct_scoring.yaml` remains absent from the active checkout.
- Task 18 remains `NOT_REPRODUCIBLE_FROM_CURRENT_CHECKOUT` because no available PR #22 candidate matched the expected frozen SHA256 `053f19066923d8d22d27b22727e75876f939f2a60480484c4028eabd07ad0855`.
- Scoring and calibration remain blocked.
- Representation-only causal-edge design remains allowed only under no-gold, no-H6-label, no-scoring, no-ranking, sample-audit constraints.

## Allowed work under this status

- Inspect sample-only causal-edge artifacts and reports.
- Audit visible-field use, edge sparsity/density, clean-vs-perturbed sample stability, and template sensitivity.
- Clarify rule limitations and future audit requirements.
- Recommend a future representation-only task that does not compare edge outputs to private labels or scoring outputs.

## Forbidden work under this status

- Restore a non-matching `configs/cct_scoring.yaml` candidate as authoritative.
- Modify the expected frozen hash.
- Run any CCT scoring, ranking, calibration, grid search, LOSO, scoring refinement, ablation, gold/H6 comparison, empirical hypothesis test, or paper-ready result table.
