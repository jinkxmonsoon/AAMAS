# AGENTS Instructions (Strict)

These instructions apply to the entire repository unless superseded by a deeper scoped AGENTS.md.

## Mission
Maintain this repository as a protocol-first scientific codebase for CCT failure diagnosis.

## Absolute prohibitions (without explicit authorization)
Do **not** silently modify any of the following:
- Experimental protocol
- Gold labels
- Existing results
- Evaluation metrics
- Baseline definitions
- Random seeds
- Dataset composition
- Claims about performance or generalization
- Output formats used for evaluation or reporting

## Required behavior for Codex/TL
1. Log protocol-impacting changes in `EXPERIMENT_CHANGELOG.md`.
2. Log reasoning decisions and caveats in `RESEARCH_LOG.md`.
3. Keep `PROTOCOL_LOCK.md` current and explicit.
4. If a requested change affects protected items, stop and request explicit authorization in writing.
5. Do not fabricate results, data statistics, or claims.

## Repository phase constraint
This repository is in initialization mode. Prefer placeholders and structure over implementation.
