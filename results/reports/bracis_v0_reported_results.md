# BRACIS v0 Reported Results Register (Complete Numerical Extraction for Task 0.5B)

Status: **Reported numbers only**. All rows are **not yet reproduced in current repo**.

Columns: Source | Method | Condition | Metric | Value | Value type | Reproduced in current repo | Tier | Risk/limitation

## 1) Trace-bank composition

| Source | Method | Condition | Metric | Value | Value type | Reproduced in current repo | Tier | Risk/limitation |
|---|---|---|---|---:|---|---|---|---|
| BRACIS v0 narrative (dataset description) | Controlled trace-bank construction | Global | Clean cases | 50 | textual report | no | secondary | Requires manifest-level verification |
| BRACIS v0 narrative (dataset description) | Controlled trace-bank construction | Global | Perturbation-derived variants | 200 | textual report | no | secondary | Generation lineage not yet audited |
| BRACIS v0 narrative (dataset description) | Controlled trace-bank construction | Global | Total traces | 250 | textual report | no | secondary | Split integrity pending |
| BRACIS v0 narrative/figure | Scenario grouping | clean/broken handoff | n | 8 | textual report | no | secondary | Group assignment reproducibility pending |
| BRACIS v0 narrative/figure | Scenario grouping | tool evidence usage / consumed-orphaned evidence | n | 8 | textual report | no | secondary | Same as above |
| BRACIS v0 narrative/figure | Scenario grouping | same-agent continuation | n | 6 | textual report | no | secondary | Same as above |
| BRACIS v0 narrative/figure | Scenario grouping | cross-agent propagation | n | 8 | textual report | no | secondary | Same as above |
| BRACIS v0 narrative/figure | Scenario grouping | recoverable vs irreversible failure | n | 10 | textual report | no | secondary | Same as above |
| BRACIS v0 narrative/figure | Scenario grouping | semantic collision pairs | n | 10 | textual report | no | secondary | Same as above |

## 2) Calibration results

| Source | Method | Condition | Metric | Value | Value type | Reproduced in current repo | Tier | Risk/limitation |
|---|---|---|---|---:|---|---|---|---|
| BRACIS v0 calibration figure | Weighted structural score | current weights | C | 0.35 | figure-extracted approximate | no | primary | Figure read; exact table unavailable |
| BRACIS v0 calibration figure | Weighted structural score | current weights | I | 0.40 | figure-extracted approximate | no | primary | Figure read |
| BRACIS v0 calibration figure | Weighted structural score | current weights | P | 0.25 | figure-extracted approximate | no | primary | Figure read |
| BRACIS v0 calibration figure | LOSO calibration | current weights | LOSO step attribution accuracy | ~0.20 | figure-extracted approximate | no | primary | Requires exact reproduction |
| BRACIS v0 calibration figure | Weighted structural score | equal weights | C | 0.33 | figure-extracted approximate | no | primary | Rounded value |
| BRACIS v0 calibration figure | Weighted structural score | equal weights | I | 0.33 | figure-extracted approximate | no | primary | Rounded value |
| BRACIS v0 calibration figure | Weighted structural score | equal weights | P | 0.33 | figure-extracted approximate | no | primary | Rounded value |
| BRACIS v0 calibration figure | LOSO calibration | equal weights | LOSO step attribution accuracy | ~0.25 | figure-extracted approximate | no | primary | Requires exact reproduction |
| BRACIS v0 calibration figure | Weighted structural score | best grid | C | 0.40 | figure-extracted approximate | no | primary | Figure read |
| BRACIS v0 calibration figure | Weighted structural score | best grid | I | 0.00 | figure-extracted approximate | no | primary | Figure read |
| BRACIS v0 calibration figure | Weighted structural score | best grid | P | 0.60 | figure-extracted approximate | no | primary | Figure read |
| BRACIS v0 calibration figure | LOSO calibration | best grid | LOSO step attribution accuracy | ~0.54 | figure-extracted approximate | no | primary | Potential tie with regularized choice |
| BRACIS v0 calibration figure/text | Weighted structural score | selected regularized | C | 0.40 | exact table value | no | primary | Regularization rationale must be reproduced |
| BRACIS v0 calibration figure/text | Weighted structural score | selected regularized | I | 0.10 | exact table value | no | primary | Same |
| BRACIS v0 calibration figure/text | Weighted structural score | selected regularized | P | 0.50 | exact table value | no | primary | Same |
| BRACIS v0 calibration figure/text | LOSO calibration | selected regularized | LOSO step attribution accuracy | ~0.54 | figure-extracted approximate | no | primary | Same nominal accuracy as best grid |

