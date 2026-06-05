# CCT Redesigned Feature Readiness Gate

- CCT_REDESIGNED_FEATURES_READY_FOR_PROTOCOL_REVIEW = no
- CCT_REDESIGNED_FEATURES_READY_FOR_SCORING = no
- Leakage status: PASS
- Total feature rows: 420
- Duplicate feature-vector count: 414
- Decision rationale: redesigned features are representation-only structural signals derived from the redesigned graph artifacts and reduce degeneracy relative to base graph signatures, but high duplicate-vector counts and constant features block protocol review readiness. This does not authorize scoring.
- Remaining blockers: feature vectors remain highly duplicated, constant features remain present: tool_alignment_edge_count, cross_agent_dependency_edge_count, cross_agent_dependency_count, tool_alignment_relation_count
