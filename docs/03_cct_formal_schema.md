# 03 — CCT Formal Schema (Placeholder)

This file will contain formal definitions for:
- Nodes (agents, states, artifacts)
- Edges (causal, communicative, dependency)
- Temporal indexing
- Failure attribution fields

Status: Formal schema remains provisional. Task 16B adds only a structural feature audit boundary; no scoring or evaluation implementation is defined here.

## Task 16B structural feature audit boundary

Full-trace CCT graph construction currently exposes structural preprocessing artifacts only. Structural feature rows may include visible candidate identifiers, step order, degree counts, token-count descriptors, evidence-count descriptors, and handoff/tool-call booleans. They must not include private labels, gold labels, label rationales, H6 evidence fields, or provenance fields.

The Task 16B variance audit may join `scenario_group` and `perturbation_type` from public full-trace corpus metadata for descriptive audit stratification only. These audit metadata fields are not scoring inputs and are not added to the feature payload.

No CCT scoring, ranking, calibration, refinement variant, ablation, empirical hypothesis test, or paper-ready result table is defined by this schema note.

## Task 17 uncalibrated scoring protocol boundary

The first uncalibrated CCT scoring protocol is defined externally in `docs/14_cct_uncalibrated_scoring_protocol.md` and `configs/cct_scoring.yaml`. The primary future scorer is a fixed transparent weighted sum over allowed visible structural features and must exclude high-risk position/identity fields from its primary formula.

This schema note does not implement scoring. Gold labels, private labels, label rationales, H6 private evidence, provenance, scenario/perturbation audit strata, trace IDs, and case IDs are forbidden as score features. No calibrated probability or causal-certainty interpretation is defined.

## Task 18B causal-flow descriptor taxonomy boundary

Future CCT feature revisions should distinguish current structural primitives from semantic causal-flow descriptors. Candidate causal-flow descriptors include visible constraint shifts, evidence conflicts, ignored evidence, downstream references to prior outputs, tool-output alignment mismatches, visible recovery/correction opportunities, unresolved caveat carryover, semantic alternative collisions, and cross-agent dependencies.

These descriptors are not implemented by Task 18B. Any future descriptor must use sanitized prediction-view fields only, avoid private/gold/provenance/audit metadata, and pass leakage, variance, shortcut, and artifact-reviewability audits before any scoring protocol revision.

## Task 18C sample descriptor prototype pointer

`docs/15_cct_causal_flow_descriptor_spec.md` defines sample-only deterministic extraction rules for three causal-flow descriptors. These descriptor rows are not part of the frozen scoring protocol, are not compared to gold labels, and require a future full-corpus leakage/variance/shortcut audit before any scoring protocol revision.
