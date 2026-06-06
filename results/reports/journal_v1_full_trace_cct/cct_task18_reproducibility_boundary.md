# Task 18 Reproducibility Boundary

## Scope

This report records the reproducibility boundary created by the missing frozen CCT scoring configuration and the Task 20F hash adjudication. It does not run scoring, ranking, gold/H6 comparison, calibration, grid search, LOSO, refinement, ablation, statistical tests, corpus/gold-label changes, or paper-ready result tables.

## Boundary decision

- Task 18 output classification: `DIAGNOSTIC_EVIDENCE_WITH_RECORDED_OUTPUTS`
- Current-repo reproducibility classification: `NOT_REPRODUCIBLE_FROM_CURRENT_CHECKOUT`
- Paper-ready empirical-evidence classification: `NOT_PAPER_READY_EMPIRICAL_EVIDENCE`
- Current use allowed: internal methodological motivation for representation redesign and provenance governance only
- Current use forbidden: superiority claims, calibrated performance claims, new hypothesis support, or paper-ready result tables

## Rationale

Task 18 depended on the frozen CCT scoring configuration expected at `configs/cct_scoring.yaml` with SHA256 `053f19066923d8d22d27b22727e75876f939f2a60480484c4028eabd07ad0855`. The active checkout does not contain that file. Task 20C/20D found no local or externally accessible authoritative file in this environment. Task 20E/20F preserved two PR #22 candidates, but neither the raw candidate hash (`435c4703a90171c8bf246a4fa9e188e70800c66c5e9446d19f74de94b32bb`) nor the PR-visible candidate hash (`1fe4362714cf79a69bd81d0ffe8b82403cc2c2e99abc9f6c7579ed0253278a4a`) matched the expected frozen hash.

## Consequence for hypotheses

- H1 remains unsupported under the current frozen uncalibrated scoring/features.
- H2 remains unsupported under the current frozen uncalibrated scoring/features.
- H3 remains blocked because calibration before feature validity and scoring-config provenance recovery is premature.
- H4 remains blocked.
- H6 remains open but unsupported by scoring evidence.

## Required recovery path

1. Provide an exact raw file, patch, archive, bundle, or signed artifact whose SHA256 is `053f19066923d8d22d27b22727e75876f939f2a60480484c4028eabd07ad0855`.
2. Restore `configs/cct_scoring.yaml` exactly from that byte source.
3. Run config-presence and scoring-protocol validators without running scoring.
4. Only after a separate explicit protocol task may any future frozen rerun or scoring-related work be considered.

## Non-action confirmation

No non-matching config was restored. No expected hash was modified. No scoring, ranking, full-corpus edge extraction, gold/H6 comparison, calibration, grid search, LOSO, scoring refinement, ablation, statistical test, corpus/gold-label change, or paper-ready result table was produced.
