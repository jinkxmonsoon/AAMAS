import json
from pathlib import Path

import pytest

from cctdiag.cct.descriptors import assert_prediction_view_safe, extract_descriptor_rows

ROOT = Path(__file__).resolve().parents[1]
FORBIDDEN_FIELDS = {
    "gold_failure_step",
    "gold_failure_agent",
    "private_labels",
    "label_rationale",
    "gold_irreversibility",
    "gold_propagation",
    "gold_recoverability",
    "propagation_evidence",
    "irreversibility_evidence",
    "recovery_opportunity",
    "provenance",
    "annotator_or_generator",
    "provenance_notes",
    "synthetic_control_rule",
}


def _find_forbidden(value):
    if isinstance(value, dict):
        return [key for key in value if key in FORBIDDEN_FIELDS] + [item for nested in value.values() for item in _find_forbidden(nested)]
    if isinstance(value, list):
        return [item for nested in value for item in _find_forbidden(nested)]
    return []


def test_descriptor_extractor_rejects_raw_private_record():
    raw_record = json.loads((ROOT / "data/processed/journal_v1_full_trace/main_full_trace_all.jsonl").read_text().splitlines()[0])

    with pytest.raises(ValueError, match="forbidden/private"):
        extract_descriptor_rows(raw_record)


def test_descriptor_raw_output_contains_no_private_or_gold_fields():
    rows = json.loads((ROOT / "results/raw/journal_v1_full_trace_cct/cct_descriptor_sample_prototype.json").read_text())

    assert rows
    assert not _find_forbidden(rows)


def test_prediction_view_guard_requires_view_shape():
    with pytest.raises(ValueError, match="prediction view"):
        assert_prediction_view_safe({"trace_id": "t1", "steps": []})
