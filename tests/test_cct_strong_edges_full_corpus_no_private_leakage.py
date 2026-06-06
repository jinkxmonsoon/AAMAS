import json
from pathlib import Path

import pytest

from scripts import audit_cct_strong_edges_full_corpus as audit_script
from cctdiag.cct.causal_edges import extract_causal_edges_from_prediction_view

FORBIDDEN_KEYS = {
    "private_labels",
    "provenance",
    "gold_failure_step",
    "gold_failure_agent",
    "gold_irreversibility",
    "gold_propagation",
    "gold_recoverability",
    "label_rationale",
    "propagation_evidence",
    "irreversibility_evidence",
    "recovery_opportunity",
    "correctness",
    "correct",
    "incorrect",
    "score",
    "rank",
}


def _walk(value):
    if isinstance(value, dict):
        for key, nested in value.items():
            yield key
            yield from _walk(nested)
    elif isinstance(value, list):
        for item in value:
            yield from _walk(item)


def test_tracked_strong_edge_sample_contains_only_in_scope_edges_and_no_private_fields():
    payload = json.loads(Path("results/raw/journal_v1_full_trace_cct/sample_cct_strong_edges_full_corpus.json").read_text(encoding="utf-8"))
    keys = set(_walk(payload))

    assert not (keys & FORBIDDEN_KEYS)
    for trace in payload["traces"]:
        for edge in trace["edges"]:
            assert edge["edge_type"] in audit_script.STRONG_EDGE_TYPES


def test_full_corpus_strong_edge_leakage_report_passes():
    text = Path("results/reports/journal_v1_full_trace_cct/cct_strong_edges_full_corpus_leakage_audit.md").read_text(
        encoding="utf-8"
    )

    assert "Leakage status: PASS" in text
    assert "Findings: 0" in text
    assert "Scenario, perturbation, and case-variant metadata are joined only after extraction" in text


def test_raw_records_are_rejected_by_edge_extractor():
    raw_record = next(audit_script.iter_records())

    with pytest.raises(ValueError):
        extract_causal_edges_from_prediction_view(raw_record, edge_types=audit_script.STRONG_EDGE_TYPES)
