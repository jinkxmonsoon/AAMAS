# Rescue Baseline Plan

## Scope

This plan defines required baselines for a future rescue experiment. It does not execute baselines, compute scores, tune parameters, run statistical tests, or produce result tables.

## Required trivial baselines

- `majority_step`: predict the most frequent failure-step position from training/protocol priors only.
- `always_s2`: always predict step 2.
- `random_step_seeded`: uniformly sample one candidate step with seed `20260605`.
- `first_step`: always predict the first candidate step.
- `last_step`: always predict the last candidate step.

## Required flat-log baselines

- `flat_log_lexical_baseline`: use visible full-trace text only, without graph/CCT features, private labels, scenario/perturbation metadata, or provenance.
- `flat_log_text_similarity_baseline`: if feasible, compare visible step text to visible terminal outcome or trace-level visible failure indicators without using gold labels or private rationales.

## Required non-CCT visible heuristic baseline

- `non_cct_visible_heuristic_baseline`: a deterministic heuristic over visible fields such as tool-output presence, handoff presence, and visible warning/error terms, with no CCT graph topology and no private/gold/provenance fields.

## Required CCT variants for comparison

- `cct_structural_old_features_diagnostic_only`: include only if existing old features can be rebuilt from prediction views; diagnostic only.
- `cct_strong_edge_step_level_features`: candidate-level features from downstream dependency, tool alignment, and cross-agent dependency edges.
- `cct_causal_flow_relation_features`: edge relation features projected onto candidate steps.
- `cct_visible_text_free_graph_features`: graph/topology features that do not use visible lexical content.
- `cct_lightweight_visible_textual_relation_features_optional`: optional if leakage-safe.

## Baseline fairness requirements

- Every baseline must use the same prediction-view input contract.
- Scenario group, perturbation type, and case variant are forbidden as model inputs.
- Private labels and provenance may be used only after predictions are frozen for evaluation.
- If any baseline violates the input contract, its result is invalid and the experiment must stop.
