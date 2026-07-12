# CCT Scoring Config Provenance Recovery Report

## Scope

Task 20C/20D is protocol-recovery and provenance work only. It does not run scoring, ranking, full-corpus edge extraction, gold/H6 comparison, calibration, grid search, LOSO, refinement, ablation, statistical tests, corpus edits, gold-label edits, or paper-ready result tables.

## Repository-state evidence

- Branch inspected: `work`
- HEAD inspected before Task 20D changes: `59f324aaa3bc923fd86e6933422b621eb18c1fb4`
- `configs/` entries observed: `ablations.yaml`, `baselines.yaml`, `corpus_plan.yaml`, `label_rubric.yaml`, `metrics.yaml`, `protocol.yaml`, `robustness.yaml`, `seeds.yaml`
- `configs/cct_scoring.yaml` exists in working tree: no
- `configs/cct_scoring.yaml` tracked by `git ls-files configs`: no
- `configs/cct_scoring.yaml` ignored by current Git ignore rules: no evidence of ignore rule
- `git log --all -- configs/cct_scoring.yaml`: no local history in the current checkout
- `git log --all --name-status -- configs/cct_scoring.yaml`: no local history in the current checkout
- Available local branches from `git branch -a`: `work` only

## Local search evidence

- `find` for `*cct_scoring.yaml`, `*cct_scoring*.yml`, and `*cct_scoring*.yaml`: no authoritative matching config found.
- Search for `cct_primary_no_position`: no local match found.
- Search for expected SHA256 `053f19066923d8d22d27b22727e75876f939f2a60480484c4028eabd07ad0855`: no local authoritative config source found.
- Search for `evidence_used_count` under `configs`, `docs`, `results`, `scripts`, `src`, and `tests`: no authoritative scoring-config source found.
- Search for local `*.bundle`, `*.patch`, `*.diff`, and `*cct_scoring*` artifacts under `/workspace`: no archived patch, saved repo bundle, or exported scoring-config artifact found.

## Known Task 17/18 commit checks

The following locally available commit/path lookups were attempted and did not contain `configs/cct_scoring.yaml`:

- `269a865f574c36b2ab8ba408db444e918928090b:configs/cct_scoring.yaml`
- `2695aa3e8c06936270b40a1b6d93eee41f55f87b:configs/cct_scoring.yaml`
- `6186a4d20787563904905f71010acfa9b325af46:configs/cct_scoring.yaml`
- `8aa8bcb81d056be759aaab17c4329c9cc2f6e3b6:configs/cct_scoring.yaml`

## External authoritative-source attempts for Task 20D

Source-priority checks:

1. GitHub PR #22 patch/diff/artifacts: attempted to fetch `pull/22/head` from the repository URL recorded in `.git/FETCH_HEAD` (`https://github.com/jinkxmonsoon/AAMAS`); fetch failed with `CONNECT tunnel failed, response 403`. A web attempt to access the PR patch also did not yield a safe accessible patch in this environment.
2. Remote branch or commit associated with Task 17: attempted to fetch all remote heads from `https://github.com/jinkxmonsoon/AAMAS`; fetch failed with `CONNECT tunnel failed, response 403`.
3. Archived patch or saved repo bundle: local filesystem search found no bundle/patch/diff containing the config.
4. Signed protocol record or exported artifact: local search found no signed protocol record or exported artifact containing the expected config/hash.

## Recovery decision

- Authoritative frozen file found locally or externally from this environment: no
- File restored in Task 20D: no
- SHA256 after recovery: not applicable because no authoritative source was accessible
- Expected frozen SHA256: `053f19066923d8d22d27b22727e75876f939f2a60480484c4028eabd07ad0855`
- Verification status: `PERMANENT_RECOVERY_BLOCKED_IN_CURRENT_ENVIRONMENT`

## Consequence for Task 18 evidence

Until an authoritative external source is provided, Task 18 frozen-config diagnostics must be treated as **not reproducible from the current repository checkout**. The diagnostic evidence may remain historically described, but the repository cannot independently verify or rerun the frozen scoring protocol from local files.

## Required external action

Do not recreate `configs/cct_scoring.yaml` from memory or infer it from reports. A separate explicitly authorized protocol-recovery task must obtain the authoritative frozen file from an accessible external source such as PR #22, an archived patch, a previous branch, a saved artifact, or another signed protocol record. After recovery, the file must be restored exactly and verified against SHA256 `053f19066923d8d22d27b22727e75876f939f2a60480484c4028eabd07ad0855`.
