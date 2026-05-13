# BRACIS v0 Reported Results Register (Reported vs Reproduced)

## Evidence status key
- Reproducibility from current repo:
  - **No** = not yet reproduced in this repository
- Result tier:
  - **Primary** = central performance/diagnostic claims
  - **Secondary** = supportive/ablation findings
  - **Contextual** = external paradigm context comparisons

## Extracted numerical items currently available from submission narrative

> Note: The desk-rejected paper full text/tables are not stored in this repository yet. This register captures numbers explicitly available in the project brief and flags all others for mandatory extraction once the manuscript artifact is imported.

| Source (section/table/figure) | Method | Condition | Metric | Value | Reproducible from current repo? | Tier | Risk / limitation |
|---|---|---|---|---:|---|---|---|
| Manuscript narrative (artifact summary) | Controlled trace bank construction | Clean diagnostic set | Case count | 50 | No | Secondary | Dataset manifest and generation lineage not yet audited in repo |
| Manuscript narrative (artifact summary) | Controlled trace bank construction | Perturbation-derived set | Variant count | 200 | No | Secondary | Perturbation protocol and uniqueness checks not yet reproduced |
| Manuscript narrative (calibration statement) | LOSO structural calibration | Selected weights | C weight | 0.40 | No | Primary | Search space, fold details, and stability not yet reproduced |
| Manuscript narrative (calibration statement) | LOSO structural calibration | Selected weights | I weight | 0.10 | No | Primary | Same as above |
| Manuscript narrative (calibration statement) | LOSO structural calibration | Selected weights | P weight | 0.50 | No | Primary | Same as above |

## Required extraction groups not yet numerically available in repo

The following groups are required for journal audit completion but their full numeric rows cannot be completed until the submitted manuscript tables/figures are imported as source artifacts.

### 1) Structural weight calibration
- Missing required fields: per-fold outcomes, objective metric, variance/CI, candidate grid, tie-breaking.

### 2) Clean-condition comparison across variants
- Missing required fields: variant-by-variant metrics for v1, V2A, V2B, V2C and baselines.

### 3) External-paradigm comparison
- Missing required fields: comparator methods, matching protocol constraints, outcome metrics, uncertainty.

### 4) Robustness table
- Missing required fields: condition-wise outcomes for paraphrase, tool-output truncation, partial observability, textual distraction.

### 5) Scenario-level results
- Missing required fields: per-scenario performance or attribution quality statistics.

### 6) Fixed / worsened / unchanged audit
- Missing required fields: counts/percentages and decision rule definitions.

### 7) Statistical tests and confidence intervals
- Missing required fields: test names, assumptions, p-values/effect sizes, CI levels and construction method.

## Reproduction status summary
- Numerical items listed: 5
- Reproduced items: 0
- Not yet reproduced items: 5
- Missing-from-repo extraction groups: 7 major groups

## Mandatory next action for this register
Import the exact BRACIS v0 manuscript artifact (PDF + supplementary tables if available) into a tracked reference location, then complete row-level extraction for every reported number with table/figure coordinates.
