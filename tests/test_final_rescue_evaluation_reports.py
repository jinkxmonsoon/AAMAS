from pathlib import Path

AMENDMENT = Path("results/reports/journal_v1_rescue/rescue_protocol_amendment_for_intratrace_ranking.md")
EVALUATION = Path("results/reports/journal_v1_rescue/final_rescue_evaluation_report.md")
ERROR = Path("results/reports/journal_v1_rescue/final_rescue_error_analysis.md")
DECISION = Path("results/reports/journal_v1_rescue/final_rescue_hypothesis_decision.md")
PREDICTIONS = Path("results/raw/journal_v1_rescue/final_rescue_predictions.json")


def test_final_rescue_reports_and_predictions_exist():
    for path in [AMENDMENT, EVALUATION, ERROR, DECISION, PREDICTIONS]:
        assert path.exists()
    assert "within-trace duplicate candidate-step rows = 0" in AMENDMENT.read_text()
    assert "flat_log_text_similarity_baseline` is omitted" in EVALUATION.read_text()
    assert "H1-R: unsupported" in DECISION.read_text()
    assert "H2-R: unsupported" in DECISION.read_text()


def test_final_rescue_records_no_paper_ready_claims():
    text = DECISION.read_text()
    assert "paper-ready performance claim" in text
    assert "return to Path B negative-evidence framing" in text
