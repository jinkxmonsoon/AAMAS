# Journal-v1 Paper Claims Matrix

## Scope

This matrix is a claim-governance document for the Path B article pivot. It does not authorize scoring, ranking, calibration, statistical testing, corpus/gold-label changes, or paper-ready performance tables.

## Allowed claims

| Claim | Where it may appear | Required qualifier | Supporting evidence |
| --- | --- | --- | --- |
| CCT provides a structured full-trace representation for auditing collaborative multi-agent failures. | Title, abstract, introduction, methods, conclusion | Use "auditing" or "diagnostic representation," not "automatic improvement." | Full-trace schema protocol, schema migration, redesigned graph artifacts. |
| The work identifies and controls failure-centered schema leakage, shortcut baselines, artifact provenance, and representation degeneracy risks. | Abstract, methods, results, discussion | Controls are repository/protocol controls, not external validation. | Leakage audits, shortcut reports, artifact manifests, scoring-config adjudication, degeneracy reports. |
| Full-trace representation is necessary for fair failure-attribution analysis. | Introduction, methods, discussion | Phrase as a protocol requirement motivated by audit risks. | Reconstruction protocol, full-trace corpus plan, schema migration plan. |
| The benchmark/protocol exposes why naive structural scoring is insufficient under the current representation. | Results, discussion, conclusion | Tie to current evidence and representation, not universal impossibility. | Task 18/18A diagnostics, Task 18B feature taxonomy, Task 24A feature degeneracy. |
| Descriptor and causal-flow representation audits can be run under prediction-view-safe constraints. | Methods, results, reproducibility appendix | State that these remain not ready for scoring. | Descriptor manifests/reports, causal-flow edge spec/audits, leakage PASS reports. |
| The project provides a reproducible foundation for future failure-attribution research. | Abstract, conclusion, reproducibility | Exclude Task 18 scoring reproduction unless exact config is recovered. | Artifact manifests, validation scripts, compact samples, protocol lock. |
| Negative findings are methodological evidence about representation and protocol risks. | Results, discussion | Negative findings are not failed superiority claims. | Task 25 synthesis and journal viability assessment. |

## Forbidden claims

| Forbidden claim | Reason |
| --- | --- |
| CCT improves automatic failure attribution. | H1/H2 remain unsupported and no scoring-ready representation exists. |
| CCT outperforms baselines. | Baseline superiority is not supported and Task 18 is not reproducible from the active checkout. |
| CCT is robust under perturbations. | Robustness has not been validated as a performance claim. |
| CCT scoring is ready for calibration. | H3 is blocked and feature validity remains insufficient. |
| A new scoring protocol v2 is justified now. | Task 24A found 6 unique feature vectors across 420 rows and 414 duplicates. |
| Descriptor-augmented features improve scoring. | Descriptor augmentation was audit-only and readiness stayed no. |
| The causal-flow redesign validates H1/H2. | Causal-flow work was representation-only and did not compare to gold labels. |
| Current scoring results are paper-ready performance evidence. | Frozen scoring config provenance is unresolved. |
| Current CCT features explain H6 outcomes. | H6 remains open but unsupported by scoring evidence. |
| The work establishes formal causal identification. | "Causal" is operational evidence-flow terminology only. |

## Claims requiring future evidence

- Automatic failure-attribution improvement over baselines.
- Robustness under perturbations.
- Valid calibrated scoring protocol.
- External-corpus validity.
- Production readiness.
- Formal causal identification.
