import json
from pathlib import Path

from cctdiag.cct.descriptors import DESCRIPTOR_NAMES, extract_descriptor_rows
from cctdiag.io.full_trace_views import make_full_trace_prediction_view

ROOT = Path(__file__).resolve().parents[1]


def test_descriptor_extraction_emits_three_rows_per_visible_step():
    record = json.loads((ROOT / "data/processed/journal_v1_full_trace/main_full_trace_all.jsonl").read_text().splitlines()[0])
    view = make_full_trace_prediction_view(record)
    rows = extract_descriptor_rows(view)

    assert len(rows) == len(view["steps"]) * len(DESCRIPTOR_NAMES)
    assert {row["descriptor_name"] for row in rows} == set(DESCRIPTOR_NAMES)
    assert all(isinstance(row["descriptor_value"], bool) for row in rows)
    assert all(row["trace_id"] == view["trace_id"] for row in rows)


def test_descriptor_sample_raw_has_expected_shape_after_prototype_script():
    raw_path = ROOT / "results/raw/journal_v1_full_trace_cct/cct_descriptor_sample_prototype.json"
    rows = json.loads(raw_path.read_text())

    assert rows
    assert {"trace_id", "step_id", "descriptor_name", "descriptor_value", "visible_fields_used", "extraction_notes", "extraction_version"}.issubset(rows[0])
    assert {row["descriptor_name"] for row in rows} == set(DESCRIPTOR_NAMES)
