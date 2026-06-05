# Journal-v1 Paper Outline After Path B Pivot

## Scope and framing lock

This document is a writing backbone only. It does not authorize new experiments, scoring, ranking, calibration, grid search, LOSO, ablation, statistical tests, corpus changes, gold-label changes, or paper-ready performance tables.

Selected frame: **protocol-first benchmark and diagnostic-representation paper**. The paper should argue that full-trace failure attribution requires explicit protocol governance, leakage controls, shortcut audits, provenance tracking, and representation-degeneracy diagnostics before any performance claim is scientifically safe.

## Tentative title options

1. **Protocol-First Failure Attribution for Multi-Agent Collaboration: Full-Trace Representation, Leakage Governance, and Negative CCT Diagnostics**
2. **Auditing Multi-Agent Failure Attribution: A Full-Trace Benchmark Protocol and Diagnostic CCT Representation Study**
3. **Why Naive Structural Scoring Fails for Collaborative Failure Attribution: A Protocol-First CCT Benchmark Audit**
4. **From Failure-Centered Labels to Full-Trace Diagnostics: A Governed Benchmark for Multi-Agent Attribution Research**
5. **Causal-Flow Representation Diagnostics for Multi-Agent Failure Attribution: Protocol, Artifacts, and Negative Findings**

## Abstract skeleton

- **Problem:** Multi-agent collaboration failures are difficult to attribute because failure-centered schemas, shortcut baselines, partial trace views, and provenance gaps can leak answers or exaggerate method readiness.
- **Approach:** We introduce a protocol-first Journal-v1 full-trace benchmark structure and audit pipeline for CCT-style collaborative failure diagnosis.
- **Governance contribution:** The protocol separates prediction-view-safe fields from private labels/provenance, records artifact manifests, and applies leakage, shortcut, and representation-degeneracy gates before scoring.
- **Diagnostic findings:** Frozen uncalibrated CCT scoring did not support H1/H2 and is not reproducible from the active checkout due to missing frozen scoring-config provenance. Descriptor augmentation and causal-flow edge redesign were leakage-safe but remained highly degenerate.
- **Implication:** The benchmark exposes why naive structural scoring and simple causal-flow feature counts are insufficient under the current representation.
- **Claim boundary:** The paper contributes a reproducible protocol and diagnostic representation audit, not evidence that CCT improves automatic attribution or outperforms baselines.

## Section-by-section structure

### 1. Introduction

- **Main argument:** Multi-agent failure attribution needs full-trace, protocol-governed benchmarks before performance claims.
- **Supporting artifacts/results:** Journal-v1 reconstruction protocol, corpus plan, schema migration plan, Task 25 backbone synthesis.
- **Allowed claims:** The work motivates full-trace representation, leakage/shortcut governance, and benchmark construction.
- **Forbidden claims:** Do not claim CCT improves attribution, outperforms baselines, or is robust.

### 2. Problem Setting and Claim Boundary

- **Main argument:** The paper studies operational failure attribution, not formal causal identification or validated performance superiority.
- **Supporting artifacts/results:** Claim reframing report, protocol lock, journal positioning update.
- **Allowed claims:** H1/H2 are unsupported, H3/H4 blocked, H6 open but unsupported; current evidence is diagnostic.
- **Forbidden claims:** Do not present hypotheses as validated or current scoring as paper-ready empirical evidence.

### 3. Benchmark and Full-Trace Schema Protocol

- **Main argument:** A failure-centered schema is unsafe for prediction unless private labels and provenance are separated from visible trace fields.
- **Supporting artifacts/results:** Reconstruction protocol, corpus plan/rubric, full-trace schema migration plan, leakage audit reports.
- **Allowed claims:** Full-trace views and prediction-view hygiene reduce leakage risk and make attribution auditing fairer.
- **Forbidden claims:** Do not claim the corpus is externally validated or production-ready.

### 4. Governance: Leakage, Shortcut, Provenance, and Artifact Reviewability

