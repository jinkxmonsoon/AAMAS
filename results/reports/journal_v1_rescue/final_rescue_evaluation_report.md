# Final Rescue Evaluation Report

## Scope
- Final minimal deterministic rescue evaluation under `configs/rescue_experiment_v1.yaml`.
- No tuning, calibration, grid search, LOSO, ablation, corpus/gold-label change, or paper-ready performance claim is performed.
- `flat_log_text_similarity_baseline` is omitted because the prediction view does not expose terminal outcome text; adding it would require a new input contract.

## Method accuracy summary
| method | family | step accuracy | macro scenario accuracy | macro perturbation accuracy | top-2 containment |
|---|---|---:|---:|---:|---:|
| majority_step | baseline | 25.00% | 25.00% | 25.00% | 25.00% |
| always_s2 | baseline | 25.00% | 25.00% | 25.00% | 25.00% |
| random_step_seeded | baseline | 17.14% | 17.14% | 17.14% | 17.14% |
| first_step | baseline | 0.00% | 0.00% | 0.00% | 0.00% |
| last_step | baseline | 25.00% | 25.00% | 25.00% | 25.00% |
| flat_log_lexical_baseline | baseline | 0.00% | 0.00% | 0.00% | 0.00% |
| non_cct_visible_heuristic_baseline | baseline | 0.00% | 0.00% | 0.00% | 0.00% |
| cct_candidate_step_structural_sum | CCT | 0.00% | 0.00% | 0.00% | 25.00% |
| cct_candidate_step_flow_only | CCT | 0.00% | 0.00% | 0.00% | 25.00% |
| cct_candidate_step_tool_alignment_only | CCT | 0.00% | 0.00% | 0.00% | 25.00% |
| cct_candidate_step_cross_agent_only | CCT | 0.00% | 0.00% | 0.00% | 25.00% |
| cct_candidate_step_visible_relation_overlap | CCT | 0.00% | 0.00% | 0.00% | 25.00% |

## Strongest references
- Best CCT variant: `cct_candidate_step_structural_sum` with step accuracy 0.00%.
- Strongest trivial baseline: `majority_step` with step accuracy 25.00%.
- Strongest non-CCT baseline overall: `majority_step` with step accuracy 25.00%.
- H2 flat/non-CCT reference: `flat_log_lexical_baseline` with step accuracy 0.00%.

## Clean vs perturbed accuracy
- majority_step: clean=25.00%; perturbed=25.00%
- always_s2: clean=25.00%; perturbed=25.00%
- random_step_seeded: clean=19.05%; perturbed=16.67%
- first_step: clean=0.00%; perturbed=0.00%
- last_step: clean=25.00%; perturbed=25.00%
- flat_log_lexical_baseline: clean=0.00%; perturbed=0.00%
- non_cct_visible_heuristic_baseline: clean=0.00%; perturbed=0.00%
- cct_candidate_step_structural_sum: clean=0.00%; perturbed=0.00%
- cct_candidate_step_flow_only: clean=0.00%; perturbed=0.00%
- cct_candidate_step_tool_alignment_only: clean=0.00%; perturbed=0.00%
- cct_candidate_step_cross_agent_only: clean=0.00%; perturbed=0.00%
- cct_candidate_step_visible_relation_overlap: clean=0.00%; perturbed=0.00%