## 3) Clean-condition variants

| Source | Method | Condition | Metric | Value | Value type | Reproduced in current repo | Tier | Risk/limitation |
|---|---|---|---|---:|---|---|---|---|
| BRACIS v0 main results table | v1 calibrated structural backbone | clean | step attribution | 0.68 | exact table value | no | primary | Not yet rerun |
| BRACIS v0 main results table | v1 calibrated structural backbone | clean | agent attribution | 0.68 | exact table value | no | primary | Not yet rerun |
| BRACIS v0 main results table | v1 calibrated structural backbone | clean | irreversibility | 0.08 | exact table value | no | primary | Low performance is major journal risk |
| BRACIS v0 main results table | v1 calibrated structural backbone | clean | propagation | 0.04 | exact table value | no | primary | Low performance is major journal risk |
| BRACIS v0 main results table | v1 calibrated structural backbone | clean | extra model calls | 0 | exact table value | no | secondary | Cost dimension only |
| BRACIS v0 main results table | V2A deterministic refinement | clean | step attribution | 0.68 | exact table value | no | primary | No gain vs v1 despite added calls |
| BRACIS v0 main results table | V2A deterministic refinement | clean | agent attribution | 0.68 | exact table value | no | primary | Same |
| BRACIS v0 main results table | V2A deterministic refinement | clean | irreversibility | 0.08 | exact table value | no | primary | Same low value |
| BRACIS v0 main results table | V2A deterministic refinement | clean | propagation | 0.04 | exact table value | no | primary | Same low value |
| BRACIS v0 main results table | V2A deterministic refinement | clean | extra model calls | 50 | exact table value | no | secondary | Higher cost, no reported gain |
| BRACIS v0 main results table | V2B deterministic refinement | clean | step attribution | 0.26 | exact table value | no | primary | Large degradation vs v1 |
| BRACIS v0 main results table | V2B deterministic refinement | clean | agent attribution | 0.36 | exact table value | no | primary | Degradation vs v1 |
| BRACIS v0 main results table | V2B deterministic refinement | clean | irreversibility | 0.08 | exact table value | no | primary | Still low |
| BRACIS v0 main results table | V2B deterministic refinement | clean | propagation | 0.04 | exact table value | no | primary | Still low |
| BRACIS v0 main results table | V2B deterministic refinement | clean | extra model calls | 50 | exact table value | no | secondary | Cost up, quality down |
| BRACIS v0 main results table | V2C deterministic refinement | clean | step attribution | 0.26 | exact table value | no | primary | Large degradation vs v1 |
| BRACIS v0 main results table | V2C deterministic refinement | clean | agent attribution | 0.36 | exact table value | no | primary | Degradation vs v1 |
| BRACIS v0 main results table | V2C deterministic refinement | clean | irreversibility | 0.08 | exact table value | no | primary | Still low |
| BRACIS v0 main results table | V2C deterministic refinement | clean | propagation | 0.04 | exact table value | no | primary | Still low |
| BRACIS v0 main results table | V2C deterministic refinement | clean | extra model calls | 50 | exact table value | no | secondary | Cost up, quality down |

## 4) Paired statistical results

| Source | Method | Condition | Metric | Value | Value type | Reproduced in current repo | Tier | Risk/limitation |
|---|---|---|---|---|---|---|---|---|
| BRACIS v0 statistical comparison | Paired bootstrap | V2C - v1 | 95% CI (step attribution delta) | [-0.58, -0.26] | textual report | no | primary | Inference pipeline not reproduced |
| BRACIS v0 statistical comparison | McNemar test | V2C vs v1 | p-value | 1.9e-5 | textual report | no | primary | Requires paired contingency reconstruction |
| BRACIS v0 statistical comparison | Interpretation | V2C - v1 | conclusion | significantly worse | textual report | no | primary | Must remain reported-only claim |

## 5) Contextual external-comparison table

