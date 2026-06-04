import json
from pathlib import Path

import pytest

from cctdiag.diagnosis.cct_scoring import score_feature_row, score_variant_rows

ROOT = Path(__file__).resolve().parents[1]


def test_score_feature_row_uses_fixed_weighted_sum_only():
    row = {
        "trace_id": "t1",
        "step_id": "s2",
        "agent_id": "a2",
        "evidence_used_count": 1,
        "has_tool_call": True,
        "output_token_count": 10,
    }
    weights = {"evidence_used_count": 0.2, "has_tool_call": 0.1, "output_token_count": 0.05}

    assert score_feature_row(row, weights) == pytest.approx(0.8)


def test_all_frozen_variants_score_feature_sample_without_gold_fields():
    config = json.loads((ROOT / "configs/cct_scoring.yaml").read_text())
    rows = [json.loads(line) for line in (ROOT / "data/interim/journal_v1_full_trace_cct/sample_cct_features.jsonl").read_text().splitlines() if line]

    for variant in config["variants"].values():
        scored = score_variant_rows(rows, variant)
        assert len(scored) == len(rows)
        assert {"trace_id", "step_id", "agent_id", "score"}.issubset(scored[0])
