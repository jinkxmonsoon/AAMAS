# Journal-v1 Full-Trace CCT Uncalibrated Feature Dominance Report

## Primary feature contribution summary

| Feature | Mean contribution | Variance | Min | Max |
|---|---:|---:|---:|---:|
| `evidence_used_count` | 0.200000 | 0.000000 | 0.200000 | 0.200000 |
| `evidence_item_count` | 0.200000 | 0.000000 | 0.200000 | 0.200000 |
| `has_tool_call` | 0.100000 | 0.000000 | 0.100000 | 0.100000 |
| `tool_output_token_count` | 2.403143 | 0.015912 | 1.950000 | 2.850000 |
| `output_token_count` | 1.723000 | 0.270971 | 1.100000 | 4.400000 |
| `has_handoff_from` | 0.080000 | 0.001600 | 0.000000 | 0.100000 |
| `has_handoff_to` | 0.080000 | 0.001600 | 0.000000 | 0.100000 |
| `in_degree` | 0.080000 | 0.001600 | 0.000000 | 0.100000 |
| `out_degree` | 0.080000 | 0.001600 | 0.000000 | 0.100000 |
| `input_token_count` | 0.862857 | 0.025763 | 0.550000 | 1.400000 |

- Dominant average feature: `tool_output_token_count`.
- Top contributing feature per trace counts: `{'output_token_count': 24, 'tool_output_token_count': 396}`.
- Mean rank1-rank2 margin: 0.296786.
- Median rank1-rank2 margin: 0.150000.
- Mean gold-minus-top margin: -0.843929.
- Median gold-minus-top margin: -0.600000.
- Mean within-trace score range: 1.141429.
- Median within-trace score range: 0.900000.
- Near-constant score traces (range <= 0.05): 0.
- Interpretation: scores are usually separated, but the largest average contributions come from broad context/tool-output fields that do not identify the gold step reliably.
