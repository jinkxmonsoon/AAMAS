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

## Task 12A evaluation-input leakage correction gate
- All diagnostic baselines and future evaluation code must consume sanitized prediction views from `src/cctdiag/io/views.py`; raw records are private evaluation artifacts, not model inputs.
- Prediction views must exclude gold labels, private label metadata, H6 rationale/evidence fields that state outcomes, provenance/control fields, and target-equivalent top-level `step_id`, `agent_id`, and failure-centered handoff pointers.
- Current Task 12A status: direct target-equivalent baseline input leakage is corrected, but evaluation remains blocked because the corpus is failure-centered and lacks full ordered multi-step traces; sanitized visible content still permits blocked step attribution.
- No CCT graph construction, CCT scoring, calibration, refinement, ablation, empirical evaluation, or paper-ready result table may proceed until a full-trace prediction-view correction task clears this gate.

## Task 12B full ordered trace schema migration freeze
- The current 420-record Journal-v1 corpus is formally marked failure-centered and not evaluation-ready; no result from it may be used as paper evidence.
- The next evaluation-ready corpus schema must use one record per complete ordered multi-step trace with a model-visible `steps` array and private labels/rationales/provenance outside prediction input.
- Top-level failure-centered `step_id`, `agent_id`, and target-equivalent handoff pointers are prohibited in future prediction views.
- Existing records may be converted only if a future audit proves enough information exists for lossless full-trace reconstruction; otherwise the corpus must be regenerated from an approved full-trace builder.
- Evaluation, CCT graph construction, CCT scoring, calibration, refinement, ablations, and paper-ready result tables remain blocked until the full-trace schema migration is implemented and audited.

## Task 13 full-trace schema validator infrastructure gate
- Full-trace schema contracts, validators, prediction-view helpers, scripts, and non-experimental fixtures are implemented for future corpus migration work only.
- These validators do not make the current failure-centered 420-record corpus evaluation-ready and do not authorize corpus regeneration.
- The Task 12B block remains active: evaluation, CCT graph construction, CCT scoring, calibration, refinement, ablations, and paper-ready result tables remain blocked until a future full-trace corpus is generated/migrated and audited.

## Task 14 full-trace pilot corpus gate
- A 14-trace non-final, non-evidential full-trace pilot may exist under `data/interim/journal_v1_full_trace_pilot/` solely to validate schema, prediction-view, and audit infrastructure.
- The pilot does not replace the blocked failure-centered main corpus, does not authorize full 420-trace regeneration, and must not be used as paper evidence.
- Current Task 14 status: pilot build/audit scripts and reports are diagnostic only; all CCT graph construction, CCT scoring, calibration, refinement, ablations, and paper-ready result tables remain blocked.

## Task 14A full-trace pilot shortcut and diversity gate
- Full-trace pilot shortcut baselines and semantic-diversity diagnostics are authorized only for the non-final 14-trace pilot.
- Current Task 14A status: pilot shortcut/diversity gate passed; this permits only a future explicitly approved full-trace main-corpus builder task and does not authorize CCT scoring, calibration, refinement, ablations, paper-ready result tables, or use of the old failure-centered corpus.

## Task 14B diagnostic sufficiency gate

Task 14B audits whether the non-final full-trace pilot is diagnostically solvable from sanitized prediction views. The audit finds that the pilot controls obvious shortcut baselines but over-corrects into semantic flattening: gold failure steps are not inferable from visible evidence in the clean pilot traces, while non-gold candidates remain plausible mainly because all steps use repeated templates.

Locked status after Task 14B:

- `FULL_TRACE_PILOT_DIAGNOSTICALLY_READY = no`.
- `FULL_TRACE_MAIN_CORPUS_GENERATION_ALLOWED = no`.
- Full 420-trace corpus generation remains blocked until the pilot builder is revised and the diagnostic sufficiency gate is rerun.
- CCT graph construction, CCT scoring, calibration, refinement variants, ablations, paper-ready result tables, and use of the old failure-centered corpus remain blocked.

## Task 14C revised full-trace pilot diagnostic sufficiency gate

Task 14C revises the non-final full-trace pilot builder so sanitized visible trace evidence supports the private gold attribution point while preserving plausible non-gold candidates. The revised pilot clears the Task 14B diagnostic sufficiency blocker for the pilot only.

Locked status after Task 14C:

- `FULL_TRACE_PILOT_DIAGNOSTICALLY_READY = yes`.
- `FULL_TRACE_MAIN_CORPUS_GENERATION_ALLOWED = future_explicit_approval_required`.
- The old failure-centered corpus remains blocked and must not be used for evaluation or paper evidence.
- Full 420-trace corpus generation remains a separate future task requiring explicit approval.
- CCT graph construction, CCT scoring, calibration, refinement variants, ablations, and paper-ready result tables remain blocked.

