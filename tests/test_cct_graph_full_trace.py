import json
from pathlib import Path

from cctdiag.cct.graph import build_cct_graph, extract_cct_feature_rows

ROOT = Path(__file__).resolve().parents[1]
FORBIDDEN_KEYS = {"private_labels", "provenance", "gold_failure_step", "gold_failure_agent", "label_rationale"}


def _contains_forbidden(value):
    if isinstance(value, dict):
        return any(key in FORBIDDEN_KEYS or _contains_forbidden(nested) for key, nested in value.items())
    if isinstance(value, list):
        return any(_contains_forbidden(item) for item in value)
    return False


def test_full_trace_cct_graph_uses_visible_fields_only():
    record = json.loads((ROOT / "data/processed/journal_v1_full_trace/main_full_trace_all.jsonl").read_text().splitlines()[0])
    graph = build_cct_graph(record)
    rows = extract_cct_feature_rows(graph)

    assert graph["trace_id"] == record["trace_id"]
    assert len(graph["nodes"]) == len(record["steps"])
    assert len(rows) == len(record["steps"])
    assert not _contains_forbidden(graph)
    assert not _contains_forbidden(rows)


def test_tracked_samples_include_clean_and_perturbed_graphs():
    sample_path = ROOT / "data/interim/journal_v1_full_trace_cct/sample_cct_graphs.jsonl"
    graphs = [json.loads(line) for line in sample_path.read_text().splitlines() if line]
    corpus = {
        json.loads(line)["trace_id"]: json.loads(line)["case_variant"]
        for line in (ROOT / "data/processed/journal_v1_full_trace/main_full_trace_all.jsonl").read_text().splitlines()
        if line
    }
    variants = {corpus[graph["trace_id"]] for graph in graphs}
    assert "clean" in variants
    assert any(variant != "clean" for variant in variants)
