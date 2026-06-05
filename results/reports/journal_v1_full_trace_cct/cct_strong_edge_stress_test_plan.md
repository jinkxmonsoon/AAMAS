# CCT Strong Edge Stress-Test Plan

## Scope

Task 22 stress-tests only the strongest sample causal-flow edge types from Task 21 under representation-only constraints. It does not restore or recreate `configs/cct_scoring.yaml`, run scoring, rank candidate steps, compare to gold/H6 labels, calibrate, grid search, run LOSO, refine scoring, ablate, perform statistical tests, alter corpus/gold labels, or produce paper-ready result tables.

## Edge types in scope

- `downstream_dependency_edge`
- `tool_alignment_edge`
- `cross_agent_dependency_edge`

## Edge types out of scope

- `constraint_shift_edge`: remains sparse and fixed-modality-lexicon dependent.
- `semantic_collision_edge`: remains highly lexical/template dependent.
- `evidence_conflict_edge`, `evidence_omission_edge`, `correction_opportunity_edge`, `correction_attempt_edge`, and `unresolved_caveat_edge`: not implemented in the current sample prototype.

## Inputs allowed

- `make_full_trace_prediction_view(record)` output only.
- Visible step messages.
- Visible tool outputs.
- Visible handoff context.
- Visible notes.

## Inputs forbidden

- `private_labels`, `gold_failure_step`, `gold_failure_agent`, H6 private evidence, label rationales, provenance, correctness fields, ranks, scores, and scenario/perturbation metadata as extraction inputs.

## Stress-test dimensions

| Dimension | Check |
| --- | --- |
| Lexical robustness | Inspect normalized extraction-note/relation patterns for repeated phrase dependence. |
| Source-target relation validity | Verify each in-scope edge type requires a visible relation, not only time/position. |
| Clean vs perturbed stability | Compare in-scope sample edge counts across clean and perturbed sampled traces descriptively only. |
| Downstream dependency specificity | Check whether edges span beyond generic temporal adjacency and require visible content carryover. |
| Tool alignment relation | Check whether edges require visible `tool_output` to `output_message` relation and avoid correctness labels. |
| Cross-agent dependency specificity | Check whether edges go beyond handoff adjacency and require visible content relation. |

## Readiness outputs

- `STRONG_CAUSAL_FLOW_EDGES_READY_FOR_NARROW_FULL_CORPUS_AUDIT = yes/no`
- `CCT_CAUSAL_FLOW_EDGES_READY_FOR_SCORING = no`
