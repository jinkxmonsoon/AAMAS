# RESEARCH LOG

Chronological decisions, assumptions, caveats, and methodological notes.

## Entry Template
- Date (UTC):
- Context:
- Decision:
- Alternatives considered:
- Risks / limitations:
- Follow-up action:

## Entries
- 2026-05-13 (UTC): Initialized repository structure for protocol traceability. Deferred all empirical implementation.
- 2026-05-13 (UTC):
  - Technical result: Hardened repository scaffold with full governance/config/data/results/notebooks directory checks in `scripts/validate_repo.py`; added placeholder packaging and protocol validator entrypoint.
  - Scientific result: No empirical findings produced; this update only increases protocol traceability and reproducibility readiness.
  - Intentionally not implemented: experiments, metrics computations, baseline logic, dataset ingestion/modification, and any result generation.
  - Remaining risk: Protocol placeholders are still uninstantiated; unauthorized future edits to locked concepts remain a governance risk if review discipline is not enforced.
- 2026-05-13 (UTC):
  - Technical result: Removed duplicate module files (`src/cctdiag/io.py`, `src/cctdiag/schema.py`), kept package-based structure, and added ambiguity detection in `scripts/validate_repo.py` to fail when both module and package exist for protected names.
  - Scientific result: No empirical findings produced; update only reduces import ambiguity risk and improves maintainability for protocol-first development.
  - Intentionally not implemented: experiments, datasets, metric computations, baselines, and any empirical reporting outputs.
  - Remaining risk: Placeholder-only package boundaries are now clean, but concrete API contracts across subpackages remain undefined until protocol-approved implementation starts.
- 2026-05-13 (UTC):
  - Current stage: Artifact-freeze and desk-reject audit preparation for journal reconstruction.
  - Task executed: Registered BRACIS desk-reject v0 as frozen reference; created claims audit and reported-results register; extended repo validation coverage for new audit artifacts.
  - Technical result: Added `docs/07_desk_reject_artifact_audit.md` and `results/reports/bracis_v0_reported_results.md` with explicit reported-vs-reproduced separation and reproduction checklist.
  - Scientific result: No empirical result produced; all reported BRACIS numbers remain non-reproduced in current repo.
  - What the audit shows: strongest near-term risks are over-strong causal wording, unverified external transfer framing, and missing end-to-end reproducibility of core tables.
  - What remains unknown: full numeric table extraction, statistical interval/test details, and scenario-level breakdown reproducibility pending manuscript import.
  - Risks: journal rejection risk remains high until all primary/secondary/contextual claims are revalidated under locked protocol.
  - Next mandatory step: import BRACIS v0 manuscript artifact and complete row-level numerical extraction + reproduction plan execution.

- 2026-05-13 (UTC):
  - Current stage: Desk-reject numerical audit completion (Task 0.5B).
  - Task executed: Completed row-level extraction of BRACIS v0 reported numbers into the results register with source/value-type/reproduction/tier/risk annotations.
  - Technical result: Expanded reported-results file to include trace-bank composition, calibration, clean variants, paired statistics, contextual external comparison, robustness, scenario-level values, and fixed/worsened/unchanged audit.
  - Scientific result: No empirical computation run; all listed values remain reported-only and not yet reproduced.
  - What the audit shows: strongest quantitative risks are low irreversibility (0.08) and low propagation (0.04), plus strong degradation of V2C versus v1 in step attribution.
  - What remains unknown: full reproducibility of all tables/figures and robustness/statistical pipelines under protocol-locked reconstruction.
  - Risks: premature journal claims would overstate evidence before reproduction and fairness-audited baselines.
  - Next mandatory step: ingest frozen BRACIS artifact files with traceable section/figure IDs and begin protocol-locked reproduction sequence.
- 2026-05-13 (UTC):
  - Current stage: Artifact ingestion and provenance freeze (Task 1).
  - Task executed: Created BRACIS v0 artifact import area, generated SHA256 manifest script/output, and added artifact inventory and validation checks.
  - Technical result: Added `data/raw/bracis_v0/`, `results/raw/bracis_v0/`, `docs/artifact_manifests/`, `scripts/make_artifact_manifest.py`, manifest markdown, inventory markdown, and ingestion tests.
  - Scientific result: No hypothesis test performed and no empirical computation executed.
  - What was imported: only placeholder README metadata files in import directories due to artifact unavailability in current environment.
  - What remains missing: actual BRACIS v0 raw traces, labels, perturbations, calibration outputs, robustness outputs, and original scripts/notebooks.
  - Risks: reproduction cannot begin until missing source artifacts are acquired and provenance-linked.
  - Next mandatory step: obtain original BRACIS v0 artifact bundle and re-run manifest generation for full immutable inventory.
