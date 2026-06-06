from pathlib import Path

DEGENERACY = Path("results/reports/journal_v1_rescue/rescue_candidate_step_feature_degeneracy_report.md")
LEAKAGE = Path("results/reports/journal_v1_rescue/rescue_candidate_step_feature_leakage_audit.md")
READINESS = Path("results/reports/journal_v1_rescue/rescue_candidate_step_feature_readiness_gate.md")
POSITION = Path("results/reports/journal_v1_rescue/rescue_candidate_step_position_identity_risk_report.md")


def test_rescue_readiness_reports_exist_and_record_required_gate():
    for path in [DEGENERACY, LEAKAGE, READINESS, POSITION]:
        assert path.exists()
    assert "Total rows: 2100" in DEGENERACY.read_text()
    assert "Leakage status: PASS" in LEAKAGE.read_text()
    assert "RESCUE_CANDIDATE_STEP_FEATURES_READY_FOR_SCORING = no" in READINESS.read_text()
    assert "Features include agent identity column: no" in POSITION.read_text()


def test_rescue_readiness_records_no_scoring_non_action():
    text = READINESS.read_text()
    assert "No scoring" in text
    assert "gold/H6 comparison" in text
    assert "paper-ready result table" in text
