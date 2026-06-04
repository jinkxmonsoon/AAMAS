# Journal-v1 Main Label-Position Bias Report

## Scope
- Corpus: `data/processed/journal_v1/main_all_traces.jsonl`.
- Total traces audited: 420.
- Diagnostic status: corpus-risk audit only; no evaluation metrics, baseline implementations, CCT scoring, calibration, or result tables were added.

## Acceptance thresholds
- No single `gold_failure_step` should exceed 40% of all traces unless explicitly justified.
- At least 3 distinct `gold_failure_step` values should each appear in at least 15% of traces.
- No single `gold_failure_agent` should dominate unless scenario-specific and documented.
- Semantic spot-check coverage must include positive and negative H6 examples and at least 3 different `gold_failure_step` values if available.
- `majority_step` and `always_s2` diagnostics must not exceed 40%; other trivial agent diagnostics remain blocked above 50%.

## Overall `gold_failure_step` distribution
| gold_failure_step | count | percentage |
|---|---:|---:|
| s2 | 105 | 25.00% |
| s3 | 105 | 25.00% |
| s4 | 105 | 25.00% |
| s5 | 105 | 25.00% |

## Overall `gold_failure_agent` distribution
| gold_failure_agent | count | percentage |
|---|---:|---:|
| a8 | 75 | 17.86% |
| a5 | 55 | 13.10% |
| a6 | 45 | 10.71% |
| a10 | 35 | 8.33% |
| a7 | 35 | 8.33% |
| a9 | 30 | 7.14% |
| a2 | 30 | 7.14% |
| a1 | 30 | 7.14% |
| a4 | 30 | 7.14% |
| a11 | 20 | 4.76% |
| a12 | 20 | 4.76% |
| a3 | 15 | 3.57% |

## `gold_failure_step` by `scenario_group`
| scenario_group | gold_failure_step | count | within-group percentage |
|---|---|---:|---:|
| clean_broken_handoff | s2 | 15 | 25.00% |
| clean_broken_handoff | s3 | 15 | 25.00% |
| clean_broken_handoff | s4 | 15 | 25.00% |
| clean_broken_handoff | s5 | 15 | 25.00% |
| complex_collaboration | s2 | 15 | 25.00% |
| complex_collaboration | s3 | 15 | 25.00% |
| complex_collaboration | s4 | 15 | 25.00% |
| complex_collaboration | s5 | 15 | 25.00% |
| cross_agent_propagation | s2 | 15 | 25.00% |
| cross_agent_propagation | s3 | 15 | 25.00% |
| cross_agent_propagation | s4 | 15 | 25.00% |
| cross_agent_propagation | s5 | 15 | 25.00% |
| recoverable_irreversible_failure | s2 | 15 | 25.00% |
| recoverable_irreversible_failure | s3 | 15 | 25.00% |
| recoverable_irreversible_failure | s4 | 15 | 25.00% |
| recoverable_irreversible_failure | s5 | 15 | 25.00% |
| same_agent_continuation | s2 | 15 | 25.00% |
| same_agent_continuation | s3 | 15 | 25.00% |
| same_agent_continuation | s4 | 15 | 25.00% |
| same_agent_continuation | s5 | 15 | 25.00% |
| semantic_collision | s2 | 15 | 25.00% |
| semantic_collision | s3 | 15 | 25.00% |
| semantic_collision | s4 | 15 | 25.00% |
| semantic_collision | s5 | 15 | 25.00% |
| tool_evidence_usage | s2 | 15 | 25.00% |
| tool_evidence_usage | s3 | 15 | 25.00% |
| tool_evidence_usage | s4 | 15 | 25.00% |
| tool_evidence_usage | s5 | 15 | 25.00% |

