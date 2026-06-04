# Journal-v1 Full-Trace CCT Feature Revision Risk Report

## Scope

This report records risks for a future feature-revision task. It does not implement descriptors, change scoring, tune weights, calibrate, grid search, run LOSO, refine, ablate, run statistical tests, or produce paper-ready result tables.

## Main risks

1. **Private-label leakage risk**: descriptors related to recovery, propagation, irreversibility, and failure causes can accidentally mirror private labels or label rationales. Future extraction must reject private fields and audit generated descriptors for gold-equivalent phrases.
2. **Lexical shortcut risk**: visible scenario-specific words such as constraints, evidence conflicts, recovery attempts, and semantic collisions may become shortcuts if templates remain too regular.
3. **Position shortcut risk**: cross-agent dependency and handoff descriptors may collapse to fixed step position unless normalized against the five-step linear graph shape.
4. **LLM-judge drift risk**: descriptors requiring semantic judgment may become non-reproducible or encode hidden priors. Deterministic extraction is preferred; any judge-based descriptor must be diagnostic-only until separately locked.
5. **Reviewability risk**: full descriptor artifacts may be large. Future tasks should follow the Task 16A artifact policy: compact samples and manifests in Git, full generated artifacts reproducible locally.
6. **Premature scoring risk**: adding descriptors directly to `configs/cct_scoring.yaml` before variance/leakage audits would violate the Task 17/18 guardrails.

## Recommended next task

Create a protocol-only descriptor extraction specification and sample-only prototype for two or three deterministic descriptors, prioritizing `handoff_constraint_shift_indicator`, `evidence_ignored_indicator`, and `downstream_reference_to_prior_output`. The next task should not score them. It should define extraction rules, generate compact samples, and run leakage/variance/shortcut audits before any scoring protocol revision is proposed.

## Non-actions confirmed

No current feature payload, frozen scoring config, diagnostic result, corpus record, gold label, baseline definition, scoring formula, ranking rule, calibration routine, grid search, LOSO routine, refinement variant, ablation, statistical test, or paper-ready result table was changed by Task 18B.
