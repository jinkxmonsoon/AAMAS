# Journal-v1 Non-CCT Baseline Diagnostics Report

## Scope and prohibitions
- Corpus: `data/processed/journal_v1/main_all_traces.jsonl`.
- Total records: 420.
- This is a **diagnostic baseline layer only**.
- This is **not CCT evaluation**.
- This is **not calibrated**.
- This is **not a final paper result table**.
- This is intended to detect whether simple non-CCT heuristics already solve the corpus.
- No CCT graph construction, CCT scoring, calibration, refinement variant, ablation, or paper-ready result table was implemented.

## Diagnostic interpretation rules
- Accuracy greater than 70% on step or agent attribution flags corpus/baseline review.
- Accuracy greater than 85% on step or agent attribution blocks evaluation pending investigation.
- If non-CCT baselines remain moderate, CCT implementation may proceed only in a later approved task.

## Baseline summary
| baseline | step accuracy | agent accuracy | tuple step-agent accuracy | irreversibility | propagation | recoverability | macro scenario | macro perturbation |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| flat_log_keyword_step | 75.00% | NA | NA | NA | NA | NA | 75.00% | 75.00% |
| flat_log_keyword_agent | NA | 100.00% | NA | NA | NA | NA | NA | NA |
| flat_log_role_agent | NA | 26.19% | NA | NA | NA | NA | NA | NA |
| flat_log_keyword_step_agent | 75.00% | 100.00% | 75.00% | NA | NA | NA | 75.00% | 75.00% |
| spectrum_inspired_step | 100.00% | NA | NA | NA | NA | NA | 100.00% | 100.00% |
| spectrum_inspired_agent | NA | 100.00% | NA | NA | NA | NA | NA | NA |
| spectrum_inspired_step_agent | 100.00% | 100.00% | 100.00% | NA | NA | NA | 100.00% | 100.00% |

## Macro-by-scenario details (step accuracy)

### flat_log_keyword_step
| group | n | step accuracy |
|---|---:|---:|
| clean_broken_handoff | 60 | 75.00% |
| complex_collaboration | 60 | 75.00% |
| cross_agent_propagation | 60 | 75.00% |
| recoverable_irreversible_failure | 60 | 75.00% |
| same_agent_continuation | 60 | 75.00% |
| semantic_collision | 60 | 75.00% |
| tool_evidence_usage | 60 | 75.00% |

### flat_log_keyword_agent
| group | n | step accuracy |
|---|---:|---:|
| clean_broken_handoff | 60 | NA |
| complex_collaboration | 60 | NA |
| cross_agent_propagation | 60 | NA |
| recoverable_irreversible_failure | 60 | NA |
| same_agent_continuation | 60 | NA |
| semantic_collision | 60 | NA |
| tool_evidence_usage | 60 | NA |

### flat_log_role_agent
| group | n | step accuracy |
|---|---:|---:|
| clean_broken_handoff | 60 | NA |
| complex_collaboration | 60 | NA |
| cross_agent_propagation | 60 | NA |
| recoverable_irreversible_failure | 60 | NA |
| same_agent_continuation | 60 | NA |
| semantic_collision | 60 | NA |
| tool_evidence_usage | 60 | NA |

### flat_log_keyword_step_agent
| group | n | step accuracy |
|---|---:|---:|
| clean_broken_handoff | 60 | 75.00% |
| complex_collaboration | 60 | 75.00% |
| cross_agent_propagation | 60 | 75.00% |
| recoverable_irreversible_failure | 60 | 75.00% |
| same_agent_continuation | 60 | 75.00% |
| semantic_collision | 60 | 75.00% |
| tool_evidence_usage | 60 | 75.00% |

### spectrum_inspired_step
| group | n | step accuracy |
|---|---:|---:|
| clean_broken_handoff | 60 | 100.00% |
| complex_collaboration | 60 | 100.00% |
| cross_agent_propagation | 60 | 100.00% |
| recoverable_irreversible_failure | 60 | 100.00% |
| same_agent_continuation | 60 | 100.00% |
| semantic_collision | 60 | 100.00% |
| tool_evidence_usage | 60 | 100.00% |

