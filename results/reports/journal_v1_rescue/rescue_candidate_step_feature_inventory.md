# Rescue Candidate-Step Feature Inventory

## Scope
- Non-scoring candidate-step feature-readiness dry run for `rescue_experiment_v1`.
- One row per candidate step per trace; no gold/H6 comparison is performed.

## Counts
- Total candidate-step rows: 2100
- Expected candidate-step rows: 2100
- Feature count: 18

## Feature names
- `incoming_strong_edge_count`
- `outgoing_strong_edge_count`
- `downstream_dependency_incoming_count`
- `downstream_dependency_outgoing_count`
- `tool_alignment_incoming_count`
- `tool_alignment_outgoing_count`
- `cross_agent_dependency_incoming_count`
- `cross_agent_dependency_outgoing_count`
- `non_adjacent_dependency_involvement_count`
- `relation_type_diversity_count`
- `visible_tool_output_alignment_indicator`
- `visible_dependency_carryover_indicator`
- `causal_flow_total_degree`
- `has_visible_tool_call`
- `has_visible_tool_output`
- `has_visible_handoff_from`
- `has_visible_handoff_to`
- `has_visible_step_notes`

## Missing/null counts
- incoming_strong_edge_count: 0
- outgoing_strong_edge_count: 0
- downstream_dependency_incoming_count: 0
- downstream_dependency_outgoing_count: 0
- tool_alignment_incoming_count: 0
- tool_alignment_outgoing_count: 0
- cross_agent_dependency_incoming_count: 0
- cross_agent_dependency_outgoing_count: 0
- non_adjacent_dependency_involvement_count: 0
- relation_type_diversity_count: 0
- visible_tool_output_alignment_indicator: 0
- visible_dependency_carryover_indicator: 0
- causal_flow_total_degree: 0
- has_visible_tool_call: 0
- has_visible_tool_output: 0
- has_visible_handoff_from: 0
- has_visible_handoff_to: 0
- has_visible_step_notes: 0

## Audit-only scenario distribution
- clean_broken_handoff: 60
- complex_collaboration: 60
- cross_agent_propagation: 60
- recoverable_irreversible_failure: 60
- same_agent_continuation: 60
- semantic_collision: 60
- tool_evidence_usage: 60

## Audit-only perturbation distribution
- non_causal_textual_distraction: 84
- none: 84
- paraphrase: 84
- partial_observability: 84
- tool_output_truncation: 84
