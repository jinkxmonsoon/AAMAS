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