- 2026-05-13 (UTC):
  - Current stage: Task 1B artifact availability verification and status correction.
  - Task executed: Searched workspace/repository for actual BRACIS v0 bundle artifacts; updated manifest classification and issued formal missing-artifacts declaration.
  - Technical result: `make_artifact_manifest.py` now classifies rows as `experimental_artifact` vs `scaffold_metadata`; current manifest shows 0 experimental artifacts and 2 scaffold files.
  - Scientific result: No experiment run; no metric or result recomputation performed.
  - What was imported: no actual BRACIS experimental bundle files in current environment.
  - What remains missing: traces, labels, perturbations, scenario metadata, calibration outputs, robustness outputs, prior result files, and original scripts/notebooks.
  - Risks: reproduction remains blocked and journal reconstruction cannot begin empirically.
  - Next mandatory step: obtain original BRACIS v0 artifact bundle from source owners and rerun manifest/inventory with immutable hashes.

- 2026-05-13 (UTC):
  - Current stage: Task 2 decision-gate definition before any reproduction/implementation.
  - Technical result: Added formal decision document (`docs/08_artifact_recovery_or_reconstruction_decision.md`) and updated protocol lock with explicit v0 reproduction block.
  - Scientific result: No hypothesis test run; no experiment, metric, or dataset generation performed.
  - Decision required: choose Path A (recover BRACIS v0 by deadline) or Path B (reconstruct BRACIS-Journal-v1 under frozen protocol).
  - Risks: delaying decision increases schedule risk; starting implementation without a gate risks claim invalidity.
  - Next mandatory step: obtain PI/TL sign-off on Path A deadline (2026-05-27 UTC) and execute fallback trigger to Path B if unmet.

- 2026-05-13 (UTC):
  - Current stage: Task 2A formal BRACIS v0 artifact recovery attempt.
  - Technical result: Added explicit recovery-attempt manifest with per-category found/imported/blocking fields and updated missing/inventory reports.
  - Scientific result: No hypothesis test and no experimental computation; reproduction status unchanged.
  - Decision required: Path A remains unavailable until source bundle is delivered; Path B trigger remains as defined in Task 2 gate.
  - Risks: continued absence of source artifacts blocks BRACIS v0 reproduction and delays journal evidence hardening.
  - Next mandatory step: request original bundle from source owners and rerun import manifest/inventory immediately upon receipt.

- 2026-05-13 (UTC):
  - Current stage: Task 3 Path B activation and Journal-v1 protocol definition.
  - Technical result: Added `docs/09_journal_v1_reconstruction_protocol.md`; updated decision gate and protocol lock to activate Journal-v1 protocol design constraints.
  - Scientific result: No empirical hypothesis tested; no experiment/data/metric/baseline/result execution performed.
  - Decision: Path B activated for protocol definition; BRACIS v0 remains unreproduced historical reference only.
  - Risks: schema/label/proxy choices may still drift if not frozen via explicit acceptance criteria and review sign-off.
  - Next mandatory step: freeze schema + label protocol + metric/baseline acceptance criteria and obtain TL/PI sign-off before any implementation or execution.

- 2026-05-13 (UTC):
  - Current stage: Task 4 operational-contract freeze for Journal-v1.
  - Technical result: Added machine-checkable contract document/config placeholders and `scripts/validate_contracts.py` + lightweight tests for required keys.
  - Scientific result: No hypothesis test; no data/label/metric/baseline/result generation or execution.
  - Decision: Journal-v1 operational contracts are frozen at interface/registry level prior to execution.
  - Risks: contract ambiguity may persist if acceptance thresholds are not finalized in next protocol freeze.
  - Next mandatory step: finalize acceptance thresholds and sign-off, then begin controlled implementation phase under lock rules.

- 2026-05-13 (UTC):
  - Current stage: Task 5 validator infrastructure before corpus generation.
  - Task executed: Implemented Journal-v1 schema and label validation modules/scripts plus non-experimental fixtures and tests.
  - Technical result: Added machine-checkable checks for required fields, enums, perturbation links, label references/confidence, provenance, and v0 empirical-source blocking.
  - Scientific result: No empirical hypothesis test; no corpus generation, no metric implementation, no baseline implementation, no results.
  - Remaining risks: controlled enums/proxy value spaces may need refinement after governance sign-off; currently interface-level.
  - Next mandatory step: wire validators into future corpus-ingestion pipeline and freeze any remaining enum/value-domain details before generating Journal-v1 data.

- 2026-05-13 (UTC):
  - Current stage: Task 6 corpus construction-plan and semantic-rubric freeze.
  - Task executed: Added Journal-v1 corpus planning/rubric document, corpus-plan and label-rubric configs, plus lightweight plan validator and tests.
  - Technical result: Frozen target counts (84 clean, 336 perturbation variants, 420 total), scenario/perturbation sets, semantic label definitions, anti-leakage rules, and corpus acceptance gates.
  - Scientific result: No hypothesis test, no corpus generation, no metric/baseline implementation, no results.
  - Remaining risks: semantic correctness still requires future adjudication quality controls; H6 remains high-risk despite structural checks.
  - Next mandatory step: finalize adjudication SOP details and integrate corpus-generation pipeline with validators before creating first pilot corpus files.

