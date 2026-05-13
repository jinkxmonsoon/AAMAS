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
