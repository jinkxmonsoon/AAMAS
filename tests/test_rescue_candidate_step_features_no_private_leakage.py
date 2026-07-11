import json
from pathlib import Path

import pytest

from cctdiag.io.full_trace_views import make_full_trace_prediction_view
from cctdiag.rescue.candidate_step_features import (
    FORBIDDEN_FEATURE_FIELDS,
    audit_candidate_step_rows_for_private_leakage,
    extract_candidate_step_feature_rows,
)

CORPUS = Path("data/processed/journal_v1_full_trace/main_full_trace_all.jsonl")
ARTIFACT = Path("results/raw/journal_v1_rescue/rescue_candidate_step_features.json")


def test_raw_record_rejected_by_candidate_step_feature_extractor():
    record = json.loads(CORPUS.read_text().splitlines()[0])
    with pytest.raises(ValueError, match="prediction-view safe"):
        extract_candidate_step_feature_rows(record)


def test_prediction_view_rows_have_no_forbidden_fields():
    record = json.loads(CORPUS.read_text().splitlines()[0])
    rows = extract_candidate_step_feature_rows(make_full_trace_prediction_view(record))
    assert audit_candidate_step_rows_for_private_leakage(rows) == []


def test_artifact_has_no_private_gold_provenance_or_scoring_fields():
    rows = json.loads(ARTIFACT.read_text())
    for row in rows:
        assert not (set(row) & FORBIDDEN_FEATURE_FIELDS)
