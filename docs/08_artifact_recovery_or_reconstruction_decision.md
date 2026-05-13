# 08 — Artifact Recovery vs Reconstruction Decision Gate

## Purpose
Define the formal gate for proceeding after Task 1B established that BRACIS v0 reproduction is blocked due to missing artifacts.

## Path A — Recover BRACIS v0 (Preferred if feasible soon)

### Required files
- Raw trace files used in BRACIS v0.
- Gold-label files and label provenance notes.
- Perturbation definitions and generated perturbation artifacts.
- Scenario metadata and split definitions.
- Calibration raw outputs.
- Robustness raw outputs.
- Prior result CSV/JSON files and generated tables/figures source artifacts.
- Original scripts/notebooks used in submitted runs.

### Expected source locations
- Original BRACIS project storage (team drive / archival repo / author machines).
- Submission package attachments or supplementary material stores.
- Historical experiment directories referenced by lead authors.

### Responsible person
- Responsible: **Task Lead (TL) with corresponding BRACIS submitting author**.

### Deadline / status
- Status: **Pending retrieval**.
- Retrieval deadline: **2026-05-27 UTC** (two-week gate from decision date).

### Reproduction readiness criteria
Path A is READY only when:
1. All required artifact classes are present and hash-recorded.
2. Manifest/inventory classify experimental artifacts > 0 and complete required categories.
3. Repository still reports BRACIS v0 as reported-only until reproduction reruns are complete.

## Path B — Reconstruct Journal v1 (Fallback if Path A misses deadline)

### Dataset version
- New dataset/version name: **BRACIS-Journal-v1**.

### Separation from BRACIS v0
- Treat BRACIS v0 as historical motivation only.
- Do not present BRACIS v0 numbers as reproduced evidence.
- Keep separate manifests, labels, splits, and result namespaces.

### Provenance requirements
- Full source tracking for every trace/label/perturbation artifact.
- Immutable hashing for all data and outputs.
- Versioned changelog entries for every protocol-impacting change.

### Required schema
- Formal CCT trace schema in `docs/03_cct_formal_schema.md` must be concretized before data generation/import.

### Required label protocol
- Explicit labeling instructions, adjudication policy, and quality checks.

### Required perturbation protocol
- Deterministic perturbation definitions with seed policy, logging, and leakage controls.

### Required baseline plan
- Pre-registered baseline set and comparison rules before experiments.

### Implications for claims
- Journal claims must be based on v1 reproduced evidence only.
- BRACIS v0 claims become contextual/historical narrative, not empirical support.

## Decision table (Path A vs Path B)

| Criterion | Path A: Recover BRACIS v0 | Path B: Reconstruct Journal v1 |
|---|---|---|
| Validity | Strong continuity with submitted artifact if complete recovery succeeds | Stronger control if redesigned under locked protocol |
| Reproducibility | High if original bundle complete; fragile if partial recovery | Potentially highest if built natively with full provenance |
| Time cost | Potentially low if artifacts quickly available | Higher due to rebuild and relabeling overhead |
| Leakage risk | Unknown until old pipeline is audited | Controllable via pre-registered safeguards |
| Overfitting risk | Unknown prior choices may be hard to audit | Lower if calibration/baselines are preregistered |
| Editorial defensibility | Good if exact recovery + rerun achieved | Good if transparent rebuild and strict claim discipline |
| Applied Intelligence support | Good if recovered evidence is reproducible | Good if v1 evidence is rigorous and complete |

## Formal recommendation
1. Choose **Path A first** if original artifacts can be provided by **2026-05-27 UTC**.
2. If not available by deadline, switch to **Path B**.
3. Under either path, BRACIS v0 remains **not reproduced** until reruns complete.
4. If Path B is selected, BRACIS v0 is historical motivation only, not empirical evidence for journal claims.


## Path decision update
- Decision date: 2026-05-13 (UTC).
- Current path: **Path B activated for protocol design** due to unavailable BRACIS v0 artifacts in Task 2A recovery attempt.
- Path A may be reconsidered only if original artifact bundle is later recovered and verified.
