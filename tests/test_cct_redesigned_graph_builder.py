import json
from pathlib import Path

from cctdiag.cct.redesigned_builder import STRONG_CAUSAL_EDGE_TYPES, build_redesigned_cct_graph
from cctdiag.io.full_trace_views import make_full_trace_prediction_view


def test_redesigned_graph_builder_includes_only_authorized_causal_edges():
    record = json.loads(Path("data/processed/journal_v1_full_trace/main_full_trace_all.jsonl").read_text().splitlines()[0])
    graph = build_redesigned_cct_graph(make_full_trace_prediction_view(record))
    edge_types = {edge["edge_type"] for edge in graph["edges"]}

    assert STRONG_CAUSAL_EDGE_TYPES <= edge_types
    assert "sequence_edge" in edge_types
    assert "visible_handoff_edge" in edge_types
    assert "constraint_shift_edge" not in edge_types
    assert "semantic_collision_edge" not in edge_types
    assert graph["construction_scope"] == "representation_only_no_scoring_no_gold_comparison"


def test_redesigned_graph_reports_expected_full_corpus_degeneracy():
    text = Path("results/reports/journal_v1_full_trace_cct_redesigned/cct_redesigned_graph_degeneracy_report.md").read_text(
        encoding="utf-8"
    )

    assert "Graph signature uniqueness before causal-flow edges: 1" in text
    assert "Graph signature uniqueness after causal-flow edges: 6" in text
    assert "Duplicate graph signature count before causal-flow edges: 419" in text
    assert "Duplicate graph signature count after causal-flow edges: 414" in text
    assert "Strong edges reduce graph degeneracy: yes" in text
