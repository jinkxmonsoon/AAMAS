# Contribution Block v1

## Scope

This contribution block is writing-only and claim-bounded. It does not authorize code changes, new experiments, scoring, ranking, calibration, ablation, statistical testing, corpus/gold-label changes, scoring-config restoration, or performance tables.

## Four contributions

1. **A protocol-first full-trace benchmark structure for collaborative failure attribution.** We define a Journal-v1 trace protocol that represents complete multi-agent interactions while separating prediction-view-safe fields from private labels, provenance, and diagnostic-only metadata.

2. **Leakage, shortcut, provenance, and artifact-governance controls.** We document the governance checks needed before attribution claims, including failure-centered schema correction, prediction-view hygiene, shortcut/baseline sanity checks, scoring-config provenance boundaries, generated-artifact policies, compact samples, and manifests.

3. **A diagnostic CCT representation audit.** We use CCT-style graphs, descriptors, and causal-flow edge prototypes as audit artifacts to examine whether the current representation contains usable structural diversity without relying on private labels or scoring.

4. **Negative findings that bound future method claims.** We consolidate evidence that frozen uncalibrated CCT scoring, descriptor augmentation, and simple causal-flow redesigned features remain insufficient under the current controlled trace bank, motivating future representation work before calibration or performance claims.

## Contribution paragraph for introduction

Our contribution is a protocol-first benchmark and diagnostic representation audit for multi-agent failure attribution. First, we define a full-trace Journal-v1 schema that separates visible prediction fields from private labels and provenance. Second, we provide leakage, shortcut, provenance, and artifact-governance controls that make failure-attribution artifacts reviewable and reproducible. Third, we use CCT-style graphs, descriptors, and causal-flow edges as diagnostic representations rather than as validated scoring mechanisms. Fourth, we report negative representation findings showing that naive structural scoring and simple causal-flow feature counts are insufficient in the current controlled trace bank. These contributions establish a bounded foundation for future failure-attribution research without claiming automatic attribution improvement, baseline outperformance, robustness, calibration readiness, or H1/H2 validation.

## Explicit forbidden-claim check

- Does the contribution block claim CCT improves attribution? **No.**
- Does it claim CCT outperforms baselines? **No.**
- Does it claim robust performance under perturbations? **No.**
- Does it claim scoring is ready for calibration? **No.**
- Does it claim H1/H2 are validated? **No.**
- Does it claim production readiness? **No.**
- Does it present performance tables or paper-ready scoring evidence? **No.**
