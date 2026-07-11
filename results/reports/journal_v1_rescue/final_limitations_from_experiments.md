# Final Limitations From Experiments

## Experimental limitations

- The trace bank is controlled and synthetic/constructed; results do not establish external validity.
- The frozen Task 18 scoring configuration remains absent from the current checkout, so the original scoring run is not reproducible here.
- Task 24A redesigned trace-level features were highly degenerate, with only 6 unique feature vectors across 420 traces.
- Task 29 candidate-step features were globally degenerate, with only 17 unique feature vectors and a 99.19% duplicate-vector rate across 2,100 rows.
- Task 30 CCT variants collapsed to `s1`, indicating that current fixed causal-flow formulas can act as a position shortcut rather than a diagnostic signal.
- The final rescue evaluation was deliberately minimal and deterministic; it did not tune weights, calibrate, grid search, perform LOSO, ablate, or run statistical tests.
- The available flat-log lexical baseline was limited by the prediction-view contract; `flat_log_text_similarity_baseline` was omitted because adding terminal outcome text would require a new input contract.
- H1/H2 and H1-R/H2-R are unsupported under the current evidence. H3/H4 remain blocked, and H6/H6-R remain open but unsupported.
- Leakage controls passed for the relevant artifacts, but leakage safety is not the same as attribution performance.
- The use of "causal-flow" is operational evidence-flow terminology; the experiments do not establish formal causal identification.

## Claim limitations

The article must not claim automatic failure-attribution improvement, baseline outperformance, perturbation robustness, calibration readiness, validated H1/H2, production readiness, external generalization, or formal causal identification.

## Constructive framing

The appropriate framing is that the project provides a protocol-first benchmark and diagnostic representation audit stack that exposes leakage, shortcut, provenance, and feature-degeneracy risks. The negative findings are valuable because they show that naive structural scoring and the current causal-flow rescue features are insufficient in the controlled trace bank.
