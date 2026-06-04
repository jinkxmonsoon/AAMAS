# Main Failure-Step Semantic Sanity Check

## Scope
- Task: 10G manual semantic sanity check for corrected Journal-v1 failure-step labels.
- Corpus inspected:
  - `data/processed/journal_v1/main_clean_traces.jsonl`
  - `data/processed/journal_v1/main_perturbed_traces.jsonl`
  - `data/processed/journal_v1/main_all_traces.jsonl`
- Guardrail: qualitative corpus sanity check only; no metrics, baselines, CCT scoring, calibration, empirical evaluation, or result tables were added.
- Corpus correction/regeneration decision: no corrective regeneration was needed because all inspected records were accepted; the expected validation command reran the deterministic builder without introducing label changes.

## Summary
- Records inspected: 6.
- Selected trace IDs:
  - `JV1_clean_broken_handoff_C001_clean`
  - `JV1_clean_broken_handoff_C002_clean`
  - `JV1_clean_broken_handoff_C003_clean`
  - `JV1_clean_broken_handoff_C004_clean`
  - `JV1_clean_broken_handoff_C002_paraphrase_P01`
  - `JV1_clean_broken_handoff_C004_partial_observability_P03`
- Coverage by `gold_failure_step`: `s2=1`, `s3=2`, `s4=1`, `s5=2`.
- Clean vs perturbed coverage: clean=4, perturbed=2.
- Classification counts: accept=6, revise=0, reject=0.
- Final blocker status: cleared; no Task 10G semantic blocker detected.

## Manual inspection table

| trace_id | parent_trace_id | perturbation_type | step_id | gold_failure_step | gold_failure_agent | propagation_evidence | irreversibility_evidence | recovery_opportunity | label_rationale | context inspected | classification | justification |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `JV1_clean_broken_handoff_C001_clean` | n/a | none | s2 | s2 | a5 | dependent agent reused unresolved output from s2 | mitigation attempt after s2 was insufficient to neutralize terminal failure | not_applicable_or_unavailable | non-visible rationale: s2/a5 anchors dependency, propagation, and correction evidence for the handoff-intake fault | input phase=`handoff-intake`; event says handoff intake had unresolved constraint mismatch; output says intake summary moved forward with unresolved gap; tool output says handoff-audit mismatch remained open; handoff a3→a5 | accept | The s2 label is aligned with handoff-intake semantics, s2-specific propagation/irreversibility evidence, matching `step_id`, matching `gold_failure_agent`, and handoff target a5. |
| `JV1_clean_broken_handoff_C002_clean` | n/a | none | s3 | s3 | a9 | handoff recipient integrated incorrect evidence originating at s3 | terminal impact from s3 was recovered before completion | available_but_missed | non-visible rationale: s3/a9 anchors dependency, propagation, and correction evidence for the evidence-integration fault | input phase=`evidence-integration`; event says evidence integration combined incompatible observations; output preserves unresolved contradiction; tool output reports incompatible observation pair retained; handoff a6→a9 | accept | The s3 label is semantically grounded in evidence integration, and both propagation and irreversibility evidence explicitly anchor to s3 without contradicting recoverability=true. |
| `JV1_clean_broken_handoff_C003_clean` | n/a | none | s4 | s4 | a2 | later steps used independent evidence channels and isolated the s4 fault | later correction at s5 successfully corrected the effect from s4 | available_but_missed | rationale stored in metadata: s4 is the structurally grounded verification-transfer failure point for a2 | input phase=`verification-transfer`; event says verification transfer accepted unchecked dependency; output says dependency validation incomplete; tool output says verification-log dependency check incomplete; handoff a12→a2 | accept | The s4 label is grounded in verification-transfer semantics. Non-propagation and recoverable irreversibility evidence correctly describe isolation/correction of an s4 fault. |
| `JV1_clean_broken_handoff_C004_clean` | n/a | none | s5 | s5 | a5 | error remained local to s5 with isolated impact | failure consequence from s5 persisted to terminal state without neutralization | not_applicable_or_unavailable | metadata rationale: s5 assigned to a5 because the final-adjudication action created the documented failure path | input phase=`final-adjudication`; event says final adjudication closed with unresolved correction cue; output says final adjudication recorded degraded conclusion; tool output says adjudication-log retained unresolved correction cue; handoff a4→a5 | accept | The s5 label is supported by a 5-step trace and final-adjudication context. Evidence explicitly refers to s5 and is consistent with non-propagation, irreversibility=true, and no recovery opportunity. |
| `JV1_clean_broken_handoff_C002_paraphrase_P01` | `JV1_clean_broken_handoff_C002_clean` | paraphrase | s3 | s3 | a9 | handoff recipient integrated incorrect evidence originating at s3 | terminal impact from s3 was recovered before completion | available_but_missed | non-visible rationale: s3/a9 anchors dependency, propagation, and correction evidence for the evidence-integration fault | parent is C002; input preserves evidence-integration event and appends `variant=paraphrase`; output/tool/handoff fields match parent | accept | The perturbation preserves parent `gold_failure_step=s3` and `gold_failure_agent=a9`; the variant text does not alter the semantic failure anchor. |
| `JV1_clean_broken_handoff_C004_partial_observability_P03` | `JV1_clean_broken_handoff_C004_clean` | partial_observability | s5 | s5 | a5 | error remained local to s5 with isolated impact | failure consequence from s5 persisted to terminal state without neutralization | not_applicable_or_unavailable | metadata rationale: s5 assigned to a5 because the final-adjudication action created the documented failure path | parent is C004; input preserves final-adjudication event and appends `variant=partial_observability`; output/tool/handoff fields match parent | accept | The perturbation preserves parent `gold_failure_step=s5` and `gold_failure_agent=a5`; no degraded-observability note changes the gold label, and evidence remains anchored to s5. |

## Non-s2 semantic grounding statement
The inspected non-s2 labels are semantically grounded. The `s3` records are tied to evidence-integration text and s3-specific evidence, the `s4` record is tied to verification-transfer text and s4-specific isolation/correction evidence, and the `s5` records are tied to final-adjudication text with s5-specific local/irreversible evidence. No inspected non-s2 record appears to be merely positionally rebalanced.

## Perturbation preservation statement
The inspected perturbed traces preserve the clean parent case's `gold_failure_step` and `gold_failure_agent`. `JV1_clean_broken_handoff_C002_paraphrase_P01` preserves parent `s3/a9`, and `JV1_clean_broken_handoff_C004_partial_observability_P03` preserves parent `s5/a5`. No inspected perturbation introduced an undocumented label change.

## Final decision
- Task 10G manual sanity gate: cleared.
- Evaluation-stage work remains outside this task and still requires separate explicit authorization under the protocol lock.
