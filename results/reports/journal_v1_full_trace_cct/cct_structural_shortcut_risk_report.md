# Journal-v1 Full-Trace CCT Structural Shortcut Risk Report

Scope: structural shortcut diagnostics only; no gold-label performance comparison is performed.

## Position and template shortcut checks

- Single features that perfectly determine step position: agent_id, agent_role, order_index, step_id
- Features that vary only by step position: agent_id, agent_role, has_handoff_from, has_handoff_to, in_degree, order_index, out_degree, step_id
- Maximum identical structural feature-vector count: 180 rows (warning threshold: 105).
- Identical-vector warning: yes.

## Graph-size constancy

- Graphs audited: 420
- Node-count unique values: [5]
- Edge-count unique values: [12]
- Interpretation: constant graph node/edge counts are expected for the current five-step linear full-trace corpus, but future scoring must not treat graph size alone as diagnostic evidence.

## Private-field shortcut checks

- Forbidden private/gold fields in feature payloads: none
- Forbidden private/gold fields in graph payloads: none
- Structural shortcut warnings: single-feature position shortcuts exist, many identical structural feature vectors exist, graph node and edge counts are constant across all traces, some features vary only by step position
