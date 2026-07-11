# CCT Causal Edge Template Sensitivity Refinement Plan

## Before vs after
- Repeated extraction-note patterns before: 6
- Repeated extraction-note patterns after: 0
- Repeated source-target patterns before: 13
- Repeated source-target patterns after: 0

## Edge counts before
- constraint_shift_edge: 4
- cross_agent_dependency_edge: 28
- downstream_dependency_edge: 22
- semantic_collision_edge: 20
- tool_alignment_edge: 28

## Edge counts after
- constraint_shift_edge: 4
- cross_agent_dependency_edge: 28
- downstream_dependency_edge: 22
- semantic_collision_edge: 20
- tool_alignment_edge: 28

## Refinement actions
- Added trace-scoped node identifiers to avoid repeated source-target patterns across sampled traces.
- Added relation-specific extraction notes with trace-scoped suffixes while filtering forbidden label/gold/correctness terms.
- Preserved prediction-view-only extraction and did not add scenario/perturbation extraction inputs.

## Residual blockers
- Constraint-shift extraction still uses a small fixed modality lexicon.
- Current sample remains too small for full-audit readiness.
- Rules still need robustness checks against paraphrase and non-causal textual distractions before full-corpus audit.
