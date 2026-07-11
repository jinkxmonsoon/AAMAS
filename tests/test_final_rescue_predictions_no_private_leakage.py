import json
from pathlib import Path

PREDICTIONS = Path("results/raw/journal_v1_rescue/final_rescue_predictions.json")
FORBIDDEN = {
    "gold_failure_step",
    "gold_failure_agent",
    "private_labels",
    "label_rationale",
    "provenance",
    "scenario_group",
    "perturbation_type",
    "case_id",
    "case_variant",
    "correctness",
    "score",
    "rank",
}


def test_final_rescue_predictions_exclude_private_gold_and_metadata_fields():
    data = json.loads(PREDICTIONS.read_text())
    assert len(data) == 420
    for item in data:
        assert not (set(item) & FORBIDDEN)
        assert "trace_id" in item
        assert "predictions" in item
        for prediction in item["predictions"].values():
            assert not (set(prediction) & FORBIDDEN)
            assert set(prediction) == {"predicted_step", "top2_steps"}
