"""Tests for the non-final full-trace pilot builder."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PILOT_DIR = ROOT / "data/interim/journal_v1_full_trace_pilot"


def load_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def test_full_trace_pilot_builder_outputs_expected_counts_and_shape():
    result = subprocess.run(
        [sys.executable, "scripts/build_full_trace_pilot_corpus.py"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    assert "FINAL: PASS" in result.stdout
    clean = load_jsonl(PILOT_DIR / "full_trace_pilot_clean.jsonl")
    perturbed = load_jsonl(PILOT_DIR / "full_trace_pilot_perturbed.jsonl")
    all_rows = load_jsonl(PILOT_DIR / "full_trace_pilot_all.jsonl")
    assert len(clean) == 7
    assert len(perturbed) == 7
    assert len(all_rows) == 14
    assert all("steps" in row and len(row["steps"]) >= 4 for row in all_rows)
    assert all("step_id" not in row and "agent_id" not in row for row in all_rows)
    assert {row["scenario_group"] for row in clean} == {
        "clean_broken_handoff",
        "tool_evidence_usage",
        "same_agent_continuation",
        "cross_agent_propagation",
        "recoverable_irreversible_failure",
        "semantic_collision",
        "complex_collaboration",
    }


def test_full_trace_pilot_perturbations_preserve_parent_private_labels():
    subprocess.run([sys.executable, "scripts/build_full_trace_pilot_corpus.py"], cwd=ROOT, check=True)
    clean_by_id = {row["trace_id"]: row for row in load_jsonl(PILOT_DIR / "full_trace_pilot_clean.jsonl")}
    for row in load_jsonl(PILOT_DIR / "full_trace_pilot_perturbed.jsonl"):
        parent = clean_by_id[row["clean_parent_trace_id"]]
        assert row["private_labels"]["gold_failure_step"] == parent["private_labels"]["gold_failure_step"]
        assert row["private_labels"]["gold_failure_agent"] == parent["private_labels"]["gold_failure_agent"]
        assert len(row["steps"]) == len(parent["steps"])
