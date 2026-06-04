# Main Failure-Step Revision Plan

## Trigger
- Task 10E found `gold_failure_step=s2` in 420/420 traces (100.00%).
- `majority_step` and `always_s2` diagnostics were therefore 100.00%, blocking evaluation.

## Authorized correction scope
- Revise only the deterministic Journal-v1 main-corpus generator and regenerate the main corpus through `scripts/build_main_corpus.py`.
- Do not manually edit JSONL corpus rows.
- Do not implement metrics, baselines, CCT scoring, calibration, or result tables.

## Semantic revision design
- Assign clean cases cyclically across `s2`, `s3`, `s4`, and `s5` using deterministic case order.
- Generate 5-step traces whenever `s5` is selected so the label is supported by `step_catalog`.
- Bind `gold_failure_agent` to the agent responsible for the selected failure step.
- Reflect the selected failure step in `step_id`, `gold_failure_step`, `gold_failure_agent`, handoff fields, phase-specific input/output/tool context, `propagation_evidence`, `irreversibility_evidence`, and `label_rationale`.
- Preserve each clean parent case's failure-step and agent labels in all perturbation variants; `degraded_observability_note` remains `none` because no perturbation intentionally changes the gold label.

## Target constraints
- No single `gold_failure_step` may exceed 40% of all traces.
- At least 3 distinct `gold_failure_step` values must each appear in at least 15% of traces.
- `majority_step` expected accuracy must be <= 40%.
- `always_s2` expected accuracy must be <= 40%.

## Post-revision gate
- Regenerate the corpus using `scripts/build_main_corpus.py`.
- Rerun schema, label consistency, leakage, integrity, H6 consistency, semantic spot-check, label-position bias, trivial-risk, manifest/hash generation, and unit-test checks.
- Evaluation may proceed past this gate only if all listed audits pass and no Task 10F shortcut threshold is violated.
