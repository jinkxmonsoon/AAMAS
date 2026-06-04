# Journal-v1 Evaluation Input Leakage Diagnosis

## Scope

- Corpus inspected: `data/processed/journal_v1/main_all_traces.jsonl`.
- Baselines inspected: `src/cctdiag/baselines/flat_log.py` and `src/cctdiag/baselines/spectrum.py`.
- Diagnostic runner inspected/updated: `scripts/run_non_cct_baseline_diagnostics.py`.
- Prior diagnostic report inspected/updated: `results/reports/journal_v1/non_cct_baseline_diagnostics_report.md`.
- This diagnosis does **not** implement CCT graph construction, CCT scoring, calibration, refinement variants, ablations, or paper-ready result tables.

## Root-cause finding

The Task 12 100% non-CCT performance was caused by **target-equivalent evaluation input leakage** and by a **failure-centered single-record corpus representation**:

1. The raw records expose `step_id` and `agent_id` as top-level fields. In the current corpus these equal `gold_failure_step` and `gold_failure_agent`, so they are direct target-equivalent pointers.
2. The raw records expose `handoff_to`, which also equals `gold_failure_agent` in the inspected corpus and therefore functions as an agent target-equivalent pointer in this failure-centered representation.
3. The raw records include private fields such as `label_rationale`, `propagation_evidence`, `irreversibility_evidence`, `recovery_opportunity`, `provenance_notes`, and `synthetic_control_rule`; these are not model-visible evaluation inputs.
4. The corpus is represented as one failure-centered record per trace rather than an ordered full multi-step trace. The visible message/tool content is therefore the content of the failure point, and phase/message terms such as `handoff-intake`, `evidence-integration`, `verification-transfer`, and `final-adjudication` remain highly predictive of the failure step even after private fields and top-level target pointers are removed.

## Cause checklist

| Potential cause | Diagnosis |
|---|---|
| Direct access to `gold_failure_step` or `gold_failure_agent` | Not intentionally used by Task 12 baselines, but raw records contained these fields before Task 12A prediction-view enforcement. |
| Use of top-level `step_id` / `agent_id` | Confirmed. `spectrum_inspired_step` used `step_id`, and `flat_log_keyword_agent` / `spectrum_inspired_agent` used `agent_id`; these are target-equivalent in the current corpus. |
| Access to `label_rationale` | Present in raw records; not used by baselines, but removed from prediction view. |
| Access to H6 evidence fields | Present in raw records; not used by baselines, but removed from prediction view because the text directly states label outcomes/dependencies. |
| Access to `provenance_notes` or `synthetic_control_rule` | Present in raw records; not used by baselines, but removed from prediction view. |
| Failure-centered trace representation | Confirmed. The corpus lacks a full ordered multi-step trace object and stores the failure-point row as the record. |
| Scenario/perturbation naming leakage | Scenario/perturbation fields are excluded from the strict prediction view; `trace_id` remains only as an identifier and baselines do not parse it. |
| Baseline implementation bug | Confirmed for Task 12 input contract: baselines accepted raw records rather than sanitized prediction views. Corrected in Task 12A. |

## Corrected diagnostic outcome after prediction-view enforcement

| baseline | step accuracy | agent accuracy | tuple step-agent accuracy |
|---|---:|---:|---:|
| flat_log_keyword_agent | NA | 25.00% | NA |
| flat_log_keyword_step | 75.00% | NA | NA |
| flat_log_keyword_step_agent | 75.00% | 25.00% | 25.00% |
| flat_log_role_agent | NA | 26.19% | NA |
| spectrum_inspired_agent | NA | 44.05% | NA |
| spectrum_inspired_step | 100.00% | NA | NA |
| spectrum_inspired_step_agent | 100.00% | 44.05% | 44.05% |


Gate status after correction: **BLOCKED**.

The agent leakage is reduced after removing `agent_id` and `handoff_to`, but step attribution remains blocked because failure-centered visible text still exposes the failure phase. The corpus must be revised to provide full ordered multi-step traces before CCT evaluation can proceed.

## Example raw record

```json
{
  "adjudication_decision": "auto_rule",
  "adjudicator": "pending",
  "agent_catalog": [
    "a3",
    "a5",
    "a9"
  ],
  "agent_id": "a5",
  "agent_role": "analyst",
  "annotator_or_generator": "main_corpus_builder",
  "case_id": "SG_CLE_C001",
  "case_variant": "clean",
  "dataset_version": "BRACIS-Journal-v1",
  "disagreement_type": "none",
  "evidence_items": [
    "ev5",
    "ev3",
    "ev9",
    "ev1"
  ],
  "evidence_used": [
    "ev3",
    "ev5"
  ],
  "generation_seed": 10001,
  "gold_failure_agent": "a5",
  "gold_failure_step": "s2",
  "gold_irreversibility": true,
  "gold_propagation": true,
  "gold_recoverability": false,
  "handoff_from": "a3",
  "handoff_to": "a5",
  "input_message": "Case 1: handoff packet omitted critical constraints; phase=handoff-intake; event=handoff intake contained an unresolved constraint mismatch; constraints=safety",
  "irreversibility_evidence": "mitigation attempt after s2 was insufficient to neutralize terminal failure",
  "label_confidence": 0.86,
  "label_rationale": "non-visible rationale: s2/a5 anchors dependency, propagation, and correction evidence for the handoff-intake fault",
  "label_source": "journal_v1_main_controlled",
  "manual_audit_status": "pending",
  "output_message": "Intake summary moved forward with an unresolved constraint gap",
  "perturbation_intensity": null,
  "perturbation_type": "none",
  "primary_labeler": "generator_rule",
  "propagation_evidence": "dependent agent reused unresolved output from s2",
  "provenance_notes": "seed=10001; deterministic diversified main corpus; non-evidential without downstream experiments",
  "recovery_opportunity": "not_applicable_or_unavailable",
  "scenario_group": "clean_broken_handoff",
  "secondary_labeler": "review_pending",
  "step_catalog": [
    "s1",
    "s2",
    "s3",
    "s4",
    "s5"
  ],
  "step_id": "s2",
  "synthetic_control_rule": "task10_main_controlled",
  "terminal_outcome": "degraded_execution",
  "tool_call": "query_incident_log",
  "tool_output": "handoff-audit: constraint mismatch remained open; record=412; signal=weak",
  "trace_id": "JV1_clean_broken_handoff_C001_clean"
}
```

## Corresponding sanitized prediction view

```json
{
  "candidate_agents": [
    "a3",
    "a5",
    "a9"
  ],
  "candidate_steps": [
    "s1",
    "s2",
    "s3",
    "s4",
    "s5"
  ],
  "case_variant": "clean",
  "model_visible_evidence_items": [
    "ev5",
    "ev3",
    "ev9",
    "ev1"
  ],
  "observed_step_content": {
    "agent_role": "analyst",
    "input_message": "Case 1: handoff packet omitted critical constraints; phase=handoff-intake; event=handoff intake contained an unresolved constraint mismatch; constraints=safety",
    "output_message": "Intake summary moved forward with an unresolved constraint gap",
    "terminal_outcome": "degraded_execution",
    "tool_call": "query_incident_log",
    "tool_output": "handoff-audit: constraint mismatch remained open; record=412; signal=weak"
  },
  "representation_warning": "failure_centered_single_record_without_full_ordered_multistep_trace",
  "trace_id": "JV1_clean_broken_handoff_C001_clean",
  "view_version": "journal_v1_prediction_view_v1"
}
```
