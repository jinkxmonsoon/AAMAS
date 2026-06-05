# CCT Causal Edge Sample Robustness Audit

## Scope

This audit evaluates the Task 20A/20B sample-only causal-edge prototype as a representation artifact. It uses no scoring outputs, ranks, gold labels, H6 labels, calibration, grid search, LOSO, ablation, statistical tests, corpus/gold-label edits, or paper-ready result tables.

## Sample audited

- Sample trace count: 14
- Clean sampled traces: 7
- Perturbed sampled traces: 7
- Total sample edge count: 102
- Implemented edge types: `constraint_shift_edge`, `downstream_dependency_edge`, `tool_alignment_edge`, `cross_agent_dependency_edge`, `semantic_collision_edge`

## Edge count stability across clean vs perturbed sampled traces

| Edge type | Clean count | Perturbed count | Stability finding |
| --- | ---: | ---: | --- |
| `constraint_shift_edge` | 2 | 2 | Stable in this sample, but sparse. |
| `downstream_dependency_edge` | 11 | 11 | Stable in this sample. |
| `tool_alignment_edge` | 14 | 14 | Stable in this sample. |
| `cross_agent_dependency_edge` | 14 | 14 | Stable in this sample. |
| `semantic_collision_edge` | 10 | 10 | Stable in this sample, but template-sensitive. |

The equal clean/perturbed counts are a descriptive robustness audit only, not a statistical test and not evidence of predictive validity.

## Rule-level robustness findings

| Edge type | Robustness finding | Remaining risk |
| --- | --- | --- |
| `constraint_shift_edge` | Detects visible modality shifts across steps and fired equally in clean and perturbed samples. | Sparse and dependent on a fixed hard/soft modality lexicon; not robust enough as a standalone full-audit rule. |
| `downstream_dependency_edge` | Requires a visible upstream-to-downstream content dependency and is not limited to adjacent steps. | Still partly dependent on recurring synthetic relation phrases after trace/step normalization. |
| `tool_alignment_edge` | Requires visible relation between `tool_output` and `output_message`; sample contains 16 align-style and 12 ignore-style tool relations. | Tool-output templates may dominate; relation labels must avoid correctness language. |
| `cross_agent_dependency_edge` | Goes beyond immediate handoff adjacency: 14 sample edges are adjacent-step dependencies and 14 span two steps. | Uses handoff context plus content overlap, so fixed five-step/five-agent templates remain a shortcut risk. |
| `semantic_collision_edge` | Captures visible alternative/selection relations in the sample and is stable across clean/perturbed pairs. | High lexical/template dependence around repeated alternative/caveat patterns; should not be promoted without stronger paraphrase checks. |

## Template and relationality audit

- Exact repeated extraction-note patterns after Task 20B refinement: 0.
- Normalized repeated source-target/relation patterns after removing trace and step identifiers: 27, indicating remaining template sensitivity at the relation-template level.
- `tool_alignment_edge` requires `tool_call`, `tool_output`, and `output_message`, preserving a visible tool-to-step relation.
- `cross_agent_dependency_edge` uses handoff context plus visible content relation rather than agent identity alone, but handoff-chain regularity remains a risk.
- `semantic_collision_edge` remains the most template-sensitive implemented edge type and should be treated as diagnostic/sample-only.

## Audit conclusion

The sample prototype is reviewable and leakage-safe for representation inspection, but it is not yet robust enough to authorize scoring. A future full-corpus audit, if authorized, should remain representation-only and should either limit scope to the more robust edge types or explicitly carry `constraint_shift_edge` and `semantic_collision_edge` as high-risk diagnostic-only rules.
