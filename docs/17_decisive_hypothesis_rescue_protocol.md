# 17 — Decisive CCT Hypothesis-Rescue Experiment Protocol v1

## Scope and non-execution lock

This document defines a future experiment protocol only. It does **not** run scoring, ranking, calibration, weight tuning, grid search, LOSO, ablation, statistical tests, corpus/gold-label changes, scoring-config restoration, or paper-ready result tables.

## Motivation

Tasks 18–24A leave H1/H2 unsupported under the current implemented CCT feature layers. Task 24A found that redesigned CCT graph features produced only 6 unique feature vectors across 420 traces, with 414 duplicate vectors. This does not falsify the CCT thesis by itself; it shows that the current featureization is too weak. The rescue experiment asks whether a prediction-view-safe, **step-level** causal-flow CCT representation can add attribution signal beyond trivial and flat-log baselines.

## Hypotheses

- **H1-R:** A prediction-view-safe CCT representation with step-level causal-flow features improves failure-step attribution over trivial and flat-log baselines in the controlled full-trace corpus.
- **H2-R:** Causal-flow graph features add diagnostic signal beyond flat textual/metadata baselines under identical prediction-view constraints.
- **H6-R:** Causal-flow relation patterns provide meaningful diagnostic signal for propagation, irreversibility, or recoverability only if evaluated without private-label leakage.

## Dataset and corpus version

- Dataset: `BRACIS-Journal-v1` full-trace controlled corpus.
- Corpus file: `data/processed/journal_v1_full_trace/main_full_trace_all.jsonl`.
- Expected trace count: 420.
- Evaluation unit for H1-R/H2-R: candidate step within a trace.
- Evaluation unit for H6-R, only if separately enabled: trace-level or candidate-step relation to propagation, irreversibility, or recoverability labels.

## Prediction-view input contract

All feature extraction and baseline inputs must consume only `make_full_trace_prediction_view(record)` from `src/cctdiag/io/full_trace_views.py`. Private labels and provenance may be loaded only after predictions are frozen for evaluation. Scenario, perturbation, and case-variant metadata are audit-only stratification fields and must not be used as model features.

## Forbidden fields

The following fields are forbidden as feature, baseline, scoring, ranking, or model inputs:

- `private_labels`
- `gold_failure_step`
- `gold_failure_agent`
- `gold_irreversibility`
- `gold_propagation`
- `gold_recoverability`
- H6 private evidence fields, including propagation/irreversibility/recovery rationales
- `label_rationale`
- `provenance`
- `scenario_group`
- `perturbation_type`
- `case_variant`
- `correctness`
- `score`
- `rank`

## Split and evaluation policy

- Primary protocol: deterministic full-corpus evaluation over the 420 controlled traces, with predictions generated from prediction views and labels revealed only after prediction freeze.
- Optional generalization check, if later authorized: deterministic grouped split by clean parent trace so clean/perturbed siblings never cross train/test boundaries.
- No LOSO, calibration, grid search, or learned weight tuning is authorized by this protocol draft.
- Random components are permitted only for `random_step_seeded` and must use seed `20260605`.

## Feature-family taxonomy

### Trace-level features

Trace-level summaries may describe the whole visible trace, such as total visible tool-output count or total causal-flow edge count. Trace-level features alone must not be used for candidate-step attribution unless transformed into candidate-relative features.

### Step-level candidate features

Step-level candidate features are the required rescue focus. They may include incoming/outgoing causal-flow degree for each candidate step, candidate step participation in downstream dependency edges, tool-alignment relations, cross-agent dependency relations, non-adjacent dependency counts, visible handoff participation, and candidate-local visible text-free structural indicators.

### Graph-level features

Graph-level features may summarize the prediction-view-safe CCT graph, including graph density, edge-type diversity, duplicate graph signature, and causal-flow edge counts. These are diagnostic covariates, not sufficient standalone candidate attribution features.

### Edge-level features

Edge-level features may encode prediction-view-safe causal-flow relation properties: edge type, source/target candidate step IDs, adjacency distance, source/target visible field families used, tool-output/output-message relation flag, and cross-agent relation flag. Edge text content must be bounded to visible fields only.

