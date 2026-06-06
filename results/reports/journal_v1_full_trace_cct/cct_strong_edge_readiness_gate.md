# CCT Strong Edge Readiness Gate

## Decision

- STRONG_CAUSAL_FLOW_EDGES_READY_FOR_NARROW_FULL_CORPUS_AUDIT = yes
- CCT_CAUSAL_FLOW_EDGES_READY_FOR_SCORING = no

## Rationale

The narrowed stress test supports a future representation-only full-corpus audit limited to `downstream_dependency_edge`, `tool_alignment_edge`, and `cross_agent_dependency_edge`. In the 14-trace sample, these edge types show clean-vs-perturbed descriptive count stability and require visible source-target relations. The authorization is narrow because normalized relation-note patterns remain repeated and must be audited explicitly at full-corpus scale.

## Conditions on the future narrow full-corpus audit

- It may extract only `downstream_dependency_edge`, `tool_alignment_edge`, and `cross_agent_dependency_edge`.
- It must use prediction-view-safe inputs only.
- It must not use private labels, gold failure step/agent, H6 private evidence, label rationales, provenance, scenario/perturbation metadata as extraction inputs, correctness fields, ranks, or scores.
- It must report leakage, phrase-template concentration, source-target relation validity, and descriptive clean/perturbed stability.
- It must not run scoring, ranking, calibration, grid search, LOSO, ablation, statistical tests, or paper-ready result tables.

## Out-of-scope blockers retained

- `constraint_shift_edge` is not ready for full-corpus audit.
- `semantic_collision_edge` is not ready for full-corpus audit.
- All unimplemented Task 20 candidate edge types remain deferred.
