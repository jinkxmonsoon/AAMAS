# Rescue Candidate-Step Feature Degeneracy Report

- Total rows: 2100
- Unique feature-vector count: 17
- Duplicate candidate-step feature-vector count: 2083
- Duplicate candidate-step feature-vector percentage: 99.19%
- Duplicate threshold (>50%) exceeded: yes
- Within-trace duplicate candidate-step rows: 0
- Traces with within-trace duplicates: 0

## Unique values per feature
- incoming_strong_edge_count: 4
- outgoing_strong_edge_count: 6
- downstream_dependency_incoming_count: 3
- downstream_dependency_outgoing_count: 3
- tool_alignment_incoming_count: 2
- tool_alignment_outgoing_count: 2
- cross_agent_dependency_incoming_count: 2
- cross_agent_dependency_outgoing_count: 2
- non_adjacent_dependency_involvement_count: 4
- relation_type_diversity_count: 4
- visible_tool_output_alignment_indicator: 2
- visible_dependency_carryover_indicator: 2
- causal_flow_total_degree: 7
- has_visible_tool_call: 1
- has_visible_tool_output: 1
- has_visible_handoff_from: 2
- has_visible_handoff_to: 2
- has_visible_step_notes: 1

## Constant features
- has_visible_tool_call
- has_visible_tool_output
- has_visible_step_notes

## Feature families over 95% constant threshold
- has_visible_tool_call
- has_visible_tool_output
- has_visible_step_notes
