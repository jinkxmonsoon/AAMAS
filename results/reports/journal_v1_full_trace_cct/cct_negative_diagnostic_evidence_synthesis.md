# CCT Negative Diagnostic Evidence Synthesis

## Scope and source availability

This synthesis consolidates Tasks 18 through 18F as a scientific decision gate. It does **not** run scoring, ranking, calibration, grid search, LOSO, refinement, ablation, statistical tests, corpus edits, gold-label edits, or paper-ready result-table generation.

The current checkout contains the Task 18F descriptor-augmented reports and manifest, but the earlier Task 18/18A/18B/18C/18D source report files named below are not present in this repository state:

- `results/reports/journal_v1_full_trace_cct/cct_uncalibrated_diagnostics_report.md`
- `results/reports/journal_v1_full_trace_cct/cct_uncalibrated_error_analysis.md`
- `results/reports/journal_v1_full_trace_cct/cct_uncalibrated_feature_dominance_report.md`
- `results/reports/journal_v1_full_trace_cct/cct_feature_semantic_audit.md`
- `results/reports/journal_v1_full_trace_cct/cct_descriptor_full_corpus_variance_report.md`
- `docs/14_cct_uncalibrated_scoring_protocol.md`
- `docs/15_cct_causal_flow_descriptor_spec.md`

Therefore, this file records the consolidated qualitative conclusions supplied by the Task 19 scientific context and cross-checks only the available Task 18F artifacts in the current checkout. Numeric claims from absent reports are intentionally not reconstructed.

## Consolidated evidence by task

### Task 18 — Frozen uncalibrated CCT scoring

- Primary conclusion: H1 and H2 are unsupported under the current frozen uncalibrated scoring/features.
- The task-level diagnostic record states that frozen uncalibrated CCT scoring underperformed diagnostic baselines.
- Variant results did not rescue the method enough to support a superiority or robustness claim.
- Diagnostic baseline comparison is negative for current CCT scoring: the current feature/scoring combination does not provide evidence of CCT advantage.
- Claim implication: no performance-superiority claim is allowed from Task 18 evidence.

### Task 18A — Error analysis, ties, and ranks

- The task-level diagnostic record states that failure was not mainly due to ties.
- The dominant issue was weak/non-discriminative features rather than tie-breaking alone.
- Rank analysis indicated that wrong steps were often separated ahead of the target by current context/tool-output contributions.
- Scientific interpretation: the failure is a representation/feature-validity problem before it is an optimization or calibration problem.

### Task 18B — Feature taxonomy and dominance

- The task-level diagnostic record states that the current feature layer mostly consists of:
  - position/identity proxies;
  - content-volume proxies;
  - coarse cardinality fields.
- These feature families are insufficiently causal for reliable full-trace failure attribution.
- Scientific interpretation: calibrating proxy-heavy features risks improving fit to artifacts rather than improving causal attribution validity.

### Task 18C/18D — Causal-flow descriptor feasibility

- The task-level diagnostic record states that causal-flow descriptors were prototyped/extracted safely.
- Descriptor feasibility is positive at the representation/audit layer: descriptors can be generated without turning them into scoring inputs.
- Feasibility is not equivalent to readiness for protocol revision or scoring.

### Task 18E — Descriptor-augmented feature readiness

- Available Task 18F-regenerated reports show descriptor-augmented rows retain expected coverage: `2100/2100` join completeness.
- Descriptor leakage status remains `PASS`.
- Current readiness is conservative:
  - `AUGMENTED_FEATURE_LAYER_READY_FOR_PROTOCOL_REVISION = no`
  - `AUGMENTED_FEATURE_LAYER_READY_FOR_SCORING = no`
- Descriptor augmentation only modestly reduced duplicate structural feature rows according to the Task 19 scientific context, so descriptor scoring remains premature.

### Task 18F — Artifact policy and reviewability

- The full descriptor-augmented JSON is treated as a generated local artifact, not a normal Git-reviewed blob.
- The compact tracked sample remains in Git for review.
- The full artifact is reproducible with `python scripts/build_cct_descriptor_augmented_features.py`.
- The manifest records full/sample hashes, line counts, byte sizes, generation command, expected row count, join completeness, leakage status, and readiness decisions.

## Hypothesis status after consolidation

- H1: unsupported under current frozen uncalibrated scoring/features.
- H2: unsupported under current frozen uncalibrated scoring/features.
- H3: blocked because calibration before feature validity is premature.
- H4: blocked because the current evidence does not support moving to broader method claims.
- H6: open but unsupported by scoring evidence.

## Failure diagnosis

The current CCT scoring path failed because the available feature/scoring layer does not yet encode sufficiently discriminative causal-flow evidence. The negative evidence points to a representation problem: proxy-heavy and coarse features can separate the wrong step, and descriptor augmentation is not yet strong enough to justify immediate scoring. This means the next methodological work should improve causal graph/feature extraction before calibration.

## Decision consequence

Immediate calibration and descriptor-scoring integration should remain blocked. The scientifically preferred next direction is to redesign CCT graph/feature extraction around richer non-position causal-flow edges before any calibration or new scoring run is authorized.
