# Full-Trace Pilot Diagnostic Sufficiency Report

## Scope
- Task 14C audit of the revised non-final Journal-v1 full-trace pilot.
- This report checks whether sanitized prediction views contain enough visible evidence to support attribution of the gold failure step without private labels.
- This is not CCT evaluation, not calibration, not refinement, not an ablation, and not a paper-ready result table.

## Before/after diagnosis
- Task 14B clean decisions before revision: accept=0, revise=7, reject=0.
- Task 14C clean decisions after revision: accept=7, revise=0, reject=0.
- Task 14B perturbed decisions before revision: accept=0, revise=7, reject=0.
- Task 14C perturbed decisions after revision: accept=7, revise=0, reject=0.
- Task 14B gold-step inferability before revision: 0/7 clean traces.
- Task 14C gold-step inferability after revision: 7/7 clean traces.
- Task 14C too-obvious clean traces: 0/7.
- Task 14C not-inferable clean traces: 0/7.
- Readiness: `FULL_TRACE_PILOT_DIAGNOSTICALLY_READY = yes`.

## Sufficiency criterion outcome
A trace is acceptable only if the prediction view contains visible evidence supporting the gold step, at least two non-gold steps remain plausible candidates, the gold step is not the only detailed step, the gold step is not recoverable only from private labels or position, and attribution is not effectively random.

The revised pilot clears this gate. Each clean trace now contains scenario-specific visible evidence supporting the private gold step while preserving multiple plausible alternatives with task-relevant actions, tools, evidence, and handoffs. The gold step is supported by content relations rather than forbidden label terms, top-level target fields, position, or being the only detailed/tool-bearing step.

## Clean-trace decisions

| trace_id | scenario_group | gold_failure_step | gold_failure_agent | visible evidence supporting gold step | why non-gold steps remain plausible but less supported | inferable without private labels? | too obvious? | not inferable? | decision |
|---|---|---:|---:|---|---|---|---|---|---|
| JV1FT_CLEBRO_C001_clean | clean_broken_handoff | s2 | a2 | s2 converts a required cap into optional background context, and later steps visibly rely on that softened transfer wording. | s1 records the cap, while s3/s4/s5 execute and verify plausible downstream work but are visibly dependent on the transfer packet. | yes | no | no | accept |
| JV1FT_TOOEVI_C002_clean | tool_evidence_usage | s3 | a3 | s3 treats a broad noisy reading as controlling even though its tool output states the narrower reading has stronger case-specific support. | s1/s2 collect and preserve evidence; s4/s5 review and deliver from the chosen plan, making them plausible but less directly supported. | yes | no | no | accept |
| JV1FT_SAMAGE_C003_clean | same_agent_continuation | s4 | a4 | s4 carries an internal-use assumption into an external-channel authorization despite a visible caveat requiring extra confirmation. | s1/s2/s3 preserve the caveat and s5 follows the authorization, so alternatives are plausible but less supported. | yes | no | no | accept |
| JV1FT_CROAGE_C004_clean | cross_agent_propagation | s5 | a5 | s5 delivers a value based on a low-confidence estimate while the stable reference and qualifier remain visible. | s1/s2/s3/s4 all handle estimates and qualifiers plausibly, but the final visible dependency occurs at s5. | yes | no | no | accept |
| JV1FT_RECIRR_C005_clean | recoverable_irreversible_failure | s2 | a2 | s2 sees that a cancellation window is required and available but forwards the packet without using the correction window. | s1 asks later agents to use the window; s3/s4/s5 work from the packet after the opportunity is missed, so they remain plausible but downstream. | yes | no | no | accept |
| JV1FT_SEMCOL_C006_clean | semantic_collision | s3 | a3 | s3 uses the internal review date as the operational renewal date although s2 distinguishes the two close terms. | s1/s2 establish both terms, and s4/s5 preserve/deliver them, making alternatives plausible but less directly supported. | yes | no | no | accept |
| JV1FT_COMCOL_C007_clean | complex_collaboration | s4 | a4 | s4 collapses the handoff summary so preliminary source A appears confirmed and closes an available correction window. | s1/s2/s3 preserve source ranking and collaboration context; s5 follows the collapsed summary, so alternatives are plausible but less supported. | yes | no | no | accept |

## Perturbed-trace decisions

| trace_id | parent_trace | perturbation_type | label semantics preserved? | necessary diagnostic evidence preserved? | shortcut hints introduced? | decision |
|---|---|---|---|---|---|---|
| JV1FT_CLEBRO_C001_paraphrase_P01 | JV1FT_CLEBRO_C001_clean | paraphrase | yes, private labels are preserved from the parent. | yes; the cap-transfer relation remains visible after paraphrase. | no explicit label shortcut detected. | accept |
| JV1FT_TOOEVI_C002_tool_output_truncation_P01 | JV1FT_TOOEVI_C002_clean | tool_output_truncation | yes, private labels are preserved from the parent. | yes; the evidence-weighting cue remains visible in s3 output even with one truncated tool output. | no explicit label shortcut detected. | accept |
| JV1FT_SAMAGE_C003_partial_observability_P01 | JV1FT_SAMAGE_C003_clean | partial_observability | yes, private labels are preserved from the parent. | yes; the external-confirmation caveat and s4 authorization remain visible. | no explicit label shortcut detected. | accept |
| JV1FT_CROAGE_C004_non_causal_textual_distraction_P01 | JV1FT_CROAGE_C004_clean | non_causal_textual_distraction | yes, private labels are preserved from the parent. | yes; the low-confidence estimate dependency remains visible. | no explicit label shortcut detected. | accept |
| JV1FT_RECIRR_C005_paraphrase_P01 | JV1FT_RECIRR_C005_clean | paraphrase | yes, private labels are preserved from the parent. | yes; the correction-window relation remains visible after paraphrase. | no explicit label shortcut detected. | accept |
| JV1FT_SEMCOL_C006_tool_output_truncation_P01 | JV1FT_SEMCOL_C006_clean | tool_output_truncation | yes, private labels are preserved from the parent. | yes; the date-role mismatch remains visible in s3 output and surrounding steps. | no explicit label shortcut detected. | accept |
| JV1FT_COMCOL_C007_partial_observability_P01 | JV1FT_COMCOL_C007_clean | partial_observability | yes, private labels are preserved from the parent. | yes; the source-ranking and correction-window interaction remains visible. | no explicit label shortcut detected. | accept |

## Conclusion
- The Task 14B diagnostic sufficiency blocker is cleared for the non-final pilot.
- The full 420-trace corpus is still not generated in this task and remains allowed only for a future explicitly approved builder task.
