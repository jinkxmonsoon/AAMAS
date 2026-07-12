# CCT Next Experiment Recommendation

## Recommendation

Choose **Option C — Redesign CCT graph/feature extraction around richer non-position causal-flow edges before scoring**.

This is a recommendation for the next methodological design task, not authorization to run scoring or revise the protocol. The next task should define and audit a richer causal-flow representation while preserving protected-item constraints.

## Why Option C is selected

- Task 18/18A evidence indicates current failure is not mainly a tie problem; it is a weak/non-discriminative feature problem.
- Task 18B indicates the current feature layer is dominated by position/identity proxies, content-volume proxies, and coarse cardinality fields.
- Task 18C/18D show causal-flow descriptors are feasible as audit/review artifacts.
- Task 18E/18F show descriptor augmentation remains reproducible and leakage-audited, but not ready for protocol revision or scoring.
- Therefore, the scientifically appropriate next step is to improve representation validity before any calibration or scoring expansion.

## Rejected immediate paths

### Immediate calibration is rejected as premature

Calibration of the current feature layer is blocked because it risks optimizing proxy-heavy, weakly causal features. H3 remains blocked until feature validity improves.

### Descriptor scoring is rejected as premature

Descriptor-augmented scoring is blocked because the readiness gate remains conservative:

- `AUGMENTED_FEATURE_LAYER_READY_FOR_PROTOCOL_REVISION = no`
- `AUGMENTED_FEATURE_LAYER_READY_FOR_SCORING = no`

### Performance-superiority positioning is rejected

The paper contribution must not be framed around CCT superiority under current evidence. Option D may be used as a claim-boundary guardrail, but it should not replace the primary methodological need to improve causal-flow representation.

## Next recommended task

Draft a no-scoring, no-calibration representation-redesign task with the following scope:

1. Define richer non-position causal-flow edge categories.
2. Specify visible-evidence constraints and leakage/shortcut audits before any scoring use.
3. Produce a compact schema/specification and review samples only.
4. Define readiness criteria for a future scoring task without running scoring.
5. Preserve existing corpus, gold labels, metrics, baselines, seeds, and output formats.

## Non-actions in this recommendation

No scoring, ranking, protocol revision, calibration, grid search, LOSO, refinement, ablation, statistical test, empirical hypothesis test, corpus change, gold-label change, or paper-ready result table is produced here.
