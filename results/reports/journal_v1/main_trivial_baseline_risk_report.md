# Journal-v1 Main Trivial-Baseline Risk Report

## Scope and guardrails
- These values are corpus-risk diagnostics only, not method results.
- No evaluation metric, baseline implementation, CCT scoring, calibration, or result table is introduced by this report.

## Diagnostic shortcut estimates
| diagnostic shortcut | expected accuracy | numerator / denominator | status |
|---|---:|---:|---|
| majority_step (`s2`) | 0.2500 (25.00%) | 105/420 | below block threshold |
| majority_agent (`a8`) | 0.1786 (17.86%) | 75/420 | below block threshold |
| always_s2 | 0.2500 (25.00%) | 105/420 | below block threshold |
| first_active_agent | 0.2500 (25.00%) | 105/420 | below block threshold |
| most_common_agent (`a8`) | 0.1786 (17.86%) | 75/420 | below block threshold |

## Evaluation gate
- Evaluation blocked: no.
- No trivial-risk diagnostic exceeded its configured block threshold.
