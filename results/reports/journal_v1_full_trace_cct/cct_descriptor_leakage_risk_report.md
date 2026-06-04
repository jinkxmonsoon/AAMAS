# Journal-v1 Full-Trace CCT Descriptor Leakage Risk Report

Descriptor extraction consumes `make_full_trace_prediction_view(record)` and the extractor rejects payloads containing private/gold/provenance fields.
- Forbidden output fields detected: none
- Private labels used: no.
- Gold labels used: no.
- Scenario/perturbation used as descriptor value: no; metadata is used only for sample audit summaries.
- Leakage status: PASS.
