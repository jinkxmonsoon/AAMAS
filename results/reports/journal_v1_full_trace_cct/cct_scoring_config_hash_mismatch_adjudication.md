# CCT Scoring Config Hash Mismatch Adjudication

## Scope

Task 20F is provenance adjudication only. It does not restore a non-matching scoring config as authoritative, modify the expected frozen hash, run scoring, rank candidate steps, compare to gold/H6 labels, calibrate, grid search, run LOSO, refine scoring, ablate, perform statistical tests, modify corpus/gold labels, or produce paper-ready result tables.

## Current repository state

- Branch inspected: `work`
- HEAD inspected before Task 20F changes: `76de0a20afe8b99d27007d184fc7fc292bc163e0`
- `configs/` entries observed: `ablations.yaml`, `baselines.yaml`, `corpus_plan.yaml`, `label_rubric.yaml`, `metrics.yaml`, `protocol.yaml`, `robustness.yaml`, `seeds.yaml`
- `configs/cct_scoring.yaml` exists in working tree: no
- Recovery action taken in this task: no file restored

## Expected frozen hash

- Expected Task 17/18 frozen SHA256: `053f19066923d8d22d27b22727e75876f939f2a60480484c4028eabd07ad0855`

## Candidate sources checked

| Candidate source | Status | Observed SHA256 | Adjudication |
| --- | --- | --- | --- |
| GitHub PR #22 raw head-branch candidate (`codex/make-cct-graph-pr-reviewable-pdxvwm/configs/cct_scoring.yaml`) | Available content recorded during Task 20E | `435c4703a90171c8bf246a4fa9e188e70800c66c5e9446d19f74de94b32bb` | Non-matching candidate; not restored |
| GitHub PR #22 visible 140-line file form | Available content recorded during Task 20E | `1fe4362714cf79a69bd81d0ffe8b82403cc2c2e99abc9f6c7579ed0253278a4a` | Non-matching candidate; not restored |
| Current local checkout | `configs/cct_scoring.yaml` absent | not applicable | No local file to verify |
| Current local Git history and known Task 17/18 commit-path checks from Task 20C | No authoritative file found | not applicable | No local authoritative source |
| External PR/remote fetches from Task 20D | Shell network fetch blocked with HTTP CONNECT 403 | not applicable | No directly fetched authoritative byte stream in this environment |

## Normalization checks

The available PR #22 candidates were not accepted as authoritative because neither the raw candidate nor the PR-visible candidate matched the expected frozen SHA256. Task 20E also checked byte-representation variants to rule out common transport-format causes before rejecting the candidates.

| Normalization or representation tested | Observed SHA256 | Matches expected frozen hash? |
| --- | --- | --- |
| Raw PR head-branch candidate as observed | `435c4703a90171c8bf246a4fa9e188e70800c66c5e9446d19f74de94b32bb` | no |
| PR-visible 140-line LF form | `1fe4362714cf79a69bd81d0ffe8b82403cc2c2e99abc9f6c7579ed0253278a4a` | no |
| PR-visible form with final newline removed | `28147cce23df815e127ab2a1b3bf6b53991060a3eed1085a137a20c5bb5d1a00` | no |
| PR-visible form normalized to CRLF with final newline | `4d7641ed36402438505a43b2d88e7e4e7b6744d93029443aa82ea756671483b1` | no |
| PR-visible form normalized to CRLF with final newline removed | `a2d3e180f5f5ec91f3a39bffbf29984144841b30ac238c3a33026eeba695b34f` | no |
| PR-visible form with UTF-8 BOM added/removed check | `7f8d4991e0d0fd6afb04f4c373959dc4edaa8b363361222c96a1de3178a46e16` | no |
| JSON/YAML canonical minified representation check from the observed candidate content | `aa0e2ecfe20e160dd506ac4a9a89cf8b35c61fe98b464ce6bcbff99f25f6a40d` | no |
| JSON/YAML pretty two-space canonical representation check from the observed candidate content | `5618a8fdb8ee461b1d4901eceffb4b01292620f2858af01ade057957671bc2d2` | no |

## Adjudication decision

- Any candidate matched the expected frozen hash: no
- PR #22 can be considered the exact Task 18 frozen config: no
- PR #22 candidate classification: `NON_MATCHING_CANDIDATE_CONFIG`
- `configs/cct_scoring.yaml` restoration status: not restored
- Expected hash status: unchanged and still authoritative for Task 17/18 provenance checks

## Required external action

To resume scoring-related reproducibility work, the user must provide an exact raw file, archive, patch, bundle, or signed protocol artifact whose byte content hashes to `053f19066923d8d22d27b22727e75876f939f2a60480484c4028eabd07ad0855`.

Alternatively, the user may explicitly authorize reclassifying the PR #22 candidate as a new scoring-protocol artifact. That would be a new protocol-freeze task and would not retroactively reproduce Task 18 diagnostics.
