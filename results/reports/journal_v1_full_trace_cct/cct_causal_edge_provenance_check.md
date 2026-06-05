# CCT Causal Edge Provenance Check

- Branch: `work`
- HEAD: `ee0da26d34d442b95a1a9e2a5e36c9d4de7204cb`
- Git status: `M EXPERIMENT_CHANGELOG.md
 M PROTOCOL_LOCK.md
 M RESEARCH_LOG.md
 M data/interim/journal_v1_full_trace_cct/sample_cct_causal_edge_augmented_graphs.jsonl
 M docs/16_cct_causal_flow_edge_redesign_spec.md
 M results/raw/journal_v1_full_trace_cct/cct_causal_edge_sample_prototype.json
 M results/reports/journal_v1_full_trace_cct/cct_causal_edge_sample_template_sensitivity_report.md
 M scripts/prototype_cct_causal_edges_sample.py
 M scripts/validate_repo.py
 M src/cctdiag/cct/causal_edges.py
 M tests/test_cct_causal_edges_no_private_leakage.py
 M tests/test_cct_causal_edges_sample.py
?? results/reports/journal_v1_full_trace_cct/cct_causal_edge_provenance_check.md
?? results/reports/journal_v1_full_trace_cct/cct_causal_edge_sample_refined_inventory.md
?? results/reports/journal_v1_full_trace_cct/cct_causal_edge_sample_refined_readiness_gate.md
?? results/reports/journal_v1_full_trace_cct/cct_causal_edge_template_sensitivity_refinement_plan.md`
- `configs/` entries: ablations.yaml, baselines.yaml, corpus_plan.yaml, label_rubric.yaml, metrics.yaml, protocol.yaml, robustness.yaml, seeds.yaml
- `configs/cct_scoring.yaml` exists: false
- `configs/cct_scoring.yaml` tracked in current index: false
- `configs/cct_scoring.yaml` history in current checkout: `none_in_current_git_history`
- Ignore-rule status: `not_ignored_by_current_gitignore`
- Diagnosis: configs/cct_scoring.yaml is absent, untracked, not ignored, and has no history in the current branch checkout; this is best treated as a branch/checkpoint provenance anomaly requiring a separate protocol-recovery task from an authoritative source.
- Safe recovery path: do not recreate or modify this config in Task 20B; open a separate protocol-recovery task to locate the authoritative frozen config and record provenance before restoring it.
