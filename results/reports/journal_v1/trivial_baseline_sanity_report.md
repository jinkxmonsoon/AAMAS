# Journal-v1 Trivial Baseline Sanity Report

## Scope and prohibitions
- Corpus: `data/processed/journal_v1/main_all_traces.jsonl`.
- Total records: 420.
- This is a **diagnostic sanity check only**.
- This is **not a paper result table**.
- This is **not a comparison against CCT**.
- This is **not evidence for H1**.
- These values are used only to detect remaining obvious shortcuts before future approved method work.
- No CCT scoring, calibration, refinement variant, ablation, or paper-ready result table was implemented.

## Shortcut-risk gate rules
- If any trivial baseline step accuracy is greater than 50%, evaluation remains blocked.
- If `majority_agent` agent accuracy is greater than 50%, evaluation remains blocked.
- If random or first/last active agent performance is unexpectedly high, flag for review.
- Otherwise, mark the trivial-baseline gate as passed.

## Baseline summary
| baseline | step accuracy | agent accuracy | tuple step-agent accuracy | irreversibility | propagation | recoverability | macro scenario | macro perturbation |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| majority_step | 25.00% | NA | NA | NA | NA | NA | 25.00% | 25.00% |
| majority_agent | NA | 17.86% | NA | NA | NA | NA | NA | NA |
| always_s2 | 25.00% | NA | NA | NA | NA | NA | 25.00% | 25.00% |
| random_step_seeded | 19.76% | NA | NA | NA | NA | NA | 19.76% | 19.76% |
| random_agent_seeded | NA | 33.10% | NA | NA | NA | NA | NA | NA |
| first_active_agent | NA | 25.00% | NA | NA | NA | NA | NA | NA |
| last_active_agent | NA | 25.00% | NA | NA | NA | NA | NA | NA |
| same_as_parent_for_perturbations | NA | NA | NA | NA | NA | NA | NA | NA |

## Macro-by-scenario details (step accuracy)

### majority_step
| group | n | step accuracy |
|---|---:|---:|
| clean_broken_handoff | 60 | 25.00% |
| complex_collaboration | 60 | 25.00% |
| cross_agent_propagation | 60 | 25.00% |
| recoverable_irreversible_failure | 60 | 25.00% |
| same_agent_continuation | 60 | 25.00% |
| semantic_collision | 60 | 25.00% |
| tool_evidence_usage | 60 | 25.00% |

### majority_agent
| group | n | step accuracy |
|---|---:|---:|
| clean_broken_handoff | 60 | NA |
| complex_collaboration | 60 | NA |
| cross_agent_propagation | 60 | NA |
| recoverable_irreversible_failure | 60 | NA |
| same_agent_continuation | 60 | NA |
| semantic_collision | 60 | NA |
| tool_evidence_usage | 60 | NA |

### always_s2
| group | n | step accuracy |
|---|---:|---:|
| clean_broken_handoff | 60 | 25.00% |
| complex_collaboration | 60 | 25.00% |
| cross_agent_propagation | 60 | 25.00% |
| recoverable_irreversible_failure | 60 | 25.00% |
| same_agent_continuation | 60 | 25.00% |
| semantic_collision | 60 | 25.00% |
| tool_evidence_usage | 60 | 25.00% |

### random_step_seeded
| group | n | step accuracy |
|---|---:|---:|
| clean_broken_handoff | 60 | 11.67% |
| complex_collaboration | 60 | 15.00% |
| cross_agent_propagation | 60 | 16.67% |
| recoverable_irreversible_failure | 60 | 23.33% |
| same_agent_continuation | 60 | 16.67% |
| semantic_collision | 60 | 31.67% |
| tool_evidence_usage | 60 | 23.33% |

### random_agent_seeded
| group | n | step accuracy |
|---|---:|---:|
| clean_broken_handoff | 60 | NA |
| complex_collaboration | 60 | NA |
| cross_agent_propagation | 60 | NA |
| recoverable_irreversible_failure | 60 | NA |
| same_agent_continuation | 60 | NA |
| semantic_collision | 60 | NA |
| tool_evidence_usage | 60 | NA |

