# Journal-v1 Full-Trace CCT Uncalibrated Diagnostics Report

Scope: controlled initial diagnostic run of the Task 17 frozen uncalibrated scoring protocol. This is not a paper-ready result table and does not include calibration, LOSO, grid search, refinement, ablation, or statistical testing.

- Branch: `work`
- Execution HEAD: `a19596a44cdd0c54739bb8141c8c9af0a3b0c3c3`
- `configs/cct_scoring.yaml` SHA256 before execution: `053f19066923d8d22d27b22727e75876f939f2a60480484c4028eabd07ad0855`

## Variant metrics

| Variant | Step accuracy | Agent accuracy | Tuple step-agent accuracy | Clean step accuracy | Perturbed step accuracy |
|---|---:|---:|---:|---:|---:|
| `cct_primary_no_position` | 0.114286 | 0.114286 | 0.114286 | 0.107143 | 0.116071 |
| `cct_flow_only` | 0.250000 | 0.250000 | 0.250000 | 0.250000 | 0.250000 |
| `cct_context_only` | 0.028571 | 0.028571 | 0.028571 | 0.000000 | 0.035714 |
| `cct_with_position_features` | 0.250000 | 0.250000 | 0.250000 | 0.250000 | 0.250000 |

## Primary macro by scenario

| Scenario | Step accuracy | n |
|---|---:|---:|
| `clean_broken_handoff` | 0.000000 | 60 |
| `complex_collaboration` | 0.050000 | 60 |
| `cross_agent_propagation` | 0.050000 | 60 |
| `recoverable_irreversible_failure` | 0.050000 | 60 |
| `same_agent_continuation` | 0.200000 | 60 |
| `semantic_collision` | 0.000000 | 60 |
| `tool_evidence_usage` | 0.450000 | 60 |

## Primary macro by perturbation

| Perturbation | Step accuracy | n |
|---|---:|---:|
| `non_causal_textual_distraction` | 0.178571 | 84 |
| `none` | 0.107143 | 84 |
| `paraphrase` | 0.071429 | 84 |
| `partial_observability` | 0.107143 | 84 |
| `tool_output_truncation` | 0.107143 | 84 |

## Diagnostic baseline comparison

| Baseline | Step accuracy | Agent accuracy | Tuple step-agent accuracy |
|---|---:|---:|---:|
| `majority_step` | 0.250000 | 0.250000 | 0.250000 |
| `majority_agent` | 0.250000 | 0.250000 | 0.250000 |
| `always_s2` | 0.250000 | 0.250000 | 0.250000 |
| `first_step` | 0.000000 | 0.000000 | 0.000000 |
| `last_step` | 0.250000 | 0.250000 | 0.250000 |
| `most_detailed_step` | 0.035714 | 0.035714 | 0.035714 |
| `simple_spectrum_visible_step` | 0.000000 | 0.000000 | 0.000000 |
| `simple_spectrum_visible_agent` | 0.000000 | 0.000000 | 0.000000 |

## Interpretation

- H1 diagnostic status: `unsupported_in_this_diagnostic_run`
- H2 diagnostic status: `unsupported_in_this_diagnostic_run`
- H6 status: `future_structural_analysis_only_no_h6_scoring_in_this_run`
- Warnings: primary CCT is near random/plausible-candidate baseline; H1 remains unsupported; high-risk position diagnostic exceeds primary CCT; structural claim is at risk; flow-only diagnostic is near random; handoff/propagation claims are weakened; one or more diagnostic non-CCT/trivial baselines match or exceed primary CCT; H2 is not supported
- Non-actions: no calibration, grid search, LOSO, refinement, ablation, statistical test, or paper-ready result table was produced.
