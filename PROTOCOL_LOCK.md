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

## Task 10G manual failure-step semantic sanity gate
- Corrected failure-step labels require a qualitative manual sanity check before any downstream evaluation-stage implementation.
- Current Task 10G status: cleared for the inspected sample; 6/6 inspected records were accepted, including clean `s2`, `s3`, `s4`, `s5` traces and two perturbed traces that preserved parent labels.
- This gate does not authorize metrics, baselines, CCT scoring, calibration, empirical evaluation, or result-table generation.

## Task 10H final pre-evaluation corpus gate
- Canonical corpus-correction provenance: PR #13 supersedes PR #12 for the Task 10E–10G corpus correction/audit sequence.
- Current final corpus gate status: cleared; `gold_failure_step` distribution is `s2/s3/s4/s5 = 105/105/105/105`, H6 semantic consistency passes, semantic spot-check passes, and the manual sanity-check sample passes.
- Shortcut gates pass: no failure step exceeds 40%, no failure agent exceeds 50%, no scenario group or perturbation type collapses to one failure step, `always_s2=25.00%`, and `majority_step=25.00%`.
- A future explicitly approved task may implement metric interfaces and trivial baselines; this gate still does not authorize CCT scoring, calibration, refinement, empirical evaluation, or paper result tables.

## Task 11 metric-interface and trivial-baseline sanity gate
- Basic metric interfaces and allowed trivial baselines are authorized only for diagnostic shortcut-risk checks on the corrected BRACIS-Journal-v1 corpus.
- Task 11 diagnostic outputs must not be treated as paper-ready result tables, CCT comparisons, CCT evidence, calibration evidence, refinement evidence, ablation evidence, or evidence for H1.
- H6 diagnostic accuracies must be `NA` when a baseline does not produce the relevant H6 prediction.
- The standalone trivial-baseline gate blocks future evaluation if any standalone trivial step baseline exceeds 50% step accuracy or if `majority_agent` exceeds 50% agent accuracy; random and first/last active agent diagnostics above 50% require review.
- Current Task 11 status: diagnostic trivial-baseline gate passed on `data/processed/journal_v1/main_all_traces.jsonl`; no CCT scoring, calibration, refinement variant, ablation, or paper-ready result table was implemented.

## Task 12 non-CCT baseline diagnostic gate
- Flat-log and spectrum-inspired baselines are authorized only as diagnostic non-CCT shortcut checks for BRACIS-Journal-v1.
- Task 12 does not authorize CCT graph construction, CCT scoring, calibration, V2 refinement, ablations, empirical hypothesis tests, or paper-ready result tables.
- If any non-CCT baseline exceeds 70% step or agent accuracy, evaluation is flagged for corpus/baseline review; if any exceeds 85%, evaluation is blocked pending investigation.
- Current Task 12 status: non-CCT diagnostics are implemented and explicitly mark the gate as blocked because simple non-CCT log/metadata heuristics exceed the 85% blocker threshold; no CCT implementation was added.
