# Main Corpus Revision Plan (Task 10B)

## Goal
Reduce templating risk while preserving frozen protocol constraints (counts, scenario groups, perturbation taxonomy, label semantics, and H6 expectations).

## Approved correction actions
1. Diversify agent names/roles:
   - rotate role sets by scenario and case seed;
   - vary failing agent among valid catalog members while preserving `gold_failure_agent` consistency.
2. Diversify task context wording:
   - scenario-aware context pools with deterministic seeded selection.
3. Diversify evidence-flow descriptions:
   - vary evidence item IDs and usage subsets with deterministic seeded patterns.
4. Diversify handoff forms:
   - rotate handoff pairs among available agents.
5. Diversify tool-call/output formats:
   - use bounded tool-call vocabulary and structured output templates.
6. Diversify rationale phrasing:
   - use multiple approved rationale templates with deterministic selection;
   - keep rationale in non-model-visible metadata fields.
7. Preserve schema/labels:
   - no changes to trace counts, scenario taxonomy, perturbation taxonomy, or H6 target-balance behavior.

## Execution steps
- Update `scripts/build_main_corpus.py` with deterministic template pools and scenario-aware variation.
- Regenerate corpus only via builder script.
- Re-run manifest, structural audit, semantic audit, leakage, integrity, and test suite.
- Keep evaluation blocked unless spot-check summary indicates blocker cleared.
