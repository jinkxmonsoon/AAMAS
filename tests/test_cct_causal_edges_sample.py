import json
from collections import Counter
from pathlib import Path

from scripts import prototype_cct_causal_edges_sample as prototype


def test_sample_selection_is_deterministic_limited_and_balanced_by_available_scenarios():
    records = prototype.select_sample_records()

    assert len(records) == 14
    assert len(records) <= prototype.MAX_SAMPLE_TRACES
    assert {record["case_variant"] for record in records} == {"clean", "perturbed"}
    assert len({record["scenario_group"] for record in records if record["case_variant"] == "clean"}) == 7
    assert len({record["scenario_group"] for record in records if record["case_variant"] == "perturbed"}) == 7


def test_sample_payload_contains_only_sample_scope_and_required_edge_types():
    records = prototype.select_sample_records()
    payload = prototype.build_sample_payload(records)
    counts = Counter(edge["edge_type"] for trace in payload["traces"] for edge in trace["edges"])

    assert payload["extraction_scope"] == "sample_only_not_full_corpus"
    assert payload["sample_trace_count"] == 14
    assert payload["sample_trace_count"] < 420
    assert counts["constraint_shift_edge"] > 0
    assert counts["downstream_dependency_edge"] > 0
    assert counts["tool_alignment_edge"] > 0
    assert counts["cross_agent_dependency_edge"] > 0
    assert set(counts).issubset(set(payload["implemented_edge_types"]))


def test_tracked_sample_prototype_artifact_is_compact_and_reviewable():
    path = Path("results/raw/journal_v1_full_trace_cct/cct_causal_edge_sample_prototype.json")
    payload = json.loads(path.read_text(encoding="utf-8"))

    assert payload["sample_trace_count"] == 14
    assert payload["sample_trace_count"] < 420
    assert payload["total_edge_count"] == sum(trace["edge_count"] for trace in payload["traces"])