| Source | Method | Condition | Metric | Value | Value type | Reproduced in current repo | Tier | Risk/limitation |
|---|---|---|---|---|---|---|---|---|
| BRACIS v0 contextual table | Spectrum-inspired baseline (adapted) | external-comparison context | agent attribution (%) | 20.0 | exact table value | no | contextual | Adapted setting; not directly comparable |
| BRACIS v0 contextual table | Spectrum-inspired baseline (adapted) | external-comparison context | step/action attribution (%) | 4.0 | exact table value | no | contextual | Not directly comparable |
| BRACIS v0 contextual table | Who&When best method (original) | external-comparison context | agent attribution (%) | 53.5 | textual report | no | contextual | Original external-paper number; not directly comparable |
| BRACIS v0 contextual table | Who&When best method (original) | external-comparison context | step/action attribution (%) | 14.2 | textual report | no | contextual | Original external-paper number; not directly comparable |
| BRACIS v0 contextual table | Who&When-style baseline (adapted) | external-comparison context | agent attribution (%) | 24.0 | exact table value | no | contextual | Adapted; not directly comparable |
| BRACIS v0 contextual table | Who&When-style baseline (adapted) | external-comparison context | step/action attribution (%) | 24.0 | exact table value | no | contextual | Adapted; not directly comparable |
| BRACIS v0 contextual table | Famas (original) | external-comparison context | agent attribution (%) | 57.61 | textual report | no | contextual | Original external-paper number; not directly comparable |
| BRACIS v0 contextual table | Famas (original) | external-comparison context | step/action attribution (%) | 29.35 | textual report | no | contextual | Original external-paper number; not directly comparable |
| BRACIS v0 contextual table | AgentRx (original tau-bench) | external-comparison context | agent attribution (%) | NA | textual report | no | contextual | Different benchmark/reporting protocol |
| BRACIS v0 contextual table | AgentRx (original tau-bench) | external-comparison context | step/action attribution (%) | 48.3 | textual report | no | contextual | Different benchmark/reporting protocol |
| BRACIS v0 contextual table | Ours calibrated structural backbone | external-comparison context | agent attribution (%) | 68.0 | exact table value | no | primary | In-context comparison still needs fair protocol audit |
| BRACIS v0 contextual table | Ours calibrated structural backbone | external-comparison context | step/action attribution (%) | 68.0 | exact table value | no | primary | Same |

## 6) Robustness table (as reported)

