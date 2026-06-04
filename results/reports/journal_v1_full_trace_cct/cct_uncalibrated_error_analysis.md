# Journal-v1 Full-Trace CCT Uncalibrated Error Analysis

Scope: descriptive error analysis of the frozen Task 18 diagnostic run only. No weights, features, scoring formula, tie-breaking, corpus records, gold labels, baselines, or protocol were changed.

- Branch: `work`
- Analysis HEAD: `1f0238278e4b152eda03184390346eaf1c8ac8e6`
- Task 18 HEAD reference: `2695aa3e8c06936270b40a1b6d93eee41f55f87b`
- `configs/cct_scoring.yaml` SHA256: `053f19066923d8d22d27b22727e75876f939f2a60480484c4028eabd07ad0855`
- Config hash matches Task 18: true

## Variant prediction distributions and correctness

| Variant | Correct | Incorrect | Step accuracy | Predicted step distribution | Predicted agent distribution |
|---|---:|---:|---:|---|---|
| `cct_primary_no_position` | 48 | 372 | 0.114286 | `{'s1': 21, 's2': 174, 's3': 90, 's4': 99, 's5': 36}` | `{'a1': 21, 'a2': 174, 'a3': 90, 'a4': 99, 'a5': 36}` |
| `cct_flow_only` | 105 | 315 | 0.250000 | `{'s2': 420}` | `{'a2': 420}` |
| `cct_context_only` | 12 | 408 | 0.028571 | `{'s1': 81, 's2': 147, 's3': 90, 's4': 72, 's5': 30}` | `{'a1': 81, 'a2': 147, 'a3': 90, 'a4': 72, 'a5': 30}` |
| `cct_with_position_features` | 105 | 315 | 0.250000 | `{'s4': 420}` | `{'a4': 420}` |

## Primary scenario errors

| Scenario | Accuracy | Error rate | Incorrect | n |
|---|---:|---:|---:|---:|
| `clean_broken_handoff` | 0.000000 | 1.000000 | 60 | 60 |
| `complex_collaboration` | 0.050000 | 0.950000 | 57 | 60 |
| `cross_agent_propagation` | 0.050000 | 0.950000 | 57 | 60 |
| `recoverable_irreversible_failure` | 0.050000 | 0.950000 | 57 | 60 |
| `same_agent_continuation` | 0.200000 | 0.800000 | 48 | 60 |
| `semantic_collision` | 0.000000 | 1.000000 | 60 | 60 |
| `tool_evidence_usage` | 0.450000 | 0.550000 | 33 | 60 |

## Primary perturbation errors

| Perturbation | Accuracy | Error rate | Incorrect | n |
|---|---:|---:|---:|---:|
| `non_causal_textual_distraction` | 0.178571 | 0.821429 | 69 | 84 |
| `none` | 0.107143 | 0.892857 | 75 | 84 |
| `paraphrase` | 0.071429 | 0.928571 | 78 | 84 |
| `partial_observability` | 0.107143 | 0.892857 | 75 | 84 |
| `tool_output_truncation` | 0.107143 | 0.892857 | 75 | 84 |

## Ranking diagnostics for primary

- Top-1 accuracy: 0.114286
- Top-2 containment: 0.207143
- Top-3 containment: 0.407143
- Mean gold-step rank: 3.600000
- Median gold-step rank: 4.000000
- Gold-step rank distribution: `{1: 48, 2: 39, 3: 84, 4: 111, 5: 138}`

## Cross-variant case sets

- Primary correct cases: 48
- Primary wrong cases: 372
- Flow-only correct while primary wrong: 78
- With-position correct while primary wrong: 96
- All variants fail: 198
- All variants agree: 0
- Variants disagree: 420

## Diagnostic interpretation answers

- Primary failure is mainly caused by weak/non-discriminative fixed features plus context contributions that often separate the wrong step, not by a tuned model failure.
- Score ties are not the main primary failure mode: primary tied-top rate is 0.285714; wrong score separation count is 276.
- Removal of position/identity features matters: the high-risk with-position diagnostic reaches 0.250000 and exceeds primary, indicating shortcut risk rather than structural support.
- Context features dilute flow features in the primary formula: context-only is weak, while primary underperforms flow-only despite adding context density fields.
- Flow-only is not substantively stronger; it matches a positional/default 0.250000 pattern and remains near a plausible-candidate baseline.
- Errors are concentrated by scenario: worst groups are `clean_broken_handoff`, `semantic_collision`; best group is `tool_evidence_usage`.
- Perturbation errors are highest for `paraphrase`.
- H1 remains unsupported after error analysis; H2 remains unsupported after error analysis.
- Recommended next task: inspect feature design and protocol assumptions before any calibration, including whether visible structural features need non-position-derived causal/flow descriptors and whether the corpus graph shape is too uniform.
- Non-actions: no calibration, grid search, LOSO, refinement, ablation, statistical test, or paper-ready result table was produced.
