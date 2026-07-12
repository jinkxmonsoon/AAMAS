# CCT Strong Edge Rule Revision Recommendation

## Scope

This recommendation is limited to representation-only rule diagnostics for `downstream_dependency_edge`, `tool_alignment_edge`, and `cross_agent_dependency_edge`. It does not add scoring features, change corpus data, compare to gold/H6 labels, calibrate, ablate, run statistical tests, or produce paper-ready results.

## Recommendations by edge type

| Edge type | Recommendation | Required visible evidence | Forbidden shortcut |
| --- | --- | --- | --- |
| `downstream_dependency_edge` | Keep as a candidate for a narrowed representation-only full-corpus audit, but add audit diagnostics for normalized relation-pattern concentration. | Upstream visible content and later visible carryover/dependency in step messages or tool output. | Generic temporal adjacency, step position, or handoff text without content carryover. |
| `tool_alignment_edge` | Keep as a candidate for a narrowed representation-only full-corpus audit, but preserve non-correctness relation labels and report align/ignore/contradict pattern concentration. | Visible `tool_output` plus visible `output_message` relation. | Correct/incorrect language, outcome labels, or tool-call presence without output-message relation. |
| `cross_agent_dependency_edge` | Keep as a candidate for a narrowed representation-only full-corpus audit only if content relation remains mandatory beyond handoff context. | Visible content relation across different handoff/step contexts. | Agent identity, fixed five-agent chain, or handoff adjacency alone. |

## Out-of-scope rule recommendations

- `constraint_shift_edge`: continue sample refinement; expand modality paraphrase checks before any full-corpus audit.
- `semantic_collision_edge`: continue sample refinement; reduce alternative/caveat template dependence before any full-corpus audit.
- `evidence_conflict_edge`, `evidence_omission_edge`, `correction_opportunity_edge`, `correction_attempt_edge`, and `unresolved_caveat_edge`: remain deferred until separately prototyped under prediction-view-only constraints.

## Recommended next task

Define a narrowed representation-only full-corpus audit design for only `downstream_dependency_edge`, `tool_alignment_edge`, and `cross_agent_dependency_edge`, with explicit checks for leakage, phrase-template concentration, clean/perturbed descriptive stability, and source-target relation validity. The next task must still prohibit scoring, ranking, gold/H6 comparison, calibration, ablation, statistical testing, and paper-ready result tables.
