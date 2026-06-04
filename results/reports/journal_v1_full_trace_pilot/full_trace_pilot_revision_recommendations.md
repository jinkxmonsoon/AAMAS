# Full-Trace Pilot Revision Recommendations

## Readiness decision after Task 14C
- `FULL_TRACE_PILOT_DIAGNOSTICALLY_READY = yes`.
- `FULL_TRACE_MAIN_CORPUS_GENERATION_ALLOWED = future_explicit_approval_required`.
- The Task 14B diagnostic sufficiency blocker is cleared for the non-final pilot, but this task does not generate or authorize silent generation of the full 420-trace corpus.

## Cleared Task 14B blockers
1. Gold failure steps are now inferable from visible prediction-view evidence in all seven clean pilot traces.
2. Gold and non-gold steps no longer rely on a single repeated message/output/tool-output template.
3. Private labels still define the evaluation target, but visible trace evidence now justifies the same attribution point.
4. Perturbed traces preserve parent label semantics and retain the necessary diagnostic evidence.

## Remaining recommendations before any full main-corpus builder task
- Further vary role order and handoff topology beyond the pilot's linear five-agent chain.
- Vary evidence cardinality and evidence-used patterns instead of keeping two evidence items and one used item on every step.
- Expand scenario-specific language templates so the full corpus does not inherit pilot regularities.
- Preserve all anti-leakage constraints: no label-revealing visible terms, no top-level failure-centered fields, and no private-label exposure in prediction views.
- Re-run schema validation, prediction-view validation, pilot audit, shortcut baselines, semantic diversity checks, and diagnostic sufficiency checks after any future builder change.

## Explicit non-actions in Task 14C
- No full 420-trace corpus was generated.
- No old failure-centered corpus was unblocked.
- No CCT graph construction or CCT scoring was implemented.
- No calibration was implemented.
- No refinement variant was implemented.
- No ablation was implemented.
- No paper-ready result table was produced.
