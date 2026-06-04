# Full-Trace Pilot Shortcut Baseline Report

## Scope
- Diagnostic pilot baselines only; not CCT evaluation and not paper evidence.
- Baselines operate only on sanitized full-trace prediction views.
- Pilot thresholds are diagnostic and interpreted cautiously for n=14.

## Thresholds
- review if step/agent accuracy > 70%.
- block if step/agent accuracy > 85%.

## Baseline results
| baseline | step accuracy | agent accuracy | tuple accuracy | macro scenario | macro perturbation |
|---|---:|---:|---:|---:|---:|
| majority_step | 28.57% | NA | NA | 28.57% | 25.71% |
| majority_agent | NA | 28.57% | NA | NA | NA |
| always_s2 | 28.57% | NA | NA | 28.57% | 25.71% |
| first_step | 0.00% | NA | NA | 0.00% | 0.00% |
| last_step | 14.29% | NA | NA | 14.29% | 22.86% |
| first_agent | NA | 0.00% | NA | NA | NA |
| last_agent | NA | 14.29% | NA | NA | NA |
| tool_presence_step | 0.00% | NA | NA | 0.00% | 0.00% |
| most_detailed_step | 50.00% | NA | NA | 50.00% | 51.43% |
| keyword_degradation_step | 14.29% | NA | NA | 14.29% | 12.86% |
| simple_spectrum_visible_step | 0.00% | NA | NA | 0.00% | 0.00% |
| simple_spectrum_visible_agent | NA | 0.00% | NA | NA | NA |

## Interpretation
- status: PASSED
- blockers: none.
- review flags: none.
