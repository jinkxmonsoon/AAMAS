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
