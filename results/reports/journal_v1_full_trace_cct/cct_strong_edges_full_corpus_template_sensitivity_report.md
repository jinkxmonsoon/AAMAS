# CCT Strong Edges Full-Corpus Template Sensitivity Report

- Repeated relation-note pattern count: 74
- Repeated source-target pattern count: 3
## Relation-note pattern counts by type
- cross_agent_dependency_edge: patterns=34, max_repeat=280
- downstream_dependency_edge: patterns=38, max_repeat=205
- tool_alignment_edge: patterns=2, max_repeat=450

## Top repeated relation-note patterns
- `tool_relation_ignore_sX_overlap_N`: 450
- `tool_relation_align_sX_overlap_N`: 390
- `cross_agent_content_sX_to_sY_alternate_caveat_check`: 280
- `cross_agent_content_sX_to_sY_alternate_check_comparable`: 245
- `content_dependency_sX_to_sY_alternate_caveat_check`: 205
- `content_dependency_sX_to_sY_alternate_check_comparable`: 95
- `content_dependency_sX_to_sY_check_confidence_qualifier`: 53
- `content_dependency_sX_to_sY_check_confidence_draft`: 35
- `content_dependency_sX_to_sY_alternate_broad_check`: 30
- `cross_agent_content_sX_to_sY_assumption_caveat_check`: 30

## Top repeated source-target patterns
- `trace:TRACE:step:sX:cross_agent_content->trace:TRACE:step:sY:cross_agent_use`: 840
- `trace:TRACE:step:sX:tool_output->trace:TRACE:step:sY:step_output`: 840
- `trace:TRACE:step:sX:visible_content->trace:TRACE:step:sY:dependent_action`: 705

## Relation-validity checks
- `tool_alignment_edge` uses visible `tool_call`, `tool_output`, and `output_message` relation fields.
- `downstream_dependency_edge` includes non-adjacent edges and therefore goes beyond generic immediate temporal adjacency.
- `cross_agent_dependency_edge` includes non-adjacent edges and requires visible content relation beyond handoff adjacency.
- Finding: full-corpus representation extraction is reviewable, but repeated templates remain audit conditions for graph-redesign integration.
