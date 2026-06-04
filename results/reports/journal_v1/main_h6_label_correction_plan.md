# Main H6 Label-Consistency Correction Plan (Task 10D)

## Objective
Remove H6 label-evidence contradictions while preserving frozen corpus counts, scenario taxonomy, perturbation taxonomy, and label-balance expectations.

## Planned corrections
1. **Irreversibility conditioning**
   - If `gold_irreversibility=true`: evidence must indicate persistence/unrecovered consequence.
   - If `gold_irreversibility=false`: evidence must indicate successful downstream correction.
2. **Recoverability conditioning**
   - If `gold_recoverability=true`: `recovery_opportunity` must be `available_and_used` or `available_but_missed`.
   - If `gold_recoverability=false`: `recovery_opportunity` must be `not_applicable_or_unavailable`.
3. **Propagation conditioning**
   - If `gold_propagation=true`: evidence must include downstream dependency/reuse/integration.
   - If `gold_propagation=false`: evidence must state local containment/no downstream reuse.
4. **Rationale policy**
   - Keep metadata-only rationale, but ensure non-generic bounded templates with semantic anchors.

## Execution steps
- Update `scripts/build_main_corpus.py` with conditional evidence generation.
- Regenerate `data/processed/journal_v1/*.jsonl` via approved builder only.
- Rerun:
  - `scripts/audit_h6_semantic_consistency.py`
  - `scripts/audit_main_corpus_semantics.py`
  - `scripts/audit_main_corpus.py`
  - schema/label/leakage/integrity checks
  - manifest generation.
- Update logs/locks/changelog and keep evaluation blocked unless H6 audit passes.
