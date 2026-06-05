# Journal-v1 Results-to-Report Plan

## Scope

This document organizes existing evidence for a Path B article. It does not create new results, run experiments, score/rank examples, compare to gold/H6 labels, calibrate, ablate, run statistical tests, or produce paper-ready performance tables.

## Main-text candidates

1. **Corpus construction and full-trace schema.**
   - Report the Journal-v1 full-trace design, scenario/perturbation structure, prediction-view separation, and migration away from failure-centered leakage risks.
   - Use compact schema diagrams or prose summaries, not performance tables.

2. **Leakage, shortcut, and provenance controls.**
   - Report leakage PASS/blocked statuses, private-label separation, shortcut-baseline sanity checks, artifact manifests, and generated-artifact policies.
   - Include the frozen scoring-config provenance blocker as a reproducibility boundary.

3. **Failure-centered schema correction.**
   - Explain why full-trace representation is required for fair attribution and why private labels/provenance cannot be used as prediction inputs.

4. **Negative diagnostic scoring result.**
   - Report Task 18 only as diagnostic evidence with H1/H2 unsupported and a reproducibility boundary.
   - Avoid paper-ready performance tables, superiority claims, or new scoring outputs.

5. **Representation diagnostics from descriptors and causal-flow edges.**
   - Summarize descriptor augmentation as leakage-safe but not scoring-ready.
   - Summarize causal-flow edge audits as prediction-view-safe but still template-sensitive/representation-only.

6. **Task 24A redesigned feature degeneracy.**
   - Report the key degeneracy facts: 420 feature rows, 13 features, 6 unique feature vectors, 414 duplicates, constant features, leakage PASS, scoring readiness no.
   - Use this as the central negative finding supporting the Path B pivot.

7. **Task 25 claim boundary.**
   - Present the final claim boundary and scientific backbone decision as part of discussion, not as an empirical result table.

## Appendix candidates

- Detailed task history from Tasks 18–25.
- Descriptor-augmented artifact inventory, leakage audit, variance report, shortcut risk report, readiness gate, and manifest.
- Causal-flow edge specification, sample prototype reports, full-corpus strong-edge audit reports, and template sensitivity reports.
- Redesigned graph artifacts, diversity/degeneracy reports, feature audit reports, and readiness gates.
- Config provenance recovery/adjudication reports and Task 18 reproducibility boundary.
- Full validation outputs and command list.
- Artifact manifests and generated-artifact policy.

## Explicit exclusions from results section

- No scoring rankings.
- No calibrated metrics.
- No grid-search/LOSO/ablation tables.
- No statistical significance tests.
- No gold/H6 comparisons for causal-flow edges or redesigned features.
- No baseline outperformance claims.
