# CCT Strong Edges Full-Corpus Artifact Manifest

## Artifact policy

The full strong-edge full-corpus JSON is a generated representation-audit artifact and is excluded from normal Git review to avoid an oversized diff. It is reproducible with `python scripts/audit_cct_strong_edges_full_corpus.py`. A compact sample artifact is tracked for review.

## Generation command

```bash
python scripts/audit_cct_strong_edges_full_corpus.py
```

## Expected outputs

- Full local artifact: `results/raw/journal_v1_full_trace_cct/cct_strong_edges_full_corpus.json`
- Tracked sample artifact: `results/raw/journal_v1_full_trace_cct/sample_cct_strong_edges_full_corpus.json`
- Total traces expected: 420
- Total edges expected: 2385
- Edge types: `downstream_dependency_edge`, `tool_alignment_edge`, `cross_agent_dependency_edge`

## Artifact stats

| Artifact | SHA256 | Lines | Bytes | Git policy |
| --- | --- | ---: | ---: | --- |
| `results/raw/journal_v1_full_trace_cct/cct_strong_edges_full_corpus.json` | `98d8e59de26bceed7b8e19420e35a8be62b095cc6874bffdacd37b2614cb9619` | 56836 | 2551467 | generated locally; ignored by normal Git |
| `results/raw/journal_v1_full_trace_cct/sample_cct_strong_edges_full_corpus.json` | `8ddbacf8707af76737865b721c66a1d15e76b65d66500bd3eac07672782847ec` | 314 | 13026 | tracked compact review sample |

## Prohibitions

This manifest does not authorize scoring, ranking, gold/H6 comparison, calibration, ablation, statistical tests, or paper-ready result tables.
