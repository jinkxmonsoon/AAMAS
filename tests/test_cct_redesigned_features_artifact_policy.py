import json
from pathlib import Path


def test_redesigned_feature_artifact_is_reviewable_and_complete():
    path = Path("results/raw/journal_v1_full_trace_cct_redesigned/cct_redesigned_features.json")
    payload = json.loads(path.read_text())

    assert path.stat().st_size < 500_000
    assert payload["artifact_type"] == "cct_redesigned_features_representation_only"
    assert payload["total_feature_rows"] == 420
    assert len(payload["feature_names"]) == 13


def test_redesigned_feature_readiness_remains_no_for_scoring_and_protocol_review():
    text = Path("results/reports/journal_v1_full_trace_cct_redesigned/cct_redesigned_feature_readiness_gate.md").read_text(
        encoding="utf-8"
    )

    assert "CCT_REDESIGNED_FEATURES_READY_FOR_PROTOCOL_REVIEW = no" in text
    assert "CCT_REDESIGNED_FEATURES_READY_FOR_SCORING = no" in text
    assert "constant features" in text
