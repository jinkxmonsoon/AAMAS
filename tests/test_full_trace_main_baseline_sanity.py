"""Tests for full-trace main corpus diagnostic baseline sanity."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RAW_PATH = ROOT / "results/raw/journal_v1_full_trace/main_full_trace_baseline_sanity.json"
REPORT_PATH = ROOT / "results/reports/journal_v1_full_trace/main_full_trace_shortcut_baseline_report.md"


def test_full_trace_main_baseline_sanity_passes_without_blockers():
    subprocess.run([sys.executable, "scripts/build_full_trace_main_corpus.py"], cwd=ROOT, check=True)
    subprocess.run([sys.executable, "scripts/audit_full_trace_main_corpus.py"], cwd=ROOT, check=True)
    result = subprocess.run(
        [sys.executable, "scripts/run_full_trace_main_baseline_sanity.py"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    assert "FINAL: PASS" in result.stdout
    raw = json.loads(RAW_PATH.read_text(encoding="utf-8"))
    assert raw["interpretation"]["status"] == "passed"
    assert raw["semantic_diversity"]["leakage_hits"] == []
    for metrics in raw["results"].values():
        for key in ("step_accuracy", "agent_accuracy"):
            value = metrics[key]
            if value is not None:
                assert value <= 0.70
    assert REPORT_PATH.is_file()
