# Rescue Experiment Acceptance Criteria

## Scope

This report defines success, failure, and blocker criteria for a future rescue experiment. It does not run scoring, ranking, calibration, tuning, statistical tests, or result-table generation.

## H1-R acceptance

H1-R is supported only if the best pre-specified CCT rescue variant exceeds the strongest trivial or flat-log baseline by at least **+10 percentage points in failure-step accuracy** or at least **+0.10 absolute macro step accuracy**. The threshold is fixed before execution.

## H2-R acceptance

H2-R is supported only if causal-flow CCT features outperform the strongest flat-log baseline under identical prediction-view inputs by at least **+10 percentage points in failure-step accuracy** or **+0.10 absolute macro step accuracy**. If flat-log wins or ties within margin, H2-R is unsupported.

## H6-R acceptance

H6-R is evaluated only if separately enabled. It requires leakage-safe H6 evaluation without H6 private evidence, label rationale, provenance, scenario/perturbation inputs, or gold leakage. Metrics must be separate from step/agent attribution and must exceed a pre-specified non-CCT visible baseline margin before any H6 claim is allowed.

## Hard blockers before scoring

- Candidate-step feature-vector duplicate rate greater than 50%.
- Any feature family constant in more than 95% of candidate rows unless excluded before scoring.
- Leakage audit failure.
- Any use of forbidden fields as feature or baseline inputs.
- Scenario, perturbation, or case-variant dependence in model inputs.
- Position/agent identity dependence dominating results.
- Missing prediction freeze before private-label evaluation.

## Failure criteria

- CCT rescue variants do not exceed the strongest baseline by the pre-specified margin.
- Flat-log baseline beats causal-flow CCT features.
- Results require post-hoc threshold changes, tuning, or calibration.
- Results are not reproducible from the new rescue config and deterministic seed.

## Execution readiness decision

- Protocol design ready: yes.
- Immediate scoring ready: no.
- Next task: implement a non-scoring candidate-step feature-readiness dry run with leakage and degeneracy audits.
