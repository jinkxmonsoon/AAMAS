# Final Artifact Index for Manuscript Use

## Scope

This index freezes the final manuscript evidence package after Task 31. It verifies presence and manuscript role of final reports, raw outputs, manifests, and claim-boundary artifacts. It does not introduce new experiments, scoring, variants, calibration, ablation, statistical testing, corpus/gold-label changes, or new experimental claims.

## Frozen package status

- Package status: frozen for manuscript drafting under Path B.
- Current scientific framing: protocol-first benchmark, diagnostic representation, leakage/shortcut/provenance governance, and negative findings.
- Scoring status: blocked; `configs/cct_scoring.yaml` remains absent from the current checkout.
- Rescue status: stopped; H1-R and H2-R remain unsupported under the current candidate-step feature representation.

## Core final evidence reports

| Artifact | Role in manuscript package | Freeze status |
| --- | --- | --- |
| `results/reports/journal_v1_rescue/final_experimental_decision_report.md` | Final experimental decision and rescue-stop rationale. | Present / frozen. |
| `results/reports/journal_v1_rescue/final_hypothesis_status_table.md` | Final hypothesis status and article framing. | Present / frozen. |
| `results/reports/journal_v1_rescue/final_negative_findings_summary.md` | Consolidated negative findings narrative. | Present / frozen. |
| `results/reports/journal_v1_rescue/final_results_for_article_tables.md` | Article-safe diagnostic numbers and caption caveats. | Present / frozen. |
| `results/reports/journal_v1_rescue/final_limitations_from_experiments.md` | Experimental limitations and forbidden performance interpretations. | Present / frozen. |

## Raw and generated evidence artifacts

| Artifact | Role in manuscript package | Freeze status |
| --- | --- | --- |
| `results/raw/journal_v1_rescue/final_rescue_predictions.json` | Frozen final rescue predictions for auditability. | Present / frozen. |
| `results/raw/journal_v1_rescue/rescue_candidate_step_features.json` | Candidate-step feature-readiness dry-run artifact. | Present / frozen. |
| `results/raw/journal_v1_full_trace_cct_redesigned/cct_redesigned_features.json` | Redesigned trace-level feature audit artifact. | Present / frozen. |
| `results/raw/journal_v1_full_trace_cct/sample_cct_strong_edges_full_corpus.json` | Compact strong-edge full-corpus audit sample. | Present / frozen. |
| `results/raw/journal_v1_full_trace_cct/sample_cct_descriptor_augmented_features.json` | Compact descriptor-augmented feature sample. | Present / frozen. |
| `data/interim/journal_v1_full_trace_cct_redesigned/cct_redesigned_graph_inventory.json` | Redesigned graph inventory. | Present / frozen. |
| `data/interim/journal_v1_full_trace_cct_redesigned/sample_cct_redesigned_graphs.jsonl` | Compact redesigned graph sample. | Present / frozen. |

## Manifests and artifact-governance documents

| Artifact | Role in manuscript package | Freeze status |
| --- | --- | --- |
| `docs/artifact_manifests/cct_redesigned_graphs_manifest.md` | Generated-artifact policy for redesigned graphs. | Present / frozen. |
| `docs/artifact_manifests/cct_strong_edges_full_corpus_manifest.md` | Generated-artifact policy for strong-edge audit outputs. | Present / frozen. |
| `docs/artifact_manifests/journal_v1_descriptor_augmented_features_manifest.md` | Generated-artifact policy for descriptor-augmented features. | Present / frozen. |

## Claim-boundary and manuscript-framing artifacts

| Artifact | Role in manuscript package | Freeze status |
| --- | --- | --- |
| `docs/paper_claims_matrix_journal_v1.md` | Allowed/forbidden claim matrix. | Present / frozen. |
| `docs/paper_evidence_map_journal_v1.md` | Evidence-to-claim map for Path B manuscript. | Present / frozen. |
| `docs/paper_results_to_report_journal_v1.md` | Main-text versus appendix result placement. | Present / frozen. |
| `docs/paper_limitations_and_threats_journal_v1.md` | Manuscript limitations and threats. | Present / frozen. |
| `docs/paper_outline_journal_v1.md` | Path B paper structure. | Present / frozen. |
| `docs/paper_target_journal_positioning_journal_v1.md` | Journal positioning and overclaiming risks. | Present / frozen. |

## Governance artifacts

| Artifact | Role in manuscript package | Freeze status |
| --- | --- | --- |
| `PROTOCOL_LOCK.md` | Protocol lock and non-action boundaries. | Present / updated for freeze. |
| `EXPERIMENT_CHANGELOG.md` | Chronological change log. | Present / updated for freeze. |
| `RESEARCH_LOG.md` | Reasoning, caveats, and interpretation log. | Present / updated for freeze. |

## Freeze note for writers

Writers should cite these artifacts as the stable evidence package. If manuscript drafting reveals a need for new numbers, new baselines, new variants, new calibration, new statistical tests, or revised hypotheses, that request must be treated as a new protocol task rather than an edit to this frozen package.
