import json
from pathlib import Path

REPORT_DIR = Path("results/reports/journal_v1_full_trace_cct")
SAMPLE_PATH = Path("results/raw/journal_v1_full_trace_cct/sample_cct_strong_edges_full_corpus.json")
MANIFEST_PATH = Path("docs/artifact_manifests/cct_strong_edges_full_corpus_manifest.md")


def test_full_corpus_strong_edge_reports_record_expected_scope_and_counts():
    inventory = (REPORT_DIR / "cct_strong_edges_full_corpus_inventory.md").read_text(encoding="utf-8")
    distribution = (REPORT_DIR / "cct_strong_edges_full_corpus_distribution_report.md").read_text(encoding="utf-8")
    readiness = (REPORT_DIR / "cct_strong_edges_full_corpus_readiness_gate.md").read_text(encoding="utf-8")

    assert "Total traces processed: 420" in inventory
    assert "Total edges generated: 2385" in inventory
    assert "cross_agent_dependency_edge: 840" in inventory
    assert "downstream_dependency_edge: 705" in inventory
    assert "tool_alignment_edge: 840" in inventory
    assert "Adjacent edge count: 525" in distribution
    assert "Non-adjacent edge count: 1860" in distribution
    assert "STRONG_CAUSAL_FLOW_EDGES_FULL_CORPUS_AUDIT_READY = yes" in readiness
    assert "CCT_CAUSAL_FLOW_EDGES_READY_FOR_SCORING = no" in readiness


def test_full_corpus_strong_edge_sample_and_manifest_are_reviewable_policy_artifacts():
    payload = json.loads(SAMPLE_PATH.read_text(encoding="utf-8"))
    manifest = MANIFEST_PATH.read_text(encoding="utf-8")

    assert payload["artifact_type"] == "sample_cct_strong_edges_full_corpus_audit"
    assert payload["sample_trace_count"] == 2
    assert set(payload["edge_types_in_scope"]) == {
        "downstream_dependency_edge",
        "tool_alignment_edge",
        "cross_agent_dependency_edge",
    }
    assert "generated locally; ignored by normal Git" in manifest
    assert "tracked compact review sample" in manifest


def test_full_corpus_strong_edge_template_report_records_relation_checks():
    text = (REPORT_DIR / "cct_strong_edges_full_corpus_template_sensitivity_report.md").read_text(encoding="utf-8")

    assert "Repeated relation-note pattern count: 74" in text
    assert "Repeated source-target pattern count: 3" in text
    assert "tool_alignment_edge` uses visible `tool_call`, `tool_output`, and `output_message`" in text
    assert "downstream_dependency_edge` includes non-adjacent edges" in text
    assert "cross_agent_dependency_edge` includes non-adjacent edges" in text
