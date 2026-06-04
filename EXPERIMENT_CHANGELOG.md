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

## 2026-06-04 — Task 16A CCT graph artifact reviewability policy

- Change type: generated-artifact governance and reproducible preprocessing policy.
- Added compact tracked CCT graph/feature samples and Markdown reports/manifests for full-trace CCT graph construction.
- Excluded reproducible full generated JSONL artifacts from normal Git review: `data/interim/journal_v1_full_trace_cct/cct_graphs.jsonl` and `data/interim/journal_v1_full_trace_cct/cct_features.jsonl`.
- Reproduction commands: `python scripts/build_cct_graphs_full_trace.py` and `python scripts/validate_cct_graphs_full_trace.py`.
- Protocol impact: reviewability and artifact-handling policy only; no experimental protocol, labels, metrics, baselines, random seeds, dataset composition, evaluation output format, or performance/generalization claim was changed.
- Explicit non-actions: no scoring, ranking, calibration, refinement, ablation, empirical hypothesis test, or paper-ready result table was produced.

## 2026-06-04 — Task 16B CCT feature variance and shortcut-risk audit

- Change type: descriptive structural feature audit and shortcut-risk documentation.
- Added `scripts/audit_cct_feature_variance.py` and three compact reports for variance diagnostics, structural shortcut warnings, and feature readiness.
- Refactored CCT graph construction into `src/cctdiag/cct/builder.py` and structural feature extraction into `src/cctdiag/cct/features.py`, with `src/cctdiag/cct/graph.py` retained as a compatibility export.
- Audit metadata note: `scenario_group` and `perturbation_type` are joined from public corpus metadata for descriptive audit stratification only and are not added to feature payloads.
- Protocol impact: feature-layer readiness governance only; no experimental protocol, gold labels, evaluation metrics, baseline definitions, random seeds, dataset composition, evaluation output format, or performance/generalization claim was changed.
- Explicit non-actions: no scoring, ranking, calibration, refinement, ablation, empirical hypothesis test, or paper-ready result table was produced.

## 2026-06-04 — Task 17 uncalibrated CCT scoring protocol freeze

- Change type: protocol freeze and guardrail validation only.
- Added `docs/14_cct_uncalibrated_scoring_protocol.md`, `configs/cct_scoring.yaml`, `scripts/validate_cct_scoring_protocol.py`, and `results/reports/journal_v1_full_trace_cct/cct_scoring_protocol_risk_report.md`.
- Frozen variants: `cct_primary_no_position`, `cct_flow_only`, `cct_context_only`, and optional high-risk `cct_with_position_features`.
- Primary formula is a fixed transparent weighted sum and excludes position/identity fields and forbidden private/gold/provenance/audit-metadata fields.
- Protocol impact: scoring protocol is frozen before execution to prevent post-hoc tuning; no labels, metrics, baselines, random seeds, dataset composition, existing results, or evaluation output artifacts were changed.
- Explicit non-actions: no scoring, ranking execution, evaluation, calibration, refinement, ablation, empirical hypothesis test, or paper-ready result table was produced.

## 2026-06-04 — Task 18 frozen uncalibrated CCT diagnostics

- Change type: controlled diagnostic execution of the previously frozen Task 17 uncalibrated scoring protocol.
- Config hash before execution: `053f19066923d8d22d27b22727e75876f939f2a60480484c4028eabd07ad0855`; `configs/cct_scoring.yaml` was not changed after results.
- Added scoring/ranking modules, diagnostic runner, raw diagnostic JSON, diagnostic report, shortcut interpretation report, and tests for scoring, ranking, and no-gold scoring access.
- Diagnostic outcome: primary CCT step/agent/tuple accuracy was 0.114286; high-risk with-position and simple majority-style diagnostics reached 0.250000, so H1/H2 remain unsupported in this initial diagnostic run.
- Protocol impact: this is diagnostic evidence only and not journal-grade evaluation; no calibration, LOSO, grid search, refinement, ablation, statistical test, or paper-ready result table was produced.

## 2026-06-04 — Task 18A frozen CCT diagnostic error analysis

- Change type: descriptive error analysis of Task 18 frozen uncalibrated diagnostics.
- Confirmed `configs/cct_scoring.yaml` still hashes to `053f19066923d8d22d27b22727e75876f939f2a60480484c4028eabd07ad0855`; no config, weight, feature, scoring, ranking, corpus, gold-label, baseline, or protocol change was made.
- Added `scripts/analyze_cct_uncalibrated_errors.py`, raw compact error-analysis JSON, and reports for error analysis, tie analysis, feature dominance, and variant disagreement.
- Interpretation: H1/H2 remain unsupported; primary failure is explained by weak fixed features, context/tool-output dominance, wrong score separation rather than ties, and shortcut/default diagnostics exceeding primary.
- Explicit non-actions: no calibration, grid search, LOSO, refinement, ablation, statistical test, or paper-ready result table was produced.

## 2026-06-04 — Task 18B CCT feature semantic audit and descriptor proposal

- Change type: feature-design audit and protocol-safe descriptor proposal only.
- Added reports for current feature semantic taxonomy, non-position causal-flow descriptor candidates, and feature-revision risks.
- Identified current weak/non-discriminative feature groups: constants/cardinality fields, position/identity proxies, position-derived flow fields, and broad content-volume proxies that dominated Task 18 scoring.
- Proposed prediction-view-safe causal-flow descriptor candidates for future audited extraction; no descriptor was implemented or scored in this task.
- Explicit non-actions: no config, weight, scoring formula, ranking rule, corpus, gold-label, baseline, calibration, grid search, LOSO, refinement, ablation, statistical test, or paper-ready result-table change was made.

## 2026-06-04 — Task 18C sample causal-flow descriptor prototype

- Change type: sample-only descriptor specification and deterministic extraction prototype.
- Added `docs/15_cct_causal_flow_descriptor_spec.md`, `src/cctdiag/cct/descriptors.py`, `scripts/prototype_cct_descriptors_sample.py`, raw sample descriptor output, and descriptor prototype/leakage/variance/readiness reports.
- Prototype sample: 14 traces and 70 step rows selected as first clean plus first perturbed trace per scenario group.
- Descriptor preview counts: `handoff_constraint_shift_indicator` positive=2/negative=68; `evidence_ignored_indicator` positive=4/negative=66; `downstream_reference_to_prior_output` positive=56/negative=14.
- Explicit non-actions: no config, weight, scoring, ranking, corpus/gold-label, baseline, calibration, grid search, LOSO, refinement, ablation, statistical test, or paper-ready result-table change was made.
