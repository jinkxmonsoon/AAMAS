from pathlib import Path
from collections import Counter
import json
import subprocess

ROOT = Path(__file__).resolve().parents[1]


def load_jsonl(p: Path):
    return [json.loads(x) for x in p.read_text(encoding="utf-8").splitlines() if x.strip()]


def test_build_main_corpus_counts():
    subprocess.run(["python", str(ROOT / "scripts/build_main_corpus.py")], check=True)
    clean = load_jsonl(ROOT / "data/processed/journal_v1/main_clean_traces.jsonl")
    pert = load_jsonl(ROOT / "data/processed/journal_v1/main_perturbed_traces.jsonl")
    all_rows = load_jsonl(ROOT / "data/processed/journal_v1/main_all_traces.jsonl")
    assert len(clean) == 84
    assert len(pert) == 336
    assert len(all_rows) == 420

    step_counts = Counter(r["gold_failure_step"] for r in all_rows)
    assert step_counts == {"s2": 105, "s3": 105, "s4": 105, "s5": 105}
    assert max(step_counts.values()) / len(all_rows) <= 0.40
    assert step_counts["s2"] / len(all_rows) <= 0.40
    assert sum(1 for v in step_counts.values() if v / len(all_rows) >= 0.15) >= 3

    clean_by_id = {r["trace_id"]: r for r in clean}
    for row in pert:
        parent = clean_by_id[row["clean_parent_trace_id"]]
        assert row["gold_failure_step"] == parent["gold_failure_step"]
        assert row["gold_failure_agent"] == parent["gold_failure_agent"]
