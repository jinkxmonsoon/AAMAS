import pytest

from cctdiag.cct.causal_edges import (
    FORBIDDEN_OUTPUT_FIELDS,
    audit_edges_for_private_leakage,
    assert_prediction_view_safe,
)
from cctdiag.io.full_trace_views import make_full_trace_prediction_view
from scripts import prototype_cct_causal_edges_sample as prototype


def test_edge_extraction_rejects_raw_record_with_private_fields():
    raw_record = prototype.select_sample_records()[0]

    with pytest.raises(ValueError, match="not prediction-view safe"):
        assert_prediction_view_safe(raw_record)


def test_prediction_view_edges_do_not_expose_private_or_scoring_fields():
    record = prototype.select_sample_records()[0]
    payload = prototype.build_sample_payload([record])
    edges = payload["traces"][0]["edges"]

    assert audit_edges_for_private_leakage(edges) == []
    for edge in edges:
        assert not (set(edge) & FORBIDDEN_OUTPUT_FIELDS)
        assert "scenario_group" not in edge
        assert "perturbation_type" not in edge
        assert "private_labels" not in edge
        assert "provenance" not in edge
        assert "score" not in edge
        assert "rank" not in edge


def test_prediction_view_used_for_extraction_has_no_private_fields():
    record = prototype.select_sample_records()[0]
    prediction_view = make_full_trace_prediction_view(record)

    assert "private_labels" not in prediction_view
    assert "provenance" not in prediction_view
    assert "scenario_group" not in prediction_view
    assert "perturbation_type" not in prediction_view


def test_scoring_config_absence_is_not_silently_recreated():
    from pathlib import Path

    scoring_config = Path("configs/cct_scoring.yaml")
    if not scoring_config.exists():
        report = Path("results/reports/journal_v1_full_trace_cct/cct_causal_edge_provenance_check.md").read_text(encoding="utf-8")
        assert "exists: false" in report
        assert "Safe recovery path" in report
