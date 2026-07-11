# CCT Descriptor-Augmented Artifact Size Report

## Diff size diagnosis
The full descriptor-augmented JSON contains 2,100 row objects and is a generated artifact. Keeping it in normal Git can make pull requests unreviewable.

## Artifact sizes
- Full local artifact: `results/raw/journal_v1_full_trace_cct/cct_descriptor_augmented_features.json`
  - SHA256: `59f3dab9d445147c7b0c2a0e15445514ddde01b3865ac74e291b1902cabd5420`
  - Lines: 50402
  - Bytes: 2772842
- Tracked sample artifact: `results/raw/journal_v1_full_trace_cct/sample_cct_descriptor_augmented_features.json`
  - SHA256: `2bcde7bcb636ba12d2f9b85dc5e5c305827db15663ff213f456853b4c9bfc0d6`
  - Lines: 242
  - Bytes: 13325

## Policy
- Keep source code, scripts, tests, compact reports, readiness reports, and manifests in Git.
- Keep only compact sample augmented feature artifacts in Git.
- Regenerate the full augmented feature artifact locally with `python scripts/build_cct_descriptor_augmented_features.py`.
- Do not track large full JSON artifacts in normal Git when they make reviews unmanageable.
- Use Git LFS or release artifacts if full generated artifacts must later be versioned.
