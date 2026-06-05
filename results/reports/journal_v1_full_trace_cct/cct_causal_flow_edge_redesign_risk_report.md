# CCT Causal-Flow Edge Redesign Risk Report

## Scope

This report audits specification risks for the proposed non-position causal-flow edge redesign. It does not implement edge extraction, features, scoring, ranking, calibration, gold-label comparison, ablations, statistical tests, or result tables.

## Global risk controls

- Extraction inputs must be limited to visible trace fields: step messages, tool calls/outputs, evidence references, visible notes, and handoff context as relation context.
- Private labels, gold fields, H6 private evidence, label rationales, provenance, scenario group, perturbation type, correctness labels, ranks, and scores are forbidden extraction inputs.
- Scenario and perturbation metadata may be used only after extraction for audit distributions.
- Edge extraction must require a visible relation between two steps, a step and evidence, or a step and tool output.

## Per-edge risk summary

| Edge type | Leakage risk | Lexical shortcut risk | Template sensitivity risk | Risk mitigation | Future status |
| --- | --- | --- | --- | --- | --- |
| `constraint_shift_edge` | Medium | Medium | Medium | Audit modal/constraint terms and require source-target relation, not phrase presence alone. | Primary candidate. |
| `evidence_conflict_edge` | Medium-high | Medium-high | High | Keep contrast lexicon conservative and require visible evidence/tool-output conflict. | Primary candidate with high-risk audit. |
| `evidence_omission_edge` | Medium | Medium-high | Medium-high | Treat absence conservatively; require upstream availability plus downstream decision context. | Experimental-only. |
| `downstream_dependency_edge` | Low-medium | Medium | Medium | Require content-bearing dependency beyond handoff adjacency or step position. | Primary candidate. |
| `correction_opportunity_edge` | Medium | Medium | Medium | Avoid private recoverability labels and require visible review/check opportunity. | Diagnostic-only. |
| `correction_attempt_edge` | Medium | Medium | Medium-high | Avoid correctness language and require explicit visible repair/revision relation. | Diagnostic-only. |
| `unresolved_caveat_edge` | Medium | Medium | High | Require trace-local caveat chain and avoid terminal/gold outcome comparison. | Experimental-only. |
| `semantic_collision_edge` | Medium | Medium-high | High | Require paired alternatives/contrast plus downstream selection relation; audit scenario-word dependence. | Primary candidate with template audit. |
| `tool_alignment_edge` | Low-medium | Medium | Medium | Use relation labels that do not imply correctness and require tool-output/step-output relation. | Primary candidate. |
| `cross_agent_dependency_edge` | Low-medium | Medium | Medium | Do not use fixed agent identity as signal; require visible content carried across agent boundary. | Primary candidate. |

## Main residual risks

1. Current corpus regularities may make deterministic edges appear more valid than they are.
2. Omission and unresolved-caveat edges are absence-sensitive and may be brittle under paraphrase.
3. Conflict and semantic-collision edges may overfit to builder templates if relation rules are too lexical.
4. Correction-oriented edges may leak recoverability concepts unless private H6 evidence and correctness language are strictly excluded.
5. Cross-agent and downstream-dependency edges can collapse into position/handoff-chain shortcuts unless content relation is mandatory.

## Required audits before any scoring consideration

- Private leakage audit.
- Lexical-template audit.
- Perturbation sensitivity audit.
- Edge sparsity/density audit.
- Duplicate graph signature audit.
- Scenario and perturbation distributions as audit-only metadata.
- No gold-label, H6-label, rank, or score comparison during readiness.