- 2026-05-13 (UTC):
  - Current stage: Task 6A scenario-group optionality ambiguity cleanup.
  - Technical result: Renamed scenario enum to `complex_collaboration` across docs/configs/contracts to align with mandatory 7-group fixed-count design.
  - Scientific result: No data generation, no label generation, no metric/baseline implementation, and no result changes.
  - Remaining risks: semantic boundary of complex collaboration still needs detailed annotation SOP examples before generation.
  - Next mandatory step: finalize scenario authoring templates and adjudication examples consistent with the frozen enum set.

- 2026-05-13 (UTC):
  - Current stage: Task 7 pre-generation/pre-experiment audit infrastructure.
  - Task executed: Implemented leakage, integrity, and split-safety audit modules/scripts with non-experimental fixture corpora and tests.
  - Technical result: Added corpus-level checks for leakage terms, duplicate IDs, parent-child linkage, dataset/scenario/perturbation validity, and split-family safety constraints.
  - Scientific result: No hypothesis test, no corpus generation, no metric/baseline implementation, no result generation.
  - Remaining risks: audit lexicons and heuristic leakage patterns may need expansion after pilot corpus review.
  - Next mandatory step: integrate audit scripts in corpus-ingestion gate so generation cannot proceed unless schema/label/leakage/integrity checks all pass.

- 2026-05-13 (UTC):
  - Current stage: Task 8 pilot validation corpus build-and-audit.
  - Task executed: Built 14-trace non-final pilot corpus (7 clean + 7 perturbed) and executed schema/label/leakage/integrity/coverage audits.
  - Technical result: Added builder and pilot-audit scripts, pilot inventory and audit report outputs, and pilot tests for builder/audit execution.
  - Scientific result: No hypothesis test and no claim-bearing experimental result; pilot is non-evidential.
  - Pilot limitations: small synthetic pilot intended for tooling/protocol shakeout only; not representative for claims.
  - Next mandatory step: log pilot lessons and freeze any rubric/scheme adjustments before main corpus generation.

- 2026-05-13 (UTC):
  - Current stage: Task 8A pilot semantic and methodological audit.
  - Task executed: Extended pilot audit reporting with explicit H6 coverage checks and produced semantic audit + lessons-learned reports.
  - Technical result: Added H6 count/rationale acceptance checks and per-case semantic review tables for clean and perturbed pilot traces.
  - Scientific result: No hypothesis test, no metric/baseline/CCT scoring implementation, no result tables; pilot remains non-evidential.
  - Remaining risks: semantic evidence depth and ambiguity handling still require rubric refinement before full corpus generation.
  - Next mandatory step: apply protocol refinements from lessons report and rerun pilot audits prior to unlocking main corpus generation.

- 2026-05-13 (UTC):
  - Current stage: Task 9 main-corpus generation readiness freeze gate.
  - Task executed: Reviewed pilot semantic audit + lessons, formalized readiness decision and pilot-to-main deltas, and added machine-checkable readiness script/test.
  - Technical result: Added `docs/12_journal_v1_main_corpus_generation_readiness.md`, `scripts/check_main_corpus_readiness.py`, and readiness unit test.
  - Scientific result: No hypothesis test; no full corpus generation; no metric/baseline/CCT scoring/result table work.
  - Remaining risks: H6 semantics still require richer adjudication exemplars before broad generation confidence.
  - Next mandatory step: approve/waive all listed deltas, then implement the future approved main-corpus builder task under lock rules.


- 2026-05-13 (UTC):
  - Current stage: Task 10 main controlled corpus generation and audit.
  - Task executed: Generated Journal-v1 main controlled corpus (84 clean + 336 perturbed = 420 total) and ran schema/label/leakage/integrity/split-safety-interface/H6 audits.
  - Technical result: Added main corpus builder/auditor scripts, generated processed corpus JSONL files, and emitted inventory/audit/H6/leakage/integrity reports.
  - Scientific result: No hypothesis test, no metric/baseline/CCT scoring/calibration/result table execution; corpus creation only.
  - Remaining risks: semantic correctness remains dependent on future adjudication quality controls despite gate passes.
  - Next mandatory step: proceed to protocol-approved downstream evaluation phases without modifying frozen protected items.


- 2026-05-13 (UTC):
  - Current stage: Task 10A main corpus artifact freeze and semantic spot-check.
  - Task executed: Generated SHA256 manifest for main corpus + report artifacts and produced descriptive semantic diagnostics/spot-check reports.
  - Technical result: Added `scripts/make_journal_v1_manifest.py`, `scripts/audit_main_corpus_semantics.py`, artifact manifest, label distribution report, semantic spot-check report, and generation risk report.
  - Corpus freeze status: Main corpus marked frozen under Task 10A lock; edits require explicit correction task.
  - Semantic spot-check outcome: revise recommendations present due to templating risk; evaluation remains blocked.
  - Remaining risks: synthetic templating may reduce semantic diversity and over-regularize label cues.
  - Next mandatory step: approve explicit correction task to address revise findings, then rerun Task 10A checks before any evaluation work.


