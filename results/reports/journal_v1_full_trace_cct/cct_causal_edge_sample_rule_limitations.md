# CCT Causal Edge Sample Rule Limitations

## Scope

This report lists limitations of the sample causal-edge extraction rules under representation-only constraints. It does not modify extraction rules, scoring protocols, corpus data, gold labels, or evaluation outputs.

## Rule status summary

| Edge type | Future full-corpus audit status | Visible evidence required | Remaining shortcut risk |
| --- | --- | --- | --- |
| `constraint_shift_edge` | Sample-only / diagnostic-only until modality lexicon is expanded and paraphrase-tested. | A visible constraint, requirement, cap, caveat, or condition in one step and a later visible softened/changed treatment of the same item. | Fixed modality words such as required/mandatory/must/cap versus optional/preference/background can overfit synthetic templates. |
| `downstream_dependency_edge` | Robust enough for a future representation-only full-corpus audit as a primary candidate, with audit flags. | Visible reuse, dependency, or carry-forward of upstream step/tool content in a later step. | Recurring handoff/dependency phrases may create phrase-only edges unless content overlap remains required. |
| `tool_alignment_edge` | Robust enough for a future representation-only full-corpus audit as a primary candidate, with correctness-language filtering. | A visible `tool_output` and a visible `output_message` relation labeled only as align/ignore/contradict without correctness claims. | Tool-output templates may make overlap easy; labels must not imply correct/incorrect. |
| `cross_agent_dependency_edge` | Robust enough for a future representation-only full-corpus audit as a primary candidate, with adjacency and template audits. | Visible content dependency across different step/handoff contexts; handoff fields may provide context but cannot be the sole trigger. | Fixed agent chains and handoff adjacency can become position/identity proxies if content relation is weakened. |
| `semantic_collision_edge` | Defer or keep diagnostic-only for future sample refinement before full-corpus audit. | Visible alternatives, conflicting readings, caveats, or selection language linking source and target steps. | High lexical/template sensitivity around repeated alternative/caveat phrases and scenario-specific semantics. |

## Rules robust enough for future representation-only full-corpus audit

- `downstream_dependency_edge`, if content relation beyond adjacency remains mandatory.
- `tool_alignment_edge`, if relation labels remain non-correctness labels and require visible tool-output/output-message relation.
- `cross_agent_dependency_edge`, if different-agent or handoff context is not treated as sufficient without visible content relation.

## Rules that remain sample-only

- `constraint_shift_edge`, because current extraction remains sparse and tied to a small modality lexicon.
- `semantic_collision_edge`, because normalized relation patterns remain template-sensitive.

## Rules deferred

- The Task 20 candidate edge types not implemented in the sample prototype remain deferred: `evidence_conflict_edge`, `evidence_omission_edge`, `correction_opportunity_edge`, `correction_attempt_edge`, and `unresolved_caveat_edge`.

## Non-action confirmation

No scoring configuration was restored or recreated. No scoring, ranking, gold/H6 comparison, calibration, grid search, LOSO, scoring refinement, ablation, statistical test, corpus/gold-label change, or paper-ready result table was produced.
