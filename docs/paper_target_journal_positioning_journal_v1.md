# Journal-v1 Target Journal Positioning

## Scope

This document supports editorial positioning for the Path B pivot. It does not authorize experiments, scoring, calibration, statistical tests, corpus changes, or paper-ready performance tables.

## Recommended article framing

Frame the manuscript as a **protocol-first benchmark and diagnostic-representation paper** for multi-agent failure attribution. The central contribution is the governed benchmark and evidence map showing why naive structural CCT scoring and simple causal-flow feature counts are insufficient under the current representation.

## Applied Intelligence fit

Applied Intelligence may remain a possible target if the manuscript emphasizes:

- practical challenges of collaborative AI failure diagnosis;
- reproducible benchmark/protocol construction;
- leakage, shortcut, provenance, and artifact-governance methodology;
- diagnostic representation analysis as a prerequisite for future automated methods;
- transparent negative findings that prevent premature method claims.

Risk: Applied Intelligence reviewers may expect empirical performance gains. The cover letter and abstract should explicitly state that this is a benchmark/protocol and diagnostic-representation contribution, not a performance-superiority method paper.

## Alternative target profiles

If the article becomes too benchmark/protocol-oriented for Applied Intelligence, consider venues or tracks receptive to:

- AI evaluation methodology;
- multi-agent system benchmarks;
- reproducibility and artifact governance;
- responsible evaluation / audit methodology;
- negative results and diagnostic benchmark papers.

Potential target categories include benchmark/data-resource tracks, reproducibility tracks, responsible AI evaluation venues, and multi-agent systems methodology workshops or special issues.

## Reviewer risks and mitigation

| Reviewer risk | Mitigation |
| --- | --- |
| "Where is the performance improvement?" | State upfront that the paper is not a performance-superiority paper; its contribution is protocol governance and representation diagnostics. |
| "Negative results are not enough." | Frame negative findings as evidence identifying leakage, shortcut, provenance, and degeneracy failure modes future methods must address. |
| "Task 18 is not reproducible." | Disclose the scoring-config provenance blocker and avoid using Task 18 as paper-ready performance evidence. |
| "Causal-flow edges sound like causal claims." | Use "causal-flow" as operational dependency/evidence-flow terminology and deny formal causal identification. |
| "Feature degeneracy weakens the method." | Treat degeneracy as the central diagnostic finding motivating the protocol-first pivot. |

## Cover letter positioning notes

- Emphasize transparent protocoling, controlled attribution, and reproducibility.
- State that the paper contributes a governed full-trace benchmark and diagnostic representation audit.
- Note that negative findings are deliberately preserved to prevent overclaiming.
- Avoid language about outperforming baselines, robustness, calibrated scoring, or validated hypothesis support.

## One-sentence positioning statement

This manuscript presents a protocol-first full-trace benchmark and diagnostic representation audit for multi-agent failure attribution, showing through governed negative evidence that naive CCT structural scoring and simple causal-flow counts are not yet sufficient for performance claims.
