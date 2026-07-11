import json
from pathlib import Path


def test_redesigned_graph_artifact_policy_tracks_sample_and_manifest():
    manifest = Path("docs/artifact_manifests/cct_redesigned_graphs_manifest.md").read_text(encoding="utf-8")
    sample_path = Path("data/interim/journal_v1_full_trace_cct_redesigned/sample_cct_redesigned_graphs.jsonl")
    inventory_path = Path("data/interim/journal_v1_full_trace_cct_redesigned/cct_redesigned_graph_inventory.json")

    assert "generated locally; ignored by normal Git" in manifest
    assert "tracked compact review sample" in manifest
    assert sample_path.exists()
    assert inventory_path.exists()
    assert len(sample_path.read_text(encoding="utf-8").splitlines()) == 2


def test_redesigned_graph_inventory_and_readiness_are_representation_only():
    inventory = json.loads(Path("data/interim/journal_v1_full_trace_cct_redesigned/cct_redesigned_graph_inventory.json").read_text())
    readiness = Path("results/reports/journal_v1_full_trace_cct_redesigned/cct_redesigned_readiness_gate.md").read_text(
        encoding="utf-8"
    )

    assert inventory["summary"]["total_redesigned_graphs"] == 420
    assert inventory["summary"]["redesigned_graph_signature_unique_count"] == 6
    assert "CCT_REDESIGNED_GRAPHS_READY_FOR_FEATURE_AUDIT = yes" in readiness
    assert "CCT_REDESIGNED_GRAPHS_READY_FOR_SCORING = no" in readiness
