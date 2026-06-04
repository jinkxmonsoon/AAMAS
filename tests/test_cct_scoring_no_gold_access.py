import pytest

from cctdiag.diagnosis.cct_scoring import score_feature_row, score_variant_rows


def test_score_feature_row_rejects_private_or_gold_fields():
    row = {
        "trace_id": "t1",
        "step_id": "s2",
        "agent_id": "a2",
        "output_token_count": 12,
        "gold_failure_step": "s2",
    }

    with pytest.raises(ValueError, match="forbidden fields"):
        score_feature_row(row, {"output_token_count": 0.1})


def test_score_variant_rows_does_not_require_private_labels():
    rows = [{"trace_id": "t1", "step_id": "s2", "agent_id": "a2", "output_token_count": 12}]
    variant = {"features": {"output_token_count": 0.1}}

    assert score_variant_rows(rows, variant)[0]["score"] == pytest.approx(1.2)
