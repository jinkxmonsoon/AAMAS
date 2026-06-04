# Journal-v1 Full-Trace CCT Feature Semantic Audit

## Scope

This audit reviews the current Task 16–18 CCT feature semantics after the frozen uncalibrated diagnostic run. It does not change features, weights, scoring, ranking, corpus records, gold labels, baselines, or protocol. It does not compute new CCT scores, compare proposed descriptors to gold labels, calibrate, grid search, run LOSO, refine, ablate, run statistical tests, or produce paper-ready result tables.

## Current feature taxonomy

| Feature | Current semantic class | Audit judgment |
|---|---|---|
| `feature_schema_version` | schema constant | Constant; not a diagnostic signal. |
| `trace_id` | trace identifier | Required for joins; forbidden as a score feature. |
| `step_id` | step identity / position proxy | High-risk identity/position feature; excluded from primary scoring. |
| `agent_id` | agent identity / position proxy in current corpus | High-risk identity/position feature because agents map to fixed step positions. |
| `agent_role` | role identity / position proxy in current corpus | High-risk identity/position feature because roles map to fixed step positions. |
| `order_index` | pure position | Purely positional and excluded from primary scoring. |
| `in_degree` | collaboration structure but position-derived in fixed graph | Weak structural signal; mostly determined by graph position. |
| `out_degree` | collaboration structure but position-derived in fixed graph | Weak structural signal; mostly determined by graph position. |
| `has_handoff_from` | handoff/flow structure but position-derived in fixed graph | Weak collaboration signal; mostly distinguishes first step from later steps. |
| `has_handoff_to` | handoff/flow structure but position-derived in fixed graph | Weak collaboration signal; mostly distinguishes final step from earlier steps. |
| `input_token_count` | content-volume proxy | Visible and safe, but not causal-flow specific. |
| `output_token_count` | content-volume proxy | Visible and safe, but dominated scoring and separated wrong steps in Task 18A. |
| `tool_output_token_count` | content-volume proxy | Visible and safe, but the dominant average scoring contributor in Task 18A. |
| `evidence_item_count` | evidence cardinality | Constant in current artifacts; weak/non-discriminative. |
| `evidence_used_count` | evidence cardinality | Constant in current artifacts; weak/non-discriminative. |
| `has_tool_call` | tool-use presence | Constant in current artifacts; weak/non-discriminative. |

## Weak or non-discriminative features

The following current features are weak for primary diagnostic attribution in the current corpus shape:

- Constant or effectively constant: `feature_schema_version`, `evidence_item_count`, `evidence_used_count`, `has_tool_call`.
- Position/identity derived: `step_id`, `agent_id`, `agent_role`, `order_index`, `in_degree`, `out_degree`, `has_handoff_from`, `has_handoff_to`.
- Content-volume proxies that dominated Task 18 scoring without reliably identifying the gold step: `tool_output_token_count`, `output_token_count`, and to a lesser extent `input_token_count`.

## Evidence-flow and propagation gaps

The current feature set does not directly represent whether a step changes a constraint, ignores evidence, contradicts tool output, carries a caveat downstream, references prior output, introduces a recoverable correction opportunity, or creates cross-agent dependency. As a result, the current features are mostly graph-position, identity, cardinality, and content-volume descriptors rather than semantic causal-flow descriptors.

## Task 18A diagnostic implication

Task 18A found that primary underperformance was not mainly a top-score tie artifact. Scores were usually separated, but the separation often favored the wrong step. This supports a feature-design diagnosis: the current features are prediction-view safe but semantically too coarse for failure attribution.
