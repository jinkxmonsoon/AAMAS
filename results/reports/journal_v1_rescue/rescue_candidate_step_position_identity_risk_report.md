# Rescue Candidate-Step Position/Identity Risk Report

- Features include step position column: no
- Features include agent identity column: no
- Features usable without position or agent fields: yes
- Position shortcut risk: review
- Agent identity shortcut risk: low

## Unique vectors by candidate step id (identifier-only audit)
- s1: 5
- s2: 4
- s3: 3
- s4: 2
- s5: 3

## Feature means by candidate step id (identifier-only audit)
- s1: incoming_strong_edge_count=1.0, outgoing_strong_edge_count=4.25, downstream_dependency_incoming_count=0.0, downstream_dependency_outgoing_count=1.25, tool_alignment_incoming_count=1.0, tool_alignment_outgoing_count=1.0, cross_agent_dependency_incoming_count=0.0, cross_agent_dependency_outgoing_count=2.0, non_adjacent_dependency_involvement_count=2.0357, relation_type_diversity_count=2.8571, visible_tool_output_alignment_indicator=1.0, visible_dependency_carryover_indicator=0.8571, causal_flow_total_degree=5.25, has_visible_tool_call=1.0, has_visible_tool_output=1.0, has_visible_handoff_from=0.0, has_visible_handoff_to=1.0, has_visible_step_notes=1.0
- s2: incoming_strong_edge_count=2.2143, outgoing_strong_edge_count=1.4286, downstream_dependency_incoming_count=0.2143, downstream_dependency_outgoing_count=0.4286, tool_alignment_incoming_count=1.0, tool_alignment_outgoing_count=1.0, cross_agent_dependency_incoming_count=1.0, cross_agent_dependency_outgoing_count=0.0, non_adjacent_dependency_involvement_count=0.3929, relation_type_diversity_count=2.6429, visible_tool_output_alignment_indicator=1.0, visible_dependency_carryover_indicator=0.6429, causal_flow_total_degree=3.6429, has_visible_tool_call=1.0, has_visible_tool_output=1.0, has_visible_handoff_from=1.0, has_visible_handoff_to=1.0, has_visible_step_notes=1.0
- s3: incoming_strong_edge_count=1.4643, outgoing_strong_edge_count=0.0, downstream_dependency_incoming_count=0.4643, downstream_dependency_outgoing_count=0.0, tool_alignment_incoming_count=0.0, tool_alignment_outgoing_count=0.0, cross_agent_dependency_incoming_count=1.0, cross_agent_dependency_outgoing_count=0.0, non_adjacent_dependency_involvement_count=1.4286, relation_type_diversity_count=1.4286, visible_tool_output_alignment_indicator=0.0, visible_dependency_carryover_indicator=0.4286, causal_flow_total_degree=1.4643, has_visible_tool_call=1.0, has_visible_tool_output=1.0, has_visible_handoff_from=1.0, has_visible_handoff_to=1.0, has_visible_step_notes=1.0
- s4: incoming_strong_edge_count=0.0714, outgoing_strong_edge_count=0.0, downstream_dependency_incoming_count=0.0714, downstream_dependency_outgoing_count=0.0, tool_alignment_incoming_count=0.0, tool_alignment_outgoing_count=0.0, cross_agent_dependency_incoming_count=0.0, cross_agent_dependency_outgoing_count=0.0, non_adjacent_dependency_involvement_count=0.0714, relation_type_diversity_count=0.0357, visible_tool_output_alignment_indicator=0.0, visible_dependency_carryover_indicator=0.0357, causal_flow_total_degree=0.0714, has_visible_tool_call=1.0, has_visible_tool_output=1.0, has_visible_handoff_from=1.0, has_visible_handoff_to=1.0, has_visible_step_notes=1.0
- s5: incoming_strong_edge_count=0.9286, outgoing_strong_edge_count=0.0, downstream_dependency_incoming_count=0.9286, downstream_dependency_outgoing_count=0.0, tool_alignment_incoming_count=0.0, tool_alignment_outgoing_count=0.0, cross_agent_dependency_incoming_count=0.0, cross_agent_dependency_outgoing_count=0.0, non_adjacent_dependency_involvement_count=0.9286, relation_type_diversity_count=0.5714, visible_tool_output_alignment_indicator=0.0, visible_dependency_carryover_indicator=0.5714, causal_flow_total_degree=0.9286, has_visible_tool_call=1.0, has_visible_tool_output=1.0, has_visible_handoff_from=1.0, has_visible_handoff_to=0.0, has_visible_step_notes=1.0
