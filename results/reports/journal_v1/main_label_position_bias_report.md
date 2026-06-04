# Journal-v1 Main Label-Position Bias Report

## Scope
- Corpus: `data/processed/journal_v1/main_all_traces.jsonl`.
- Total traces audited: 420.
- Diagnostic status: corpus-risk audit only; no evaluation metrics, baseline implementations, CCT scoring, calibration, or result tables were added.

## Acceptance thresholds
- No single `gold_failure_step` should exceed 50% of all traces unless explicitly justified.
- No single `gold_failure_agent` should dominate unless scenario-specific and documented.
- Semantic spot-check coverage must include positive and negative H6 examples and at least 3 different `gold_failure_step` values if available.
- If any trivial shortcut diagnostic exceeds 50%, evaluation remains blocked pending corpus revision or explicit justification.

## Overall `gold_failure_step` distribution
| gold_failure_step | count | percentage |
|---|---:|---:|
| s2 | 420 | 100.00% |

## Overall `gold_failure_agent` distribution
| gold_failure_agent | count | percentage |
|---|---:|---:|
| a11 | 55 | 13.10% |
| a8 | 45 | 10.71% |
| a5 | 40 | 9.52% |
| a9 | 40 | 9.52% |
| a12 | 40 | 9.52% |
| a2 | 35 | 8.33% |
| a10 | 35 | 8.33% |
| a3 | 35 | 8.33% |
| a4 | 35 | 8.33% |
| a7 | 25 | 5.95% |
| a6 | 20 | 4.76% |
| a1 | 15 | 3.57% |

## `gold_failure_step` by `scenario_group`
| scenario_group | gold_failure_step | count | within-group percentage |
|---|---|---:|---:|
| clean_broken_handoff | s2 | 60 | 100.00% |
| complex_collaboration | s2 | 60 | 100.00% |
| cross_agent_propagation | s2 | 60 | 100.00% |
| recoverable_irreversible_failure | s2 | 60 | 100.00% |
| same_agent_continuation | s2 | 60 | 100.00% |
| semantic_collision | s2 | 60 | 100.00% |
| tool_evidence_usage | s2 | 60 | 100.00% |

## `gold_failure_step` by `perturbation_type`
| perturbation_type | gold_failure_step | count | within-group percentage |
|---|---|---:|---:|
| non_causal_textual_distraction | s2 | 84 | 100.00% |
| none | s2 | 84 | 100.00% |
| paraphrase | s2 | 84 | 100.00% |
| partial_observability | s2 | 84 | 100.00% |
| tool_output_truncation | s2 | 84 | 100.00% |

## `gold_failure_agent` by `scenario_group`
| scenario_group | gold_failure_agent | count | within-group percentage |
|---|---|---:|---:|
| clean_broken_handoff | a5 | 15 | 25.00% |
| clean_broken_handoff | a10 | 10 | 16.67% |
| clean_broken_handoff | a9 | 5 | 8.33% |
| clean_broken_handoff | a2 | 5 | 8.33% |
| clean_broken_handoff | a11 | 5 | 8.33% |
| clean_broken_handoff | a8 | 5 | 8.33% |
| clean_broken_handoff | a3 | 5 | 8.33% |
| clean_broken_handoff | a7 | 5 | 8.33% |
| clean_broken_handoff | a4 | 5 | 8.33% |
| complex_collaboration | a7 | 10 | 16.67% |
| complex_collaboration | a9 | 10 | 16.67% |
| complex_collaboration | a12 | 10 | 16.67% |
| complex_collaboration | a10 | 5 | 8.33% |
| complex_collaboration | a2 | 5 | 8.33% |
| complex_collaboration | a3 | 5 | 8.33% |
| complex_collaboration | a11 | 5 | 8.33% |
| complex_collaboration | a4 | 5 | 8.33% |
| complex_collaboration | a8 | 5 | 8.33% |
| cross_agent_propagation | a2 | 15 | 25.00% |
| cross_agent_propagation | a8 | 15 | 25.00% |
| cross_agent_propagation | a9 | 10 | 16.67% |
| cross_agent_propagation | a6 | 5 | 8.33% |
| cross_agent_propagation | a3 | 5 | 8.33% |
| cross_agent_propagation | a12 | 5 | 8.33% |
| cross_agent_propagation | a10 | 5 | 8.33% |
| recoverable_irreversible_failure | a11 | 20 | 33.33% |
| recoverable_irreversible_failure | a5 | 10 | 16.67% |
| recoverable_irreversible_failure | a6 | 5 | 8.33% |
| recoverable_irreversible_failure | a10 | 5 | 8.33% |
| recoverable_irreversible_failure | a1 | 5 | 8.33% |
| recoverable_irreversible_failure | a9 | 5 | 8.33% |
| recoverable_irreversible_failure | a4 | 5 | 8.33% |
| recoverable_irreversible_failure | a3 | 5 | 8.33% |
| same_agent_continuation | a5 | 15 | 25.00% |
| same_agent_continuation | a11 | 15 | 25.00% |
| same_agent_continuation | a12 | 10 | 16.67% |
| same_agent_continuation | a4 | 5 | 8.33% |
| same_agent_continuation | a2 | 5 | 8.33% |
| same_agent_continuation | a10 | 5 | 8.33% |
| same_agent_continuation | a3 | 5 | 8.33% |
| semantic_collision | a12 | 10 | 16.67% |
| semantic_collision | a4 | 10 | 16.67% |
| semantic_collision | a8 | 10 | 16.67% |
| semantic_collision | a9 | 10 | 16.67% |
| semantic_collision | a11 | 5 | 8.33% |
| semantic_collision | a3 | 5 | 8.33% |
| semantic_collision | a2 | 5 | 8.33% |
| semantic_collision | a1 | 5 | 8.33% |
| tool_evidence_usage | a7 | 10 | 16.67% |
| tool_evidence_usage | a8 | 10 | 16.67% |
| tool_evidence_usage | a6 | 10 | 16.67% |
| tool_evidence_usage | a10 | 5 | 8.33% |
| tool_evidence_usage | a3 | 5 | 8.33% |
| tool_evidence_usage | a4 | 5 | 8.33% |
| tool_evidence_usage | a12 | 5 | 8.33% |
| tool_evidence_usage | a11 | 5 | 8.33% |
| tool_evidence_usage | a1 | 5 | 8.33% |

