#!/usr/bin/env python3
import argparse, json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from cctdiag.schema.validators import validate_label_consistency
from cctdiag.schema.errors import ValidationError


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--fixtures-only", action="store_true")
    ap.add_argument("--corpus-path")
    args = ap.parse_args()
    files = [ROOT / "tests/fixtures/journal_v1/minimal_valid_trace.json", ROOT / "tests/fixtures/journal_v1/minimal_invalid_label_reference.json"] if args.fixtures_only else [Path(args.corpus_path)] if args.corpus_path else []
    failed = False
    for f in files:
        if str(f).endswith(".jsonl"):
            import json
            rows=[json.loads(line) for line in Path(f).read_text().splitlines() if line.strip()]
            for r in rows:
                steps=r.get("step_catalog", [r.get("step_id")])
                agents=r.get("agent_catalog", [r.get("agent_id")])
                trace_steps=[{"step_id":s, "agent_id":agents[min(i, len(agents)-1)]} for i,s in enumerate(steps)]
                try:
                    validate_label_consistency(r, trace_steps)
                except ValidationError as e:
                    print(f"FAIL {r.get('trace_id')}: {e}")
                    failed=True
            if not failed:
                print(f"PASS {Path(f).name}")
        else:
            data = json.loads(f.read_text())
            try:
                validate_label_consistency(data["record"], data["trace_steps"])
                print(f"PASS {f.name}")
            except ValidationError as e:
                print(f"FAIL {f.name}: {e}")
                if "invalid" not in f.name:
                    failed = True
    print("FINAL:", "PASS" if not failed else "FAIL")
    return 0 if not failed else 1

if __name__ == "__main__":
    raise SystemExit(main())
