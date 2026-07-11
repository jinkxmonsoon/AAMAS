# Final Negative Findings Summary

## Consolidated negative findings

1. **Initial CCT scoring did not support H1/H2.** Task 18 produced a negative diagnostic outcome, and the frozen scoring configuration is not reproducible from the current checkout.
2. **Descriptor augmentation did not create a scoring-ready representation.** Descriptor audits remained representation-only and did not authorize scoring, calibration, or gold/H6 comparison.
3. **Causal-flow edge audits were leakage-safe but insufficient as a scoring foundation.** The strongest edge types were useful for representation diagnostics, but readiness gates continued to block scoring.
4. **Redesigned trace-level graph features remained highly degenerate.** Task 24A found only 6 unique feature vectors across 420 traces, with 414 duplicates.
5. **Candidate-step features were distinguishable within trace but globally degenerate.** Task 29 produced 2,100 candidate-step rows with leakage PASS, but only 17 unique global vectors and a 99.19% duplicate-vector rate.
6. **The final rescue evaluation collapsed to a position shortcut.** Task 30 best CCT variant predicted `s1` for all 420 traces, producing 0.00% step accuracy while `majority_step`, `always_s2`, and `last_step` reached 25.00%.
7. **H1-R/H2-R are unsupported.** The best CCT variant did not clear the pre-specified +10 percentage-point margin over the strongest baseline and did not provide demonstrated signal beyond the available flat-log/non-CCT reference.

## Interpretation for the article

These findings should be framed as methodological evidence: full-trace protocol governance and leakage-safe representation audits are necessary because naive structural scoring and the current causal-flow featureization can fail badly. They should not be framed as evidence that CCT improves automatic failure attribution.

## Rescue stop rationale

The rescue path stops because the final fixed-formula evaluation was designed to decide whether there was any preliminary support under the current candidate-step features. Since the best CCT variant underperformed trivial baselines and collapsed to `s1`, further optimization would be a new protocol rather than a continuation of the authorized rescue.
