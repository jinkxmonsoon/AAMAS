# Journal-v1 Full-Trace CCT Uncalibrated Variant Disagreement Report

| Pair | Agreement | Disagreement | Agreement rate | Left correct/right wrong | Right correct/left wrong |
|---|---:|---:|---:|---:|---:|
| `cct_primary_no_position__vs__cct_flow_only` | 174 | 246 | 0.414286 | 21 | 78 |
| `cct_primary_no_position__vs__cct_context_only` | 321 | 99 | 0.764286 | 36 | 0 |
| `cct_primary_no_position__vs__cct_with_position_features` | 99 | 321 | 0.235714 | 39 | 96 |
| `cct_flow_only__vs__cct_with_position_features` | 0 | 420 | 0.000000 | 105 | 105 |

Variant disagreement confirms that the primary formula often selects different steps than flow/position diagnostics; flow-only and with-position never select the same step in this fixed graph shape, yet both reach 0.250000 because each collapses to a different single-position/default prediction.