## Task 15 full-trace main corpus generation gate

Task 15 generates and audits the BRACIS-Journal-v1 full ordered multi-step main corpus under the Task 14C pilot design. This creates corpus artifacts only and does not authorize empirical evaluation.

Locked status after Task 15:

- `FULL_TRACE_MAIN_CORPUS_READY_FOR_FUTURE_EVALUATION_TASK = yes` for a future explicitly approved evaluation task only.
- The old failure-centered corpus remains blocked and must not be used for evaluation or paper evidence.
- CCT graph construction, CCT scoring, calibration, refinement variants, ablations, empirical hypothesis tests, and paper-ready result tables remain blocked until explicitly authorized in a later task.

## Task 18F descriptor-augmented artifact reviewability gate
- Descriptor-augmented feature artifacts are governed as generated audit/review artifacts, not as evaluation outputs.
- Normal Git tracking keeps source code, tests, compact reports, readiness gates, manifests, and a compact sample artifact only.
- The full descriptor-augmented feature JSON is reproducible with `python scripts/build_cct_descriptor_augmented_features.py` and is excluded from normal Git review to avoid oversized diffs.
- If full generated artifacts must later be versioned, use Git LFS or release artifact handling rather than unreviewable normal Git JSON diffs.
- Current readiness remains conservative: `AUGMENTED_FEATURE_LAYER_READY_FOR_PROTOCOL_REVISION = no` and `AUGMENTED_FEATURE_LAYER_READY_FOR_SCORING = no`.
- Task 18F does not authorize scoring, ranking, protocol revision, calibration, grid search, LOSO, refinement, ablation, statistical testing, empirical hypothesis testing, or paper-ready result tables.

## Task 19 CCT negative diagnostic evidence and revision-path gate
- Current hypothesis status is locked as: H1 unsupported under current frozen uncalibrated scoring/features; H2 unsupported under current frozen uncalibrated scoring/features; H3 blocked because calibration before feature validity is premature; H4 blocked; H6 open but unsupported by scoring evidence.
- Immediate calibration of current features is blocked.
- Immediate descriptor-augmented scoring is blocked because descriptor readiness remains `AUGMENTED_FEATURE_LAYER_READY_FOR_PROTOCOL_REVISION = no` and `AUGMENTED_FEATURE_LAYER_READY_FOR_SCORING = no`.
- Selected next methodological direction is Option C: a future explicitly scoped redesign of CCT graph/feature extraction around richer non-position causal-flow edges before scoring.
- Claim boundaries are restricted to methodology, protocol, benchmark construction, leakage correction, full-trace representation, artifact governance, and diagnostic findings; no superiority claim is currently allowed.
- Task 19 does not authorize scoring, ranking, protocol revision, calibration, grid search, LOSO, refinement, ablation, statistical testing, corpus changes, gold-label changes, or paper-ready result tables.

## Task 20 CCT causal-flow edge redesign specification gate
- Task 20 defines a specification-only richer non-position causal-flow edge redesign; no graph-builder behavior, descriptor extraction, feature extraction, scoring, ranking, calibration, grid search, LOSO, refinement, ablation, statistical testing, corpus content, or gold labels are changed.
- Candidate edge types are `constraint_shift_edge`, `evidence_conflict_edge`, `evidence_omission_edge`, `downstream_dependency_edge`, `correction_opportunity_edge`, `correction_attempt_edge`, `unresolved_caveat_edge`, `semantic_collision_edge`, `tool_alignment_edge`, and `cross_agent_dependency_edge`.
- Anti-leakage constraints forbid private labels, gold fields, H6 private evidence, label rationales, provenance, correctness fields, ranks/scores, and scenario/perturbation fields as extraction inputs.
- Anti-shortcut constraints forbid extraction based on step position, agent identity, fixed scenario names, perturbation labels, builder-specific phrases alone, or content volume alone.
- Readiness is locked as `CCT_CAUSAL_FLOW_EDGE_SPEC_READY_FOR_SAMPLE_PROTOTYPE = yes` and `CCT_CAUSAL_FLOW_EDGES_READY_FOR_SCORING = no`.
- The next recommended task is a sample-only edge prototype with leakage/shortcut audits and no gold-label comparison or scoring.

## Task 20A sample-only CCT causal-flow edge prototype gate
- Task 20A permits a compact sample-only prototype for `constraint_shift_edge`, `downstream_dependency_edge`, `tool_alignment_edge`, `cross_agent_dependency_edge`, and conservative `semantic_collision_edge` extraction from prediction views only.
- Edge extraction must consume `make_full_trace_prediction_view(record)` output; raw records containing private labels/provenance are rejected by the extraction module.
- The sample is capped below full-corpus scope and selected deterministically without gold labels; full-corpus edge extraction remains blocked.
- Readiness is locked as `CCT_CAUSAL_FLOW_EDGE_SAMPLE_PROTOTYPE_READY_FOR_FULL_AUDIT = no` and `CCT_CAUSAL_FLOW_EDGES_READY_FOR_SCORING = no`.
- No graph-builder behavior, existing feature extraction, descriptor extraction, scoring configuration, corpus content, gold labels, scoring, ranking, calibration, grid search, LOSO, refinement, ablation, statistical testing, or paper-ready result tables are authorized by this task.