| Source | Method | Condition | Metric | Value | Value type | Reproduced in current repo | Tier | Risk/limitation |
|---|---|---|---|---:|---|---|---|---|
| BRACIS v0 robustness table | v1 | Clean | step attribution | 0.68 | exact table value | no | primary | Pending rerun |
| BRACIS v0 robustness table | v1 | Clean | agent attribution | 0.68 | exact table value | no | primary | Pending rerun |
| BRACIS v0 robustness table | v1 | Clean | irreversibility | 0.08 | exact table value | no | primary | Major journal risk: low value |
| BRACIS v0 robustness table | v1 | Clean | propagation | 0.04 | exact table value | no | primary | Major journal risk: low value |
| BRACIS v0 robustness table | v1 | Clean | extra model calls | 0 | exact table value | no | secondary | Cost only |
| BRACIS v0 robustness table | V2C | Clean | step attribution | 0.26 | exact table value | no | primary | Worse than v1 |
| BRACIS v0 robustness table | V2C | Clean | agent attribution | 0.36 | exact table value | no | primary | Worse than v1 |
| BRACIS v0 robustness table | V2C | Clean | irreversibility | 0.08 | exact table value | no | primary | Low |
| BRACIS v0 robustness table | V2C | Clean | propagation | 0.04 | exact table value | no | primary | Low |
| BRACIS v0 robustness table | V2C | Clean | extra model calls | 50 | exact table value | no | secondary | High extra cost |
| BRACIS v0 robustness table | v1 | Paraphrase | step attribution | 0.68 | exact table value | no | primary | Reported stable; not reproduced |
| BRACIS v0 robustness table | v1 | Paraphrase | agent attribution | 0.68 | exact table value | no | primary | Same |
| BRACIS v0 robustness table | v1 | Paraphrase | irreversibility | 0.08 | exact table value | no | primary | Low |
| BRACIS v0 robustness table | v1 | Paraphrase | propagation | 0.04 | exact table value | no | primary | Low |
| BRACIS v0 robustness table | v1 | Paraphrase | extra model calls | 0 | exact table value | no | secondary | Cost only |
| BRACIS v0 robustness table | V2C | Paraphrase | step attribution | 0.26 | exact table value | no | primary | Worse than v1 |
| BRACIS v0 robustness table | V2C | Paraphrase | agent attribution | 0.36 | exact table value | no | primary | Worse than v1 |
| BRACIS v0 robustness table | V2C | Paraphrase | irreversibility | 0.08 | exact table value | no | primary | Low |
| BRACIS v0 robustness table | V2C | Paraphrase | propagation | 0.04 | exact table value | no | primary | Low |
| BRACIS v0 robustness table | V2C | Paraphrase | extra model calls | 50 | exact table value | no | secondary | High cost |
| BRACIS v0 robustness table | v1 | Tool-output truncation | step attribution | 0.68 | exact table value | no | primary | Reported stable |
| BRACIS v0 robustness table | v1 | Tool-output truncation | agent attribution | 0.68 | exact table value | no | primary | Reported stable |
| BRACIS v0 robustness table | v1 | Tool-output truncation | irreversibility | 0.08 | exact table value | no | primary | Low |
| BRACIS v0 robustness table | v1 | Tool-output truncation | propagation | 0.04 | exact table value | no | primary | Low |
| BRACIS v0 robustness table | v1 | Tool-output truncation | extra model calls | 0 | exact table value | no | secondary | Cost only |
| BRACIS v0 robustness table | V2C | Tool-output truncation | step attribution | 0.26 | exact table value | no | primary | Worse than v1 |
| BRACIS v0 robustness table | V2C | Tool-output truncation | agent attribution | 0.36 | exact table value | no | primary | Worse than v1 |
| BRACIS v0 robustness table | V2C | Tool-output truncation | irreversibility | 0.08 | exact table value | no | primary | Low |
| BRACIS v0 robustness table | V2C | Tool-output truncation | propagation | 0.04 | exact table value | no | primary | Low |
| BRACIS v0 robustness table | V2C | Tool-output truncation | extra model calls | 50 | exact table value | no | secondary | High cost |
| BRACIS v0 robustness table | v1 | Partial observability | step attribution | 0.68 | exact table value | no | primary | Reported stable |
| BRACIS v0 robustness table | v1 | Partial observability | agent attribution | 0.68 | exact table value | no | primary | Reported stable |
| BRACIS v0 robustness table | v1 | Partial observability | irreversibility | 0.08 | exact table value | no | primary | Low |
| BRACIS v0 robustness table | v1 | Partial observability | propagation | 0.04 | exact table value | no | primary | Low |
| BRACIS v0 robustness table | v1 | Partial observability | extra model calls | 0 | exact table value | no | secondary | Cost only |
| BRACIS v0 robustness table | V2C | Partial observability | step attribution | 0.26 | exact table value | no | primary | Worse than v1 |
| BRACIS v0 robustness table | V2C | Partial observability | agent attribution | 0.36 | exact table value | no | primary | Worse than v1 |
| BRACIS v0 robustness table | V2C | Partial observability | irreversibility | 0.08 | exact table value | no | primary | Low |
| BRACIS v0 robustness table | V2C | Partial observability | propagation | 0.04 | exact table value | no | primary | Low |
| BRACIS v0 robustness table | V2C | Partial observability | extra model calls | 50 | exact table value | no | secondary | High cost |
| BRACIS v0 robustness table | v1 | Textual distraction | step attribution | 0.68 | exact table value | no | primary | Reported stable |
| BRACIS v0 robustness table | v1 | Textual distraction | agent attribution | 0.68 | exact table value | no | primary | Reported stable |
| BRACIS v0 robustness table | v1 | Textual distraction | irreversibility | 0.08 | exact table value | no | primary | Low |
| BRACIS v0 robustness table | v1 | Textual distraction | propagation | 0.04 | exact table value | no | primary | Low |
| BRACIS v0 robustness table | v1 | Textual distraction | extra model calls | 0 | exact table value | no | secondary | Cost only |
| BRACIS v0 robustness table | V2C | Textual distraction | step attribution | 0.26 | exact table value | no | primary | Worse than v1 |
| BRACIS v0 robustness table | V2C | Textual distraction | agent attribution | 0.36 | exact table value | no | primary | Worse than v1 |
| BRACIS v0 robustness table | V2C | Textual distraction | irreversibility | 0.08 | exact table value | no | primary | Low |
| BRACIS v0 robustness table | V2C | Textual distraction | propagation | 0.04 | exact table value | no | primary | Low |
| BRACIS v0 robustness table | V2C | Textual distraction | extra model calls | 50 | exact table value | no | secondary | High cost |
| BRACIS v0 robustness note | v1 | perturbation stability | step stability | 1.00 | textual report | no | secondary | Needs exact perturbation audit reproduction |
| BRACIS v0 robustness note | v1 | perturbation stability | tuple stability | 1.00 | textual report | no | secondary | Same |

## 7) Scenario-level step attribution

