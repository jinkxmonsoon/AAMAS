#!/usr/bin/env python3
import argparse, json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from cctdiag.schema.validators import validate_record_schema
from cctdiag.schema.errors import ValidationError


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--fixtures-only", action="store_true")
    ap.add_argument("--corpus-path")
    args = ap.parse_args()
    files = [ROOT / "tests/fixtures/journal_v1/minimal_valid_trace.json", ROOT / "tests/fixtures/journal_v1/minimal_invalid_trace_missing_field.json"] if args.fixtures_only else [Path(args.corpus_path)] if args.corpus_path else []
    failed = False
    for f in files:
        if str(f).endswith(".jsonl"):
            rows=[json.loads(line) for line in Path(f).read_text().splitlines() if line.strip()]
            for rec in rows:
                try:
                    validate_record_schema(rec)
                except ValidationError as e:
                    print(f"FAIL {rec.get('trace_id')}: {e}")
                    failed=True
            if not failed:
                print(f"PASS {Path(f).name}")
        else:
            raw = json.loads(f.read_text())
            rec = raw["record"] if "record" in raw else raw
            try:
                validate_record_schema(rec)
                print(f"PASS {f.name}")
            except ValidationError as e:
                print(f"FAIL {f.name}: {e}")
                if "invalid" not in f.name:
                    failed = True
    print("FINAL:", "PASS" if not failed else "FAIL")
    return 0 if not failed else 1

if __name__ == "__main__":
    raise SystemExit(main())
