# Journal-v1 Full-Trace CCT Scoring Protocol Risk Report

## Scope

This is a protocol-risk report only. It freezes guardrails for a future uncalibrated scoring task and does not execute scoring, ranking, evaluation, calibration, refinement, ablation, empirical hypothesis testing, or paper-ready result table generation.

## Task 16B risks carried forward

- Several structural fields are position or identity shortcuts: `step_id`, `order_index`, `agent_id`, and `agent_role`.
- Flow fields can be partly position-derived in the current fixed five-step graph shape.
- Graph node count and edge count are constant across the current full-trace CCT artifacts.
- Identical structural feature vectors occur frequently enough to require shortcut-risk interpretation in any future scoring report.

## Guardrails frozen for future scoring

- Primary scoring must use `cct_primary_no_position` from `configs/cct_scoring.yaml`.
- Primary scoring must exclude high-risk position/identity fields.
- Scenario, perturbation, trace, case, provenance, and private/gold fields are forbidden as score features.
- Weights are fixed before execution; no learned parameters, grid search, LOSO tuning, calibration, or post-performance adjustment is permitted.
- Diagnostic variants must include `cct_flow_only` and `cct_context_only`; `cct_with_position_features` is optional and high-risk, not primary.

## Readiness decision

Decision: `protocol_frozen_scoring_not_run`.

A future scoring task may be proposed only after this protocol validator passes and the future task explicitly acknowledges the Task 16B shortcut warnings. No empirical claim is authorized by this report.
