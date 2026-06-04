# Journal-v1 Non-CCT Baseline Leakage Correction Plan

## Current status

Task 12A corrected the immediate baseline input bug by introducing a strict prediction-view module and updating flat-log/spectrum diagnostics to operate on sanitized views only. Corrected diagnostics still block evaluation because step attribution remains 100% for `spectrum_inspired_step`, indicating remaining leakage through failure-centered visible content.

## Corrections completed in Task 12A

1. Added `src/cctdiag/io/views.py` with:
   - `make_prediction_view(record)`;
   - `make_private_label_view(record)`;
   - `assert_no_gold_leakage(prediction_view)`.
2. Removed gold labels, private metadata, H6 rationale/evidence fields, target-equivalent top-level `step_id`/`agent_id`, and top-level handoff pointers from prediction input.
3. Updated non-CCT baselines to reject raw records and consume prediction views only.
4. Regenerated non-CCT diagnostic raw/report outputs.

## Remaining blocker

The corpus still lacks a full ordered multi-step trace representation. Each record is centered on the failure step, so even sanitized visible fields can reveal the target step through phase and event content. This is not safe for CCT evaluation.

## Required follow-up before CCT

- Revise the corpus schema to include an ordered full-trace representation for every trace.
- Store per-step visible fields in a `steps` array or equivalent structure, with step and agent identifiers used only to enumerate all candidate events, not to mark the failure point.
- Keep private labels/rationales/evidence/provenance outside the prediction view.
- Regenerate or migrate Journal-v1 records through an explicitly approved corpus-schema correction task.
- Rerun leakage diagnostics and non-CCT baselines on the full-trace prediction view.
- Proceed to CCT implementation only after the corrected full-trace view no longer triggers blocker thresholds.

## Prohibited work while blocked

- No CCT graph construction.
- No CCT scoring.
- No calibration.
- No V2 refinement.
- No ablations.
- No paper-ready result tables.
