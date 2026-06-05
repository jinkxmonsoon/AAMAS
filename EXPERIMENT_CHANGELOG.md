# EXPERIMENT CHANGELOG

All protocol, evaluation, and experiment-design changes must be recorded here.

## Template
- Date (UTC):
- Author:
- Change type:
- Affected artifact(s):
- Justification:
- Authorization reference:
- Expected validity impact:

## Entries
- 2026-05-13 (UTC) — Repository initialized with protocol-first placeholders; no experiment logic added.

- Date (UTC): 2026-05-13
- Author: Codex TL
- Change type: Protocol clarity update (non-empirical)
- Affected artifact(s): scenario group enum in docs/configs/contracts
- Justification: Renamed `optional_extra_complex_collaboration` to `complex_collaboration` to remove optionality ambiguity while preserving fixed 7-group count.
- Authorization reference: Task 6A instruction
- Expected validity impact: Indirect support for H1–H6 scenario balance integrity; no data/results affected.

- Date (UTC): 2026-05-13
- Author: Codex TL
- Change type: Readiness-gate review
- Affected artifact(s): readiness documentation and gate script
- Justification: Pilot lessons reviewed; no additional protocol/config structural changes required beyond explicit readiness gate formalization.
- Authorization reference: Task 9 instruction
- Expected validity impact: Improves gating discipline before main-corpus generation; no empirical results affected.


