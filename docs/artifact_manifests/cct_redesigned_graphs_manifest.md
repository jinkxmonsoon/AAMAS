# CCT Redesigned Graph Artifact Manifest

## Artifact policy

The full redesigned graph JSONL is a generated representation artifact and is excluded from normal Git review to avoid oversized diffs. It is reproducible with `python scripts/build_cct_redesigned_graphs.py`. The compact sample graph JSONL, inventory JSON, reports, and manifest are tracked.

## Generation command

```bash
python scripts/build_cct_redesigned_graphs.py
```

## Expected outputs

- Full local graphs: `data/interim/journal_v1_full_trace_cct_redesigned/cct_redesigned_graphs.jsonl`
- Tracked sample graphs: `data/interim/journal_v1_full_trace_cct_redesigned/sample_cct_redesigned_graphs.jsonl`
- Tracked inventory JSON: `data/interim/journal_v1_full_trace_cct_redesigned/cct_redesigned_graph_inventory.json`
- Total redesigned graphs expected: 420
- Causal-flow edge types: `downstream_dependency_edge`, `tool_alignment_edge`, `cross_agent_dependency_edge`

## Artifact stats

| Artifact | SHA256 | Lines | Bytes | Git policy |
| --- | --- | ---: | ---: | --- |
| `data/interim/journal_v1_full_trace_cct_redesigned/cct_redesigned_graphs.jsonl` | `5f882228dc1cad39d01338f28f9ab8d2817c2e72ca6c7f50aac0a00b40648165` | 420 | 4186416 | generated locally; ignored by normal Git |
| `data/interim/journal_v1_full_trace_cct_redesigned/sample_cct_redesigned_graphs.jsonl` | `cad21797081164fbb2b2956d398b525dfd26351059a026d555c7d1d03f251a5d` | 2 | 19264 | tracked compact review sample |
| `data/interim/journal_v1_full_trace_cct_redesigned/cct_redesigned_graph_inventory.json` | `56a8811d8a94d3f653c49843bed2a118c6973291f21a6d52fd7e65d21365465a` | 2579 | 108263 | tracked compact inventory |

## Prohibitions

This manifest does not authorize scoring, ranking, gold/H6 comparison, calibration, ablation, statistical tests, or paper-ready result tables.
