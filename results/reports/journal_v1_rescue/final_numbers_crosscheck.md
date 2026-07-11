# Final Numbers Crosscheck

## Scope

This crosscheck records internally consistent numbers that may be reused for manuscript writing as diagnostic evidence only. It does not recompute results, run scoring, introduce new variants, revise hypotheses, or generate new experimental claims.

## Corpus and artifact counts

| Number | Frozen value | Source artifact/report | Crosscheck status |
| --- | ---: | --- | --- |
| Final rescue traces | 420 | `final_experimental_decision_report.md`; `final_results_for_article_tables.md` | Consistent. |
| Candidate-step feature rows | 2,100 | `rescue_candidate_step_feature_inventory.md`; `final_results_for_article_tables.md` | Consistent with 420 traces × 5 candidate steps. |
| Candidate-step global unique feature vectors | 17 | `rescue_candidate_step_feature_degeneracy_report.md`; `final_results_for_article_tables.md` | Consistent. |
| Candidate-step duplicate-vector rate | 99.19% | `rescue_candidate_step_feature_degeneracy_report.md`; `final_results_for_article_tables.md` | Consistent. |
| Within-trace duplicate candidate rows | 0 | `rescue_candidate_step_feature_degeneracy_report.md`; `final_results_for_article_tables.md` | Consistent. |
| Redesigned trace-level feature rows | 420 | `cct_redesigned_feature_inventory.md`; `final_results_for_article_tables.md` | Consistent. |
| Redesigned trace-level unique feature vectors | 6 | `cct_redesigned_feature_degeneracy_report.md`; `final_results_for_article_tables.md` | Consistent. |
| Redesigned trace-level duplicate feature vectors | 414 | `cct_redesigned_feature_degeneracy_report.md`; `final_results_for_article_tables.md` | Consistent with 420 - 6. |
| Strong-edge full-corpus traces | 420 | `cct_strong_edges_full_corpus_inventory.md` | Consistent with final rescue trace count. |
| Strong-edge total edges | 2,385 | `cct_strong_edges_full_corpus_inventory.md` | Consistent with Task 23 reports. |

## Final rescue accuracy crosscheck

| Method or decision item | Frozen value | Crosscheck status |
| --- | ---: | --- |
| `majority_step` accuracy | 25.00% | Strongest non-CCT baseline. |
| `always_s2` accuracy | 25.00% | Ties strongest trivial baseline. |
| `last_step` accuracy | 25.00% | Ties strongest trivial baseline. |
| `random_step_seeded` accuracy | 17.14% | Below strongest trivial baseline. |
| `flat_log_lexical_baseline` accuracy | 0.00% | Available flat-log baseline under current prediction view. |
| `non_cct_visible_heuristic_baseline` accuracy | 0.00% | Non-CCT visible heuristic reference. |
| Best CCT variant | `cct_candidate_step_structural_sum` | Same as final decision report. |
| Best CCT step accuracy | 0.00% | Below strongest baseline. |
| Best CCT top-2 containment | 25.00% | Diagnostic only, not sufficient for H1-R/H2-R support. |
| Most common best-CCT predicted step | `s1` for 420 traces | Confirms position collapse. |
| H1-R margin over strongest baseline | -0.250 | Below required +0.100. |
| H2-R margin over flat/non-CCT reference | 0.000 | Below required +0.100. |
| H1-R final status | Unsupported | Consistent with final hypothesis decision. |
| H2-R final status | Unsupported | Consistent with final hypothesis decision. |
| Rescue continuation | No | Return to Path B negative-evidence framing. |

## Manuscript-use rule

These numbers may be used to support diagnostic and negative-evidence statements. They must not be reframed as optimized performance evidence, robust superiority evidence, calibration evidence, external-validation evidence, or proof of formal causal identification.