- Date (UTC): 2026-05-13
- Author: Codex TL
- Change type: Main controlled corpus generation and audit (non-metric, non-claim)
- Affected artifact(s): data/processed/journal_v1/*, results/reports/journal_v1/*, scripts/build_main_corpus.py, scripts/audit_main_corpus.py, tests/test_main_corpus_builder.py, tests/test_main_corpus_audit.py
- Justification: Execute Task 10 under frozen protocol to generate independent Journal-v1 main controlled corpus and verify structural/semantic governance gates.
- Authorization reference: Task 10 instruction
- Expected validity impact: Enables downstream hypothesis-testing phases without introducing empirical performance claims in this task.


- Date (UTC): 2026-05-13
- Author: Codex TL
- Change type: Corpus freeze + semantic spot-check governance
- Affected artifact(s): docs/artifact_manifests/journal_v1_main_corpus_manifest.md, results/reports/journal_v1/main_semantic_spotcheck_report.md, results/reports/journal_v1/main_label_distribution_report.md, results/reports/journal_v1/main_generation_risk_report.md, scripts/make_journal_v1_manifest.py, scripts/audit_main_corpus_semantics.py
- Justification: Freeze Task 10 corpus artifact and document semantic diversity/bias risks before any evaluation implementation.
- Authorization reference: Task 10A instruction
- Expected validity impact: Strengthens pre-evaluation artifact immutability and exposes residual semantic templating risk.

- Date (UTC): 2026-05-13
- Author: Codex TL
- Change type: Evaluation block notice
- Affected artifact(s): results/reports/journal_v1/main_semantic_spotcheck_report.md, PROTOCOL_LOCK.md
- Justification: Spot-check produced revise recommendations; evaluation remains blocked until explicit correction task approval.
- Authorization reference: Task 10A instruction (revise/reject handling)
- Expected validity impact: Prevents premature evaluation on potentially biased corpus samples.


- Date (UTC): 2026-05-13
- Author: Codex TL
- Change type: Main-corpus templating-risk correction and re-freeze
- Affected artifact(s): scripts/build_main_corpus.py, data/processed/journal_v1/*.jsonl, results/reports/journal_v1/*, docs/artifact_manifests/journal_v1_main_corpus_manifest.md
- Justification: Resolve Task 10A semantic blocker by diversifying generation patterns while preserving frozen protocol counts/semantics.
- Authorization reference: Task 10B instruction
- Expected validity impact: Reduces construction-bias risk and clears pre-evaluation templating blocker without introducing performance claims.


- Date (UTC): 2026-05-13
- Author: Codex TL
- Change type: H6 semantic consistency correction and re-audit
- Affected artifact(s): scripts/audit_h6_semantic_consistency.py, scripts/build_main_corpus.py, data/processed/journal_v1/*.jsonl, results/reports/journal_v1/main_h6_* reports, docs/artifact_manifests/journal_v1_main_corpus_manifest.md
- Justification: Resolve detected contradictions between H6 labels and evidence fields before any evaluation-stage implementation.
- Authorization reference: Task 10D instruction
- Expected validity impact: Removes label-evidence semantic contradictions and strengthens H6 proxy validity for downstream evaluation.

- Date (UTC): 2026-06-04
- Author: Codex TL
- Change type: Pre-evaluation label-position and trivial-shortcut risk gate
- Affected artifact(s): scripts/audit_label_position_bias.py, results/reports/journal_v1/main_label_position_bias_report.md, results/reports/journal_v1/main_trivial_baseline_risk_report.md, results/reports/journal_v1/main_label_position_bias_correction_plan.md, results/reports/journal_v1/main_semantic_spotcheck_report.md, PROTOCOL_LOCK.md, RESEARCH_LOG.md, docs/11_journal_v1_corpus_plan_and_label_rubric.md
- Justification: Audit Journal-v1 main corpus for positional shortcuts and trivial corpus-risk diagnostics before any evaluation-stage implementation.
- Authorization reference: Task 10E instruction
- Expected validity impact: Blocks evaluation until label-position shortcut risk is corrected or explicitly justified; protects future H1–H4/H6 tests from trivial step-position solutions.

- Date (UTC): 2026-06-04
- Author: Codex TL
- Change type: Main-corpus gold-failure-step positional-bias correction and re-freeze
- Affected artifact(s): scripts/build_main_corpus.py, data/processed/journal_v1/*.jsonl, results/reports/journal_v1/*, docs/artifact_manifests/journal_v1_main_corpus_manifest.md, PROTOCOL_LOCK.md, RESEARCH_LOG.md, docs/11_journal_v1_corpus_plan_and_label_rubric.md
- Justification: Resolve Task 10E blocking positional shortcut where all traces had `gold_failure_step=s2`, while preserving protocol counts and avoiding any evaluation-stage implementation.
- Authorization reference: Task 10F instruction
- Expected validity impact: Restores viability of future structural step-attribution evaluation by reducing majority/always-s2 shortcut risk to 25.00%; no performance claims introduced.

- Date (UTC): 2026-06-04
- Author: Codex TL
- Change type: Manual semantic sanity gate for corrected failure-step labels
- Affected artifact(s): results/reports/journal_v1/main_failure_step_semantic_sanity_check.md, docs/artifact_manifests/journal_v1_main_corpus_manifest.md, PROTOCOL_LOCK.md, RESEARCH_LOG.md, scripts/validate_repo.py
- Justification: Verify that Task 10F's non-s2 failure-step labels are semantically grounded before any evaluation-stage implementation.
- Authorization reference: Task 10G instruction
- Expected validity impact: Adds qualitative assurance that corrected step labels are not merely positionally rebalanced; no performance claims introduced.

- Date (UTC): 2026-06-04
- Author: Codex TL
- Change type: Final pre-evaluation corpus gate consolidation
- Affected artifact(s): results/reports/journal_v1/final_pre_evaluation_gate_report.md, docs/artifact_manifests/journal_v1_main_corpus_manifest.md, PROTOCOL_LOCK.md, RESEARCH_LOG.md, scripts/validate_repo.py
- Justification: Consolidate corrected Journal-v1 corpus state after Tasks 10F/10G and verify no remaining obvious shortcut blocks the next approved evaluation-preparation task.
- Authorization reference: Task 10H instruction
- Expected validity impact: Clarifies PR #13 supersedes PR #12 and clears corpus-level shortcut gates while preserving prohibition on CCT scoring, calibration, refinement, empirical evaluation, and paper result tables.

- 2026-06-04 (UTC):
  - Task 11 implemented diagnostic metric interfaces in `src/cctdiag/metrics/` and allowed trivial-baseline sanity checks in `src/cctdiag/baselines/trivial.py`.
  - Added `scripts/run_trivial_baseline_sanity.py` to write diagnostic-only outputs to `results/raw/journal_v1/trivial_baseline_sanity.json` and `results/reports/journal_v1/trivial_baseline_sanity_report.md`.
  - Added unit tests for attribution metrics, H6 `NA` handling, macro grouping, trivial baseline predictions, seeded random baselines, and shortcut-risk interpretation.
  - Protocol impact: metric interfaces and baseline definitions were added under the explicit Task 11 authorization; corpus JSONL files, gold labels, perturbation definitions, CCT scoring, calibration, refinement variants, ablations, and paper-ready result tables were not modified or implemented.

- 2026-06-04 (UTC):
  - Task 12 implemented deterministic flat-log and spectrum-inspired non-CCT diagnostic baselines in `src/cctdiag/baselines/flat_log.py` and `src/cctdiag/baselines/spectrum.py`.
  - Added `scripts/run_non_cct_baseline_diagnostics.py` to write diagnostic-only outputs to `results/raw/journal_v1/non_cct_baseline_diagnostics.json` and `results/reports/journal_v1/non_cct_baseline_diagnostics_report.md`.
  - Added unit tests for flat-log and spectrum-inspired baseline determinism.
  - Protocol impact: baseline definitions and diagnostic threshold reporting were added under explicit Task 12 authorization; corpus JSONL files, gold labels, perturbation definitions, CCT modules, calibration, refinement variants, ablations, and paper-ready result tables were not modified or implemented.

- 2026-06-04 (UTC):
  - Task 12A audited target leakage in non-CCT diagnostics and added `src/cctdiag/io/views.py` for sanitized prediction/private label views.
  - Updated flat-log and spectrum-inspired baselines plus `scripts/run_non_cct_baseline_diagnostics.py` so non-CCT diagnostics operate on prediction views only and reject raw records exposing forbidden fields.
  - Added leakage diagnosis, evaluation input contract, and correction-plan reports under `results/reports/journal_v1/`; regenerated `results/raw/journal_v1/non_cct_baseline_diagnostics.json` and the non-CCT diagnostic report.
  - Protocol impact: direct target-equivalent input leakage was corrected, but evaluation remains blocked because the corpus lacks full ordered multi-step trace representation; corpus JSONL files, gold labels, perturbation definitions, CCT modules, calibration, refinement variants, ablations, and paper-ready result tables were not modified or implemented.

- 2026-06-04 (UTC):
  - Task 12B froze the full ordered trace schema migration plan in `docs/13_full_trace_schema_migration_plan.md` and added the blocker report `results/reports/journal_v1/full_trace_schema_blocker_report.md`.
  - Updated operational contracts, corpus/rubric notes, protocol/corpus/label configs, protocol lock, and research log to mark the current 420-record corpus as failure-centered and not evaluation-ready.
  - Protocol impact: all evaluation, CCT graph construction/scoring, calibration, refinement, ablations, and paper-ready result tables remain blocked until a future approved full-trace schema migration and audit; no corpus JSONL files, gold labels, or perturbation definitions were modified.

- 2026-06-04 (UTC):
  - Task 13 implemented full ordered trace schema contracts, validators, prediction-view helpers, validation scripts, and non-experimental fixtures.
  - Added tests for valid/invalid full-trace fixtures and full-trace prediction-view privacy/candidate preservation.
  - Protocol impact: validator infrastructure clarifies the frozen full-trace schema but does not regenerate corpus files, change gold labels, modify perturbation definitions, implement CCT scoring, calibration, refinement, ablations, or produce paper-ready result tables.

- 2026-06-04 (UTC):
  - Task 14 built and audited a non-final 14-trace Journal-v1 full-trace pilot corpus under `data/interim/journal_v1_full_trace_pilot/`.
  - Added `scripts/build_full_trace_pilot_corpus.py`, `scripts/audit_full_trace_pilot_corpus.py`, pilot reports, and tests for pilot builder/audit behavior.
  - Protocol impact: this pilot validates full-trace schema/prediction-view infrastructure only; the old failure-centered corpus remains blocked, the full 420-trace corpus was not generated, and no CCT scoring, calibration, refinement, ablation, or paper-ready result table was produced.

- 2026-06-04 (UTC):
  - Task 14A added `scripts/run_full_trace_pilot_baseline_sanity.py` and generated full-trace pilot shortcut-baseline, semantic-diversity, and readiness-gate reports.
  - The full-trace pilot readiness gate passed for the 14-trace non-final pilot; this authorizes only a future explicitly approved full-trace main-corpus builder task.
  - Protocol impact: the old failure-centered corpus remains blocked, the full 420-trace corpus was not generated, and no CCT scoring, calibration, refinement, ablation, or paper-ready result table was produced.

## Task 14B — Audit full-trace pilot diagnostic sufficiency

- Added diagnostic sufficiency, candidate plausibility, and revision recommendation reports for the non-final Journal-v1 full-trace pilot.
- Audited all 7 clean traces and all 7 perturbed traces for whether gold failure steps are inferable from sanitized prediction-view evidence, whether non-gold steps remain plausible, and whether perturbations preserve label semantics without adding shortcuts.
- Found a protocol blocker for scaling: the pilot avoids obvious shortcut baselines but is too semantically flattened; all clean traces require revision because the controlled gold step is not supported by distinctive visible evidence.
- Updated readiness to `FULL_TRACE_PILOT_DIAGNOSTICALLY_READY = no` and `FULL_TRACE_MAIN_CORPUS_GENERATION_ALLOWED = no`.
- No full 420-trace corpus generation, CCT scoring, calibration, refinement, ablation, or paper-ready result table was produced.

## Task 14C — Revise full-trace pilot for diagnostic sufficiency

- Revised `scripts/build_full_trace_pilot_corpus.py` so each mandatory scenario group contains scenario-specific visible diagnostic evidence supporting the private gold failure step while preserving plausible non-gold alternatives.
- Regenerated only the non-final full-trace pilot JSONL files under `data/interim/journal_v1_full_trace_pilot/`.
- Re-ran pilot structural audit, shortcut-baseline sanity, semantic diversity, schema validation, prediction-view validation, and tests.
- Updated diagnostic sufficiency, candidate plausibility, semantic spot-check, generation-risk, and readiness reports to record that Task 14B's pilot diagnostic-sufficiency blocker is cleared.
- Status: `FULL_TRACE_PILOT_DIAGNOSTICALLY_READY = yes`; `FULL_TRACE_MAIN_CORPUS_GENERATION_ALLOWED = future_explicit_approval_required`.
- No full 420-trace corpus generation, CCT scoring, calibration, refinement, ablation, or paper-ready result table was produced.

## Task 15 — Generate and audit Journal-v1 full-trace main corpus

- Generated the BRACIS-Journal-v1 full ordered multi-step main corpus under `data/processed/journal_v1_full_trace/` with 84 clean traces, 336 perturbed traces, and 420 total traces.
- Added full-trace main corpus builder, audit, and baseline-sanity scripts plus raw audit/baseline outputs and reports under `results/reports/journal_v1_full_trace/` and `results/raw/journal_v1_full_trace/`.
- Verified schema validation, prediction-view validation, diagnostic sufficiency, candidate plausibility, lexical leakage, label/H6 distributions, perturbation coverage, and shortcut-baseline thresholds.
- Status: full-trace main corpus is ready only for a future explicitly approved evaluation task; the old failure-centered corpus remains blocked.
- No CCT scoring, calibration, refinement, ablation, empirical hypothesis test, or paper-ready result table was produced.

## 2026-06-05 — Task 18F descriptor-augmented artifact reviewability
- Change type: artifact governance and reproducibility documentation only; no experimental protocol, labels, metrics, baselines, seeds, dataset composition, or claims were changed.
- Added a reproducible builder for descriptor-augmented feature rows and compact reports/manifests documenting the generated artifact policy.
- Excluded the full generated descriptor-augmented JSON from normal Git review and kept a compact tracked sample artifact for code review.
- Recorded expected row count 2,100, join completeness 2,100/2,100, leakage status PASS, and conservative readiness decisions in reports/manifests.
- No scoring, ranking, protocol revision, calibration, grid search, LOSO, refinement, ablation, statistical test, empirical hypothesis test, or paper-ready result table was produced.

## 2026-06-05 — Task 19 CCT diagnostic evidence consolidation and revision-path gate
- Change type: evidence synthesis and claim-boundary documentation only; no experimental protocol, labels, metrics, baselines, seeds, dataset composition, scoring outputs, or performance claims were changed.
- Added negative diagnostic evidence synthesis, revision-path decision gate, claim-boundary update, and next-experiment recommendation reports under `results/reports/journal_v1_full_trace_cct/`.
- Preserved H1/H2 as unsupported under current frozen uncalibrated scoring/features and recorded H3 as blocked until feature validity improves.
- Selected Option C as the recommended future path: redesign CCT graph/feature extraction around richer non-position causal-flow edges before calibration or scoring.
- Explicitly rejected immediate calibration and descriptor-augmented scoring as premature.
- No scoring, ranking, protocol revision, calibration, grid search, LOSO, refinement, ablation, statistical test, empirical hypothesis test, corpus change, gold-label change, or paper-ready result table was produced.

## 2026-06-05 — Task 20 CCT causal-flow edge redesign specification
- Change type: representation specification and governance documentation only; no experimental protocol, labels, metrics, baselines, seeds, dataset composition, graph-builder behavior, feature extraction, scoring outputs, or performance claims were changed.
- Added `docs/16_cct_causal_flow_edge_redesign_spec.md` defining candidate richer non-position causal-flow edge types and strict representation/descriptor/scoring separation.
- Added risk, readiness, and claim-boundary reports under `results/reports/journal_v1_full_trace_cct/`.
- Locked readiness as `CCT_CAUSAL_FLOW_EDGE_SPEC_READY_FOR_SAMPLE_PROTOTYPE = yes` and `CCT_CAUSAL_FLOW_EDGES_READY_FOR_SCORING = no`.
- Recommended a future sample-only edge prototype; no implementation, scoring, ranking, gold-label comparison, calibration, grid search, LOSO, refinement, ablation, statistical test, corpus change, gold-label change, or paper-ready result table was produced.

## 2026-06-05 — Task 20A sample-only CCT causal-flow edge prototype
- Change type: sample-only representation prototype and audit documentation; no experimental protocol, labels, metrics, baselines, seeds, dataset composition, scoring configuration, graph-builder behavior, scoring outputs, or performance claims were changed.
- Added a prediction-view-only causal-edge module and sample prototype script for selected Task 20 edge types.
- Generated compact sample raw edge output, optional sample graph preview, inventory, leakage audit, template-sensitivity report, and readiness gate.
- Locked readiness as `CCT_CAUSAL_FLOW_EDGE_SAMPLE_PROTOTYPE_READY_FOR_FULL_AUDIT = no` and `CCT_CAUSAL_FLOW_EDGES_READY_FOR_SCORING = no`.
- No full-corpus extraction, scoring, ranking, gold-label comparison, H6-label comparison, calibration, grid search, LOSO, refinement, ablation, statistical test, corpus change, gold-label change, or paper-ready result table was produced.

## 2026-06-05 — Task 20B sample causal-edge refinement and provenance check
- Change type: sample-only prototype refinement and protocol provenance documentation; no experimental protocol, labels, metrics, baselines, seeds, dataset composition, scoring configuration, graph-builder behavior, scoring outputs, or performance claims were changed.
- Refined sample edge identifiers and extraction notes to reduce repeated extraction-note and repeated source-target patterns while preserving prediction-view-only extraction.
- Added provenance, template-sensitivity refinement, refined inventory, and refined readiness reports under `results/reports/journal_v1_full_trace_cct/`.
- Recorded that `configs/cct_scoring.yaml` is absent from this checkout, untracked, not ignored, and absent from current Git history; no recovery or recreation was performed.
- Readiness remains `CCT_CAUSAL_FLOW_EDGE_SAMPLE_PROTOTYPE_READY_FOR_FULL_AUDIT = no` and `CCT_CAUSAL_FLOW_EDGES_READY_FOR_SCORING = no`.
- No full-corpus extraction, scoring, ranking, gold-label comparison, H6-label comparison, calibration, grid search, LOSO, scoring refinement, ablation, statistical test, corpus change, gold-label change, or paper-ready result table was produced.

## 2026-06-05 — Task 20C frozen CCT scoring config provenance recovery
- Change type: protocol provenance recovery documentation only; no experimental protocol, labels, metrics, baselines, seeds, dataset composition, scoring configuration, scoring outputs, or performance claims were changed.
- Confirmed `configs/cct_scoring.yaml` is absent from the current checkout and not available from local path history or known Task 17/18 commit-path lookups.
- Added provenance recovery report, blocked-state validation script, and tests documenting that the file was not recreated from memory.
- Recovery status: `RECOVERY_BLOCKED_NO_AUTHORITATIVE_LOCAL_SOURCE`; expected frozen SHA256 remains `053f19066923d8d22d27b22727e75876f939f2a60480484c4028eabd07ad0855`.
- No scoring, ranking, full-corpus extraction, gold-label comparison, H6-label comparison, calibration, grid search, LOSO, scoring refinement, ablation, statistical test, corpus change, gold-label change, or paper-ready result table was produced.

## 2026-06-05 — Task 20D external frozen CCT scoring config recovery attempt
- Change type: external protocol provenance recovery documentation only; no experimental protocol, labels, metrics, baselines, seeds, dataset composition, scoring configuration, scoring outputs, or performance claims were changed.
- Attempted external recovery from GitHub PR #22 and remote heads using the repository URL recorded in `.git/FETCH_HEAD`; fetch access failed with HTTP CONNECT 403 in this environment.
- No local archived patch, saved bundle, signed protocol record, exported artifact, or known commit-path source contained `configs/cct_scoring.yaml`.
- Recovery status: `PERMANENT_RECOVERY_BLOCKED_IN_CURRENT_ENVIRONMENT`; `configs/cct_scoring.yaml` was not recreated from memory or inferred reports.
- Task 18 frozen-config diagnostics must be treated as not reproducible from the current repository checkout until an authoritative external source is provided.
- No scoring, ranking, full-corpus extraction, gold/H6 comparison, calibration, grid search, LOSO, scoring refinement, ablation, statistical test, corpus change, gold-label change, or paper-ready result table was produced.

## 2026-06-05 — Task 20F frozen CCT scoring config hash mismatch adjudication
- Change type: protocol provenance adjudication documentation only; no experimental protocol, labels, metrics, baselines, seeds, dataset composition, scoring configuration, scoring outputs, or performance claims were changed.
- Added `cct_scoring_config_hash_mismatch_adjudication.md` and `cct_task18_reproducibility_boundary.md` to document the mismatch between the expected frozen hash and available PR #22 candidates.
- Classified PR #22 raw hash `435c4703a90171c8bf246a4fa9e188e70800c66c5e9446d19f74de94b32bb` and PR-visible hash `1fe4362714cf79a69bd81d0ffe8b82403cc2c2e99abc9f6c7579ed0253278a4a` as non-matching candidate configs.
- `configs/cct_scoring.yaml` was not restored, the expected hash was not modified, and Task 18 remains not reproducible from the current checkout until an exact byte source is supplied.
- Non-action confirmation: no scoring, ranking, full-corpus extraction, gold-label comparison, H6-label comparison, calibration, grid search, LOSO, scoring refinement, ablation, statistical test, empirical hypothesis test, corpus change, gold-label change, or paper-ready result table was performed.

## 2026-06-05 — Task 21 representation-only CCT causal-edge robustness audit
- Change type: representation-only audit documentation; no experimental protocol, labels, metrics, baselines, seeds, dataset composition, scoring configuration, scoring outputs, or performance claims were changed.
- Added representation-only status, sample robustness audit, rule limitations, and next readiness decision reports for the sample causal-edge prototype.
- Recorded that `configs/cct_scoring.yaml` remains absent, Task 18 remains not reproducible from the current checkout, and scoring/calibration remain blocked.
- Readiness decision: `REPRESENTATION_ONLY_EDGE_ROBUSTNESS_READY_FOR_FULL_CORPUS_AUDIT = no`; `CCT_CAUSAL_FLOW_EDGES_READY_FOR_SCORING = no`.
- Non-action confirmation: no config restoration/recreation, scoring, ranking, full-corpus extraction, gold-label comparison, H6-label comparison, calibration, grid search, LOSO, scoring refinement, ablation, statistical test, empirical hypothesis test, corpus change, gold-label change, or paper-ready result table was performed.

## 2026-06-05 — Task 22 strongest CCT causal-flow edge stress test
- Change type: narrowed representation-only stress-test documentation; no experimental protocol, labels, metrics, baselines, seeds, dataset composition, scoring configuration, scoring outputs, or performance claims were changed.
- Added stress-test plan, report, rule-revision recommendation, and readiness gate for `downstream_dependency_edge`, `tool_alignment_edge`, and `cross_agent_dependency_edge` only.
- Out-of-scope edge types remain documented limitations: `constraint_shift_edge`, `semantic_collision_edge`, and unimplemented Task 20 candidate edge types.
- Readiness decision: `STRONG_CAUSAL_FLOW_EDGES_READY_FOR_NARROW_FULL_CORPUS_AUDIT = yes` for a future representation-only audit of the three in-scope edge types; `CCT_CAUSAL_FLOW_EDGES_READY_FOR_SCORING = no`.
- Non-action confirmation: no config restoration/recreation, scoring, ranking, gold-label comparison, H6-label comparison, calibration, grid search, LOSO, ablation, statistical test, empirical hypothesis test, corpus change, gold-label change, or paper-ready result table was performed.

## 2026-06-05 — Task 23 full-corpus strong-edge representation audit
- Change type: representation-only full-corpus edge audit and generated-artifact governance; no experimental protocol, labels, metrics, baselines, seeds, dataset composition, scoring configuration, scoring outputs, or performance claims were changed.
- Added `scripts/audit_cct_strong_edges_full_corpus.py` to extract only `downstream_dependency_edge`, `tool_alignment_edge`, and `cross_agent_dependency_edge` from prediction-view-safe full-trace records.
- Added full-corpus inventory, leakage, distribution, template-sensitivity, and readiness reports plus a tracked compact sample and artifact manifest; the full generated JSON is ignored by normal Git.
- Audit output: 420 traces, 2,385 total strong edges, leakage PASS, and scoring readiness remains `CCT_CAUSAL_FLOW_EDGES_READY_FOR_SCORING = no`.
- Non-action confirmation: no config restoration/recreation, scoring, ranking, gold-label comparison, H6-label comparison, calibration, grid search, LOSO, ablation, statistical test, empirical hypothesis test, corpus change, gold-label change, or paper-ready result table was performed.

## 2026-06-05 — Task 24 redesigned CCT graph integration
- Change type: representation-only graph artifact integration and generated-artifact governance; no experimental protocol, labels, metrics, baselines, seeds, dataset composition, scoring configuration, scoring outputs, or performance claims were changed.
- Added redesigned graph builder and validation modules plus `scripts/build_cct_redesigned_graphs.py` to integrate only `downstream_dependency_edge`, `tool_alignment_edge`, and `cross_agent_dependency_edge` into prediction-view-safe graph artifacts.
- Added redesigned graph inventory, leakage, diversity, degeneracy, and readiness reports under `results/reports/journal_v1_full_trace_cct_redesigned/`, plus compact tracked sample/inventory artifacts and a manifest.
- Audit output: 420 redesigned graphs; graph signature uniqueness increased from 1 to 6; duplicate graph signatures decreased from 419 to 414; leakage PASS; scoring readiness remains no.
- Non-action confirmation: no config restoration/recreation, scoring, ranking, gold-label comparison, H6-label comparison, calibration, grid search, LOSO, ablation, statistical test, empirical hypothesis test, corpus change, gold-label change, or paper-ready result table was performed.

## 2026-06-05 — Task 24A redesigned CCT graph feature audit
- Change type: representation-only feature extraction and audit; no experimental protocol, labels, metrics, baselines, seeds, dataset composition, scoring configuration, scoring outputs, or performance claims were changed.
- Added redesigned feature extraction module and audit script to derive trace-level structural features from redesigned graph artifacts.
- Added redesigned feature inventory, leakage, variance, degeneracy, and readiness reports plus raw feature artifact under `results/raw/journal_v1_full_trace_cct_redesigned/`.
- Audit output: 420 feature rows, 13 feature names, leakage PASS, 6 unique feature vectors, 414 duplicate feature vectors, and readiness `CCT_REDESIGNED_FEATURES_READY_FOR_PROTOCOL_REVIEW = no` / `CCT_REDESIGNED_FEATURES_READY_FOR_SCORING = no`.
- Non-action confirmation: no config restoration/recreation, scoring, ranking, gold-label comparison, H6-label comparison, calibration, grid search, LOSO, ablation, statistical test, empirical hypothesis test, corpus change, gold-label change, or paper-ready result table was performed.

## 2026-06-05 — Task 25 scientific backbone decision after redesigned feature audit
- Change type: scientific decision and article-claim governance only; no experimental protocol, labels, metrics, baselines, seeds, dataset composition, scoring configuration, scoring outputs, or performance claims were changed.
- Added backbone synthesis, claim reframing, next pivot plan, and journal viability assessment reports under `results/reports/journal_v1_full_trace_cct_redesigned/`.
- Selected Path B: pivot to a protocol-first benchmark/diagnostic-representation paper rather than a performance-oriented method paper.
- Rejected immediate scoring protocol v2 because Task 24A redesigned features remain highly degenerate and not ready for protocol review or scoring.
- Non-action confirmation: no scoring, ranking, gold-label comparison, H6-label comparison, calibration, grid search, LOSO, ablation, statistical test, empirical hypothesis test, corpus change, gold-label change, or paper-ready result table was performed.

## 2026-06-05 — Task 26 journal article backbone after Path B pivot
- Change type: writing-structure and claim-governance documentation only; no experimental protocol, labels, metrics, baselines, seeds, dataset composition, scoring configuration, scoring outputs, or performance claims were changed.
- Added Journal-v1 paper outline, evidence map, claims matrix, contribution statements, results-to-report plan, limitations/threats, and target-journal positioning documents under `docs/`.
- The article frame remains Path B: protocol-first benchmark construction, full-trace representation, leakage/shortcut/provenance governance, causal-flow representation diagnostics, and negative findings.
- Non-action confirmation: no code implementation, scoring, ranking, gold-label comparison, H6-label comparison, calibration, grid search, LOSO, ablation, statistical test, empirical hypothesis test, corpus change, gold-label change, scoring-config restoration, or paper-ready performance table was performed.