## `gold_failure_step` by `perturbation_type`
| perturbation_type | gold_failure_step | count | within-group percentage |
|---|---|---:|---:|
| non_causal_textual_distraction | s2 | 21 | 25.00% |
| non_causal_textual_distraction | s3 | 21 | 25.00% |
| non_causal_textual_distraction | s4 | 21 | 25.00% |
| non_causal_textual_distraction | s5 | 21 | 25.00% |
| none | s2 | 21 | 25.00% |
| none | s3 | 21 | 25.00% |
| none | s4 | 21 | 25.00% |
| none | s5 | 21 | 25.00% |
| paraphrase | s2 | 21 | 25.00% |
| paraphrase | s3 | 21 | 25.00% |
| paraphrase | s4 | 21 | 25.00% |
| paraphrase | s5 | 21 | 25.00% |
| partial_observability | s2 | 21 | 25.00% |
| partial_observability | s3 | 21 | 25.00% |
| partial_observability | s4 | 21 | 25.00% |
| partial_observability | s5 | 21 | 25.00% |
| tool_output_truncation | s2 | 21 | 25.00% |
| tool_output_truncation | s3 | 21 | 25.00% |
| tool_output_truncation | s4 | 21 | 25.00% |
| tool_output_truncation | s5 | 21 | 25.00% |

## `gold_failure_agent` by `scenario_group`
| scenario_group | gold_failure_agent | count | within-group percentage |
|---|---|---:|---:|
| clean_broken_handoff | a5 | 15 | 25.00% |
| clean_broken_handoff | a2 | 10 | 16.67% |
| clean_broken_handoff | a8 | 10 | 16.67% |
| clean_broken_handoff | a9 | 5 | 8.33% |
| clean_broken_handoff | a10 | 5 | 8.33% |
| clean_broken_handoff | a3 | 5 | 8.33% |
| clean_broken_handoff | a6 | 5 | 8.33% |
| clean_broken_handoff | a11 | 5 | 8.33% |
| complex_collaboration | a7 | 15 | 25.00% |
| complex_collaboration | a10 | 15 | 25.00% |
| complex_collaboration | a2 | 10 | 16.67% |
| complex_collaboration | a5 | 10 | 16.67% |
| complex_collaboration | a6 | 5 | 8.33% |
| complex_collaboration | a4 | 5 | 8.33% |
| cross_agent_propagation | a8 | 20 | 33.33% |
| cross_agent_propagation | a9 | 10 | 16.67% |
| cross_agent_propagation | a5 | 5 | 8.33% |
| cross_agent_propagation | a3 | 5 | 8.33% |
| cross_agent_propagation | a12 | 5 | 8.33% |
| cross_agent_propagation | a1 | 5 | 8.33% |
| cross_agent_propagation | a2 | 5 | 8.33% |
| cross_agent_propagation | a7 | 5 | 8.33% |
| recoverable_irreversible_failure | a5 | 15 | 25.00% |
| recoverable_irreversible_failure | a6 | 10 | 16.67% |
| recoverable_irreversible_failure | a11 | 10 | 16.67% |
| recoverable_irreversible_failure | a1 | 10 | 16.67% |
| recoverable_irreversible_failure | a4 | 5 | 8.33% |
| recoverable_irreversible_failure | a8 | 5 | 8.33% |
| recoverable_irreversible_failure | a9 | 5 | 8.33% |
| same_agent_continuation | a8 | 15 | 25.00% |
| same_agent_continuation | a5 | 10 | 16.67% |
| same_agent_continuation | a4 | 10 | 16.67% |
| same_agent_continuation | a11 | 5 | 8.33% |
| same_agent_continuation | a1 | 5 | 8.33% |
| same_agent_continuation | a6 | 5 | 8.33% |
| same_agent_continuation | a12 | 5 | 8.33% |
| same_agent_continuation | a10 | 5 | 8.33% |
| semantic_collision | a8 | 15 | 25.00% |
| semantic_collision | a6 | 10 | 16.67% |
| semantic_collision | a4 | 10 | 16.67% |
| semantic_collision | a9 | 5 | 8.33% |
| semantic_collision | a10 | 5 | 8.33% |
| semantic_collision | a7 | 5 | 8.33% |
| semantic_collision | a12 | 5 | 8.33% |
| semantic_collision | a1 | 5 | 8.33% |
| tool_evidence_usage | a7 | 10 | 16.67% |
| tool_evidence_usage | a8 | 10 | 16.67% |
| tool_evidence_usage | a6 | 10 | 16.67% |
| tool_evidence_usage | a10 | 5 | 8.33% |
| tool_evidence_usage | a3 | 5 | 8.33% |
| tool_evidence_usage | a9 | 5 | 8.33% |
| tool_evidence_usage | a1 | 5 | 8.33% |
| tool_evidence_usage | a12 | 5 | 8.33% |
| tool_evidence_usage | a2 | 5 | 8.33% |

