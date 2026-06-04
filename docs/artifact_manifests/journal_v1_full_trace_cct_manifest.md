# Journal-v1 Full-Trace CCT Artifact Manifest

## Generated artifact policy

- Keep source code, tests, scripts, configs, compact samples, and compact Markdown reports in Git.
- Exclude full generated CCT JSONL artifacts from normal Git because they are reproducible and can make PR diffs unreviewable.
- Regenerate full artifacts locally with `python scripts/build_cct_graphs_full_trace.py`.
- Validate with `python scripts/validate_cct_graphs_full_trace.py`.
- Audit feature variance with `python scripts/audit_cct_feature_variance.py`.
- If project policy later requires versioned full artifacts, use Git LFS or release artifacts rather than normal Git blobs.

## Artifact hashes and counts

| Path | Bytes | Lines | SHA256 | Git policy |
|---|---:|---:|---|---|
| `data/interim/journal_v1_full_trace_cct/cct_graphs.jsonl` | 1101996 | 420 | `3cf635ec35a36d1ce188a4a21dc6a2af787ac539a56f3874afc9668819e46b18` | excluded from normal Git; reproducible local artifact |
| `data/interim/journal_v1_full_trace_cct/cct_features.jsonl` | 935340 | 2100 | `1568587e2d7a11adeb16fae009ef74ec43678105d0ecb215478a60a8a6447f93` | excluded from normal Git; reproducible local artifact |
| `data/interim/journal_v1_full_trace_cct/sample_cct_graphs.jsonl` | 5225 | 2 | `0daa9f5ea00b7e3f2dcfe60a8cf66108b54b40d59a7c8759fa8edd5559078144` | tracked compact sample |
| `data/interim/journal_v1_full_trace_cct/sample_cct_features.jsonl` | 4341 | 10 | `61d912cf3537bfed120a81c2c7291c0fb723e58e46e4a6959112d70c706fb8fc` | tracked compact sample |

## Expected command outputs

- `python scripts/build_cct_graphs_full_trace.py`: writes 420 graphs, 2,100 feature rows, 2 sample graphs, and 10 sample feature rows.
- `python scripts/validate_cct_graphs_full_trace.py`: passes graph count, feature count, sample coverage, and leakage checks.
- `python scripts/audit_cct_feature_variance.py`: writes descriptive variance, structural shortcut-risk, and readiness-gate reports without scoring.
