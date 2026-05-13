# BRACIS v0 Formal Artifact Recovery Attempt

Date: 2026-05-13 (UTC)
Status: **Completed recovery attempt; Path A unavailable; reproduction remains BLOCKED**.

## Search scope (accessible TL locations only)
- `/workspace/AAMAS` repository tree
- `/workspace` workspace tree (maxdepth 7)
- filename/pattern probes: `*bracis*`, `*trace*`, `*label*`, `*scenario*`, `*perturb*`, `*calib*`, `*robust*`, `*mcnemar*`, `*bootstrap*`, `*.csv`, `*.json`, `*.jsonl`, `*.ipynb`, `*.xlsx`, `*.parquet`

## Required bundle checklist and recovery status

| Artifact category | Expected filename/pattern (if known) | Expected source location | Searched location(s) | Found | Imported | SHA256 if imported | Blocking status |
|---|---|---|---|---|---|---|---|
| Raw traces | `*trace*`, `*.jsonl`, `*.json`, `*.csv` | Prior BRACIS run storage | `/workspace/AAMAS`, `/workspace` | no | no | n/a | BLOCKING |
| Gold labels | `*label*`, `gold*`, `*.csv`, `*.json` | Prior BRACIS label package | `/workspace/AAMAS`, `/workspace` | no | no | n/a | BLOCKING |
| Scenario metadata | `*scenario*`, `metadata*` | Prior BRACIS metadata files | `/workspace/AAMAS`, `/workspace` | no | no | n/a | BLOCKING |
| Perturbation definitions/files | `*perturb*` | Prior BRACIS perturbation bundle | `/workspace/AAMAS`, `/workspace` | no | no | n/a | BLOCKING |
| Calibration outputs | `*calib*`, calibration tables/JSON | Prior BRACIS output folder | `/workspace/AAMAS`, `/workspace` | no | no | n/a | BLOCKING |
| Clean-condition result outputs | result tables/csv/json | Prior BRACIS output folder | `/workspace/AAMAS`, `/workspace` | no | no | n/a | BLOCKING |
| Robustness outputs | `*robust*` outputs (not configs) | Prior BRACIS output folder | `/workspace/AAMAS`, `/workspace` | no | no | n/a | BLOCKING |
| Scenario-level breakdown outputs | scenario breakdown tables | Prior BRACIS analysis folder | `/workspace/AAMAS`, `/workspace` | no | no | n/a | BLOCKING |
| Statistical test outputs | `*mcnemar*`, `*bootstrap*`, stats exports | Prior BRACIS analysis folder | `/workspace/AAMAS`, `/workspace` | no | no | n/a | BLOCKING |
| Scripts/notebooks used for v0 | `*.ipynb`, run scripts | Prior BRACIS code bundle | `/workspace/AAMAS`, `/workspace` | no | no | n/a | BLOCKING |
| Generated tables/figures | `tables/*`, `figures/*`, exported artifacts | Prior BRACIS artifact package | `/workspace/AAMAS`, `/workspace` | no | no | n/a | BLOCKING |

## Recovery outcome
- No real BRACIS v0 experimental artifacts were found in accessible locations.
- Only scaffold/metadata files exist in current import directories.
- Path A (recover BRACIS v0) remains unavailable until the original bundle is provided by source owners.
