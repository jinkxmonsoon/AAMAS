# 07 — BRACIS Desk-Reject Artifact Audit (Frozen Reference)

## Artifact registration
- Artifact name: **BRACIS desk-reject v0**
- Status: **Rejected submission; not journal-grade evidence**
- Role: **Frozen reference artifact for reconstruction in journal extension**
- Audit mode: **Document-only audit. No experiment, metric, baseline, or dataset execution/modification performed.**

## Scope and evidence boundary
This audit distinguishes between:
1. **Reported evidence** (claims/numbers stated in the submitted manuscript), and
2. **Reproduced evidence** (numbers re-derived from this repository).

Current repository state for this task: **no reproduced evidence available**. All empirical items below are therefore marked **Not yet reproduced**.

## Claim classification

### A) Supported by current reported evidence (inside manuscript narrative)
1. CCT is presented as a structured collaboration trace representation for diagnostic analysis.
   - Classification basis: internally coherent with manuscript framing.
   - Journal caveat: must remain operational/engineering claim unless independently reproduced.

2. CCT “causal” language is operational (dependency/evidence-flow), not formal causal identification.
   - Classification basis: acceptable if explicitly bounded in wording.
   - Journal caveat: terminology must be constrained and consistently restated.

### B) Partially supported
3. Controlled trace bank exists with clean and perturbation-derived variants.
   - Reported statement: 50 clean diagnostic cases and 200 perturbation-derived variants.
   - Partiality reason: count/split provenance and generation logs not yet revalidated in this repo.

4. Leakage audit is reported.
   - Partiality reason: method/results are reported, but no local reproduction yet.

5. LOSO-based weight calibration with selected weights (C=0.40, I=0.10, P=0.50).
   - Partiality reason: plausible as reported result but not re-executed; hyperparameter search boundary not yet audited here.

6. v1 calibrated structural backbone improves controlled attribution quality.
   - Partiality reason: reported outcome exists; sensitivity and interval robustness not independently rerun.

7. Deterministic refinement variants (V2A/V2B/V2C) show limited/conditional gains.
   - Partiality reason: effect heterogeneity and failure modes not independently validated.

8. Robustness under paraphrase/tool truncation/partial observability/textual distraction.
   - Partiality reason: robustness conditions are reported but stress distribution and confidence stability unverified.

### C) Unsupported (in current repository as of audit)
9. Any numerical claim as **reproduced** by this repository.
10. Any claim of external transfer strength as confirmed.
11. Any claim that current code reproduces BRACIS tables/figures.

### D) Risky for journal review
12. Over-strong “causal” wording without explicit operational qualification.
13. Generalization claims from synthetic/controlled settings to broad real-world collaboration failures.
14. External-paradigm comparison claims absent matched protocol and calibration fairness disclosure.
15. Robustness claims lacking interval estimates, multiplicity control, and scenario-balance diagnostics.

### E) Must be removed or weakened (until reproduced)
16. Any definitive superiority claim (absolute or broad).
17. Any external transfer claim phrased as validated rather than exploratory.
18. Any claim implying leakage immunity without reproduced audit artifacts.

## Limitations explicitly tracked from paper narrative
- Synthetic data dependence.
- Gold-label governance burden and potential label noise.
- Attribution irreversibility/path dependence concerns.
- Error propagation along structured traces.
- Unknown out-of-domain generalization.

## Reproduction Required Before Journal Claims (Checklist)
- [ ] Dataset count verification (clean + perturbation-derived counts and splits)
- [ ] Schema validation reproduction
- [ ] Gold-label validation and inter-annotator checks (if available)
- [ ] Leakage audit reproduction
- [ ] Metric reproduction
- [ ] LOSO calibration reproduction (including search boundary)
- [ ] Main table reproduction
- [ ] Robustness reproduction
- [ ] Scenario-level breakdown reproduction
- [ ] Statistical test and confidence interval reproduction

## Audit conclusion
BRACIS desk-reject v0 is now formally frozen as a reference artifact for reconstruction. No claim should be promoted to journal-grade evidence until reproduced under the protocol-first repository controls.


## Task 0.5B update
Task 0.5B completed row-level numerical extraction into `results/reports/bracis_v0_reported_results.md`.
Reproduction remains pending: all extracted values are still marked as not reproduced in this repository.
Major journal-risk flags remain active, especially low irreversibility and propagation performance in reported results.
