# CCT Causal Edge Sample Leakage Audit

- Leakage status: PASS
- Extraction input: `make_full_trace_prediction_view(record)` only.
- Raw private/provenance fields are not passed to edge extraction.
- Scenario and perturbation metadata are used only for sample-selection/audit composition, not as extraction inputs.
- Findings: 0