| Source | Method | Condition | Metric | Value | Value type | Reproduced in current repo | Tier | Risk/limitation |
|---|---|---|---|---|---|---|---|---|
| BRACIS v0 scenario plot | v1 vs V2C | clean/broken handoff (n=8) | v1 step attribution | 1.000 | figure-extracted approximate | no | primary | Plot-read value |
| BRACIS v0 scenario plot | v1 vs V2C | clean/broken handoff (n=8) | V2C step attribution | 0.375 | figure-extracted approximate | no | primary | Plot-read value |
| BRACIS v0 scenario plot | v1 vs V2C | clean/broken handoff (n=8) | delta (V2C - v1) | -0.625 | figure-extracted approximate | no | primary | Plot-read value |
| BRACIS v0 scenario plot | v1 vs V2C | cross-agent propagation (n=8) | v1 step attribution | 0.000 | figure-extracted approximate | no | primary | Plot-read value |
| BRACIS v0 scenario plot | v1 vs V2C | cross-agent propagation (n=8) | V2C step attribution | 0.000 | figure-extracted approximate | no | primary | Plot-read value |
| BRACIS v0 scenario plot | v1 vs V2C | cross-agent propagation (n=8) | delta (V2C - v1) | 0.000 | figure-extracted approximate | no | primary | Plot-read value |
| BRACIS v0 scenario plot | v1 vs V2C | recoverable vs irreversible failure (n=10) | v1 step attribution | 1.000 | figure-extracted approximate | no | primary | Plot-read value |
| BRACIS v0 scenario plot | v1 vs V2C | recoverable vs irreversible failure (n=10) | V2C step attribution | 0.300 | figure-extracted approximate | no | primary | Plot-read value |
| BRACIS v0 scenario plot | v1 vs V2C | recoverable vs irreversible failure (n=10) | delta (V2C - v1) | -0.700 | figure-extracted approximate | no | primary | Plot-read value |
| BRACIS v0 scenario plot | v1 vs V2C | same-agent continuation (n=6) | v1 step attribution | 0.333 | figure-extracted approximate | no | primary | Plot-read value |
| BRACIS v0 scenario plot | v1 vs V2C | same-agent continuation (n=6) | V2C step attribution | 0.333 | figure-extracted approximate | no | primary | Plot-read value |
| BRACIS v0 scenario plot | v1 vs V2C | same-agent continuation (n=6) | delta (V2C - v1) | 0.000 | figure-extracted approximate | no | primary | Plot-read value |
| BRACIS v0 scenario plot | v1 vs V2C | semantic collision pairs (n=10) | v1 step attribution | 1.000 | figure-extracted approximate | no | primary | Plot-read value |
| BRACIS v0 scenario plot | v1 vs V2C | semantic collision pairs (n=10) | V2C step attribution | 0.400 | figure-extracted approximate | no | primary | Plot-read value |
| BRACIS v0 scenario plot | v1 vs V2C | semantic collision pairs (n=10) | delta (V2C - v1) | -0.600 | figure-extracted approximate | no | primary | Plot-read value |
| BRACIS v0 scenario plot | v1 vs V2C | tool consumed/orphaned evidence (n=8) | v1 step attribution | 0.500 | figure-extracted approximate | no | primary | Plot-read value |
| BRACIS v0 scenario plot | v1 vs V2C | tool consumed/orphaned evidence (n=8) | V2C step attribution | 0.125 | figure-extracted approximate | no | primary | Plot-read value |
| BRACIS v0 scenario plot | v1 vs V2C | tool consumed/orphaned evidence (n=8) | delta (V2C - v1) | -0.375 | figure-extracted approximate | no | primary | Plot-read value |

## 8) Fixed / worsened / unchanged audit

| Source | Method | Condition | Metric | Value | Value type | Reproduced in current repo | Tier | Risk/limitation |
|---|---|---|---|---:|---|---|---|---|
| BRACIS v0 refinement audit | V2C vs v1 case-level comparison | clean set | fixed by refinement | 2 | textual report | no | secondary | Decision rule reproduction pending |
| BRACIS v0 refinement audit | V2C vs v1 case-level comparison | clean set | worsened by refinement | 23 | textual report | no | primary | Strong negative signal; must verify carefully |
| BRACIS v0 refinement audit | V2C vs v1 case-level comparison | clean set | unchanged | 25 | textual report | no | secondary | Pending reproduction |

## Summary status
- Total rows registered in this file: comprehensive for all numbers provided in BRACIS v0 brief/PDF-facing task requirements.
- Reproduced rows: 0.
- All figures read from plots are explicitly marked `figure-extracted approximate`.
- External original-paper numbers are explicitly contextual and not directly comparable.
