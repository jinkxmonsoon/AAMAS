# 09 — BRACIS-Journal-v1 Reconstruction Protocol (Path B Activated)

## Protocol activation status
- Dataset version name: **BRACIS-Journal-v1**.
- Relationship to BRACIS v0: **independent reconstruction**, not a reproduced continuation.
- Allowed use of BRACIS v0: historical motivation and problem framing only.
- Forbidden use of BRACIS v0: reproduced empirical evidence.

## Minimum corpus design (definition only; no data generation)
- Clean diagnostic cases: required.
- Perturbation-derived variants: required.
- Scenario groups: required and explicitly versioned.

### Required metadata per case
- `case_id`, `trace_id`, `scenario_group`, `split_tag`, `difficulty_tag`, `source_type`, `version`.

### Required gold-label fields
- `gold_step_attribution`, `gold_agent_attribution`, `gold_tuple` (if used), `irreversibility_label/proxy`, `propagation_label/proxy`, `label_confidence`.

### Required observability audit fields
- `missing_observation_flags`, `tool_visibility_flags`, `message_truncation_flags`, `known_blindspots`.

### Required provenance fields
- `data_origin`, `construction_method`, `annotator_ids_or_roles`, `timestamp_utc`, `artifact_hash`, `protocol_version`.

## Required high-level trace schema
- `trace_id`
- `scenario_group`
- `case_id`
- `step_id`
- `agent_id`
- `agent_role`
- message/input/output fields
- tool_call fields
- tool_output fields
- handoff fields
- evidence-flow fields
- terminal outcome
- gold diagnostic tuple
- provenance/version fields

## Gold-label protocol
- Who labels: at least two independent labelers plus one adjudicator role.
- Label fields: step, agent, tuple (if applicable), irreversibility, propagation, rationale.
- Disagreement handling: disagreement log + structured conflict taxonomy.
- Adjudication protocol: third-party adjudication with written resolution note.
- Label confidence: mandatory scalar/confidence bucket per label.
- Label provenance: each label linked to annotator role/id and timestamp.
- Label origin typing: explicitly mark synthetic/control-derived vs manually audited labels.

## Mandatory metrics (protocol requirement only)
- Step attribution accuracy.
- Agent attribution accuracy.
- Tuple accuracy (if applicable).
- Irreversibility accuracy and/or proxy-validity checks.
- Propagation accuracy and/or proxy-validity checks.
- Robustness stability.
- Judge/refinement call rate.
- Cost/runtime where applicable.

## Mandatory baselines (protocol requirement only)
- Flat-log heuristic baseline.
- Spectrum-inspired baseline.
- Random or majority baseline.
- v1 calibrated CCT backbone.
- Ablated structural variants:
  - no criticality,
  - no irreversibility,
  - no propagation,
  - no evidence-flow,
  - no handoff.
- V2/refinement variants treated as secondary mechanisms only.

## Mandatory analyses
- LOSO calibration.
- Weight sensitivity.
- Scenario-level breakdown.
- Robustness by perturbation type and intensity.
- Fixed/worsened/unchanged audit for refinement.
- Statistical tests.
- Failure analysis focused on irreversibility and propagation.

## Claim boundaries
### Allowed claims
- Protocol design and governance claims.
- Reproducibility pipeline readiness claims.
- Clearly marked reported-vs-reproduced status statements.

### Forbidden claims
- Any performance/generalization claim without reproduced evidence.
- Any implication that BRACIS v0 is reproduced.
- Any over-strong causal claim implying formal causal identification.

### Claims requiring future evidence
- Structural superiority beyond flat-log baselines.
- Calibration robustness across scenarios.
- Transferability/external paradigm effectiveness.
- Validity of irreversibility/propagation proxies.

### Wording constraint for “causal”
Use “causal” strictly as operational dependency/evidence-flow terminology unless formal causal identification is explicitly established.

## No execution yet
- No dataset generated.
- No labels created.
- No metric implemented.
- No baseline implemented.
- No result produced.
- No BRACIS v0 number reused as reproduced evidence.
