# PROTOCOL LOCK (Frozen Placeholders)

Status: **LOCKED PLACEHOLDERS — INITIALIZATION PHASE**

This document reserves protocol slots that must be explicitly filled and approved before experiments begin.

## Locked sections (placeholders)
- Task definitions: TBD (locked)
- Agent configurations: TBD (locked)
- Dataset splits/composition: TBD (locked)
- Gold label policy: TBD (locked)
- Random seed policy: TBD (locked)
- Metrics definitions: See `docs/04_metrics_definition.md` (placeholder locked)
- Baseline catalog: TBD (locked)
- Output schema: TBD (locked)
- Statistical testing plan: TBD (locked)

## Change policy
Any change to these sections requires:
1. Explicit written authorization.
2. Changelog entry in `EXPERIMENT_CHANGELOG.md`.
3. Rationale entry in `RESEARCH_LOG.md`.

## BRACIS v0 artifact-status note
- BRACIS v0 reproduction is blocked until artifacts are recovered.
- No v0 result may be treated as reproduced.


## Path B activation note (Journal v1)
- Path B is activated for protocol design of **BRACIS-Journal-v1**.
- BRACIS-Journal-v1 is independent from BRACIS v0 unless original artifacts are later recovered and verified.
- No v1 experiment may run before schema, label protocol, metrics, baselines, and acceptance criteria are frozen in protocol documents.


## Task 4 operational-contract freeze gate
- Operational contracts must be frozen before any Journal-v1 corpus generation.
- No Journal-v1 data generation may occur before Task 4 completion.
- No metric or baseline implementation may occur before contracts are frozen.

- No Journal-v1 corpus file may be accepted unless it passes schema and label validation.
