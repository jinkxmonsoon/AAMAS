"""Tests for the Journal-v1 full-trace main corpus builder."""

from __future__ import annotations

import json
import subprocess
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data/processed/journal_v1_full_trace"


def load_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def test_full_trace_main_builder_outputs_expected_counts_and_distributions():
    result = subprocess.run(
        [sys.executable, "scripts/build_full_trace_main_corpus.py"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    assert "FINAL: PASS" in result.stdout
    clean = load_jsonl(DATA_DIR / "main_full_trace_clean.jsonl")
    perturbed = load_jsonl(DATA_DIR / "main_full_trace_perturbed.jsonl")
    all_rows = load_jsonl(DATA_DIR / "main_full_trace_all.jsonl")
    assert len(clean) == 84
    assert len(perturbed) == 336
    assert len(all_rows) == 420
    assert Counter(row["scenario_group"] for row in clean) == {
        "clean_broken_handoff": 12,
        "tool_evidence_usage": 12,
        "same_agent_continuation": 12,
        "cross_agent_propagation": 12,
        "recoverable_irreversible_failure": 12,
        "semantic_collision": 12,
        "complex_collaboration": 12,
    }
    assert Counter(row["private_labels"]["gold_failure_step"] for row in all_rows) == {
        "s2": 105,
        "s3": 105,
        "s4": 105,
        "s5": 105,
    }
    assert all("step_id" not in row and "agent_id" not in row for row in all_rows)


def test_full_trace_main_builder_creates_all_perturbations_per_parent():
    subprocess.run([sys.executable, "scripts/build_full_trace_main_corpus.py"], cwd=ROOT, check=True)
    clean = load_jsonl(DATA_DIR / "main_full_trace_clean.jsonl")
    perturbed = load_jsonl(DATA_DIR / "main_full_trace_perturbed.jsonl")
    by_parent = {}
    for row in perturbed:
        by_parent.setdefault(row["clean_parent_trace_id"], set()).add(row["perturbation_type"])
    expected = {"paraphrase", "tool_output_truncation", "partial_observability", "non_causal_textual_distraction"}
    assert all(by_parent[row["trace_id"]] == expected for row in clean)
