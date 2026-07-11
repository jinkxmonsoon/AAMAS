# Final Results for Article Tables

## Scope and framing

The following numbers may be used in the article only as diagnostic and negative-evidence summaries. They must not be presented as optimized performance results, superiority evidence, calibration evidence, robustness evidence, or paper-ready method-comparison tables.

## Candidate article table: protocol and representation diagnostics

| Diagnostic item | Value | Allowed framing | Forbidden framing |
| --- | ---: | --- | --- |
| Full-trace corpus size used in final rescue | 420 traces | Controlled trace-bank scope for the final diagnostic rescue. | External validity or production readiness. |
| Candidate-step rows in Task 29 | 2,100 rows | One row per candidate step per trace. | Evidence of scoring readiness by itself. |
| Candidate-step global unique feature vectors | 17 | Evidence of severe global degeneracy. | Evidence of rich representation. |
| Candidate-step duplicate-vector rate | 99.19% | Diagnostic blocker/limitation. | Robustness or generalization evidence. |
| Within-trace duplicate candidate rows | 0 | Justification for one high-risk intra-trace rescue evaluation. | Justification for calibration or open-ended tuning. |
| Redesigned trace-level unique feature vectors | 6 | Evidence that trace-level redesigned features remain degenerate. | Evidence of representation sufficiency. |
| Redesigned trace-level duplicate feature vectors | 414 | Negative evidence about feature diversity. | Performance evidence. |

## Candidate article table: final fixed-formula rescue results

| Method | Family | Step accuracy | Top-2 containment | Article-use note |
| --- | --- | ---: | ---: | --- |
| `majority_step` | Baseline | 25.00% | 25.00% | Strongest non-CCT reference. |
| `always_s2` | Baseline | 25.00% | 25.00% | Trivial position reference. |
| `last_step` | Baseline | 25.00% | 25.00% | Trivial position reference. |
| `random_step_seeded` | Baseline | 17.14% | 17.14% | Seeded random reference. |
| `first_step` | Baseline | 0.00% | 0.00% | Position reference. |
| `flat_log_lexical_baseline` | Baseline | 0.00% | 0.00% | Available flat-log reference under current prediction view. |
| `non_cct_visible_heuristic_baseline` | Baseline | 0.00% | 0.00% | Non-CCT visible heuristic reference. |
| `cct_candidate_step_structural_sum` | CCT | 0.00% | 25.00% | Best CCT variant, but collapsed to `s1`. |
| `cct_candidate_step_flow_only` | CCT | 0.00% | 25.00% | Unsupported. |
| `cct_candidate_step_tool_alignment_only` | CCT | 0.00% | 25.00% | Unsupported. |
| `cct_candidate_step_cross_agent_only` | CCT | 0.00% | 25.00% | Unsupported. |
| `cct_candidate_step_visible_relation_overlap` | CCT | 0.00% | 25.00% | Unsupported. |

## Candidate article table: final hypothesis decisions

| Decision item | Value | Article-use note |
| --- | --- | --- |
| H1-R margin over strongest baseline | -0.250 | Negative diagnostic evidence; required margin was +0.100. |
| H2-R margin over flat/non-CCT reference | 0.000 | No demonstrated added CCT signal under current prediction-view constraints. |
| H1-R final status | Unsupported | Rescue path stops. |
| H2-R final status | Unsupported | Rescue path stops. |
| CCT rescue continuation | No | Return to Path B negative-evidence framing. |

## Required caption caveat

Any article table using these numbers should state that the results are diagnostic evidence from a fixed-formula rescue evaluation after feature-readiness audits, not optimized or calibrated performance results.
