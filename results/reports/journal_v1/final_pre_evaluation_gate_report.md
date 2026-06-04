# Final Pre-Evaluation Gate Report

## Scope and provenance
- Task: 10H final pre-evaluation corpus gate and shortcut audit consolidation.
- Canonical corpus-correction PR: PR #13 supersedes PR #12.
- Final branch: `work`.
- Audited source HEAD before this consolidation commit: `ff1e61fa5e6a5f22555cdde4af1999f66cd6ad05`.
- Corpus: `data/processed/journal_v1/main_all_traces.jsonl`.
- Guardrail: this is a corpus-gate report only; no CCT scoring, calibration, refinement, empirical evaluation, or paper result tables are implemented.

## Final decision
- Evaluation allowed / blocked: **allowed**.
- Scope of allowance: a future explicitly approved task may implement metric interfaces and trivial baselines; this report does not authorize CCT scoring, calibration, refinement, empirical runs, or paper result tables.

## Shortcut checks
| check | status | evidence |
|---|---|---|
| no single failure step > 40% | PASS | top=s2 25.00% |
| no single failure agent > 50% | PASS | top=a8 17.86% |
| no scenario has all failures at one step | PASS | collapsed=none |
| no perturbation type collapses to one failure step | PASS | collapsed=none |
| always_s2 <= 40% | PASS | 25.00% |
| majority_step <= 40% | PASS | 25.00% |

## `gold_failure_step` distribution overall
| gold_failure_step | count | percentage |
|---|---:|---:|
| s2 | 105 | 25.00% |
| s3 | 105 | 25.00% |
| s4 | 105 | 25.00% |
| s5 | 105 | 25.00% |

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

## `gold_failure_agent` distribution overall
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

## H6 label distribution
| H6 label | false | true |
|---|---:|---:|
| gold_propagation | 210 | 210 |
| gold_irreversibility | 210 | 210 |
| gold_recoverability | 210 | 210 |

## Semantic spot-check summary
- Source report: `results/reports/journal_v1/main_semantic_spotcheck_report.md`.
- Sampled records: 19.
- Accept/revise/reject: 19/0/0.
- Templating risk level: low.
- Semantic spot-check blocker: no.

## Manual sanity-check summary
- Source report: `results/reports/journal_v1/main_failure_step_semantic_sanity_check.md`.
- Inspected records: 6.
- Coverage: clean `s2`, `s3`, `s4`, `s5`; perturbed `s3` and `s5` child traces.
- Accept/revise/reject: 6/0/0.
- Non-s2 semantic grounding: accepted in inspected sample.
- Perturbation preservation: inspected perturbed traces preserve parent `gold_failure_step` and `gold_failure_agent`.

## Remaining known risks
- The corpus remains synthetic and controlled; shortcut checks do not establish external validity.
- Manual sanity checking covered a small sample, not full human adjudication of every trace.
- Balanced failure-step and H6 distributions reduce obvious shortcuts but do not prove future model behavior or hypothesis outcomes.
- Future evaluation must still keep corpus family split safety, leakage checks, metric definitions, and baseline definitions under protocol control.

## Gate conclusion
- Final pre-evaluation corpus gate: **cleared**.
- No CCT scoring, calibration, refinement, empirical evaluation, or paper result table was produced by this task.
