from pathlib import Path
from cctdiag.io.loaders import load_jsonl
from cctdiag.audit.leakage import find_leakage

ROOT = Path(__file__).resolve().parents[1]

def test_leakage_detects_leaky_fixture():
    issues = find_leakage(load_jsonl(str(ROOT / 'tests/fixtures/journal_v1/minimal_corpus_leakage.jsonl')))
    assert issues

def test_leakage_passes_valid_fixture():
    issues = find_leakage(load_jsonl(str(ROOT / 'tests/fixtures/journal_v1/minimal_corpus_valid.jsonl')))
    assert not issues
