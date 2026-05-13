from pathlib import Path
from cctdiag.io.loaders import load_jsonl
from cctdiag.audit.integrity import audit_integrity

ROOT = Path(__file__).resolve().parents[1]

def test_integrity_detects_bad_parent_link():
    issues = audit_integrity(load_jsonl(str(ROOT / 'tests/fixtures/journal_v1/minimal_corpus_bad_parent_link.jsonl')))
    assert any('bad_parent_link' in x for x in issues)

def test_integrity_detects_duplicate_ids():
    issues = audit_integrity(load_jsonl(str(ROOT / 'tests/fixtures/journal_v1/minimal_corpus_duplicate_trace_id.jsonl')))
    assert 'duplicate_trace_id' in issues