- 2026-05-13 (UTC):
  - Current stage: Task 10B templating-risk blocker resolution.
  - Task executed: Diagnosed repetitive generation artifacts, implemented deterministic diversification in builder, regenerated main corpus, and reran freeze/audit pipeline.
  - Technical result: Added diagnosis + revision-plan reports and updated semantic audit to report sampled/accept/revise/reject counts with blocker status.
  - Semantic spot-check outcome: sampled=18, accept=18, revise=0, reject=0; blocker cleared.
  - Scientific result: No metrics/baselines/CCT scoring/calibration/results; corpus governance only.
  - Remaining risks: synthetic generation bias can recur if template pools are narrowed in future edits.
  - Next mandatory step: begin only protocol-approved evaluation tasks under lock constraints.


- 2026-05-13 (UTC):
  - Current stage: Task 10D H6 semantic consistency resolution.
  - Task executed: Audited full main corpus for H6 label-evidence contradictions, implemented builder-level conditional evidence generation, regenerated corpus, and reran full audit suite.
  - Technical result: Added `audit_h6_semantic_consistency.py`, diagnosis/correction-plan reports, and PASS H6 consistency audit output.
  - Inconsistency summary: detected 660 pre-correction issues across irreversibility, recoverability, and propagation semantics; corrected via regeneration; post-correction unresolved contradictions = 0.
  - Scientific result: No metrics, baselines, CCT scoring, calibration, or result tables executed.
  - Next mandatory step: proceed only with protocol-approved evaluation tasks now that H6 semantic consistency gate passes.

- 2026-06-04 (UTC):
  - Current stage: Task 10E Journal-v1 label-position and trivial-baseline risk audit.
  - Task executed: Added `scripts/audit_label_position_bias.py`, generated label-position and trivial-shortcut risk reports, added a correction plan, and expanded semantic spot-check sampling to force positive/negative H6 coverage when available.
  - Technical result: `gold_failure_step=s2` occurs in 420/420 traces (100.00%); top `gold_failure_agent=a11` occurs in 55/420 traces (13.10%).
  - Trivial-risk diagnostics: `always_s2=100.00%`, `majority_step=100.00%`, `majority_agent=13.10%`.
  - Gate result: evaluation remains blocked because label-position concentration and trivial step shortcuts exceed the 50% threshold.
  - Scientific result: No empirical hypothesis tested; no metric implementation, baseline implementation, CCT scoring, calibration, or result table added.
  - Caveat: The corpus was not edited because gold labels and dataset composition are protected items; correction requires explicit authorization or a written scientific justification.

- 2026-06-04 (UTC):
  - Current stage: Task 10F Journal-v1 failure-step positional-bias correction.
  - Task executed: Revised `scripts/build_main_corpus.py` to assign semantically grounded failure steps across `s2`, `s3`, `s4`, and supported `s5` traces, regenerated the main corpus, reran audits, and regenerated the manifest.
  - Distribution correction: before correction `s2=420/420 (100.00%)`; after correction `s2=105`, `s3=105`, `s4=105`, `s5=105` out of 420 traces (25.00% each).
  - Trivial-risk diagnostics after correction: `majority_step=25.00%`, `always_s2=25.00%`, `majority_agent=17.86%` (`a8=75/420`).
  - H6 distribution after correction remains balanced: propagation true/false = 210/210, irreversibility true/false = 210/210, recoverability true/false = 210/210; H6 semantic consistency reports PASS.
  - Semantic spot-check outcome: sampled=19, accept=19, revise=0, reject=0; no semantic spot-check blocker.
  - Scientific result: No empirical hypothesis tested; no metric implementation, baseline implementation, CCT scoring, calibration, or result table added.
  - Caveat: The corrected corpus remains synthetic and controlled; future evaluation still requires a separate approved task under the protocol lock.

- 2026-06-04 (UTC):
  - Current stage: Task 10G manual semantic sanity check for corrected failure-step labels.
  - Task executed: Manually inspected six complete records from the regenerated Journal-v1 corpus: one clean record each for `s2`, `s3`, `s4`, and `s5`, plus two perturbed records derived from clean parents.
  - Manual outcome: accept=6, revise=0, reject=0; no semantic sanity blocker detected.
  - Non-s2 grounding result: inspected `s3`, `s4`, and `s5` records align `step_id`, `gold_failure_step`, `gold_failure_agent`, evidence fields, label rationale, and phase-specific trace context.
  - Perturbation result: inspected perturbed records preserve parent clean labels (`s3/a9` and `s5/a5`) without undocumented gold-label changes.
  - Scientific result: No empirical hypothesis tested; no metric implementation, baseline implementation, CCT scoring, calibration, or result table added.
  - Caveat: This is a small qualitative sanity sample, not a substitute for future full adjudication or evaluation-stage controls.

