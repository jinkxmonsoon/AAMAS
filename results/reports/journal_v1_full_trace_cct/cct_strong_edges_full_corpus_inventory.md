# CCT Strong Edges Full-Corpus Inventory

- Branch: `work`
- HEAD before audit run: `1d32a233e623dc8b3a05f7327d9bbac857df38ba`
- `configs/cct_scoring.yaml` exists: False
- Task 18 reproducibility status: `NOT_REPRODUCIBLE_FROM_CURRENT_CHECKOUT`
- Scope: representation-only full-corpus audit; no scoring dependency.
- Input corpus: `data/processed/journal_v1_full_trace/main_full_trace_all.jsonl`
- Full local raw output: `results/raw/journal_v1_full_trace_cct/cct_strong_edges_full_corpus.json` (generated, ignored by Git)
- Tracked compact sample output: `results/raw/journal_v1_full_trace_cct/sample_cct_strong_edges_full_corpus.json`
- Artifact manifest: `docs/artifact_manifests/cct_strong_edges_full_corpus_manifest.md`
- Total traces processed: 420
- Total clean traces: 84
- Total perturbed traces: 336
- Total edges generated: 2385
- Edge types in scope: `downstream_dependency_edge`, `tool_alignment_edge`, `cross_agent_dependency_edge`
- Edge types out of scope: `constraint_shift_edge`, `semantic_collision_edge`, `evidence_conflict_edge`, `evidence_omission_edge`, `correction_opportunity_edge`, `correction_attempt_edge`, `unresolved_caveat_edge`

## Edge counts by type
- cross_agent_dependency_edge: 840
- downstream_dependency_edge: 705
- tool_alignment_edge: 840