## `gold_failure_agent` by `perturbation_type`
| perturbation_type | gold_failure_agent | count | within-group percentage |
|---|---|---:|---:|
| non_causal_textual_distraction | a8 | 15 | 17.86% |
| non_causal_textual_distraction | a5 | 11 | 13.10% |
| non_causal_textual_distraction | a6 | 9 | 10.71% |
| non_causal_textual_distraction | a10 | 7 | 8.33% |
| non_causal_textual_distraction | a7 | 7 | 8.33% |
| non_causal_textual_distraction | a9 | 6 | 7.14% |
| non_causal_textual_distraction | a2 | 6 | 7.14% |
| non_causal_textual_distraction | a1 | 6 | 7.14% |
| non_causal_textual_distraction | a4 | 6 | 7.14% |
| non_causal_textual_distraction | a11 | 4 | 4.76% |
| non_causal_textual_distraction | a12 | 4 | 4.76% |
| non_causal_textual_distraction | a3 | 3 | 3.57% |
| none | a8 | 15 | 17.86% |
| none | a5 | 11 | 13.10% |
| none | a6 | 9 | 10.71% |
| none | a10 | 7 | 8.33% |
| none | a7 | 7 | 8.33% |
| none | a9 | 6 | 7.14% |
| none | a2 | 6 | 7.14% |
| none | a1 | 6 | 7.14% |
| none | a4 | 6 | 7.14% |
| none | a11 | 4 | 4.76% |
| none | a12 | 4 | 4.76% |
| none | a3 | 3 | 3.57% |
| paraphrase | a8 | 15 | 17.86% |
| paraphrase | a5 | 11 | 13.10% |
| paraphrase | a6 | 9 | 10.71% |
| paraphrase | a10 | 7 | 8.33% |
| paraphrase | a7 | 7 | 8.33% |
| paraphrase | a9 | 6 | 7.14% |
| paraphrase | a2 | 6 | 7.14% |
| paraphrase | a1 | 6 | 7.14% |
| paraphrase | a4 | 6 | 7.14% |
| paraphrase | a11 | 4 | 4.76% |
| paraphrase | a12 | 4 | 4.76% |
| paraphrase | a3 | 3 | 3.57% |
| partial_observability | a8 | 15 | 17.86% |
| partial_observability | a5 | 11 | 13.10% |
| partial_observability | a6 | 9 | 10.71% |
| partial_observability | a10 | 7 | 8.33% |
| partial_observability | a7 | 7 | 8.33% |
| partial_observability | a9 | 6 | 7.14% |
| partial_observability | a2 | 6 | 7.14% |
| partial_observability | a1 | 6 | 7.14% |
| partial_observability | a4 | 6 | 7.14% |
| partial_observability | a11 | 4 | 4.76% |
| partial_observability | a12 | 4 | 4.76% |
| partial_observability | a3 | 3 | 3.57% |
| tool_output_truncation | a8 | 15 | 17.86% |
| tool_output_truncation | a5 | 11 | 13.10% |
| tool_output_truncation | a6 | 9 | 10.71% |
| tool_output_truncation | a10 | 7 | 8.33% |
| tool_output_truncation | a7 | 7 | 8.33% |
| tool_output_truncation | a9 | 6 | 7.14% |
| tool_output_truncation | a2 | 6 | 7.14% |
| tool_output_truncation | a1 | 6 | 7.14% |
| tool_output_truncation | a4 | 6 | 7.14% |
| tool_output_truncation | a11 | 4 | 4.76% |
| tool_output_truncation | a12 | 4 | 4.76% |
| tool_output_truncation | a3 | 3 | 3.57% |

## Bias finding
- Top `gold_failure_step`: `s2` = 105/420 (25.00%).
- Top `gold_failure_agent`: `a8` = 75/420 (17.86%).
- Distinct step values meeting >=15% share: 4.
- Label-position bias detected: no.
- Evaluation blocked: no.
