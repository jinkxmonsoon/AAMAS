# Journal-v1 Full-Trace CCT Feature Inventory

Feature rows are structural, model-visible descriptors extracted from graph nodes. They are not predictions or scores.

- Feature schema rows generated locally: 2100
- One feature row is emitted per trace step.
- Private labels and provenance are not feature inputs.
- Feature payload fields: `feature_schema_version`, `trace_id`, `step_id`, `agent_id`, `agent_role`, `order_index`, `in_degree`, `out_degree`, `input_token_count`, `output_token_count`, `tool_output_token_count`, `evidence_item_count`, `evidence_used_count`, `has_tool_call`, `has_handoff_from`, `has_handoff_to`.
- `scenario_group` and `perturbation_type` are not included in feature payloads; the variance audit joins them from public corpus metadata only for descriptive audit stratification.
