import json
from pathlib import Path

from cctdiag.io.full_trace_views import make_full_trace_prediction_view
from cctdiag.rescue.candidate_step_features import FEATURE_NAMES, extract_candidate_step_feature_rows

CORPUS = Path("data/processed/journal_v1_full_trace/main_full_trace_all.jsonl")
ARTIFACT = Path("results/raw/journal_v1_rescue/rescue_candidate_step_features.json")


def test_candidate_step_feature_rows_shape_from_prediction_view():
    record = json.loads(CORPUS.read_text().splitlines()[0])
    rows = extract_candidate_step_feature_rows(make_full_trace_prediction_view(record))
    assert len(rows) == 5
    assert {row["candidate_step_id"] for row in rows} == {"s1", "s2", "s3", "s4", "s5"}
    for row in rows:
        assert set(FEATURE_NAMES).issubset(row)
        assert row["feature_version"] == "rescue_candidate_step_features_v1"


def test_candidate_step_feature_artifact_has_expected_rows():
    rows = json.loads(ARTIFACT.read_text())
    assert len(rows) == 2100
    assert len({row["trace_id"] for row in rows}) == 420
    assert all(set(FEATURE_NAMES).issubset(row) for row in rows)