- 2026-06-04 (UTC):
  - Current stage: Task 10H final pre-evaluation corpus gate and shortcut audit consolidation.
  - Task executed: Consolidated Task 10F/10G corrected corpus status into `final_pre_evaluation_gate_report.md`, confirming PR #13 supersedes PR #12 as the canonical corpus-correction provenance.
  - Gate evidence: `gold_failure_step` distribution remains `s2=105`, `s3=105`, `s4=105`, `s5=105`; top `gold_failure_agent=a8` is 75/420 (17.86%).
  - Shortcut diagnostics: `majority_step=25.00%`, `always_s2=25.00%`, `majority_agent=17.86%`; no scenario group or perturbation type collapses to one failure step.
  - H6 and semantic evidence: H6 semantic consistency reports PASS; H6 labels are balanced 210/210 for propagation, irreversibility, and recoverability; semantic spot-check remains 19/0/0 accept/revise/reject; manual sanity check remains 6/0/0 accept/revise/reject.
  - Gate result: final pre-evaluation corpus gate cleared for a future explicitly approved task to implement metric interfaces and trivial baselines.
  - Scientific result: No CCT scoring, calibration, refinement, empirical evaluation, or paper result table added.

- 2026-06-04 (UTC):
  - Current stage: Task 11 metric-interface and trivial-baseline sanity checks.
  - Reasoning decision: implement only accuracy-style metric interfaces and allowed trivial baselines so future CCT evaluation can rely on tested metric plumbing without testing CCT itself.
  - Diagnostic result: standalone trivial baselines did not exceed blocker thresholds on the corrected corpus; the gate is marked passed in the diagnostic report.
  - Caveat: `same_as_parent_for_perturbations` is implemented as a prediction-propagation diagnostic that does not read parent gold labels; without external parent predictions it reports `NA`, avoiding gold-label leakage in the standalone sanity script.
  - Scientific result: no CCT scoring, calibration, refinement variant, ablation, empirical hypothesis test, or paper-ready result table was implemented.

- 2026-06-04 (UTC):
  - Current stage: Task 12 non-CCT baseline diagnostics.
  - Provenance confirmation: active branch at task start was `work`; active HEAD at task start was `12efebd8ede932c6c707feafec4841930c71430a` (`Implement metric interfaces and trivial baseline sanity checks`).
  - PR #15 commit-hash discrepancy note: the user summary referenced `6153857`, while the local active history shows `12efebd`; the GitHub-reported `bde39fc` was not present as the local active HEAD in this workspace. The final active Task 12 commit is recorded in the final handoff/PR metadata because a commit cannot stably contain its own hash.
  - Reasoning decision: implement transparent deterministic baselines that intentionally test whether flat log text and non-gold metadata already identify failure attribution without CCT structure.
  - Diagnostic result: non-CCT diagnostics exceed the 85% blocker threshold, so the report marks evaluation blocked pending corpus/baseline investigation.
  - Scientific result: no CCT graph construction, CCT scoring, calibration, refinement variant, ablation, empirical hypothesis test, or paper-ready result table was implemented.

- 2026-06-04 (UTC):
  - Current stage: Task 12A evaluation-input leakage audit and correction.
  - Root-cause decision: Task 12 100% baselines were caused by raw-record baseline access to target-equivalent `step_id`, `agent_id`, and `handoff_to`, plus the deeper failure-centered single-record corpus representation.
  - Correction: introduced sanitized prediction views that remove gold labels, private metadata, H6 evidence/rationale fields, provenance/control fields, and target-equivalent top-level failure pointers before baseline prediction.
  - Corrected diagnostic result: agent leakage is reduced, but `spectrum_inspired_step` remains at 100% step accuracy and the gate remains blocked because visible content still represents the failure point rather than a full ordered trace.
  - Required next step: approve a corpus-schema correction task for full ordered multi-step trace representation before any CCT implementation.
  - Scientific result: no CCT graph construction, CCT scoring, calibration, refinement variant, ablation, empirical hypothesis test, or paper-ready result table was implemented.

- 2026-06-04 (UTC):
  - Current stage: Task 12B full ordered trace schema migration freeze.
  - Diagnosis: the current corpus is failure-centered because top-level `step_id`, `agent_id`, and `handoff_to` identify the failure point/agent, while visible message/tool fields describe the failure event rather than all candidate steps.
  - Migration decision: existing records are not evaluation-ready; the default future path is regeneration from an approved full-trace builder unless a future audit proves lossless conversion into full ordered traces is possible without fabricating non-failure steps.
  - Frozen requirement: one record must equal one complete ordered multi-step trace with a model-visible `steps` array and private labels/rationales/H6 evidence/provenance outside prediction input.
  - Blocked status: evaluation, CCT graph construction, CCT scoring, calibration, refinement, ablations, and paper-ready result tables remain blocked until full-trace migration is implemented and audited.
  - Scientific result: no empirical hypothesis was tested; no corpus regeneration, CCT scoring, calibration, refinement, ablation, or paper-ready result table was produced.

- 2026-06-04 (UTC):
  - Current stage: Task 13 full ordered trace schema validators and fixtures.
  - Implementation decision: add validation and prediction-view infrastructure before any corpus regeneration so future full-trace data can be audited against the frozen Task 12B migration plan.
  - Fixture decision: use non-experimental fixtures only, including one minimal valid full trace and targeted invalid examples for missing steps, gold-step mismatch, failure-centered top-level fields, and insufficient candidate agents.
  - Blocked status remains unchanged: the current failure-centered corpus is still not evaluation-ready, and CCT graph construction/scoring, calibration, refinement, ablations, and paper-ready result tables remain blocked.
  - Scientific result: no empirical hypothesis was tested; no corpus regeneration, CCT scoring, calibration, refinement, ablation, or paper-ready result table was produced.

