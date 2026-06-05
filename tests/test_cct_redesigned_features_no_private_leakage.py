import json
from pathlib import Path

from cctdiag.cct.redesigned_features import redesigned_feature_leakage_findings

FORBIDDEN_KEYS = {
    "private_labels",
    "provenance",
    "gold_failure_step",
    "gold_failure_agent",
    "label_rationale",
    "correctness",
    "correct",
    "incorrect",
    "score",
    "rank",
    "scenario_group",
    "perturbation_type",
}


def test_redesigned_feature_output_contains_no_private_or_scoring_fields():
    payload = json.loads(Path("results/raw/journal_v1_full_trace_cct_redesigned/cct_redesigned_features.json").read_text())
    rows = payload["features"]

    assert payload["total_feature_rows"] == 420
    assert redesigned_feature_leakage_findings(rows) == []
    for row in rows:
        assert not (set(row) & FORBIDDEN_KEYS)


def test_redesigned_feature_leakage_report_passes():
    text = Path("results/reports/journal_v1_full_trace_cct_redesigned/cct_redesigned_feature_leakage_audit.md").read_text(
        encoding="utf-8"
    )

    assert "Leakage status: PASS" in text
    assert "Findings: 0" in text
    assert "Scenario and perturbation metadata are not feature inputs" in text
