import json
from pathlib import Path

from cctdiag.cct.redesigned_features import FEATURE_NAMES, extract_redesigned_graph_features


def test_redesigned_feature_module_extracts_required_features_from_sample_graph():
    graph = json.loads(Path("data/interim/journal_v1_full_trace_cct_redesigned/sample_cct_redesigned_graphs.jsonl").read_text().splitlines()[0])
    row = extract_redesigned_graph_features(graph)

    assert set(FEATURE_NAMES) <= set(row)
    assert row["causal_flow_edge_count_total"] >= 4
    assert row["tool_alignment_edge_count"] == 2
    assert row["cross_agent_dependency_edge_count"] == 2
    assert "gold_failure_step" not in row


def test_redesigned_feature_reports_record_counts_and_degeneracy():
    inventory = Path("results/reports/journal_v1_full_trace_cct_redesigned/cct_redesigned_feature_inventory.md").read_text(
        encoding="utf-8"
    )
    degeneracy = Path("results/reports/journal_v1_full_trace_cct_redesigned/cct_redesigned_feature_degeneracy_report.md").read_text(
        encoding="utf-8"
    )

    assert "Total feature rows: 420" in inventory
    assert "causal_flow_edge_count_total" in inventory
    assert "Unique feature-vector count: 6" in degeneracy
    assert "Duplicate feature-vector count: 414" in degeneracy
    assert "Redesigned features reduce degeneracy relative to previous base graph signatures: yes" in degeneracy
