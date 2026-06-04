# 11 — Journal-v1 Corpus Plan and Semantic Label Rubric (Frozen)

## Corpus identity
- dataset_version: BRACIS-Journal-v1
- relationship to BRACIS v0: independent reconstruction
- BRACIS v0 numbers may not be used as target values or empirical evidence

## Corpus phases (planning only)
1. Pilot validation corpus
2. Main controlled corpus
3. Robustness extension
4. Optional external probe

## Proposed minimum main corpus design
- Scenario groups: 7
- Clean cases per group: 12
- Total clean cases: 84
- Core perturbations per clean case: 4
- Total perturbation-derived variants: 336
- Total main controlled traces: 420

### Scenario groups
- clean_broken_handoff
- tool_evidence_usage
- same_agent_continuation
- cross_agent_propagation
- recoverable_irreversible_failure
- semantic_collision
- complex_collaboration

### Core perturbations
- paraphrase
- tool_output_truncation
- partial_observability
- non_causal_textual_distraction

### Optional robustness perturbations
- evidence_order_shuffle
- irrelevant_tool_noise
- handoff_ambiguity

## Case ID and trace ID conventions
- Clean case ID: `SG_<group_short>_C###`
- Clean trace ID: `JV1_<group_short>_C###_clean`
- Perturbed trace ID: `JV1_<group_short>_C###_<perturbation_type>_P##`
- Parent-child linkage: every perturbation includes `clean_parent_trace_id`
- Optional suffixes: `_S<seed>` and `_PV<protocol_version>` for provenance

## Semantic label rubric
### gold_failure_step
- The first step where the decisive failure-inducing error is introduced.

### gold_failure_agent
- Agent responsible for the `gold_failure_step` output/action.

### gold_irreversibility
- Positive: failure cannot be corrected downstream with available context/tools.
- Negative: downstream correction is feasible and sufficient.
- Borderline: correction depends on unstated assumptions/tool access.
- Required evidence: explicit downstream attempts/outcomes or impossibility rationale.
- Mark uncertain when evidence is insufficient to decide.

### gold_propagation
- Positive: downstream step/agent materially depends on faulty earlier output.
- Negative: error remains local and is not reused downstream.
- Borderline: reuse appears lexical only without decision impact.
- Required evidence: explicit dependency chain across step(s)/agent(s).
- Distinguish repetition from dependency: textual repetition alone is insufficient.

### gold_recoverability
- Recoverable failure: terminal outcome can be corrected with plausible intervention.
- Unrecoverable failure: terminal outcome cannot be corrected under constraints.
- Recovered intermediate error: early error occurred but was resolved before terminal outcome.
- Relation to terminal outcome must be explicit.

## Anti-leakage rules
- Gold label fields may not appear in `input_message`/`output_message`.
- No explicit marker like “this is the failing step” inside trace content.
- Scenario names must not directly reveal the target label.
- Perturbation variants must not inject label hints.
- `label_rationale` must be stored outside model-visible trace fields.

## Label provenance fields
- synthetic_control_rule
- primary_labeler
- secondary_labeler
- adjudicator
- manual_audit_status
- label_confidence
- label_rationale
- disagreement_type
- adjudication_decision

## Acceptance criteria for generated corpus
- 100% schema validation pass
- 100% label consistency validation pass
- no duplicate trace_id
- every perturbation has valid clean parent
- every clean case has expected perturbation variants
- every scenario group reaches target count
- every gold_failure_step exists
- every gold_failure_agent appears in trace
- every irreversibility/propagation/recoverability label has rationale
- leakage audit passes before metric execution

## Scientific risk notes
- Passing validation does not imply semantic label correctness.
- H6 (irreversibility/propagation proxies) remains high-risk.
- Scenario balance does not imply external validity.
- Journal-v1 must not be tuned to reproduce BRACIS v0 numbers.

## No execution yet
No traces, labels, perturbations, metrics, baselines, or results are generated in this task.

## Mandatory-group clarification
- `complex_collaboration` is part of the **mandatory** main corpus and included in the fixed 84/336/420 counts.
- Any additional optional external/extended scenario groups may be added only via `EXPERIMENT_CHANGELOG.md` entry and explicit protocol approval.


## Audit infrastructure status (Task 7)
- Leakage audit infrastructure implemented (`scripts/audit_leakage.py`, `src/cctdiag/audit/leakage.py`).
- Corpus integrity audit infrastructure implemented (`scripts/audit_corpus_integrity.py`, `src/cctdiag/audit/integrity.py`).
- Leakage audit is required before any metric execution.
- Corpus integrity audit is required before any metric execution.


## Pilot corpus status (Task 8)
- Pilot corpus is non-final and non-evidential.
- Pilot traces may be used only to refine protocol and tooling before main corpus generation.
- Pilot findings may not be used for journal performance claims.


## Pilot semantic-audit status (Task 8A)
- Pilot semantic audit and lessons reports are completed under `results/reports/journal_v1_pilot/`.
- Pilot remains non-final and non-evidential.
- Pilot findings are for protocol refinement only before main corpus generation.

- Main corpus readiness gate is defined in `docs/12_journal_v1_main_corpus_generation_readiness.md` and must pass before generation.


## Main corpus status (Task 10)
- Main controlled corpus generation is now implemented via `scripts/build_main_corpus.py` under frozen plan counts (84/336/420).
- Main corpus must pass schema, label, leakage, integrity, split-safety, and H6 distribution audits via `scripts/audit_main_corpus.py`.
- This task generates corpus assets only; no metrics, baselines, scoring, calibration, or claim tables are produced.


## Task 10B clarification
- Main-corpus generator must maintain lexical/structural diversity across scenario groups while preserving frozen counts and label semantics.
- Semantic spot-check summary must explicitly report sampled/accept/revise/reject counts and blocker status before evaluation starts.

## Task 10E pre-evaluation shortcut-risk gate
- Before metrics, baselines, CCT scoring, calibration, or result tables are implemented, the main corpus must be audited with `scripts/audit_label_position_bias.py`.
- The audit must report `gold_failure_step` and `gold_failure_agent` distributions overall, by `scenario_group`, and by `perturbation_type`.
- Diagnostic-only shortcut estimates must include `majority_step`, `majority_agent`, `always_s2`, `first_active_agent` when computable, and `most_common_agent`.
- These diagnostics are corpus-risk checks only and must not be reported as method results.
- Evaluation remains blocked if one `gold_failure_step` or any trivial shortcut diagnostic exceeds 50% without explicit written justification or an approved corpus-revision task.
- Current audit status: blocked because all 420 main-corpus traces have `gold_failure_step=s2`, making `majority_step` and `always_s2` diagnostics 100.00%.

## Task 10F failure-step positional-bias correction
- The main-corpus generator must assign `gold_failure_step` from semantically grounded trace phases rather than a fixed position.
- Required supported values are `s2`, `s3`, `s4`, and `s5` when the trace has length 5.
- The selected failure step must be reflected in `step_id`, `gold_failure_step`, `gold_failure_agent`, handoff context, phase-specific trace text, H6 evidence fields, and `label_rationale`.
- Perturbation variants preserve the clean parent case's `gold_failure_step` unless an explicitly documented degraded-observability change is approved.
- Current corrected distribution is `s2/s3/s4/s5 = 105/105/105/105` traces (25.00% each), satisfying the <=40% majority-step and always-s2 constraints.
