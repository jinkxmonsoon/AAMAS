# CCT Claim Boundary Update

## Updated unsupported claims

- H1 is unsupported under current frozen uncalibrated scoring/features.
- H2 is unsupported under current frozen uncalibrated scoring/features.
- H3 remains blocked because calibration before feature validity is premature.
- H4 remains blocked.
- H6 remains open but unsupported by scoring evidence.
- Current descriptors are not ready for scoring.
- No CCT performance-superiority claim is currently allowed.
- No claim of generalization, robustness, calibrated performance, or paper-ready empirical advantage is currently allowed.

## Allowed claims under current evidence

Current claims must be limited to:

- methodology and protocol governance;
- benchmark construction and auditability;
- leakage correction and prediction-view hygiene;
- full-trace representation design;
- diagnostic findings about current scoring/feature failure modes;
- artifact reproducibility and reviewability policy;
- conservative readiness gates that block premature scoring/calibration.

## Forbidden claim patterns

The following claim forms remain forbidden unless a future explicitly authorized task produces valid evidence:

- CCT outperforms diagnostic baselines.
- CCT is robust under perturbation.
- CCT scoring is calibrated or ready for calibration.
- Descriptor-augmented features improve scoring.
- Current CCT features explain H6 outcomes.
- Current results are paper-ready empirical evidence.

## Boundary rationale

The negative diagnostic evidence points to a feature/representation validity problem rather than a simple scoring-weight problem. The repository should therefore avoid superiority language and preserve the protocol-first claim boundary until richer causal-flow feature extraction is specified, audited, and separately authorized for any future scoring.
