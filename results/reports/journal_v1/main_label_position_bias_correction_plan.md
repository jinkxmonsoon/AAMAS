# Journal-v1 Main Label-Position Bias Correction Plan

## Status
- Evaluation remains blocked.
- Exact blocking reason: `gold_failure_step=s2` appears in 420/420 traces (100.00%), causing `majority_step` and `always_s2` shortcut diagnostics to exceed 50%.

## Non-action taken in this task
- The corpus was not silently edited.
- Gold labels were not changed.
- No metrics, baselines, CCT scoring, calibration, or result tables were implemented.

## Required before evaluation can proceed
1. Obtain explicit authorization for corpus revision or a written scientific justification for the observed step-position concentration.
2. If revision is authorized, revise generation/labeling procedures so failure-step positions are structurally diversified without changing the protected protocol silently.
3. Regenerate or relabel only under the approved correction task, then rerun the full audit suite including this script.
4. Keep `EXPERIMENT_CHANGELOG.md`, `RESEARCH_LOG.md`, and `PROTOCOL_LOCK.md` synchronized with the gate status.
