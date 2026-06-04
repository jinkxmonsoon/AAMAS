# Main H6 Label-Consistency Diagnosis (Task 10D)

## Audit snapshot before correction
- total_traces: 420
- total_inconsistencies: 660
- categories:
  - irrev_false_but_persistent: 210
  - recover_false_but_available: 155
  - recover_true_but_unavailable: 85
  - prop_false_but_downstream: 210

## Semantic decision table

| Field combination | Intended interpretation | Valid? | Required correction |
|---|---|---|---|
| `gold_irreversibility=false` + evidence says no correction/persistent failure | Contradiction (evidence indicates irreversible effect) | Invalid | Align evidence with recoverable phrasing OR set label true (builder-level fix chosen: evidence alignment) |
| `gold_irreversibility=true` + evidence says successfully corrected | Contradiction (evidence indicates reversibility) | Invalid | Enforce persistent/unrecovered evidence wording |
| `gold_recoverability=false` + `recovery_opportunity` available/available_but_missed | Contradiction (opportunity implies recoverability path) | Invalid | Set opportunity to `not_applicable_or_unavailable` |
| `gold_recoverability=true` + no/none opportunity | Contradiction (recoverability requires explicit opportunity) | Invalid | Set opportunity to available state |
| `gold_propagation=true` + evidence only textual repetition | Weak proxy evidence | Invalid | Require explicit downstream dependency language |
| `gold_propagation=false` + evidence indicates downstream use/integration | Contradiction (evidence indicates propagation) | Invalid | Replace with local-only non-propagation evidence |
| Generic rationale without trace-specific anchor | Weak adjudication traceability | Conditionally invalid | Use bounded rationale templates with explicit semantic anchors |

## Root cause
- The inconsistency is primarily caused by generation logic not conditioning evidence fields on H6 labels.
- Rubric ambiguity is secondary; rubric already requires explicit evidence and dependency/recovery semantics.

## Resolution path
- Update builder logic to condition `irreversibility_evidence`, `recovery_opportunity`, and `propagation_evidence` on H6 label values.
- Regenerate corpus via approved builder and rerun all audits + manifest.
