# 14 — CCT Uncalibrated Scoring Protocol Freeze

## Status

This document freezes the first uncalibrated CCT scoring protocol before any CCT scoring or evaluation is run. It is protocol-only. It does not compute predictions, rank records, compare against gold labels, calibrate weights, run refinement variants, perform ablations, test empirical hypotheses, or generate paper-ready result tables.

## Provenance

- Active branch at protocol freeze: `work`.
- Active local commit at protocol freeze: `efce2682977950580d47fcdd2c45e21dfe0cba42` before this Task 17 commit.
- PR #21 discrepancy note: prior local handoff text referred to commit `276467...`, while the GitHub PR summary reportedly showed commit `38b9c46`; the active repository commit inspected for this protocol task was `efce2682977950580d47fcdd2c45e21dfe0cba42`.

## Objective for a future execution task

The first uncalibrated CCT scorer will produce diagnostic candidate scores for candidate steps within each trace. Candidate agents may be summarized only through their associated candidate steps. Scores must not be interpreted as calibrated probabilities, causal certainty, or paper-ready evidence.

## Primary formula

The primary formula is a transparent weighted sum over predefined structural feature values. Weights are fixed in `configs/cct_scoring.yaml` before any future scoring run. No learned parameters, leave-one-scenario-out tuning, grid search, calibration, or post-performance adjustment is allowed.

## Allowed feature groups

### A. Evidence/tool support

- `evidence_used_count`
- `evidence_item_count`
- `has_tool_call`
- `tool_output_token_count`
- `output_token_count` when justified as visible diagnostic context rather than verbosity alone

### B. Handoff/flow support

- `has_handoff_from`
- `has_handoff_to`
- `in_degree`
- `out_degree`
- `downstream_dependency_count` if present in a future visible feature payload
- `propagation_candidate_count` if present in a future visible feature payload

### C. Context density

- `input_token_count`
- `output_token_count`
- `local_context_density` if present in a future visible feature payload

## Restricted/high-risk feature groups

The following are excluded from the primary formula because Task 16B identified position and template shortcut risk:

- `step_id`
- `order_index`
- `agent_id`
- `agent_role`
- `terminal_proximity`
- pure position-derived degree features if not normalized

These may appear only in explicitly documented diagnostic variants, never as primary scoring inputs unless a later protocol amendment provides a strong written justification before execution.

## Forbidden fields

The scorer must not use any gold label, `private_labels`, `label_rationale`, H6 private evidence fields, provenance fields, `scenario_group`, `perturbation_type`, `trace_id`, or `case_id` as score features. Scenario and perturbation may be used only for future aggregate reporting after predictions exist.

## Frozen variants

- `cct_primary_no_position`: primary uncalibrated weighted-sum scorer excluding position and identity fields.
- `cct_flow_only`: diagnostic variant using handoff/flow support only.
- `cct_context_only`: diagnostic variant using context-density fields only.
- `cct_with_position_features`: optional high-risk diagnostic variant, not primary, used only to quantify shortcut sensitivity.

## Mandatory future reporting

Any future scoring task must report step accuracy, agent accuracy, tuple step-agent accuracy, macro by scenario, macro by perturbation, comparison to trivial baselines, comparison to non-CCT baselines, and shortcut-risk interpretation. Those reports are not produced in this task.

## Future blocker rules

- If primary CCT performs similarly to a position-only diagnostic, claims must be weakened.
- If `cct_with_position_features` dominates `cct_primary_no_position`, the structural claim is at risk.
- If `cct_flow_only` performs near random, handoff/propagation claims are weakened.
- If non-CCT baselines exceed CCT, H1/H2 cannot be claimed.
- If results are high only on clean traces but fail under perturbation, robustness claims are blocked.

## Explicit non-actions

No scoring, ranking, evaluation, calibration, refinement, ablation, empirical hypothesis test, or paper-ready result table is produced by this protocol freeze.