## Allowed CCT feature families

- Old structural CCT features, diagnostic-only if available and prediction-view safe.
- Strong-edge step-level features from `downstream_dependency_edge`, `tool_alignment_edge`, and `cross_agent_dependency_edge`.
- Causal-flow relation features derived from visible source/target step relations.
- Visible text-free graph features: counts, degrees, distances, edge-type diversity, and candidate-relative topology.
- Optional lightweight visible textual relation features, only if leakage audit confirms they use visible messages/tool outputs and do not encode scenario/perturbation/private labels.

## Required baselines

- `majority_step`
- `always_s2`
- `random_step_seeded`
- `first_step`
- `last_step`
- `flat_log_lexical_baseline`
- `flat_log_text_similarity_baseline`, if feasible without private-label leakage
- `non_cct_visible_heuristic_baseline`

## Required CCT variants

- `cct_structural_old_features_diagnostic_only`
- `cct_strong_edge_step_level_features`
- `cct_causal_flow_relation_features`
- `cct_visible_text_free_graph_features`
- `cct_lightweight_visible_textual_relation_features_optional`

## Metrics

### H1-R metrics

- Primary: failure-step accuracy.
- Secondary: macro step accuracy by scenario group and perturbation type as audit-only stratification after predictions are frozen.
- Secondary: candidate-step rank may be recorded only if the future implementation naturally emits ordered scores, but no ranking task is authorized in this protocol draft.

### H2-R metrics

- Primary: failure-step accuracy of causal-flow CCT variant versus the strongest flat-log baseline under identical prediction-view inputs.
- Secondary: macro improvement over flat-log baseline by scenario/perturbation audit strata after predictions are frozen.

### H6-R metrics

Only if H6 evaluation is separately enabled and leakage-safe:

- Propagation label accuracy or macro-F1.
- Irreversibility label accuracy or macro-F1.
- Recoverability label accuracy or macro-F1.
- H6 metrics must be reported separately from step/agent attribution metrics.

## Acceptance criteria

### H1-R

H1-R is supported only if the best pre-specified CCT rescue variant exceeds the strongest trivial or flat-log baseline by at least **+10 percentage points in failure-step accuracy** or by a pre-specified macro improvement of at least **+0.10 absolute macro step accuracy**. The threshold must not be changed after running.

### H2-R

H2-R is supported only if causal-flow CCT features outperform the strongest flat-log baseline under identical prediction-view inputs by the same pre-specified margin. If a flat-log baseline wins or ties within margin, H2-R is unsupported.

### H6-R

H6-R is supportable only if H6 labels are evaluated without H6 private evidence, label rationale, provenance, scenario/perturbation inputs, or leakage. H6-R must meet a separately pre-specified macro-F1 or accuracy margin over a non-CCT visible baseline before any H6 claim is allowed.

## Failure criteria and hard blockers

- If candidate-step feature-vector degeneracy exceeds **50% duplicate candidate-step vectors**, do not run scoring.
- If any feature family is constant across more than **95%** of candidate rows, it must be excluded or the run is blocked until redesigned.
- If leakage audit fails, do not run scoring.
- If any baseline or CCT variant uses forbidden fields, invalidate the run.
- If trivial baselines exceed or tie CCT within the pre-specified margin, H1-R/H2-R remain unsupported.
- If results depend primarily on step position or agent identity, claims are blocked.
- If `configs/cct_scoring.yaml` remains absent, this rescue experiment must use a new explicitly versioned rescue config and must not claim reproduction of Task 18.

## Readiness decision

- `RESCUE_EXPERIMENT_PROTOCOL_READY_FOR_IMPLEMENTATION = yes`
- `RESCUE_EXPERIMENT_READY_TO_RUN_NOW = no`

The next task must implement validators and dry-run feature extraction first, then stop before scoring if degeneracy or leakage blockers fire.

## Exact next execution task

Implement a **non-scoring rescue feature-readiness dry run** that builds candidate-step feature matrices for each pre-specified variant, runs leakage and degeneracy checks, and reports whether scoring is allowed. The dry run must not compute attribution scores or compare predictions to gold labels.
