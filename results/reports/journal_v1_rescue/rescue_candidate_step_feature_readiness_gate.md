# Rescue Candidate-Step Feature Readiness Gate

- RESCUE_CANDIDATE_STEP_FEATURES_READY_FOR_SCORING = no
- Authorized next action if yes: one future minimal scoring task under `configs/rescue_experiment_v1.yaml` only.
- Recommended next action if no: redesign candidate-step features once, then rerun this dry-run gate before scoring.
- Total candidate-step rows: 2100
- Leakage status: PASS
- Duplicate candidate-step feature-vector percentage: 99.19%
- Feature families over 95% constant threshold: 3

## Blockers
- duplicate candidate-step feature vectors exceed 50%
- feature families exceed 95% constant threshold: has_visible_tool_call, has_visible_tool_output, has_visible_step_notes

## Non-action confirmation
- No scoring, ranking, gold/H6 comparison, calibration, tuning, grid search, LOSO, ablation, statistical test, corpus/gold-label change, scoring-config restoration, or paper-ready result table was produced.
