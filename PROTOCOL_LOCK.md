# PROTOCOL LOCK (Frozen Placeholders)

Status: **LOCKED PLACEHOLDERS — INITIALIZATION PHASE**

This document reserves protocol slots that must be explicitly filled and approved before experiments begin.

## Locked sections (placeholders)
- Task definitions: TBD (locked)
- Agent configurations: TBD (locked)
- Dataset splits/composition: TBD (locked)
- Gold label policy: TBD (locked)
- Random seed policy: TBD (locked)
- Metrics definitions: See `docs/04_metrics_definition.md` (placeholder locked)
- Baseline catalog: TBD (locked)
- Output schema: TBD (locked)
- Statistical testing plan: TBD (locked)

## Change policy
Any change to these sections requires:
1. Explicit written authorization.
2. Changelog entry in `EXPERIMENT_CHANGELOG.md`.
3. Rationale entry in `RESEARCH_LOG.md`.

## BRACIS v0 artifact-status note
- BRACIS v0 reproduction is blocked until artifacts are recovered.
- No v0 result may be treated as reproduced.


## Path B activation note (Journal v1)
- Path B is activated for protocol design of **BRACIS-Journal-v1**.
- BRACIS-Journal-v1 is independent from BRACIS v0 unless original artifacts are later recovered and verified.
- No v1 experiment may run before schema, label protocol, metrics, baselines, and acceptance criteria are frozen in protocol documents.


## Task 4 operational-contract freeze gate
- Operational contracts must be frozen before any Journal-v1 corpus generation.
- No Journal-v1 data generation may occur before Task 4 completion.
- No metric or baseline implementation may occur before contracts are frozen.

- No Journal-v1 corpus file may be accepted unless it passes schema and label validation.

## Task 6 corpus-plan and rubric freeze gate
- Journal-v1 corpus construction plan and semantic label rubric must be frozen before generating any real corpus file.
- No corpus generation is allowed unless `configs/corpus_plan.yaml` and `configs/label_rubric.yaml` pass plan validation.
- No Journal-v1 metric execution may occur unless schema, label, leakage, and integrity audits pass.
- Pilot corpus may not be used in final reported results.
- Final corpus generation remains blocked until pilot audit passes and pilot lessons are logged.
- Full corpus generation remains blocked until pilot semantic audit and lessons report are complete.
- Full corpus generation remains blocked until Task 9 readiness check passes.
- If Task 9 passes, generation is allowed only through a future approved main-corpus builder task.


## Task 10 main-corpus generation and audit gate
- Main controlled corpus generation is permitted only through `scripts/build_main_corpus.py` and must write only to `data/processed/journal_v1/`.
- Main corpus acceptance requires PASS on schema, label, leakage, integrity, split-safety-interface, and H6 distribution audits via `scripts/audit_main_corpus.py`.
- This gate does not permit metrics, baselines, CCT scoring, calibration, or result-table generation.


## Task 10A main-corpus freeze and semantic spot-check gate
- Main corpus is frozen after `docs/artifact_manifests/journal_v1_main_corpus_manifest.md` generation.
- No file under `data/processed/journal_v1/` may be edited after freeze except via explicit approved correction task.
- No metric, baseline, CCT scoring, calibration, or result-table work may run until Task 10A semantic spot-check passes or blockers are explicitly waived.


## Task 10B templating-risk resolution note
- Main corpus was regenerated via approved builder to reduce templating artifacts while preserving frozen counts/taxonomy/label semantics.
- Task 10A semantic blocker is cleared only when spot-check reports `accept` majority with no rejects and explicit summary counts.
- If future spot-checks detect systemic templating, evaluation is re-blocked pending approved correction task.


## Task 10D H6 semantic consistency gate
- Main corpus evaluation remains blocked unless `scripts/audit_h6_semantic_consistency.py` reports FINAL: PASS.
- Any future H6 contradiction requires corpus correction via approved builder and manifest regeneration before evaluation resumes.

## Task 10E label-position and trivial-shortcut risk gate
- Main corpus evaluation is blocked unless `scripts/audit_label_position_bias.py` reports shortcut risk below the pre-evaluation thresholds or an explicit written corpus justification/revision task is approved.
- No single `gold_failure_step` may exceed 50% of the corpus without explicit justification.
- If any trivial corpus-risk diagnostic (`majority_step`, `majority_agent`, `always_s2`, `first_active_agent` when computable, or `most_common_agent`) exceeds 50%, metric, baseline, CCT scoring, calibration, and result-table work remain blocked.
- Current Task 10E status: blocked because `gold_failure_step=s2` appears in 420/420 traces (100.00%), so `majority_step` and `always_s2` diagnostic expected accuracy are both 100.00%.

## Task 10F failure-step positional-bias correction gate
- Main corpus generation now uses semantically grounded failure-step assignment across `s2`, `s3`, `s4`, and `s5` where trace length supports `s5`.
- Task 10F acceptance requires no single `gold_failure_step` above 40%, at least 3 step values each at or above 15%, `majority_step <= 40%`, and `always_s2 <= 40%`.
- Current Task 10F status: cleared by regenerated corpus with `s2/s3/s4/s5 = 105/105/105/105` traces (25.00% each); metric, baseline, CCT scoring, calibration, and result-table implementation remain prohibited until a separate explicitly approved evaluation task.
