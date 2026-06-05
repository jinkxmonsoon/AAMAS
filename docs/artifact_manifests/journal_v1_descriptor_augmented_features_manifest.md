# Journal-v1 Descriptor-Augmented Features Manifest

## Generation command
```bash
python scripts/build_cct_descriptor_augmented_features.py
```

## Expected outputs
- Full local artifact: `results/raw/journal_v1_full_trace_cct/cct_descriptor_augmented_features.json` (generated, ignored for normal Git review)
- Tracked sample artifact: `results/raw/journal_v1_full_trace_cct/sample_cct_descriptor_augmented_features.json`
- Compact reports: `results/reports/journal_v1_full_trace_cct/*descriptor_augmented*.md`

## Expected counts
- Source trace count: 420
- Expected row count: 2100
- Join completeness: 2100/2100
- Descriptor columns: descriptor_agent_role, descriptor_handoff_context, descriptor_visible_step_evidence
- Leakage status: PASS
- AUGMENTED_FEATURE_LAYER_READY_FOR_PROTOCOL_REVISION = no
- AUGMENTED_FEATURE_LAYER_READY_FOR_SCORING = no

## Artifact hashes and sizes
| Artifact | SHA256 | Lines | Bytes | Git policy |
| --- | --- | ---: | ---: | --- |
| `results/raw/journal_v1_full_trace_cct/cct_descriptor_augmented_features.json` | `59f3dab9d445147c7b0c2a0e15445514ddde01b3865ac74e291b1902cabd5420` | 50402 | 2772842 | regenerate locally; ignored |
| `results/raw/journal_v1_full_trace_cct/sample_cct_descriptor_augmented_features.json` | `2bcde7bcb636ba12d2f9b85dc5e5c305827db15663ff213f456853b4c9bfc0d6` | 242 | 13325 | tracked compact sample |

## Review policy
Keep code, tests, compact reports, readiness gates, and manifests in Git. Keep only compact sample augmented feature artifacts in Git. If full generated artifacts need archival/versioning later, use Git LFS or release artifact handling rather than normal Git diffs.

## Non-actions
No scoring, ranking, protocol revision, calibration, grid search, LOSO, refinement, ablation, statistical test, empirical hypothesis test, or paper-ready result table is produced by this artifact build.
