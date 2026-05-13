#!/usr/bin/env python3
import argparse, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from cctdiag.io.loaders import load_jsonl
from cctdiag.audit.integrity import audit_integrity

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--fixtures-only', action='store_true'); ap.add_argument('--corpus-path'); ap.add_argument('--complete-corpus-check', action='store_true')
    a=ap.parse_args()
    files=[ROOT/'tests/fixtures/journal_v1/minimal_corpus_valid.jsonl', ROOT/'tests/fixtures/journal_v1/minimal_corpus_bad_parent_link.jsonl', ROOT/'tests/fixtures/journal_v1/minimal_corpus_duplicate_trace_id.jsonl'] if a.fixtures_only else [Path(a.corpus_path)]
    failed=False
    for f in files:
        issues=audit_integrity(load_jsonl(str(f)), complete_corpus_check=a.complete_corpus_check)
        if issues:
            print('FAIL', f.name, issues)
            if 'bad_parent_link' not in f.name and 'duplicate_trace_id' not in f.name: failed=True
        else:
            print('PASS', f.name)
    print('FINAL:', 'FAIL' if failed else 'PASS'); return 1 if failed else 0
if __name__=='__main__': raise SystemExit(main())
