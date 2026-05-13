# Journal-v1 Pilot Semantic Audit (Non-final, Non-evidential)

## Clean-case semantic review

| trace_id | scenario_group | gold_failure_step | gold_failure_agent | gold_irreversibility | gold_propagation | gold_recoverability | why non-trivial | evidence supporting label | possible leakage risk | possible ambiguity | decision |
|---|---|---|---|---|---|---|---|---|---|---|---|
| JV1_clean_broken_handoff_C001_clean | clean_broken_handoff | s2 | a2 | true | false | false | Handoff introduces dependency break under partial context | Handoff fields + failed terminal outcome + unresolved output | Low (no explicit gold terms in messages) | Whether downstream could recover with richer tools | Revise |
| JV1_tool_evidence_usage_C002_clean | tool_evidence_usage | s2 | a2 | false | true | false | Evidence-use mismatch propagates to later decision | evidence_items/evidence_used plus propagated failure marker | Low | Distinguish evidence omission from benign omission | Accept |
| JV1_same_agent_continuation_C003_clean | same_agent_continuation | s2 | a2 | false | false | true | Same-agent continuation with intermediate fix potential | recoverability true with non-terminal correction interpretation | Low | Need stronger explicit recovered intermediate trace signal | Revise |
| JV1_cross_agent_propagation_C004_clean | cross_agent_propagation | s2 | a2 | true | true | false | Cross-agent dependency chain and failure spread | handoff + propagation true + failed terminal outcome | Low | Irreversibility proof needs explicit failed recovery attempt | Revise |
| JV1_recoverable_irreversible_failure_C005_clean | recoverable_irreversible_failure | s2 | a2 | false | false | true | Recoverability-focused scenario with controlled failure | recoverability true, irreversibility false | Low | Could be confused with local-only transient error | Accept |
| JV1_semantic_collision_C006_clean | semantic_collision | s2 | a2 | true | false | false | Semantic mismatch creates hard-to-recover downstream failure | irreversible true with failed terminal outcome | Low | Need stronger explicit contradiction evidence markers | Revise |
| JV1_complex_collaboration_C007_clean | complex_collaboration | s2 | a2 | false | true | true | Multi-constraint collaboration chain with competing context | propagation true + recoverability true | Low | Recoverability and propagation may conflict without richer evidence | Revise |

## Perturbed variant review

| trace_id | parent trace | perturbation type | label preserved | new leakage introduced | semantics changed | decision |
|---|---|---|---|---|---|---|
| JV1_paraphrase_P01_broken_handoff_C001_paraphrase_P01 | JV1_clean_broken_handoff_C001_clean | paraphrase | yes | no | no material change | Accept |
| JV1_tool_evidence_usage_C002_tool_output_truncation_P02 | JV1_tool_evidence_usage_C002_clean | tool_output_truncation | yes | no | minor observability impact only | Accept |
| JV1_same_agent_continuation_C003_partial_observability_P03 | JV1_same_agent_continuation_C003_clean | partial_observability | yes | no | moderate ambiguity increase | Revise |
| JV1_cross_agent_propagation_C004_non_causal_textual_distraction_P04 | JV1_cross_agent_propagation_C004_clean | non_causal_textual_distraction | yes | no | no material semantic shift | Accept |
| JV1_recoverable_irreversible_failure_C005_paraphrase_P05 | JV1_recoverable_irreversible_failure_C005_clean | paraphrase | yes | no | no material change | Accept |
| JV1_semantic_collision_C006_tool_output_truncation_P06 | JV1_semantic_collision_C006_clean | tool_output_truncation | yes | no | possible extra ambiguity | Revise |
| JV1_complex_collaboration_C007_partial_observability_P07 | JV1_complex_collaboration_C007_clean | partial_observability | yes | no | ambiguity increase likely | Revise |

## Summary
- Pilot passes structural audits, but multiple scenarios need richer semantic evidence templates before main corpus generation.
- Pilot remains non-final and non-evidential.
