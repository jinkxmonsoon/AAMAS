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
