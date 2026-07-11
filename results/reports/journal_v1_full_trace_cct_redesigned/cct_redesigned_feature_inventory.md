# CCT Redesigned Feature Inventory

- Branch: `work`
- HEAD before feature audit: `3f6689254c46232afc0234559ae3493e41f5732c`
- `configs/cct_scoring.yaml` exists: False
- Task 18 reproducibility status: `NOT_REPRODUCIBLE_FROM_CURRENT_CHECKOUT`
- Scope: representation-only redesigned graph feature audit; no scoring dependency.
- Source graph artifact: `data/interim/journal_v1_full_trace_cct_redesigned/cct_redesigned_graphs.jsonl`
- Raw feature output: `results/raw/journal_v1_full_trace_cct_redesigned/cct_redesigned_features.json`
- Total traces processed: 420
- Total feature rows: 420

## Feature names
- causal_flow_edge_count_total
- downstream_dependency_edge_count
- tool_alignment_edge_count
- cross_agent_dependency_edge_count
- incoming_causal_flow_edge_count
- outgoing_causal_flow_edge_count
- non_adjacent_dependency_count
- cross_agent_dependency_count
- tool_alignment_relation_count
- causal_flow_degree
- causal_flow_in_degree
- causal_flow_out_degree
- causal_flow_edge_type_diversity
