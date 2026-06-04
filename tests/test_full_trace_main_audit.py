"""Tests for the Journal-v1 full-trace main corpus audit."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT_DIR = ROOT / "results/reports/journal_v1_full_trace"
RAW_DIR = ROOT / "results/raw/journal_v1_full_trace"


def test_full_trace_main_audit_passes_and_writes_reports():
    subprocess.run([sys.executable, "scripts/build_full_trace_main_corpus.py"], cwd=ROOT, check=True)
    result = subprocess.run(
        [sys.executable, "scripts/audit_full_trace_main_corpus.py"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    assert "FINAL: PASS" in result.stdout
    for name in [
        "main_full_trace_inventory.md",
        "main_full_trace_audit_report.md",
        "main_full_trace_label_distribution_report.md",
        "main_full_trace_h6_distribution_report.md",
        "main_full_trace_diagnostic_sufficiency_report.md",
        "main_full_trace_candidate_plausibility_report.md",
        "main_full_trace_generation_risk_report.md",
        "main_full_trace_readiness_gate.md",
    ]:
        assert (REPORT_DIR / name).is_file()
    raw = json.loads((RAW_DIR / "main_full_trace_audit_summary.json").read_text(encoding="utf-8"))
    assert raw["counts"] == {"clean": 84, "perturbed": 336, "all": 420}
    assert raw["diagnostic_sufficiency"]["accept"] == 420
    assert raw["candidate_plausibility"]["accept"] == 420
    assert raw["leakage_hits"] == []
