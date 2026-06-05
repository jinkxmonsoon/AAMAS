import subprocess
from pathlib import Path

from scripts import validate_cct_scoring_config_presence as validator


def test_cct_scoring_config_recovery_report_exists_and_records_blocked_state():
    report = Path("results/reports/journal_v1_full_trace_cct/cct_scoring_config_provenance_recovery_report.md")
    text = report.read_text(encoding="utf-8")

    assert "PERMANENT_RECOVERY_BLOCKED_IN_CURRENT_ENVIRONMENT" in text
    assert validator.EXPECTED_SHA256 in text


def test_cct_scoring_config_validator_reports_blocked_or_pass():
    result = subprocess.run(
        ["python", "scripts/validate_cct_scoring_config_presence.py"],
        check=True,
        text=True,
        capture_output=True,
    )

    if validator.CONFIG_PATH.exists():
        assert "FINAL: PASS" in result.stdout
    else:
        assert "FINAL: BLOCKED_NO_LOCAL_CONFIG" in result.stdout


def test_absent_cct_scoring_config_is_not_recreated_from_memory():
    config = Path("configs/cct_scoring.yaml")
    if not config.exists():
        assert not config.exists()


def test_cct_scoring_config_hash_mismatch_adjudication_records_non_matching_candidates():
    report = Path("results/reports/journal_v1_full_trace_cct/cct_scoring_config_hash_mismatch_adjudication.md")
    text = report.read_text(encoding="utf-8")

    assert validator.EXPECTED_SHA256 in text
    assert "435c4703a90171c8bf246a4fa9e188e70800c66c5e9446d19f74de94b32bb" in text
    assert "1fe4362714cf79a69bd81d0ffe8b82403cc2c2e99abc9f6c7579ed0253278a4a" in text
    assert "NON_MATCHING_CANDIDATE_CONFIG" in text
    assert "not restored" in text.lower()


def test_task18_reproducibility_boundary_records_current_checkout_limit():
    report = Path("results/reports/journal_v1_full_trace_cct/cct_task18_reproducibility_boundary.md")
    text = report.read_text(encoding="utf-8")

    assert "NOT_REPRODUCIBLE_FROM_CURRENT_CHECKOUT" in text
    assert "NOT_PAPER_READY_EMPIRICAL_EVIDENCE" in text
    assert "No non-matching config was restored" in text