## Task 20B sample causal-edge refinement and provenance gate
- Task 20B refines only the sample causal-edge prototype to reduce template-pattern repetition; extraction remains capped to the deterministic sample and prediction-view-only inputs.
- `configs/cct_scoring.yaml` is absent in the current branch checkout, untracked, not ignored by current `.gitignore`, and has no history in current Git history; this is recorded as a protocol provenance anomaly, not silently repaired.
- Recreating or modifying `configs/cct_scoring.yaml` remains blocked pending a separate explicitly authorized protocol-recovery task with authoritative provenance.
- Readiness remains `CCT_CAUSAL_FLOW_EDGE_SAMPLE_PROTOTYPE_READY_FOR_FULL_AUDIT = no` and `CCT_CAUSAL_FLOW_EDGES_READY_FOR_SCORING = no`.
- No full-corpus extraction, graph-builder behavior change, feature extraction, descriptor extraction, scoring, ranking, gold/H6 comparison, calibration, grid search, LOSO, scoring refinement, ablation, statistical testing, corpus change, gold-label change, or paper-ready result table is authorized by this task.

## Task 20C frozen CCT scoring config provenance recovery gate
- Task 20C confirms that `configs/cct_scoring.yaml` is absent from the current branch checkout, untracked by `git ls-files`, not ignored by current ignore rules, and unavailable in current local Git history for the inspected path.
- Known Task 17/18 commit-path lookups for `configs/cct_scoring.yaml` did not locate an authoritative local source.
- Because no authoritative local source was found, recovery is blocked and the file must not be recreated from memory or inferred from reports.
- A separate explicitly authorized protocol-recovery task must obtain the authoritative frozen file from PR #22, an archived patch, previous branch, saved artifact, or signed protocol record, then verify SHA256 `053f19066923d8d22d27b22727e75876f939f2a60480484c4028eabd07ad0855`.
- No scoring, ranking, full-corpus edge extraction, gold/H6 comparison, calibration, grid search, LOSO, scoring refinement, ablation, statistical testing, corpus change, gold-label change, or paper-ready result table is authorized by this task.

## Task 20D external CCT scoring config recovery gate
- Task 20D attempted external recovery using the repository URL recorded in `.git/FETCH_HEAD` (`https://github.com/jinkxmonsoon/AAMAS`), including PR #22 and remote branch fetches, but access failed with HTTP CONNECT 403 in this environment.
- No local archived patch, saved bundle, signed protocol record, exported artifact, or known Task 17/18 commit-path source contained `configs/cct_scoring.yaml`.
- Recovery status is locked as `PERMANENT_RECOVERY_BLOCKED_IN_CURRENT_ENVIRONMENT`; `configs/cct_scoring.yaml` was not recreated or modified.
- Until an authoritative external source is provided, Task 18 frozen-config diagnostics are not reproducible from the current repository checkout.
- No scoring, ranking, full-corpus extraction, gold/H6 comparison, calibration, grid search, LOSO, scoring refinement, ablation, statistical testing, corpus change, gold-label change, or paper-ready result table is authorized by this task.

## Task 20F frozen CCT scoring config hash mismatch adjudication gate
- Task 20F adjudicates the mismatch between the expected frozen `configs/cct_scoring.yaml` SHA256 and PR #22 candidate contents; it is provenance adjudication only.
- Expected frozen SHA256 remains `053f19066923d8d22d27b22727e75876f939f2a60480484c4028eabd07ad0855` and was not modified.
- PR #22 raw candidate SHA256 `435c4703a90171c8bf246a4fa9e188e70800c66c5e9446d19f74de94b32bb` and PR-visible candidate SHA256 `1fe4362714cf79a69bd81d0ffe8b82403cc2c2e99abc9f6c7579ed0253278a4a` are classified as non-matching candidate configs.
- No non-matching config is restored as authoritative; `configs/cct_scoring.yaml` remains absent until an exact byte source matching the expected frozen hash is provided.
- Task 18 diagnostics are locked as recorded diagnostic evidence that is not reproducible from the current checkout and not paper-ready empirical evidence.
- Scoring, ranking, gold/H6 comparison, full-corpus edge extraction, calibration, grid search, LOSO, scoring refinement, ablation, statistical testing, and paper-ready result tables remain blocked.

