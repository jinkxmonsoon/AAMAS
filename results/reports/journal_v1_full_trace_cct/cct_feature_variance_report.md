# Journal-v1 Full-Trace CCT Feature Variance Report

Scope: descriptive structural feature diagnostics only. This report does not compute predictions, compare to gold labels, rank candidates, learn weights, calibrate outputs, run refinements, run ablations, test hypotheses, or produce paper-ready result tables.

- Feature rows audited: 2100
- Feature names: agent_id, agent_role, evidence_item_count, evidence_used_count, feature_schema_version, has_handoff_from, has_handoff_to, has_tool_call, in_degree, input_token_count, order_index, out_degree, output_token_count, step_id, tool_output_token_count, trace_id
- Constant features: evidence_item_count, evidence_used_count, feature_schema_version, has_tool_call
- High-variance features (>=10 unique values): output_token_count

## Feature diagnostics

| Feature | Missing/null | Unique values | Numeric min | Numeric max | Numeric mean |
|---|---:|---:|---:|---:|---:|
| `agent_id` | 0 | 5 | n/a | n/a | n/a |
| `agent_role` | 0 | 5 | n/a | n/a | n/a |
| `evidence_item_count` | 0 | 1 | 2 | 2 | 2 |
| `evidence_used_count` | 0 | 1 | 1 | 1 | 1 |
| `feature_schema_version` | 0 | 1 | n/a | n/a | n/a |
| `has_handoff_from` | 0 | 2 | 0 | 1 | 0.8 |
| `has_handoff_to` | 0 | 2 | 0 | 1 | 0.8 |
| `has_tool_call` | 0 | 1 | 1 | 1 | 1 |
| `in_degree` | 0 | 2 | 0 | 2 | 1.6 |
| `input_token_count` | 0 | 6 | 11 | 28 | 17.257 |
| `order_index` | 0 | 5 | 0 | 4 | 2 |
| `out_degree` | 0 | 2 | 0 | 2 | 1.6 |
| `output_token_count` | 0 | 19 | 11 | 44 | 17.23 |
| `step_id` | 0 | 5 | n/a | n/a | n/a |
| `tool_output_token_count` | 0 | 7 | 13 | 19 | 16.021 |
| `trace_id` | 0 | 420 | n/a | n/a | n/a |

## Audit metadata variation

`scenario_group` and `perturbation_type` are joined from the public full-trace corpus record for audit stratification only. They are not added to the feature payload and are not scoring inputs.

- Features varying within/by scenario-group audit strata: agent_id, agent_role, has_handoff_from, has_handoff_to, in_degree, input_token_count, order_index, out_degree, output_token_count, step_id, tool_output_token_count, trace_id
- Features varying within/by perturbation-type audit strata: agent_id, agent_role, has_handoff_from, has_handoff_to, in_degree, input_token_count, order_index, out_degree, output_token_count, step_id, tool_output_token_count, trace_id
