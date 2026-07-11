# Final Rescue Error Analysis

- Best evaluated CCT variant: `cct_candidate_step_structural_sum`
- Most common predicted step: s1 (420 traces)
- Prediction collapse to one position: yes
- Behaves like first/last/majority baseline: yes

## Best scenario groups
- tool_evidence_usage: 0.00%
- semantic_collision: 0.00%
- same_agent_continuation: 0.00%

## Worst scenario groups
- clean_broken_handoff: 0.00%
- complex_collaboration: 0.00%
- cross_agent_propagation: 0.00%

## Perturbation accuracy
- non_causal_textual_distraction: 0.00%
- none: 0.00%
- paraphrase: 0.00%
- partial_observability: 0.00%
- tool_output_truncation: 0.00%

## Example failure modes
- trace `JV1FTMAIN_CLEBRO_C01_clean`: predicted s1 but gold step was s2 (reported after prediction freeze).
- trace `JV1FTMAIN_CLEBRO_C02_clean`: predicted s1 but gold step was s3 (reported after prediction freeze).
- trace `JV1FTMAIN_CLEBRO_C03_clean`: predicted s1 but gold step was s4 (reported after prediction freeze).
- trace `JV1FTMAIN_CLEBRO_C04_clean`: predicted s1 but gold step was s5 (reported after prediction freeze).
- trace `JV1FTMAIN_CLEBRO_C05_clean`: predicted s1 but gold step was s2 (reported after prediction freeze).
