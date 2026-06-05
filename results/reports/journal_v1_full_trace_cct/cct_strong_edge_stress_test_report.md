# CCT Strong Edge Stress-Test Report

## Scope

This report evaluates only `downstream_dependency_edge`, `tool_alignment_edge`, and `cross_agent_dependency_edge` in the existing sample-only causal-edge artifact. It uses no scoring outputs, ranks, gold labels, H6 labels, calibration, grid search, LOSO, ablation, statistical tests, corpus/gold-label edits, or paper-ready result tables.

## Sample/subset audited

- Sample trace count: 14
- Clean sampled traces: 7
- Perturbed sampled traces: 7
- In-scope edge count: 78
- In-scope edge types: `downstream_dependency_edge`, `tool_alignment_edge`, `cross_agent_dependency_edge`
- Out-of-scope implemented edge types: `constraint_shift_edge`, `semantic_collision_edge`

## Clean vs perturbed descriptive stability

| Edge type | Clean count | Perturbed count | Clean mean per trace | Perturbed mean per trace | Finding |
| --- | ---: | ---: | ---: | ---: | --- |
| `downstream_dependency_edge` | 11 | 11 | 1.57 | 1.57 | Stable in this sample. |
| `tool_alignment_edge` | 14 | 14 | 2.00 | 2.00 | Stable in this sample. |
| `cross_agent_dependency_edge` | 14 | 14 | 2.00 | 2.00 | Stable in this sample. |

These counts are descriptive stress-test checks only. They are not statistical tests and do not evaluate prediction quality.

## Lexical robustness and repeated phrase dependence

| Edge type | Normalized repeated pattern finding | Interpretation |
| --- | --- | --- |
| `downstream_dependency_edge` | 7 normalized relation-note patterns repeated; largest repeated pattern count is 10. | Stronger than deferred edges but still phrase-template sensitive. |
| `tool_alignment_edge` | 2 normalized relation-note patterns repeated: align-style and ignore-style. | Relation is visible and simple, but current diagnostics compress many cases into two lexical buckets. |
| `cross_agent_dependency_edge` | 9 normalized relation-note patterns repeated; largest repeated pattern count is 12. | Captures visible cross-step content relation, but sample templates recur across traces. |

## Source-target relation validity

| Edge type | Relation-validity finding |
| --- | --- |
| `downstream_dependency_edge` | Uses visible `input_message`, `output_message`, and `tool_output`; source-target deltas span 1, 2, 3, and 4 steps, so it is not solely adjacent temporal order. |
| `tool_alignment_edge` | Uses visible `tool_call`, `tool_output`, and `output_message`; all edges are within-step tool-to-output relations, which is appropriate for this edge type and not a cross-step rank signal. |
| `cross_agent_dependency_edge` | Uses visible handoff context plus `input_message`, `output_message`, and `tool_output`; 14 edges are adjacent-step dependencies and 14 span two steps, so it goes beyond handoff adjacency in half the sample. |

## Edge-specific stress conclusions

- `downstream_dependency_edge`: relation validity is acceptable for a narrowed representation-only audit, but diagnostics should record normalized phrase-pattern concentration.
- `tool_alignment_edge`: relation validity is acceptable because tool output and step output are both required; future diagnostics should split align/ignore/contradict evidence without correctness language.
- `cross_agent_dependency_edge`: relation validity is acceptable only when visible content relation remains mandatory; handoff adjacency alone must remain insufficient.

## Out-of-scope limitations

- `constraint_shift_edge` remains out of scope because it is sparse and tied to a small modality lexicon.
- `semantic_collision_edge` remains out of scope because it is highly dependent on repeated alternative/caveat templates.
- Not-implemented Task 20 candidate edges remain deferred and were not evaluated.
