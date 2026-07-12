# CCT Causal Edge Next Readiness Decision

## Decision

- REPRESENTATION_ONLY_EDGE_ROBUSTNESS_READY_FOR_FULL_CORPUS_AUDIT = no
- CCT_CAUSAL_FLOW_EDGES_READY_FOR_SCORING = no

## Rationale

The Task 20A/20B sample prototype remains useful for representation-only inspection, and clean/perturbed sample edge counts are stable across the 14 sampled traces. However, the current evidence is still sample-only; normalized relation patterns remain template-sensitive; `constraint_shift_edge` is sparse and lexicon-bound; and `semantic_collision_edge` is highly dependent on repeated alternative/caveat patterns. These blockers prevent authorizing a full-corpus audit of the complete edge set.

## Allowed next task

The recommended next task is further sample refinement and stress-testing under prediction-view-only constraints. A future task may either:

1. refine the sample rules for `constraint_shift_edge` and `semantic_collision_edge`; or
2. define a narrowed representation-only full-corpus audit limited to `downstream_dependency_edge`, `tool_alignment_edge`, and `cross_agent_dependency_edge`, with no scoring and no gold/H6 comparison.

## Blockers to resolve before full-corpus audit readiness

- Reduce fixed modality-lexicon dependence for `constraint_shift_edge`.
- Reduce normalized relation-template repetition for `semantic_collision_edge`.
- Add explicit paraphrase-distraction checks in sample mode before expanding scope.
- Preserve `configs/cct_scoring.yaml` blocked status unless an exact byte source matching the expected frozen hash is recovered in a separate task.

## Non-action confirmation

No config restoration/recreation, scoring, ranking, full-corpus extraction, gold/H6 comparison, calibration, grid search, LOSO, scoring refinement, ablation, statistical test, empirical hypothesis test, corpus/gold-label change, or paper-ready result table was produced.