## Task 21 representation-only causal-edge robustness audit gate
- Task 21 continues only representation-level causal-edge robustness auditing after the frozen scoring-config hash mismatch remains unresolved.
- `configs/cct_scoring.yaml` remains absent, Task 18 remains not reproducible from the current checkout, and scoring/calibration remain blocked.
- Sample audit findings: clean and perturbed sampled traces have matching edge counts by implemented type, but normalized relation-template repetition, sparse modality-shift detection, and semantic-collision template dependence remain blockers.
- Readiness remains conservative: `REPRESENTATION_ONLY_EDGE_ROBUSTNESS_READY_FOR_FULL_CORPUS_AUDIT = no` and `CCT_CAUSAL_FLOW_EDGES_READY_FOR_SCORING = no`.
- No config restoration/recreation, scoring, ranking, full-corpus extraction, gold/H6 comparison, calibration, grid search, LOSO, scoring refinement, ablation, statistical testing, or paper-ready result table is authorized.

## Task 22 narrowed strong causal-flow edge stress-test gate
- Task 22 stress-tests only `downstream_dependency_edge`, `tool_alignment_edge`, and `cross_agent_dependency_edge` under representation-only constraints.
- `constraint_shift_edge`, `semantic_collision_edge`, and unimplemented Task 20 edge types remain out of scope for the narrowed readiness decision.
- Stress-test finding: the three in-scope edge types show clean-vs-perturbed descriptive count stability in the 14-trace sample and retain visible relation requirements, but normalized phrase-pattern repetition remains an audit condition.
- Readiness is narrowly set to `STRONG_CAUSAL_FLOW_EDGES_READY_FOR_NARROW_FULL_CORPUS_AUDIT = yes` for a future representation-only full-corpus audit of the three in-scope edge types only.
- `CCT_CAUSAL_FLOW_EDGES_READY_FOR_SCORING = no`; scoring, ranking, gold/H6 comparison, calibration, grid search, LOSO, ablation, statistical testing, and paper-ready result tables remain blocked.

## Task 23 representation-only full-corpus strong-edge audit gate
- Task 23 runs a full-corpus representation-only audit for `downstream_dependency_edge`, `tool_alignment_edge`, and `cross_agent_dependency_edge` only.
- `configs/cct_scoring.yaml` remains absent/blocked and Task 18 remains `NOT_REPRODUCIBLE_FROM_CURRENT_CHECKOUT`; this audit does not depend on the scoring config.
- Full-corpus audit summary: 420 traces processed, 2,385 strong edges generated, with 705 downstream-dependency edges, 840 tool-alignment edges, and 840 cross-agent-dependency edges.
- Generated-artifact policy applies: the full JSON is reproducible by `python scripts/audit_cct_strong_edges_full_corpus.py` and ignored by normal Git, while a compact sample and manifest are tracked.
- Readiness is representation-only: `STRONG_CAUSAL_FLOW_EDGES_FULL_CORPUS_AUDIT_READY = yes`, `STRONG_CAUSAL_FLOW_EDGES_READY_FOR_GRAPH_REDESIGN_INTEGRATION = yes`, and `CCT_CAUSAL_FLOW_EDGES_READY_FOR_SCORING = no`.
- No scoring, ranking, gold/H6 comparison, calibration, grid search, LOSO, ablation, statistical testing, empirical hypothesis testing, corpus/gold-label changes, or paper-ready result tables are authorized.

## Task 24 representation-only redesigned CCT graph integration gate
- Task 24 integrates only the three authorized strong causal-flow edge types (`downstream_dependency_edge`, `tool_alignment_edge`, `cross_agent_dependency_edge`) into redesigned CCT graph artifacts.
- `configs/cct_scoring.yaml` remains absent/blocked and Task 18 remains `NOT_REPRODUCIBLE_FROM_CURRENT_CHECKOUT`; redesigned graph construction is independent from scoring configuration.
- Full redesigned graph build summary: 420 redesigned graphs, 705 downstream-dependency edges, 840 tool-alignment edges, 840 cross-agent-dependency edges, plus prediction-view-safe base sequence/handoff edges.
- Graph-signature uniqueness increases from 1 base signature to 6 redesigned signatures and duplicate signatures decrease from 419 to 414, so strong edges reduce graph degeneracy under representation-only audit criteria.
- Generated-artifact policy applies: full redesigned graph JSONL is reproducible by `python scripts/build_cct_redesigned_graphs.py` and ignored by normal Git; compact sample, inventory, reports, and manifest are tracked.
- Readiness is representation-only: `CCT_REDESIGNED_GRAPHS_READY_FOR_FEATURE_AUDIT = yes` and `CCT_REDESIGNED_GRAPHS_READY_FOR_SCORING = no`.
- No scoring, ranking, gold/H6 comparison, calibration, grid search, LOSO, ablation, statistical testing, empirical hypothesis testing, corpus/gold-label changes, or paper-ready result tables are authorized.
