# CCT Causal-Flow Edge Readiness Gate

## Gate status

- `CCT_CAUSAL_FLOW_EDGE_SPEC_READY_FOR_SAMPLE_PROTOTYPE = yes`
- `CCT_CAUSAL_FLOW_EDGES_READY_FOR_SCORING = no`

## Decision rationale

The specification is ready for a future sample-only prototype because it defines candidate edge types, visible-field constraints, forbidden fields, directionality expectations, risk controls, and validation requirements. Edges are not ready for scoring because no extractor, leakage audit, template audit, perturbation-sensitivity audit, duplicate-signature audit, or edge-density audit has been implemented or reviewed.

## Required next task

The next task should be a sample-only edge prototype that:

1. leaves graph-builder behavior and existing features unchanged;
2. emits compact sample graph artifacts only;
3. audits leakage and shortcut/template sensitivity;
4. does not compare edges to gold labels or H6 labels;
5. does not score, rank, calibrate, grid search, run LOSO, refine, ablate, statistically test, or produce paper-ready result tables.
