# Journal-v1 Candidate Contribution Statements

## Scope

These candidate contributions implement the Path B writing frame only. They are not performance claims and do not authorize new experiments, scoring, calibration, statistical tests, corpus changes, or paper-ready result tables.

## Candidate contribution set

1. **Protocol-first benchmark construction.** We define a Journal-v1 full-trace benchmark protocol for collaborative multi-agent failure attribution, separating visible prediction fields from private labels, provenance, and diagnostic-only metadata.

2. **Full-trace schema and leakage governance.** We document a migration from failure-centered records to full-trace prediction views, including leakage, shortcut, provenance, and artifact-reviewability gates that constrain what a future attribution method may observe.

3. **Diagnostic CCT representation audit.** We use CCT-style graph and feature artifacts as a diagnostic lens to show that proxy-heavy structural features, descriptor augmentation, and simple causal-flow edge counts remain insufficiently diverse under the current controlled trace bank.

4. **Negative findings as methodological evidence.** We consolidate negative CCT scoring and representation findings to show that naive structural scoring is not scientifically ready for calibration or superiority claims under the current representation.

5. **Reproducible artifact governance for future research.** We provide compact tracked samples, generated-artifact policies, manifests, validation scripts, and readiness gates that make future failure-attribution research auditable without committing unreviewable full artifacts.

## Short contribution paragraph for introduction

This paper contributes a protocol-first benchmark and diagnostic representation audit for multi-agent failure attribution. Rather than claiming performance superiority, it defines full-trace prediction-view hygiene, leakage and shortcut controls, artifact provenance requirements, and representation-degeneracy gates. Across CCT scoring diagnostics, descriptor augmentation, causal-flow edge audits, and redesigned graph-feature extraction, the evidence shows that naive structural scoring and simple causal-flow feature counts are insufficient in the current controlled trace bank. The resulting artifact is a reproducible foundation for future attribution methods, with explicit claim boundaries and readiness gates.

## Claims excluded from contributions

The contribution list must not include automatic attribution improvement, baseline outperformance, robustness, calibration readiness, validated H1/H2, production readiness, or formal causal identification.
