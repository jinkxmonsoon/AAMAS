# CCT Backbone Decision Synthesis

## Scope

Task 25 is a scientific backbone decision only. It does not implement code, features, scoring, ranking, calibration, grid search, LOSO, ablation, statistical tests, empirical hypothesis tests, corpus changes, gold-label changes, or paper-ready result tables.

## Selected path

- Selected path: **Path B — stop empirical method optimization and pivot the article toward protocol-first benchmark construction, full-trace representation, leakage/shortcut audits, causal-flow representation diagnostics, and negative findings.**
- Path A status: rejected because redesigned features do not provide sufficient representation diversity for a new frozen scoring protocol v2.
- Path C status: not selected because the current artifact is still viable as a protocol/benchmark/diagnostic-representation paper even though it is not viable as a performance-superiority method paper.

## Evidence synthesis across Tasks 18–24A

### Task 18 diagnostic scoring outcome

Task 18 produced a frozen uncalibrated CCT diagnostic run, but the consolidated diagnostic record states that H1 and H2 were unsupported under the current frozen uncalibrated scoring/features. Diagnostic baselines were not outperformed in a way that permits a superiority claim. The failure diagnosis was not a simple tie-breaking issue; it reflected weak/non-discriminative proxy-heavy features.

### Task 18 reproducibility boundary

The frozen scoring configuration expected at `configs/cct_scoring.yaml` remains absent from the current checkout. Task 20F adjudicated PR #22 candidate hashes as non-matching the expected frozen hash. Task 18 is therefore recorded as diagnostic evidence with outputs, but `NOT_REPRODUCIBLE_FROM_CURRENT_CHECKOUT` and not paper-ready empirical evidence.

### Task 18A error analysis

Task 18A concluded that the failure was not mainly due to ties. Wrong steps could be separated ahead of the target by context/tool-output contributions, indicating a representation and feature-validity problem rather than a calibration problem.

### Task 18B–18F descriptor findings

Task 18B classified the current feature layer as dominated by position/identity proxies, content-volume proxies, and coarse cardinality fields. Tasks 18C/18D showed that causal-flow descriptors can be prototyped safely. Task 18E/18F showed descriptor augmentation was reproducible and leakage-safe, but readiness stayed conservative: descriptor features were not ready for protocol revision or scoring, and duplicate-row reduction was only modest.

### Task 20–23 causal-flow edge findings

Tasks 20–22 specified and stress-tested richer non-position causal-flow edges under prediction-view-only constraints. Task 23 ran a representation-only full-corpus audit of the strongest three edge types: `downstream_dependency_edge`, `tool_alignment_edge`, and `cross_agent_dependency_edge`. The audit processed 420 traces, generated 2,385 strong edges, and leakage remained PASS. However, template sensitivity persisted, so the evidence supported graph redesign integration only, not scoring.

### Task 24 graph redesign findings

Task 24 integrated the three strongest causal-flow edge types into redesigned CCT graph artifacts. Graph signature uniqueness improved from 1 to 6, and duplicate graph signatures decreased from 419 to 414. This is a measurable representation improvement, but it is modest and remains representation-only.

### Task 24A feature degeneracy findings

Task 24A extracted redesigned graph features and found 420 feature rows, 13 representation-only feature names, leakage PASS, 6 unique feature vectors, and 414 duplicate feature vectors. Several features remained constant: `tool_alignment_edge_count`, `cross_agent_dependency_edge_count`, `cross_agent_dependency_count`, and `tool_alignment_relation_count`. Readiness remained `CCT_REDESIGNED_FEATURES_READY_FOR_PROTOCOL_REVIEW = no` and `CCT_REDESIGNED_FEATURES_READY_FOR_SCORING = no`.

## Decision answers

- Did redesigned CCT features materially improve representation diversity? **No.** They improved diversity slightly relative to the base graph signature, but 6 unique vectors across 420 traces and 414 duplicate vectors are too degenerate to justify scoring.
- Is a new scoring protocol scientifically justified now? **No.** Scoring remains blocked by feature degeneracy and missing frozen-config provenance.
- Should immediate calibration remain blocked? **Yes.** Calibration before representation validity would optimize a still-degenerate feature layer.
- Should the article continue as a performance-oriented method paper? **No.** Current evidence does not support performance-superiority claims.
- Should the article pivot to a protocol/benchmark/diagnostic-representation paper? **Yes.** The strongest scientific backbone is protocol-first benchmark construction, leakage/shortcut governance, representation diagnostics, and negative findings.

## Current hypothesis status

- H1: unsupported under current evidence.
- H2: unsupported under current evidence.
- H3: blocked because calibration before feature validity is premature.
- H4: blocked because broader method claims are not supported.
- H6: open but unsupported by scoring evidence.