- 2026-06-04 (UTC):
  - Current stage: Task 13A full-trace schema infrastructure verification.
  - Provenance confirmation: verification was run on branch `work` starting from HEAD `5e98706cb19e81f7a66726198a6d7d6298a93a82`.
  - Validation evidence: `python scripts/validate_repo.py`, `python scripts/validate_full_trace_schema.py --fixtures-only`, `python scripts/validate_full_trace_prediction_view.py --fixtures-only`, and `python -m pytest` all passed.
  - Fixture outcome: the valid full-trace fixture passed; invalid fixtures failed for expected missing-steps, gold-step-not-in-steps, failure-centered-top-level-fields, and insufficient-agent-candidate reasons.
  - Blocked status remains unchanged: the current failure-centered corpus remains not evaluation-ready, and no corpus generation, CCT graph construction/scoring, calibration, refinement, ablation, or paper-ready result table was performed.

- 2026-06-04 (UTC):
  - Current stage: Task 14 full-trace pilot corpus build and audit.
  - Pilot result: generated 7 clean and 7 perturbed non-final full traces covering all mandatory scenario groups and core perturbation types.
  - Audit result: full-trace schema validation and prediction-view validation passed; semantic spot-check accept/revise/reject counts were 14/0/0.
  - Distribution check: `gold_failure_step` coverage includes `s2`, `s3`, `s4`, and `s5`; H6 labels include at least two true and two false examples for propagation, irreversibility, and recoverability.
  - Caveat: this pilot is non-evidential and must not be used for paper results; the previous failure-centered corpus remains blocked and the full 420-trace corpus was not generated.
  - Scientific result: no empirical hypothesis was tested; no CCT scoring, calibration, refinement, ablation, or paper-ready result table was produced.

- 2026-06-04 (UTC):
  - Current stage: Task 14A full-trace pilot shortcut and semantic-diversity gate.
  - Diagnostic baseline result: all pilot shortcut baselines remained below the 70% review threshold and 85% block threshold when run on sanitized full-trace prediction views.
  - Semantic diversity result: no leakage term hits were detected; gold steps were not systematically more detailed than non-gold steps; gold steps were not the only steps with tool calls/evidence.
  - Readiness decision: `FULL_TRACE_PILOT_READY_FOR_MAIN_CORPUS = yes`, permitting only a future explicitly approved full-trace main-corpus builder task.
  - Caveat: this is pilot-only diagnostic evidence and not a paper result; the old failure-centered corpus remains blocked.
  - Scientific result: no empirical hypothesis was tested; no full 420-trace corpus generation, CCT scoring, calibration, refinement, ablation, or paper-ready result table was produced.

## Task 14B — Diagnostic sufficiency and candidate plausibility audit

- Current stage: Task 14B full-trace pilot diagnostic sufficiency audit.
- Clean-trace decisions: accept=0, revise=7, reject=0.
- Perturbed-trace decisions: accept=0, revise=7, reject=0.
- Gold-step inferability from visible prediction-view evidence: 0 of 7 clean traces; too-obvious shortcut cases: 0; not-inferable cases: 7.
- Reasoning decision: the pilot should not be scaled even though Task 14A shortcut baselines stayed below threshold, because the visible step content is overly templated and does not provide distinctive causal evidence for the private gold attribution point.
- Repeated-template caveat: input messages, output messages, tool outputs, evidence structures, role order, and handoff chains are too uniform for a diagnostically meaningful benchmark.
- Readiness decision: `FULL_TRACE_PILOT_DIAGNOSTICALLY_READY = no`; `FULL_TRACE_MAIN_CORPUS_GENERATION_ALLOWED = no`.
- Scientific result: no empirical hypothesis was tested; no full 420-trace corpus generation, CCT scoring, calibration, refinement, ablation, or paper-ready result table was produced.

## Task 14C — Revised pilot diagnostic sufficiency

- Current stage: Task 14C full-trace pilot builder revision for diagnostic sufficiency.
- Before revision from Task 14B: clean accept=0/revise=7/reject=0; perturbed accept=0/revise=7/reject=0; gold-step inferability=0/7 clean traces.
- After revision: clean accept=7/revise=0/reject=0; perturbed accept=7/revise=0/reject=0; gold-step inferability=7/7 clean traces; too-obvious=0/7; not-inferable=0/7.
- Reasoning decision: the pilot now uses scenario-specific visible causal evidence, such as cap-transfer softening, evidence weighting, channel authorization, weak-estimate dependency, missed correction window, date-role mismatch, and source-ranking collapse.
- Caveat: the pilot remains non-final and non-evidential; full main-corpus generation requires explicit future approval and broader structural diversity.
- Scientific result: no empirical hypothesis was tested; no full 420-trace corpus generation, CCT scoring, calibration, refinement, ablation, or paper-ready result table was produced.

