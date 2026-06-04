# Main Full-Trace Shortcut Baseline Report

## Scope
- Diagnostic main-corpus baselines only; not CCT evaluation and not paper evidence.
- Baselines operate only on sanitized full-trace prediction views.
- Thresholds are diagnostic and do not constitute paper results.

## Thresholds
- review if step/agent accuracy > 70%.
- block if step/agent accuracy > 85%.

## Baseline results
| baseline | step accuracy | agent accuracy | tuple accuracy | macro scenario | macro perturbation |
|---|---:|---:|---:|---:|---:|
| majority_step | 25.00% | NA | NA | 25.00% | 25.00% |
| majority_agent | NA | 25.00% | NA | NA | NA |
| always_s2 | 25.00% | NA | NA | 25.00% | 25.00% |
| first_step | 0.00% | NA | NA | 0.00% | 0.00% |
| last_step | 25.00% | NA | NA | 25.00% | 25.00% |
| first_agent | NA | 0.00% | NA | NA | NA |
| last_agent | NA | 25.00% | NA | NA | NA |
| tool_presence_step | 0.00% | NA | NA | 0.00% | 0.00% |
| most_detailed_step | 3.57% | NA | NA | 3.57% | 3.57% |
| keyword_degradation_step | 0.00% | NA | NA | 0.00% | 0.00% |
| simple_spectrum_visible_step | 0.00% | NA | NA | 0.00% | 0.00% |
| simple_spectrum_visible_agent | NA | 0.00% | NA | NA | NA |

## Interpretation
- status: PASSED
- blockers: none.
- review flags: none.
