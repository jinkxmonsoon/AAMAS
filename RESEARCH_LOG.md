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