## Task 15 — Full-trace main corpus generation and audit

- Current stage: Task 15 full-trace main corpus generation and audit.
- Provenance before generation: branch `work`; pre-generation HEAD `a23c14051411338d8929ae0971ec76e068ce0828`; Task 14C pilot files/reports existed and Task 14C validation commands passed.
- Generated counts: clean=84, perturbed=336, total=420.
- Distribution decision: gold failure steps and agents are balanced across s2/a2, s3/a3, s4/a4, and s5/a5 at 105 records each in the full all-traces file.
- Audit outcome: diagnostic sufficiency accept=420/revise=0/reject=0; candidate plausibility accept=420/revise=0/reject=0; lexical leakage hits=0.
- Shortcut-baseline outcome: all diagnostic baselines remained below the 70% review threshold and 85% block threshold.
- Caveat: this is corpus-generation and audit evidence only; it is not an empirical hypothesis test and does not compare CCT or any method.
- Scientific result: no CCT scoring, calibration, refinement, ablation, empirical hypothesis test, or paper-ready result table was produced; the old failure-centered corpus remains blocked.

## Task 16A — CCT graph artifact reviewability

- Current stage: generated-artifact reviewability and manifest freeze for full-trace CCT graph construction.
- Diff diagnosis: the current branch's prior-commit diff did not contain Task 16 CCT graph artifacts, but the required inspection commands were run and the newly generated full local CCT artifacts measured approximately 1.1M for `cct_graphs.jsonl` and 916K for `cct_features.jsonl`.
- Reasoning decision: keep code, tests, scripts, compact samples, compact Markdown reports, and manifests in Git; exclude full generated JSONL artifacts from normal Git because they are reproducible and can make PRs unreviewable.
- Reproducibility decision: full artifacts are regenerated by `python scripts/build_cct_graphs_full_trace.py` and validated by `python scripts/validate_cct_graphs_full_trace.py`; sample files provide reviewable examples of one clean and one perturbed trace graph plus corresponding feature rows.
- Caveat: graph construction and structural feature extraction are preprocessing artifacts only; feature rows are not predictions, scores, rankings, calibration outputs, refinement outputs, ablations, empirical tests, or paper-ready results.
- Scientific result: no empirical hypothesis was tested; no scoring, ranking, calibration, refinement, ablation, or paper-ready result table was produced.

## Task 16B — CCT structural feature variance and shortcut-risk audit

- Current stage: pre-scoring structural feature audit.
- Feature rows audited: 2,100 rows from 420 regenerated full-trace CCT graphs.
- Reasoning decision: compute descriptive variance, missingness, uniqueness, numeric ranges, position-shortcut checks, duplicate-vector checks, graph-size constancy, and private-field leakage checks without using gold labels as targets.
- Audit outcome: no private/gold fields were detected in graph or feature payloads; constant features and position-determined fields were explicitly identified; graph node count and edge count were constant at 5 and 12 respectively.
- Shortcut caveat: `agent_id`, `agent_role`, `order_index`, and `step_id` perfectly determine step position in the current fixed five-step corpus shape, and duplicate structural vectors exceed the warning threshold.
- Readiness decision: `ready_with_shortcut_warnings`; future scoring remains a separate authorization task and must acknowledge the documented warnings before proceeding.
- Scientific result: no empirical hypothesis was tested; no scoring, ranking, evaluation, calibration, refinement, ablation, or paper-ready result table was produced.

## Task 17 — Uncalibrated CCT scoring protocol freeze

- Current stage: protocol-only freeze before any CCT scoring execution.
- Provenance: branch `work`; active repository commit inspected at task start was `efce2682977950580d47fcdd2c45e21dfe0cba42`.
- PR discrepancy note: prior local handoff text referenced `276467...`, while the user reports GitHub PR #21 showed `38b9c46`; this task records the active local commit actually inspected as `efce2682977950580d47fcdd2c45e21dfe0cba42`.
- Reasoning decision: freeze `cct_primary_no_position` and diagnostic variants before performance is visible, excluding high-risk position/identity features from the primary formula because Task 16B found shortcut warnings.
- Guardrail decision: forbid gold/private/provenance fields, scenario/perturbation as score features, trace/case IDs as score features, learned parameters, LOSO, grid search, calibration, and post-performance adjustment.
- Future blocker rules: claims must be weakened or blocked if position diagnostics match or dominate primary CCT, flow-only is near random, non-CCT baselines exceed CCT, or robustness fails under perturbation.
- Scientific result: no empirical hypothesis was tested; no scoring, ranking execution, evaluation, calibration, refinement, ablation, or paper-ready result table was produced.

## Task 18 — Frozen uncalibrated CCT diagnostic run

