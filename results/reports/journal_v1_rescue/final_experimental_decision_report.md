# Final Experimental Decision Report After Rescue

## Scope

This report consolidates the final experimental state after the Task 30 minimal rescue evaluation. It is an article-evidence summary, not a new experiment. No new CCT variants, tuned weights, calibration, grid search, LOSO, ablation, statistical tests, corpus edits, gold-label edits, or scoring-config restoration were performed for this consolidation.

## Evidence inputs

- Task 18 diagnostic scoring outcome: H1/H2 were unsupported, and the frozen scoring configuration is not reproducible from the current checkout.
- Task 24A redesigned trace-level feature audit: 420 traces produced only 6 unique feature vectors and 414 duplicate feature vectors.
- Task 29 candidate-step dry run: 2,100 candidate-step rows were leakage-safe, but global feature duplication remained severe; within-trace duplicate rows were 0.
- Task 30 final fixed-formula rescue evaluation: deterministic CCT candidate-step variants were compared against pre-specified trivial, flat-log, and visible non-CCT baselines.

## Task 30 baseline vs CCT result

| Method family | Best method | Step accuracy | Top-2 containment | Interpretation |
| --- | --- | ---: | ---: | --- |
| Strongest non-CCT baseline | `majority_step` | 25.00% | 25.00% | Strongest reference for H1-R acceptance. |
| Other trivial baseline tie | `always_s2` / `last_step` | 25.00% | 25.00% | Confirms that positional shortcuts remain strong relative to CCT variants. |
| Random baseline | `random_step_seeded` | 17.14% | 17.14% | Seeded reference baseline. |
| Flat-log lexical baseline | `flat_log_lexical_baseline` | 0.00% | 0.00% | H2-R flat/non-CCT reference available under the prediction-view contract. |
| Non-CCT visible heuristic | `non_cct_visible_heuristic_baseline` | 0.00% | 0.00% | Non-CCT visible heuristic reference. |
| Best CCT rescue variant | `cct_candidate_step_structural_sum` | 0.00% | 25.00% | Did not exceed the strongest baseline and collapsed to s1. |

The omitted `flat_log_text_similarity_baseline` remains omitted because the current prediction view does not expose terminal outcome text; adding that baseline would require a new input contract rather than an implementation detail.

## CCT collapse finding

The best CCT rescue variant predicted `s1` for all 420 traces. This is a decisive failure mode: the fixed causal-flow feature formulas produced a position collapse rather than useful failure-step discrimination. Because the controlled corpus has no gold `s1` failures in the evaluated split, step accuracy for all CCT variants was 0.00%.

## Final hypothesis decision

- H1-R: unsupported. The best CCT variant trailed the strongest non-CCT baseline by 25.00 percentage points, rather than exceeding it by the pre-specified +10 percentage-point margin.
- H2-R: unsupported. CCT did not outperform the available flat-log/non-CCT reference under identical prediction-view constraints.
- H6-R: not tested. H6 remains open but unsupported; no H6 private evidence was used.

## Why the rescue path stops

The rescue path stops because the final pre-specified, fixed-formula evaluation did not produce preliminary support for H1-R or H2-R. Continuing with tuning, calibration, grid search, ablation, or new variants would violate the purpose of Task 30 as a final minimal decision point and would risk converting negative diagnostic evidence into open-ended optimization.

## Path B article claim boundary

Path B remains the scientific backbone. The article may claim that the project provides a protocol-first full-trace benchmark, diagnostic representation, leakage/shortcut/provenance governance, and negative evidence showing that naive structural scoring and the current causal-flow featureization are insufficient. The article must not claim CCT improves automatic attribution, outperforms baselines, is robust under perturbation, is calibration-ready, validates H1/H2, or provides paper-ready performance superiority evidence.

## Article-use decision

The Task 30 numbers are suitable for article use only as diagnostic negative evidence about the current representation. They must be framed as evidence that the current CCT causal-flow rescue features failed to support failure-step attribution, not as a performance-oriented benchmark result or an optimized method comparison.
