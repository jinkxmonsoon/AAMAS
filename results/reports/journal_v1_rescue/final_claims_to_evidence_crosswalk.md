# Final Claims-to-Evidence Crosswalk

## Scope

This crosswalk maps manuscript claims to the frozen evidence package. It does not revise hypotheses, add experimental claims, run new analyses, or authorize performance-superiority language.

## Allowed claims and required evidence

| Allowed manuscript claim | Required wording constraint | Primary evidence artifacts |
| --- | --- | --- |
| CCT provides a structured full-trace representation for auditing collaborative multi-agent failures. | Use "auditing" or "diagnostic representation"; avoid "improves attribution." | `docs/09_journal_v1_reconstruction_protocol.md`; `docs/13_full_trace_schema_migration_plan.md`; `docs/03_cct_formal_schema.md`; redesigned graph reports. |
| The project identifies and controls leakage, shortcut, provenance, and representation-degeneracy risks. | State controls as protocol/repository controls, not as external validation. | `docs/paper_claims_matrix_journal_v1.md`; leakage audit reports; `cct_scoring_config_provenance_recovery_report.md`; degeneracy reports. |
| Naive structural scoring and current causal-flow featureization are insufficient in the controlled trace bank. | Tie to the current controlled corpus and feature implementation; do not universalize. | `final_experimental_decision_report.md`; `final_negative_findings_summary.md`; `final_numbers_crosscheck.md`. |
| The rescue evaluation closed H1-R/H2-R as unsupported under current features. | Present as a fixed-formula diagnostic rescue result, not as a broad impossibility theorem. | `final_hypothesis_status_table.md`; `final_rescue_hypothesis_decision.md`; `final_results_for_article_tables.md`. |
| Full-trace prediction-view constraints support leakage-safe audits. | Do not equate leakage safety with attribution performance. | `rescue_candidate_step_feature_leakage_audit.md`; `cct_redesigned_feature_leakage_audit.md`; descriptor and strong-edge leakage reports. |
| The work provides a reproducible foundation for future failure-attribution research. | Exclude Task 18 scoring reproduction unless exact frozen config provenance is restored. | Artifact manifests; `scripts/validate_repo.py`; `PROTOCOL_LOCK.md`; compact sample artifacts. |

## Negative evidence crosswalk

| Negative finding | Evidence artifacts | Allowed article use |
| --- | --- | --- |
| Task 18 H1/H2 unsupported and not reproducible from current checkout. | `cct_task18_reproducibility_boundary.md`; final hypothesis status table. | Motivate protocol-first pivot and provenance governance. |
| Redesigned trace-level features remained degenerate. | `cct_redesigned_feature_degeneracy_report.md`; final numbers crosscheck. | Show current graph redesign is insufficient for scoring readiness. |
| Candidate-step features were globally degenerate despite within-trace uniqueness. | `rescue_candidate_step_feature_degeneracy_report.md`; final numbers crosscheck. | Explain why the rescue was high-risk and diagnostic. |
| Final CCT rescue collapsed to `s1` and underperformed baseline. | `final_rescue_error_analysis.md`; `final_experimental_decision_report.md`; final numbers crosscheck. | Support H1-R/H2-R unsupported and rescue-stop decision. |
| Current causal-flow features do not validate H1/H2/H6. | `final_hypothesis_status_table.md`; `final_do_not_claim_list.md`. | Maintain claim boundary. |

## Writer instruction

Every results paragraph should be traceable to one of the artifacts listed above and should preserve the diagnostic-negative framing. If a sentence requires a new comparison, metric, tuned variant, robustness claim, or external generalization claim, it is outside this frozen evidence package.