## Confusion matrices over s1-s5
### majority_step
- gold s1: s1:0, s2:0, s3:0, s4:0, s5:0
- gold s2: s1:0, s2:105, s3:0, s4:0, s5:0
- gold s3: s1:0, s2:105, s3:0, s4:0, s5:0
- gold s4: s1:0, s2:105, s3:0, s4:0, s5:0
- gold s5: s1:0, s2:105, s3:0, s4:0, s5:0
### always_s2
- gold s1: s1:0, s2:0, s3:0, s4:0, s5:0
- gold s2: s1:0, s2:105, s3:0, s4:0, s5:0
- gold s3: s1:0, s2:105, s3:0, s4:0, s5:0
- gold s4: s1:0, s2:105, s3:0, s4:0, s5:0
- gold s5: s1:0, s2:105, s3:0, s4:0, s5:0
### random_step_seeded
- gold s1: s1:0, s2:0, s3:0, s4:0, s5:0
- gold s2: s1:21, s2:19, s3:23, s4:20, s5:22
- gold s3: s1:22, s2:22, s3:20, s4:23, s5:18
- gold s4: s1:18, s2:27, s3:21, s4:17, s5:22
- gold s5: s1:23, s2:18, s3:20, s4:28, s5:16
### first_step
- gold s1: s1:0, s2:0, s3:0, s4:0, s5:0
- gold s2: s1:105, s2:0, s3:0, s4:0, s5:0
- gold s3: s1:105, s2:0, s3:0, s4:0, s5:0
- gold s4: s1:105, s2:0, s3:0, s4:0, s5:0
- gold s5: s1:105, s2:0, s3:0, s4:0, s5:0
### last_step
- gold s1: s1:0, s2:0, s3:0, s4:0, s5:0
- gold s2: s1:0, s2:0, s3:0, s4:0, s5:105
- gold s3: s1:0, s2:0, s3:0, s4:0, s5:105
- gold s4: s1:0, s2:0, s3:0, s4:0, s5:105
- gold s5: s1:0, s2:0, s3:0, s4:0, s5:105
### flat_log_lexical_baseline
- gold s1: s1:0, s2:0, s3:0, s4:0, s5:0
- gold s2: s1:15, s2:0, s3:90, s4:0, s5:0
- gold s3: s1:105, s2:0, s3:0, s4:0, s5:0
- gold s4: s1:15, s2:0, s3:90, s4:0, s5:0
- gold s5: s1:15, s2:0, s3:90, s4:0, s5:0
### non_cct_visible_heuristic_baseline
- gold s1: s1:0, s2:0, s3:0, s4:0, s5:0
- gold s2: s1:0, s2:0, s3:105, s4:0, s5:0
- gold s3: s1:0, s2:105, s3:0, s4:0, s5:0
- gold s4: s1:0, s2:105, s3:0, s4:0, s5:0
- gold s5: s1:0, s2:105, s3:0, s4:0, s5:0
### cct_candidate_step_structural_sum
- gold s1: s1:0, s2:0, s3:0, s4:0, s5:0
- gold s2: s1:105, s2:0, s3:0, s4:0, s5:0
- gold s3: s1:105, s2:0, s3:0, s4:0, s5:0
- gold s4: s1:105, s2:0, s3:0, s4:0, s5:0
- gold s5: s1:105, s2:0, s3:0, s4:0, s5:0
### cct_candidate_step_flow_only
- gold s1: s1:0, s2:0, s3:0, s4:0, s5:0
- gold s2: s1:105, s2:0, s3:0, s4:0, s5:0
- gold s3: s1:105, s2:0, s3:0, s4:0, s5:0
- gold s4: s1:105, s2:0, s3:0, s4:0, s5:0
- gold s5: s1:105, s2:0, s3:0, s4:0, s5:0
### cct_candidate_step_tool_alignment_only
- gold s1: s1:0, s2:0, s3:0, s4:0, s5:0
- gold s2: s1:105, s2:0, s3:0, s4:0, s5:0
- gold s3: s1:105, s2:0, s3:0, s4:0, s5:0
- gold s4: s1:105, s2:0, s3:0, s4:0, s5:0
- gold s5: s1:105, s2:0, s3:0, s4:0, s5:0
### cct_candidate_step_cross_agent_only
- gold s1: s1:0, s2:0, s3:0, s4:0, s5:0
- gold s2: s1:105, s2:0, s3:0, s4:0, s5:0
- gold s3: s1:105, s2:0, s3:0, s4:0, s5:0
- gold s4: s1:105, s2:0, s3:0, s4:0, s5:0
- gold s5: s1:105, s2:0, s3:0, s4:0, s5:0
### cct_candidate_step_visible_relation_overlap
- gold s1: s1:0, s2:0, s3:0, s4:0, s5:0
- gold s2: s1:105, s2:0, s3:0, s4:0, s5:0
- gold s3: s1:105, s2:0, s3:0, s4:0, s5:0
- gold s4: s1:105, s2:0, s3:0, s4:0, s5:0
- gold s5: s1:105, s2:0, s3:0, s4:0, s5:0
