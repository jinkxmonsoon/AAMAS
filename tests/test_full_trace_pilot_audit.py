"""Tests for the non-final full-trace pilot audit."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT_DIR = ROOT / "results/reports/journal_v1_full_trace_pilot"


def test_full_trace_pilot_audit_passes_and_writes_reports():
    subprocess.run([sys.executable, "scripts/build_full_trace_pilot_corpus.py"], cwd=ROOT, check=True)
    result = subprocess.run(
        [sys.executable, "scripts/audit_full_trace_pilot_corpus.py"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    assert "FINAL: PASS" in result.stdout
    for name in [
        "full_trace_pilot_inventory.md",
        "full_trace_pilot_audit_report.md",
        "full_trace_pilot_semantic_spotcheck.md",
        "full_trace_pilot_generation_risk_report.md",
    ]:
        assert (REPORT_DIR / name).is_file()
    audit = (REPORT_DIR / "full_trace_pilot_audit_report.md").read_text(encoding="utf-8")
    semantic = (REPORT_DIR / "full_trace_pilot_semantic_spotcheck.md").read_text(encoding="utf-8")
    assert "FINAL: PASS" in audit
    assert "Prediction-view validation: PASS" in audit
    assert "accept: 14" in semantic
    assert "reject: 0" in semantic
