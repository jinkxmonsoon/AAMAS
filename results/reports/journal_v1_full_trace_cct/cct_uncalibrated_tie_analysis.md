# Journal-v1 Full-Trace CCT Uncalibrated Tie Analysis

| Variant | Tied top traces | Tied top percent | Avg tied candidates | Tie-break can affect predicted step | Tie-break missed tied gold | Accuracy tied | Accuracy non-tied | Wrong score separation traces |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `cct_primary_no_position` | 120 | 0.285714 | 2.200000 | 120 | 12 | 0.200000 | 0.080000 | 276 |
| `cct_flow_only` | 420 | 1.000000 | 3.000000 | 420 | 210 | 0.250000 | n/a | 0 |
| `cct_context_only` | 108 | 0.257143 | 2.194444 | 108 | 0 | 0.000000 | 0.038462 | 300 |
| `cct_with_position_features` | 0 | 0.000000 | 1.000000 | 0 | 0 | n/a | 0.250000 | 315 |

Primary underperformance is not mainly a tie artifact because most primary errors are non-tied wrong score separations.
