from pathlib import Path
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
