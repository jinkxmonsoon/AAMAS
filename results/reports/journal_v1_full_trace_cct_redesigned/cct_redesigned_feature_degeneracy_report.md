# CCT Redesigned Feature Degeneracy Report

- Unique feature-vector count: 6
- Duplicate feature-vector count: 414
- Previous base duplicate graph signature count: 419
- Previous base unique graph signature count: 1
- Redesigned graph duplicate signature count: 414
- Redesigned graph unique signature count: 6
- Redesigned features reduce degeneracy relative to previous base graph signatures: yes
- Clean unique feature-vector count: 6
- Perturbed unique feature-vector count: 6
## Scenario distribution (audit-only metadata)
- clean_broken_handoff: 60
- complex_collaboration: 60
- cross_agent_propagation: 60
- recoverable_irreversible_failure: 60
- same_agent_continuation: 60
- semantic_collision: 60
- tool_evidence_usage: 60

## Perturbation distribution (audit-only metadata)
- non_causal_textual_distraction: 84
- none: 84
- paraphrase: 84
- partial_observability: 84
- tool_output_truncation: 84

- Position-derived assessment: features do not include step position, agent identity, scenario, or perturbation fields as feature inputs; base graph topology is still regular, so degeneracy remains substantial
