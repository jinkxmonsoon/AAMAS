# Rescue Experiment Design Rationale

## Scope

This report explains the design of the decisive CCT hypothesis-rescue protocol. It does not run scoring, ranking, calibration, tuning, grid search, LOSO, ablation, statistical tests, corpus/gold-label changes, scoring-config restoration, or paper-ready result tables.

## Why a rescue protocol is needed

H1/H2 remain unsupported. Task 18 reported negative frozen uncalibrated CCT diagnostics, and Task 18 is not reproducible from the active checkout because the frozen scoring configuration is missing. Task 24A then showed that redesigned CCT graph features remain highly degenerate: 6 unique feature vectors across 420 traces and 414 duplicate vectors. This means current trace-level graph features are inadequate for attribution, but it does not prove that CCT’s causal-flow thesis is false.

## Decisive design principle

The rescue experiment must move from trace-level graph summaries to **candidate step-level causal-flow features**. Failure-step attribution is a candidate-step decision, so each candidate step must receive features describing its visible causal-flow role: incoming/outgoing dependencies, tool alignment participation, cross-agent dependency participation, non-adjacent dependency involvement, and visible relation evidence.

## Why not calibrate now

Calibration would optimize a degenerate or leakage-prone representation. The protocol therefore requires leakage and degeneracy blockers before any future scoring run.

## Why compare against flat-log baselines

H2-R requires demonstrating that causal-flow graph features add signal beyond flat textual or metadata baselines under identical prediction-view constraints. If a flat-log baseline wins, the CCT rescue hypothesis remains unsupported.

## Scoring-config boundary

This protocol is not a reproduction of Task 18 and does not restore `configs/cct_scoring.yaml`. It defines a new rescue experiment configuration, `configs/rescue_experiment_v1.yaml`, for a future explicitly authorized execution task.

## Readiness

The protocol is ready for implementation of a non-scoring feature-readiness dry run. It is not ready for immediate scoring until feature degeneracy and leakage checks pass.
