# Main Semantic Spot-check Report

- Procedure: 2 clean traces per scenario group + 1 perturbed trace per perturbation type.
- Outcome: revise items detected due to templating risk; evaluation remains blocked pending explicit correction task.

| trace_id | scenario_group | perturbation_type | gold_failure_step | gold_failure_agent | gold_irreversibility | gold_propagation | gold_recoverability | rationale plausible | lexical leakage | non-trivial | overly templated | recommendation |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| JV1_clean_broken_handoff_C001_clean | clean_broken_handoff | none | s2 | a2 | True | True | False | yes | no | yes | yes | revise |
| JV1_tool_evidence_usage_C013_clean | tool_evidence_usage | none | s2 | a2 | True | True | False | yes | no | yes | yes | revise |
| JV1_same_agent_continuation_C025_clean | same_agent_continuation | none | s2 | a2 | True | True | False | yes | no | yes | yes | revise |
| JV1_cross_agent_propagation_C037_clean | cross_agent_propagation | none | s2 | a2 | True | True | False | yes | no | yes | yes | revise |
| JV1_recoverable_irreversible_failure_C049_clean | recoverable_irreversible_failure | none | s2 | a2 | True | True | False | yes | no | yes | yes | revise |
| JV1_semantic_collision_C061_clean | semantic_collision | none | s2 | a2 | True | True | False | yes | no | yes | yes | revise |
| JV1_complex_collaboration_C073_clean | complex_collaboration | none | s2 | a2 | True | True | False | yes | no | yes | yes | revise |
| JV1_clean_broken_handoff_C002_clean | clean_broken_handoff | none | s2 | a2 | False | True | True | yes | no | yes | yes | revise |
| JV1_tool_evidence_usage_C014_clean | tool_evidence_usage | none | s2 | a2 | False | True | True | yes | no | yes | yes | revise |
| JV1_same_agent_continuation_C026_clean | same_agent_continuation | none | s2 | a2 | False | True | True | yes | no | yes | yes | revise |
| JV1_cross_agent_propagation_C038_clean | cross_agent_propagation | none | s2 | a2 | False | True | True | yes | no | yes | yes | revise |
| JV1_recoverable_irreversible_failure_C050_clean | recoverable_irreversible_failure | none | s2 | a2 | False | True | True | yes | no | yes | yes | revise |
| JV1_semantic_collision_C062_clean | semantic_collision | none | s2 | a2 | False | True | True | yes | no | yes | yes | revise |
| JV1_complex_collaboration_C074_clean | complex_collaboration | none | s2 | a2 | False | True | True | yes | no | yes | yes | revise |
| JV1_clean_broken_handoff_C001_paraphrase_P01 | clean_broken_handoff | paraphrase | s2 | a2 | True | True | False | yes | no | yes | yes | revise |
| JV1_clean_broken_handoff_C001_tool_output_truncation_P02 | clean_broken_handoff | tool_output_truncation | s2 | a2 | True | True | False | yes | no | yes | yes | revise |
| JV1_clean_broken_handoff_C001_partial_observability_P03 | clean_broken_handoff | partial_observability | s2 | a2 | True | True | False | yes | no | yes | yes | revise |
| JV1_clean_broken_handoff_C001_non_causal_textual_distraction_P04 | clean_broken_handoff | non_causal_textual_distraction | s2 | a2 | True | True | False | yes | no | yes | yes | revise |
