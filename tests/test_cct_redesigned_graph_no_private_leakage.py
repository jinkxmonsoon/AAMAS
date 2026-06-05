import json
from pathlib import Path

import pytest

from cctdiag.cct.redesigned_builder import build_redesigned_cct_graph
from cctdiag.cct.redesigned_validation import redesigned_graph_leakage_findings

FORBIDDEN_KEYS = {
    "private_labels",
    "provenance",
    "gold_failure_step",
    "gold_failure_agent",
    "gold_irreversibility",
    "gold_propagation",
    "gold_recoverability",
    "label_rationale",
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


def test_redesigned_sample_graphs_contain_no_private_or_scoring_fields():
    graphs = [json.loads(line) for line in Path("data/interim/journal_v1_full_trace_cct_redesigned/sample_cct_redesigned_graphs.jsonl").read_text().splitlines()]
    keys = {key for graph in graphs for key in _walk(graph)}

    assert not (keys & FORBIDDEN_KEYS)
    assert redesigned_graph_leakage_findings(graphs) == []


def test_raw_record_rejected_by_redesigned_builder():
    raw_record = json.loads(Path("data/processed/journal_v1_full_trace/main_full_trace_all.jsonl").read_text().splitlines()[0])

    with pytest.raises(ValueError):
        build_redesigned_cct_graph(raw_record)


def test_redesigned_leakage_report_passes():
    text = Path("results/reports/journal_v1_full_trace_cct_redesigned/cct_redesigned_graph_leakage_audit.md").read_text(
        encoding="utf-8"
    )

    assert "Leakage status: PASS" in text
    assert "Findings: 0" in text
    assert "make_full_trace_prediction_view(record)" in text
