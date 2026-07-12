# Editorial Positioning Note v1

## Scope

This note is for cover-letter and editorial framing only. It does not authorize experiments, scoring, calibration, statistical testing, corpus/gold-label changes, scoring-config restoration, or performance tables.

## One-sentence positioning

This manuscript presents a protocol-first full-trace benchmark and diagnostic representation audit for multi-agent failure attribution, showing through governed negative evidence that naive CCT structural scoring and simple causal-flow counts are not yet sufficient for performance claims.

## Applied Intelligence positioning

Applied Intelligence remains plausible if the manuscript is framed around practical evaluation methodology for collaborative AI systems: trace completeness, leakage and shortcut governance, artifact provenance, diagnostic representation design, and reproducible negative findings. The paper should be positioned as a benchmark/protocol contribution that prevents premature performance claims, not as a new state-of-the-art attribution method.

## Cover letter emphasis

- The manuscript addresses a practical problem: how to audit collaborative multi-agent failures without leaking labels or overclaiming method readiness.
- The contribution is the full-trace protocol, prediction-view separation, artifact governance, and diagnostic evidence map.
- Negative findings are deliberately preserved because they identify representation-degeneracy and provenance risks that future methods must solve.
- The work is reproducible where manifests and scripts exist, while the Task 18 scoring run is explicitly bounded by missing frozen scoring-config provenance.

## Reviewer-risk response points

| Likely reviewer concern | Response posture |
| --- | --- |
| "Where is the performance gain?" | The paper is not framed as a performance-superiority method paper; it is a protocol and diagnostic benchmark paper. |
| "Why include negative findings?" | Negative findings are the evidence that current structural representations are insufficient and that calibration would be premature. |
| "Is CCT validated?" | No. CCT is used here as a diagnostic representation and audit scaffold, not as a validated automatic attribution method. |
| "Does causal-flow mean causal identification?" | No. The term denotes operational dependency/evidence-flow structure, not formal statistical causal identification. |
| "Can Task 18 be reproduced?" | Not from the active checkout; the missing frozen scoring config is disclosed as a reproducibility boundary. |

## Forbidden editorial framing

Do not frame the paper as showing CCT improves attribution, outperforms baselines, is robust under perturbations, is calibrated, validates H1/H2, is production-ready, or supplies paper-ready performance evidence.