## `gold_failure_agent` by `perturbation_type`
| perturbation_type | gold_failure_agent | count | within-group percentage |
|---|---|---:|---:|
| non_causal_textual_distraction | a11 | 11 | 13.10% |
| non_causal_textual_distraction | a8 | 9 | 10.71% |
| non_causal_textual_distraction | a5 | 8 | 9.52% |
| non_causal_textual_distraction | a9 | 8 | 9.52% |
| non_causal_textual_distraction | a12 | 8 | 9.52% |
| non_causal_textual_distraction | a2 | 7 | 8.33% |
| non_causal_textual_distraction | a10 | 7 | 8.33% |
| non_causal_textual_distraction | a3 | 7 | 8.33% |
| non_causal_textual_distraction | a4 | 7 | 8.33% |
| non_causal_textual_distraction | a7 | 5 | 5.95% |
| non_causal_textual_distraction | a6 | 4 | 4.76% |
| non_causal_textual_distraction | a1 | 3 | 3.57% |
| none | a11 | 11 | 13.10% |
| none | a8 | 9 | 10.71% |
| none | a5 | 8 | 9.52% |
| none | a9 | 8 | 9.52% |
| none | a12 | 8 | 9.52% |
| none | a2 | 7 | 8.33% |
| none | a10 | 7 | 8.33% |
| none | a3 | 7 | 8.33% |
| none | a4 | 7 | 8.33% |
| none | a7 | 5 | 5.95% |
| none | a6 | 4 | 4.76% |
| none | a1 | 3 | 3.57% |
| paraphrase | a11 | 11 | 13.10% |
| paraphrase | a8 | 9 | 10.71% |
| paraphrase | a5 | 8 | 9.52% |
| paraphrase | a9 | 8 | 9.52% |
| paraphrase | a12 | 8 | 9.52% |
| paraphrase | a2 | 7 | 8.33% |
| paraphrase | a10 | 7 | 8.33% |
| paraphrase | a3 | 7 | 8.33% |
| paraphrase | a4 | 7 | 8.33% |
| paraphrase | a7 | 5 | 5.95% |
| paraphrase | a6 | 4 | 4.76% |
| paraphrase | a1 | 3 | 3.57% |
| partial_observability | a11 | 11 | 13.10% |
| partial_observability | a8 | 9 | 10.71% |
| partial_observability | a5 | 8 | 9.52% |
| partial_observability | a9 | 8 | 9.52% |
| partial_observability | a12 | 8 | 9.52% |
| partial_observability | a2 | 7 | 8.33% |
| partial_observability | a10 | 7 | 8.33% |
| partial_observability | a3 | 7 | 8.33% |
| partial_observability | a4 | 7 | 8.33% |
| partial_observability | a7 | 5 | 5.95% |
| partial_observability | a6 | 4 | 4.76% |
| partial_observability | a1 | 3 | 3.57% |
| tool_output_truncation | a11 | 11 | 13.10% |
| tool_output_truncation | a8 | 9 | 10.71% |
| tool_output_truncation | a5 | 8 | 9.52% |
| tool_output_truncation | a9 | 8 | 9.52% |
| tool_output_truncation | a12 | 8 | 9.52% |
| tool_output_truncation | a2 | 7 | 8.33% |
| tool_output_truncation | a10 | 7 | 8.33% |
| tool_output_truncation | a3 | 7 | 8.33% |
| tool_output_truncation | a4 | 7 | 8.33% |
| tool_output_truncation | a7 | 5 | 5.95% |
| tool_output_truncation | a6 | 4 | 4.76% |
| tool_output_truncation | a1 | 3 | 3.57% |

## Bias finding
- Top `gold_failure_step`: `s2` = 420/420 (100.00%).
- Top `gold_failure_agent`: `a11` = 55/420 (13.10%).
- Label-position bias detected: yes.
- Evaluation blocked: yes.
- Blocking reason: `s2` exceeds the 50% step-dominance threshold.
