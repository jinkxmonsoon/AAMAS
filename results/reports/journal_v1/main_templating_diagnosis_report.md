# Main Templating Diagnosis Report (Task 10B)

## Scope reviewed
- `results/reports/journal_v1/main_semantic_spotcheck_report.md`
- `results/reports/journal_v1/main_generation_risk_report.md`
- `scripts/build_main_corpus.py`
- `data/processed/journal_v1/main_all_traces.jsonl`

## Findings
- Repeated phrase patterns: `input_message`, `output_message`, `label_rationale`, `propagation_evidence`, and `irreversibility_evidence` were near-constant templates.
- Repeated structural patterns: fixed `step_catalog` length/content (`s1..s4`) and fixed single failure step (`s2`) for all traces.
- Repeated agent-role patterns: constant `agent_catalog` (`a1,a2,a3`), `agent_id` (`a2`), and `agent_role` (`reviewer`).
- Repeated tool-call patterns: fixed `tool_call=lookup_context` with homogeneous `tool_output` style.
- Repeated label-rationale patterns: same rationale sentence across all traces.
- Most affected scenario groups: all seven groups similarly affected (systemic generation issue).
- Affected trace families: both clean and perturbed traces (perturbed inherit clean templates).

## Risk assessment
- Validity risk: models may learn synthetic regularities rather than collaborative-failure semantics.
- Leakage risk: no direct lexical gold-label leakage detected in audited fields.
- Blocker status: semantic spot-check blocker from Task 10A is valid and requires generator diversification.
