# CCT Redesigned Feature Variance Report

## Missing/null counts
- causal_flow_edge_count_total: 0
- downstream_dependency_edge_count: 0
- tool_alignment_edge_count: 0
- cross_agent_dependency_edge_count: 0
- incoming_causal_flow_edge_count: 0
- outgoing_causal_flow_edge_count: 0
- non_adjacent_dependency_count: 0
- cross_agent_dependency_count: 0
- tool_alignment_relation_count: 0
- causal_flow_degree: 0
- causal_flow_in_degree: 0
- causal_flow_out_degree: 0
- causal_flow_edge_type_diversity: 0

## Unique value counts
- causal_flow_edge_count_total: 3
- downstream_dependency_edge_count: 3
- tool_alignment_edge_count: 1
- cross_agent_dependency_edge_count: 1
- incoming_causal_flow_edge_count: 3
- outgoing_causal_flow_edge_count: 3
- non_adjacent_dependency_count: 3
- cross_agent_dependency_count: 1
- tool_alignment_relation_count: 1
- causal_flow_degree: 3
- causal_flow_in_degree: 2
- causal_flow_out_degree: 3
- causal_flow_edge_type_diversity: 2

## Numeric feature ranges
- causal_flow_edge_count_total: min=4, max=6, mean=5.6786
- downstream_dependency_edge_count: min=0, max=2, mean=1.6786
- tool_alignment_edge_count: min=2, max=2, mean=2.0
- cross_agent_dependency_edge_count: min=2, max=2, mean=2.0
- incoming_causal_flow_edge_count: min=4, max=6, mean=5.6786
- outgoing_causal_flow_edge_count: min=4, max=6, mean=5.6786
- non_adjacent_dependency_count: min=1, max=3, mean=2.4286
- cross_agent_dependency_count: min=2, max=2, mean=2.0
- tool_alignment_relation_count: min=2, max=2, mean=2.0
- causal_flow_degree: min=8, max=12, mean=11.3571
- causal_flow_in_degree: min=2, max=3, mean=2.25
- causal_flow_out_degree: min=3, max=5, mean=4.25
- causal_flow_edge_type_diversity: min=2, max=3, mean=2.8571

- Constant features: tool_alignment_edge_count, cross_agent_dependency_edge_count, cross_agent_dependency_count, tool_alignment_relation_count
- Sparse features: none
- Dense features: causal_flow_edge_count_total, tool_alignment_edge_count, cross_agent_dependency_edge_count, incoming_causal_flow_edge_count, outgoing_causal_flow_edge_count, non_adjacent_dependency_count, cross_agent_dependency_count, tool_alignment_relation_count, causal_flow_degree, causal_flow_in_degree, causal_flow_out_degree, causal_flow_edge_type_diversity
