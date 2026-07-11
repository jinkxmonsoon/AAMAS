# Rescue Protocol Amendment for Intratrace Ranking

## Scope
- This amendment authorizes one final minimal deterministic rescue evaluation only.
- It does not authorize calibration, weight tuning, grid search, LOSO, ablation, corpus/gold-label changes, scoring-config restoration, or paper-ready performance claims.

## Rationale
- Global candidate-step feature-vector duplication remains a severe limitation: Task 29 reported 99.19% duplicate candidate-step feature vectors.
- Task 29 also reported within-trace duplicate candidate-step rows = 0, meaning each trace's five candidate steps are distinguishable by the current feature representation.
- Because failure-step attribution is an intra-trace selection problem, this amendment permits one high-risk fixed-formula intra-trace evaluation despite global degeneracy.

## Boundary
- Predictions must be generated before private labels are read for evaluation.
- Scenario and perturbation metadata may be used only after prediction for stratified reporting.
- If CCT does not exceed the strongest baseline by the pre-specified margin, H1-R/H2-R are closed as unsupported and the rescue path stops.