### first_active_agent
| group | n | step accuracy |
|---|---:|---:|
| clean_broken_handoff | 60 | NA |
| complex_collaboration | 60 | NA |
| cross_agent_propagation | 60 | NA |
| recoverable_irreversible_failure | 60 | NA |
| same_agent_continuation | 60 | NA |
| semantic_collision | 60 | NA |
| tool_evidence_usage | 60 | NA |

### last_active_agent
| group | n | step accuracy |
|---|---:|---:|
| clean_broken_handoff | 60 | NA |
| complex_collaboration | 60 | NA |
| cross_agent_propagation | 60 | NA |
| recoverable_irreversible_failure | 60 | NA |
| same_agent_continuation | 60 | NA |
| semantic_collision | 60 | NA |
| tool_evidence_usage | 60 | NA |

### same_as_parent_for_perturbations
| group | n | step accuracy |
|---|---:|---:|
| clean_broken_handoff | 60 | NA |
| complex_collaboration | 60 | NA |
| cross_agent_propagation | 60 | NA |
| recoverable_irreversible_failure | 60 | NA |
| same_agent_continuation | 60 | NA |
| semantic_collision | 60 | NA |
| tool_evidence_usage | 60 | NA |

## Macro-by-perturbation details (step accuracy)

### majority_step
| group | n | step accuracy |
|---|---:|---:|
| non_causal_textual_distraction | 84 | 25.00% |
| none | 84 | 25.00% |
| paraphrase | 84 | 25.00% |
| partial_observability | 84 | 25.00% |
| tool_output_truncation | 84 | 25.00% |

### majority_agent
| group | n | step accuracy |
|---|---:|---:|
| non_causal_textual_distraction | 84 | NA |
| none | 84 | NA |
| paraphrase | 84 | NA |
| partial_observability | 84 | NA |
| tool_output_truncation | 84 | NA |

### always_s2
| group | n | step accuracy |
|---|---:|---:|
| non_causal_textual_distraction | 84 | 25.00% |
| none | 84 | 25.00% |
| paraphrase | 84 | 25.00% |
| partial_observability | 84 | 25.00% |
| tool_output_truncation | 84 | 25.00% |

### random_step_seeded
| group | n | step accuracy |
|---|---:|---:|
| non_causal_textual_distraction | 84 | 15.48% |
| none | 84 | 26.19% |
| paraphrase | 84 | 10.71% |
| partial_observability | 84 | 23.81% |
| tool_output_truncation | 84 | 22.62% |

### random_agent_seeded
| group | n | step accuracy |
|---|---:|---:|
| non_causal_textual_distraction | 84 | NA |
| none | 84 | NA |
| paraphrase | 84 | NA |
| partial_observability | 84 | NA |
| tool_output_truncation | 84 | NA |

### first_active_agent
| group | n | step accuracy |
|---|---:|---:|
| non_causal_textual_distraction | 84 | NA |
| none | 84 | NA |
| paraphrase | 84 | NA |
| partial_observability | 84 | NA |
| tool_output_truncation | 84 | NA |

### last_active_agent
| group | n | step accuracy |
|---|---:|---:|
| non_causal_textual_distraction | 84 | NA |
| none | 84 | NA |
| paraphrase | 84 | NA |
| partial_observability | 84 | NA |
| tool_output_truncation | 84 | NA |

### same_as_parent_for_perturbations
| group | n | step accuracy |
|---|---:|---:|
| non_causal_textual_distraction | 84 | NA |
| none | 84 | NA |
| paraphrase | 84 | NA |
| partial_observability | 84 | NA |
| tool_output_truncation | 84 | NA |

## Shortcut-risk interpretation
- Gate status: **PASSED**.
- Blockers: none.
- Review flags: none.
- Raw JSON output: `results/raw/journal_v1/trivial_baseline_sanity.json`.