- **Main argument:** Scientific benchmark claims require explicit controls for leakage, shortcut baselines, frozen artifacts, and generated-file reviewability.
- **Supporting artifacts/results:** Leakage audits, shortcut baseline sanity findings, descriptor artifact manifests, scoring-config provenance reports, generated-artifact policies.
- **Allowed claims:** The repository identifies and controls known governance risks; full generated artifacts are reproducible but kept reviewable through samples/manifests.
- **Forbidden claims:** Do not treat blocked scoring-config provenance as resolved.

### 5. Diagnostic CCT Scoring Outcome and Negative Evidence

- **Main argument:** The negative Task 18/18A diagnostics show that naive/frozen uncalibrated structural scoring was not sufficient, and failure was not merely tie-related.
- **Supporting artifacts/results:** Task 18 reports, error analysis, feature dominance, reproducibility boundary.
- **Allowed claims:** H1/H2 remain unsupported under the current evidence; the result motivates representation diagnostics.
- **Forbidden claims:** Do not report Task 18 as reproduced from the active checkout or as performance evidence.

### 6. Descriptor and Causal-Flow Representation Diagnostics

- **Main argument:** Descriptor augmentation and causal-flow edge prototypes can be extracted under prediction-view-safe constraints, but simple structural counts still do not provide enough diversity.
- **Supporting artifacts/results:** Descriptor audits Tasks 18B–18F; causal-flow edge spec/audits Tasks 20–23; redesigned graph reports Task 24; redesigned feature audit Task 24A.
- **Allowed claims:** These audits expose representation degeneracy and template/shortcut risks.
- **Forbidden claims:** Do not claim descriptor features or causal-flow edges are ready for scoring.

### 7. Results Organization: What the Paper Reports

- **Main argument:** Results should be presented as audit outcomes and diagnostic evidence, not performance tables.
- **Supporting artifacts/results:** Feature degeneracy reports, leakage PASS reports, readiness gates, claim-boundary reports.
- **Allowed claims:** Report compact counts such as leakage status, unique feature-vector counts, duplicate counts, artifact readiness decisions, and blocked-scoring status.
- **Forbidden claims:** Do not present rankings, calibrated scores, statistical significance, or superiority tables.

### 8. Discussion

- **Main argument:** Negative findings are a contribution because they identify why proxy-heavy or count-based CCT representations are insufficient.
- **Supporting artifacts/results:** Task 25 decision synthesis, journal viability assessment, next pivot plan.
- **Allowed claims:** The work provides a reproducible foundation for future failure-attribution research and a set of failure modes future methods must overcome.
- **Forbidden claims:** Do not imply current CCT representations solve H1/H2/H6.

### 9. Limitations and Threats to Validity

- **Main argument:** The paper must foreground limits around controlled/synthetic traces, missing scoring provenance, no demonstrated performance gain, high degeneracy, template sensitivity, no external validation, and no formal causal identification.
- **Supporting artifacts/results:** Limitations document, scoring-config adjudication, redesigned feature degeneracy report.
- **Allowed claims:** Limitations are central to the protocol-first contribution.
- **Forbidden claims:** Do not minimize blocked reproducibility or feature degeneracy.

### 10. Reproducibility and Artifact Appendix

- **Main argument:** The repository supports review through compact tracked samples, manifests, validation scripts, and clear generated-artifact policies.
- **Supporting artifacts/results:** Artifact manifests, validation commands, generated sample paths, readiness gates.
- **Allowed claims:** Artifacts are governed and reproducible where scripts and manifests exist.
- **Forbidden claims:** Do not claim unavailable frozen scoring config can reproduce Task 18.

### 11. Conclusion

- **Main argument:** The paper provides a governed benchmark and diagnostic representation audit showing that naive structural scoring and simple causal-flow counts are insufficient, thereby defining safer requirements for future attribution methods.
- **Allowed claims:** Protocol-first benchmark foundation and negative diagnostic evidence.
- **Forbidden claims:** No performance superiority, robustness, calibration readiness, or hypothesis validation.
