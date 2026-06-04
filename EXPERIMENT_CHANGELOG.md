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
