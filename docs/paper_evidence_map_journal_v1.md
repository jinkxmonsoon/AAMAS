# Journal-v1 Paper Evidence Map

## Scope

This evidence map connects Path B article claims to existing artifacts only. It does not introduce new experiments, scoring, ranking, calibration, statistical tests, corpus edits, gold-label edits, or paper-ready performance tables.

## Evidence map by major claim

| Major claim | Evidence source | What the evidence supports | Boundary / caveat |
| --- | --- | --- | --- |
| CCT requires a full-trace representation to audit collaborative failures. | `docs/09_journal_v1_reconstruction_protocol.md`, `docs/11_journal_v1_corpus_plan_and_label_rubric.md`, `docs/13_full_trace_schema_migration_plan.md` | The protocol specifies complete trace visibility, private-label separation, and full-trace audit fields. | Does not prove automatic attribution performance. |
| Failure-centered schemas create leakage and shortcut risks unless prediction views are enforced. | Full-trace schema migration plan, leakage reports, prediction-view-safe builders and audits. | The project distinguishes visible fields from private labels/provenance and audits outputs for forbidden fields. | Leakage PASS is repository/protocol evidence, not external validation. |
| Shortcut and baseline sanity checks are necessary before method claims. | Main full-trace shortcut/baseline reports and Task 18 diagnostic baseline comparisons. | The article can state that shortcuts and baselines were explicitly audited before claims. | Cannot state CCT outperformed baselines. |
| Task 18 negative diagnostic scoring did not support H1/H2. | `results/reports/journal_v1_full_trace_cct/cct_negative_diagnostic_evidence_synthesis.md`, Task 18 diagnostics, Task 25 synthesis. | Frozen uncalibrated CCT scoring was insufficient under the current feature layer. | Task 18 is diagnostic evidence, not paper-ready performance evidence. |
| Task 18 is not reproducible from the active checkout. | `results/reports/journal_v1_full_trace_cct/cct_task18_reproducibility_boundary.md`, scoring-config recovery/adjudication reports. | Missing frozen `configs/cct_scoring.yaml` provenance must be disclosed. | Do not restore/recreate the config or rerun scoring without a separate authorized task. |
| Task 18A error analysis shows failure was not mainly tie-related. | `results/reports/journal_v1_full_trace_cct/cct_uncalibrated_error_analysis.md`, `cct_negative_diagnostic_evidence_synthesis.md`. | The failure mode points toward weak/non-discriminative features and context/tool-output contributions selecting wrong steps. | Does not authorize calibration or scoring revision. |
| Task 18B feature taxonomy found proxy-heavy features. | `results/reports/journal_v1_full_trace_cct/cct_feature_semantic_audit.md`, feature dominance reports. | Existing features were dominated by position/identity proxies, content-volume proxies, and coarse cardinality fields. | The taxonomy is diagnostic, not a replacement scoring protocol. |
| Tasks 18C–18F descriptor work was reproducible but not scoring-ready. | Descriptor spec/audits, `docs/artifact_manifests/journal_v1_descriptor_augmented_features_manifest.md`, descriptor readiness gate. | Descriptor augmentation can be generated under artifact policy and leakage controls. | Readiness remained no for protocol revision/scoring. |
| Tasks 20–23 causal-flow edges can be audited under prediction-view-only constraints. | `docs/16_cct_causal_flow_edge_redesign_spec.md`, sample/full-corpus edge audit reports. | Strongest edges (`downstream_dependency_edge`, `tool_alignment_edge`, `cross_agent_dependency_edge`) were audited without private labels. | Edge audits remained representation-only; scoring stayed blocked. |
| Task 24 redesigned graphs modestly reduced graph degeneracy. | Redesigned graph diversity/degeneracy reports. | Graph signature uniqueness improved from 1 to 6; duplicate signatures decreased from 419 to 414. | Improvement is modest and not enough for scoring. |
| Task 24A redesigned features remain highly degenerate. | Redesigned feature inventory, variance, degeneracy, and readiness reports. | 420 rows yielded 6 unique feature vectors, 414 duplicates, and multiple constant features. | This blocks protocol review and scoring readiness. |
| Task 25 justifies Path B. | Backbone decision synthesis, claim reframing, pivot plan, journal viability assessment. | The strongest article backbone is protocol/benchmark/diagnostic representation with negative findings. | Performance-oriented method claims are forbidden. |

## Evidence by paper section

- **Introduction:** Use the reconstruction protocol, corpus plan, and Task 25 decision to motivate protocol-first failure attribution.
- **Methods / Benchmark protocol:** Use full-trace schema migration, leakage controls, artifact manifests, and prediction-view enforcement.
- **Diagnostic findings:** Use Task 18 negative diagnostics, Task 18A error analysis, Task 18B feature taxonomy, descriptor audits, causal-flow audits, and Task 24A degeneracy.
- **Discussion:** Use Path B decision reports to explain why negative findings are methodological evidence.
- **Limitations:** Use scoring-config provenance blocker, feature degeneracy, template sensitivity, controlled trace-bank caveat, and no external validation.

## Evidence not to use as paper-ready performance evidence

- Frozen uncalibrated CCT scores from Task 18, because the scoring config is not recoverable from the active checkout.
- Descriptor-augmented feature rows, because readiness for scoring remained no.
- Causal-flow edge counts, redesigned graph signatures, and redesigned feature vectors, because they are representation diagnostics only.
- Any baseline comparison as a superiority claim.