### spectrum_inspired_agent
| group | n | step accuracy |
|---|---:|---:|
| clean_broken_handoff | 60 | NA |
| complex_collaboration | 60 | NA |
| cross_agent_propagation | 60 | NA |
| recoverable_irreversible_failure | 60 | NA |
| same_agent_continuation | 60 | NA |
| semantic_collision | 60 | NA |
| tool_evidence_usage | 60 | NA |

### spectrum_inspired_step_agent
| group | n | step accuracy |
|---|---:|---:|
| clean_broken_handoff | 60 | 100.00% |
| complex_collaboration | 60 | 100.00% |
| cross_agent_propagation | 60 | 100.00% |
| recoverable_irreversible_failure | 60 | 100.00% |
| same_agent_continuation | 60 | 100.00% |
| semantic_collision | 60 | 100.00% |
| tool_evidence_usage | 60 | 100.00% |

## Macro-by-perturbation details (step accuracy)

### flat_log_keyword_step
| group | n | step accuracy |
|---|---:|---:|
| non_causal_textual_distraction | 84 | 75.00% |
| none | 84 | 75.00% |
| paraphrase | 84 | 75.00% |
| partial_observability | 84 | 75.00% |
| tool_output_truncation | 84 | 75.00% |

### flat_log_keyword_agent
| group | n | step accuracy |
|---|---:|---:|
| non_causal_textual_distraction | 84 | NA |
| none | 84 | NA |
| paraphrase | 84 | NA |
| partial_observability | 84 | NA |
| tool_output_truncation | 84 | NA |

### flat_log_role_agent
| group | n | step accuracy |
|---|---:|---:|
| non_causal_textual_distraction | 84 | NA |
| none | 84 | NA |
| paraphrase | 84 | NA |
| partial_observability | 84 | NA |
| tool_output_truncation | 84 | NA |

### flat_log_keyword_step_agent
| group | n | step accuracy |
|---|---:|---:|
| non_causal_textual_distraction | 84 | 75.00% |
| none | 84 | 75.00% |
| paraphrase | 84 | 75.00% |
| partial_observability | 84 | 75.00% |
| tool_output_truncation | 84 | 75.00% |

### spectrum_inspired_step
| group | n | step accuracy |
|---|---:|---:|
| non_causal_textual_distraction | 84 | 100.00% |
| none | 84 | 100.00% |
| paraphrase | 84 | 100.00% |
| partial_observability | 84 | 100.00% |
| tool_output_truncation | 84 | 100.00% |

### spectrum_inspired_agent
| group | n | step accuracy |
|---|---:|---:|
| non_causal_textual_distraction | 84 | NA |
| none | 84 | NA |
| paraphrase | 84 | NA |
| partial_observability | 84 | NA |
| tool_output_truncation | 84 | NA |

### spectrum_inspired_step_agent
| group | n | step accuracy |
|---|---:|---:|
| non_causal_textual_distraction | 84 | 100.00% |
| none | 84 | 100.00% |
| paraphrase | 84 | 100.00% |
| partial_observability | 84 | 100.00% |
| tool_output_truncation | 84 | 100.00% |

## Diagnostic interpretation
- Gate status: **BLOCKED**.
- Blockers: flat_log_keyword_agent.agent_accuracy=1.0000 exceeds block threshold 0.85; flat_log_keyword_step_agent.agent_accuracy=1.0000 exceeds block threshold 0.85; spectrum_inspired_step.step_accuracy=1.0000 exceeds block threshold 0.85; spectrum_inspired_agent.agent_accuracy=1.0000 exceeds block threshold 0.85; spectrum_inspired_step_agent.step_accuracy=1.0000 exceeds block threshold 0.85; spectrum_inspired_step_agent.agent_accuracy=1.0000 exceeds block threshold 0.85
- Review flags: flat_log_keyword_step.step_accuracy=0.7500 exceeds review threshold 0.70; flat_log_keyword_step_agent.step_accuracy=0.7500 exceeds review threshold 0.70
- Raw JSON output: `results/raw/journal_v1/non_cct_baseline_diagnostics.json`.
