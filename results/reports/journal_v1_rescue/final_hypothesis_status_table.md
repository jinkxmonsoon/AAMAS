# Final Hypothesis Status Table

## Scope

This table records the final hypothesis status after the failed Task 30 rescue evaluation. It is a claim-governance artifact and does not authorize additional scoring, tuning, calibration, ablation, or performance claims.

| Hypothesis | Final status | Evidence basis | Article framing |
| --- | --- | --- | --- |
| H1 | Unsupported | Task 18 diagnostic scoring did not support automatic failure-step attribution improvement, and the scoring configuration is not reproducible from the current checkout. | Mention only as negative diagnostic evidence and motivation for protocol-first framing. |
| H2 | Unsupported | Task 18 and later representation audits did not show CCT superiority over baselines. | Do not claim baseline outperformance. |
| H3 | Blocked | Calibration remains blocked by missing frozen scoring-config provenance and insufficient feature validity. | State that calibration is not authorized. |
| H4 | Blocked | Robustness/performance testing is not justified without a scoring-ready representation. | Do not claim perturbation robustness. |
| H6 | Open but unsupported | H6 was not evaluated with leakage-safe evidence in a scoring-ready protocol. | May describe as a future research question only. |
| H1-R | Unsupported | Task 30 best CCT variant `cct_candidate_step_structural_sum` had 0.00% step accuracy versus 25.00% for `majority_step`; margin = -0.250 against a required +0.100. | Use as final rescue failure evidence. |
| H2-R | Unsupported | Task 30 CCT variants did not outperform the available flat-log/non-CCT reference under the prediction-view contract; margin = 0.000 against a required +0.100. | Use as evidence that current causal-flow features do not add demonstrated diagnostic signal. |
| H6-R | Not tested / unsupported | No H6 labels or private H6 evidence were used in Task 30. | Do not make H6 performance or relation-signal claims. |

## Final decision

The rescue path is closed under the current feature representation. The article should proceed, if at all, under Path B: protocol-first benchmark construction, diagnostic representation governance, and negative findings about naive structural and current causal-flow features.
