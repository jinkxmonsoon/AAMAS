# 12 — Journal-v1 Main Corpus Generation Readiness Gate

## Pilot audit status
- Pilot corpus audit: PASS (`results/reports/journal_v1_pilot/pilot_audit_report.md`)
- Pilot semantic audit: present
- Pilot lessons learned: present
- Pilot remains non-final and non-evidential.

## H6 coverage status (from pilot)
- propagation_true: 6
- irreversibility_true: 6
- recoverability_true: 6
- recovered_intermediate: 0
- uncertain_or_borderline: 0
- Status: sufficient for pilot gate, not sufficient for final claims.

## Accepted pilot design elements
- Parent-child perturbation linkage pattern.
- Multi-step, multi-agent trace shape.
- Baseline anti-leakage field separation.

## Revised design elements
- Require stronger evidence templates for irreversibility=true.
- Require explicit dependency notes for propagation=true.
- Require explicit opportunity-for-correction evidence for recoverability=true.
- Add uncertainty/borderline label handling examples in annotation SOP.

## Rejected pilot design elements
- Implicit semantic justification without explicit evidence anchors.
- Using partial observability perturbation without uncertainty handling constraints.

## Remaining risks
- H6 semantics remain high-risk until richer annotation exemplars are frozen.
- Semantic collision and complex collaboration cases need tighter authoring constraints.
- Pilot size is too small for any claim-bearing inference.

## Explicit decision
- **Decision: NOT READY** for unrestricted main corpus generation.
- **Conditional readiness:** main corpus generation may start only through approved builder task after Task 9 gate checks pass and protocol deltas are acknowledged.

## Pilot-to-main protocol delta

| Issue observed | Affected scenario/perturbation | Required change | File/config updated | Hypothesis affected | Risk reduced | Status |
|---|---|---|---|---|---|---|
| Weak irreversibility evidence | recoverable_irreversible_failure, semantic_collision | require failed-recovery evidence anchor | docs/12 + docs/11 | H6 | false positives on irreversibility | applied |
| Propagation ambiguity | cross_agent_propagation, complex_collaboration | require explicit downstream dependency note | docs/12 + docs/11 | H6, H1 | textual repetition confusion | applied |
| Recoverability ambiguity | same_agent_continuation, recoverable_irreversible_failure | require explicit correction opportunity evidence | docs/12 + docs/11 | H6 | inconsistent recoverability labels | applied |
| Partial-observability uncertainty | partial_observability | enforce uncertainty policy example requirement | docs/12 + lessons | H6 | overconfident labels | applied |
| Pilot evidential misuse risk | all | keep pilot non-evidential lock | PROTOCOL_LOCK.md | H1-H6 | claim contamination | applied |

## Main-corpus H6 distribution expectations (pre-generation)
- Minimum positive `gold_propagation`: 20
- Minimum negative `gold_propagation`: 20
- Minimum positive `gold_irreversibility`: 20
- Minimum negative `gold_irreversibility`: 20
- Minimum positive `gold_recoverability`: 20
- Minimum negative `gold_recoverability`: 20
- Uncertain/borderline policy: allowed only with explicit evidence-gap rationale and adjudicator sign-off; target share <= 15% per H6 label family.

## Main-corpus semantic quality requirements
- Every `propagation=true` must show downstream dependency, not mere repetition.
- Every `irreversibility=true` must show unrecovered consequence after failure step.
- Every `recoverability=true` must show explicit later correction opportunity.
- Every `semantic_collision` case must include semantically close but diagnostically distinct alternatives.
- Every `complex_collaboration` case must include at least two collaboration mechanisms among handoff, evidence flow, propagation, tool use, recovery opportunity.

## Main-corpus perturbation constraints
- `paraphrase` must preserve label semantics.
- `tool_output_truncation` must not remove sole gold-label evidence unless explicitly marked degraded observability.
- `partial_observability` must preserve enough evidence for auditability.
- `non_causal_textual_distraction` must not introduce label hints.
- Perturbation variants must preserve labels or explicitly document label changes.

## Full-corpus generation acceptance gate
Main corpus generation may begin only if:
1. Pilot audit passed.
2. Pilot semantic audit exists.
3. Pilot lessons learned exists.
4. Required protocol deltas applied or explicitly waived.
5. `configs/corpus_plan.yaml` and `configs/label_rubric.yaml` present and validated.
6. `PROTOCOL_LOCK.md` permits generation only through approved future builder task.
7. No metrics/baselines/results implementations are introduced as part of this gate.

## Readiness blockers
- none