- Current stage: controlled initial diagnostic execution of the Task 17 frozen uncalibrated CCT protocol.
- Provenance: branch `work`; execution started from HEAD `a19596a44cdd0c54739bb8141c8c9af0a3b0c3c3`; `configs/cct_scoring.yaml` SHA256 before execution was `053f19066923d8d22d27b22727e75876f939f2a60480484c4028eabd07ad0855`.
- Variants executed exactly as frozen: `cct_primary_no_position`, `cct_flow_only`, `cct_context_only`, and high-risk diagnostic `cct_with_position_features`.
- Diagnostic result: primary CCT step/agent/tuple accuracy was 0.114286; flow-only was 0.250000; context-only was 0.028571; with-position was 0.250000.
- Breakdown: primary clean step accuracy was 0.107143 and perturbed step accuracy was 0.116071; primary scenario step accuracy ranged from 0.000000 to 0.450000; primary perturbation step accuracy ranged from 0.071429 to 0.178571.
- Interpretation: H1 remains unsupported in this diagnostic run because primary CCT is near random/plausible-candidate baseline; H2 remains unsupported because majority/always/last-step diagnostics match or exceed primary CCT; H6 remains future structural analysis only.
- Caveat: gold labels were accessed only for evaluation after scoring; scoring modules operate on visible CCT feature rows and reject private/gold fields.
- Scientific result: diagnostic-only evidence; no calibration, grid search, LOSO, refinement, ablation, statistical test, or paper-ready result table was produced.

## Task 18A — Frozen uncalibrated CCT diagnostic error analysis

- Current stage: descriptive error analysis of Task 18 diagnostics without protocol changes.
- Provenance: branch `work`; analysis started from HEAD `1f0238278e4b152eda03184390346eaf1c8ac8e6`; Task 18 HEAD reference is `2695aa3e8c06936270b40a1b6d93eee41f55f87b`; `configs/cct_scoring.yaml` SHA256 remained `053f19066923d8d22d27b22727e75876f939f2a60480484c4028eabd07ad0855`.
- Error analysis outcome: primary predicted steps were distributed across all steps but remained inaccurate; flow-only collapsed to `s2` for all traces and with-position collapsed to `s4` for all traces, both reaching 0.250000 through single-position/default behavior.
- Tie analysis: primary tied-top rate was 0.285714; most primary errors were non-tied wrong score separations, so ties are not the main failure driver.
- Feature dominance: `tool_output_token_count` and `output_token_count` dominated average primary contributions; scores were separated rather than degenerate, but separation favored wrong steps.
- Ranking diagnostics: primary top-2 containment was 0.207143, top-3 containment was 0.407143, mean gold rank was 3.600000, and median gold rank was 4.000000.
- Interpretation: H1 and H2 remain unsupported after error analysis; before calibration, the next task should inspect feature design and graph-shape assumptions for non-position-derived causal/flow descriptors and excessive graph uniformity.
- Scientific result: interpretive diagnostic analysis only; no calibration, grid search, LOSO, refinement, ablation, statistical test, protocol change, or paper-ready result table was produced.

## Task 18B — CCT feature semantics and descriptor-design audit

- Current stage: feature-design feasibility audit after Task 18A error analysis.
- Reasoning decision: do not calibrate or tune the underperforming frozen scorer; first inspect whether the current feature layer has enough semantic causal-flow information.
- Current feature diagnosis: the feature set is dominated by identifiers/position proxies, constant evidence/tool cardinalities, position-derived flow fields, and content-volume proxies; it lacks direct descriptors for constraint shifts, ignored evidence, tool-output mismatch, unresolved caveats, visible correction/recovery attempts, and cross-agent causal dependency.
- Proposal: define prediction-view-safe candidate descriptors, with deterministic extraction preferred and any LLM/judge-based descriptor limited to a future diagnostic variant until separately locked and audited.
- Recommended next task: protocol-only descriptor extraction specification and sample-only prototype for deterministic `handoff_constraint_shift_indicator`, `evidence_ignored_indicator`, and `downstream_reference_to_prior_output`, followed by leakage/variance/shortcut audits before scoring is reconsidered.
- Scientific result: design audit only; H1/H2 remain unsupported from Task 18/18A, and no scoring, calibration, grid search, LOSO, refinement, ablation, statistical test, or paper-ready result table was produced.

## Task 18C — Sample-only causal-flow descriptor prototype

- Current stage: protocol-safe sample prototype for deterministic causal-flow descriptors.
- Sample: 14 traces, 70 step rows, selected as first clean and first perturbed trace per scenario group.
- Implemented descriptor subset: `handoff_constraint_shift_indicator`, `evidence_ignored_indicator`, and `downstream_reference_to_prior_output`, extracted only from sanitized prediction views.
- Prototype results: handoff shift positive=2/negative=68; evidence ignored positive=4/negative=66; downstream reference positive=56/negative=14; leakage audit passed with no private/gold fields in descriptor output.
- Readiness decision: `DESCRIPTOR_PROTOTYPE_READY_FOR_FULL_AUDIT = yes`; `DESCRIPTOR_READY_FOR_SCORING = no`.
- Recommended next task: full-corpus descriptor extraction and leakage/variance/shortcut audit only, with no scoring until a later protocol revision is explicitly approved.
- Scientific result: descriptor feasibility preview only; no descriptor-to-gold comparison, scoring, ranking, calibration, grid search, LOSO, refinement, ablation, statistical test, or paper-ready result table was produced.
