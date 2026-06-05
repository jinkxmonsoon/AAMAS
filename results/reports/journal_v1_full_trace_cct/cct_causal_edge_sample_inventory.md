# CCT Causal Edge Sample Inventory

- Input corpus: `data/processed/journal_v1_full_trace/main_full_trace_all.jsonl`
- Sampling rule: first clean and first perturbed trace per scenario group, deterministic sorted scenario order, maximum 20 traces, no gold-label selection
- Sample trace count: 14
- Total edge count: 102
- Edge counts by type:
- constraint_shift_edge: 4
- cross_agent_dependency_edge: 28
- downstream_dependency_edge: 22
- semantic_collision_edge: 20
- tool_alignment_edge: 28

## Visible fields used by edge type
- constraint_shift_edge: input_message, output_message, tool_output, visible_step_notes
- cross_agent_dependency_edge: handoff_from, handoff_to, input_message, output_message, tool_output
- downstream_dependency_edge: input_message, output_message, tool_output
- semantic_collision_edge: input_message, output_message, tool_output, visible_step_notes
- tool_alignment_edge: tool_call, tool_output, output_message

## Non-implemented edge types
- correction_attempt_edge: diagnostic-only in Task 20 spec; deferred
- correction_opportunity_edge: diagnostic-only in Task 20 spec; deferred
- evidence_conflict_edge: not in Task 20A required subset
- evidence_omission_edge: absence-sensitive; deferred until stronger audit design
- unresolved_caveat_edge: absence-sensitive; deferred
