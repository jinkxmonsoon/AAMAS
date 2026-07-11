# Journal-v1 Limitations and Threats to Validity

## Scope

This document enumerates limitations for the Path B article frame. It does not authorize new experiments, scoring, calibration, statistical testing, corpus/gold-label edits, or performance tables.

## Core limitations

1. **Controlled/synthetic trace-bank limitation.** The Journal-v1 trace bank is controlled and protocol-constructed; external ecological validity remains untested.

2. **No demonstrated performance gain.** H1/H2 remain unsupported, and the paper must not claim improved automatic attribution or baseline outperformance.

3. **H1/H2 unsupported.** Current evidence supports a diagnostic/protocol contribution, not validation of structural failure attribution or performance superiority.

4. **H3/H4 blocked.** Calibration and broader method claims remain premature because representation validity is insufficient.

5. **H6 open but unsupported.** Propagation, irreversibility, and recoverability may require richer causal-flow representation, but current scoring evidence does not support H6 claims.

6. **Scoring config provenance blocker.** The frozen `configs/cct_scoring.yaml` used by Task 18 is absent from the current checkout, and PR #22 candidates did not match the expected frozen hash. Task 18 is diagnostic evidence but not reproducible from the active checkout.

7. **High feature degeneracy.** Task 24A redesigned features produced only 6 unique feature vectors across 420 rows, with 414 duplicate vectors and multiple constant features.

8. **Template sensitivity risk.** Causal-flow edge extraction remains vulnerable to repeated phrases and lexical templates, especially for deferred edge types and simple count features.

9. **No external validation yet.** The artifact has not been tested across independent corpora, production traces, or external annotation protocols.

10. **No production readiness.** The repository is a scientific protocol artifact, not an operational diagnostic system.

11. **No formal causal identification.** The term "causal" is used for operational dependency/evidence-flow representation, not formal statistical causal identification.

12. **Artifact governance dependency.** Large generated artifacts are reproducible by scripts and represented by compact samples/manifests; reviewers must follow manifest commands rather than expect every full JSON artifact in Git.

## Threats by validity category

- **Construct validity:** Structural edge and feature counts may not capture the semantic failure mechanisms needed for attribution.
- **Internal validity:** Leakage controls reduce known risks, but template and proxy shortcuts remain possible.
- **External validity:** Controlled scenario groups may not reflect open-ended real-world multi-agent failures.
- **Conclusion validity:** No statistical tests or performance tables are produced; claims must remain diagnostic and protocol-oriented.
- **Reproducibility validity:** Most generated artifacts are reproducible by scripts, but Task 18 scoring is bounded by missing frozen-config provenance.
