# CCT Failure Diagnosis (Protocol-First Repository)

This repository initializes a **journal-grade, protocol-first** research workspace for studying whether **Collaboration Causal Traces (CCT)** help diagnose collaborative failure in LLM-based multi-agent systems.

## Project orientation
- Target publication standards: close to *Autonomous Agents and Multi-Agent Systems*.
- Initial submission venue trajectory: *Applied Intelligence*.
- Current stage: **infrastructure and protocol lock only** (no new experiments).

## Reproducibility philosophy
1. **Protocol before performance**: protocol artifacts are versioned and locked before empirical work.
2. **Traceability over convenience**: all meaningful research changes must be logged.
3. **No silent drift**: metrics, seeds, datasets, labels, and output formats are protected.
4. **Claim discipline**: no performance/generalization claims without supporting results.

## Scope of this initialization task
- Create required folders and placeholder files.
- Add governance documents for protocol and claims.
- Add validation script to check repository integrity.

## Minimal validation command
```bash
python scripts/validate_repo.py
```

A passing run confirms required files/directories exist.

## What is intentionally not implemented
- No experiment execution pipelines.
- No baseline implementations.
- No datasets or synthetic statistics.
- No result tables or empirical claims.
