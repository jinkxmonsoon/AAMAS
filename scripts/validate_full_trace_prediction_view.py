#!/usr/bin/env python3
"""Validate full-trace prediction-view construction on files or fixtures."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from cctdiag.io.full_trace_views import (  # noqa: E402
    assert_no_full_trace_private_leakage,
    make_full_trace_prediction_view,
)
from cctdiag.schema.errors import ValidationError  # noqa: E402

FIXTURE_EXPECTATIONS = {
    "minimal_valid_full_trace.json": True,
    "invalid_missing_steps.json": False,
    "invalid_gold_step_not_in_steps.json": False,
    "invalid_failure_centered_top_level.json": False,
    "invalid_single_candidate_trace.json": False,
}


def iter_records(path: Path):
    if path.suffix == ".jsonl":
        for line in path.read_text(encoding="utf-8").splitlines():
            if line.strip():
                yield json.loads(line)
    else:
        yield json.loads(path.read_text(encoding="utf-8"))


def validate_file(path: Path, expect_valid: bool | None = None) -> bool:
    errors: list[str] = []
    for index, record in enumerate(iter_records(path)):
        try:
            view = make_full_trace_prediction_view(record)
            assert_no_full_trace_private_leakage(view)
        except (ValidationError, ValueError) as exc:
            errors.append(f"record[{index}]: {exc}")
    valid = not errors
    expected = valid if expect_valid is None else expect_valid
    if valid == expected:
        if valid:
            print(f"PASS {path.name}")
        else:
            print(f"PASS {path.name} failed as expected: {'; '.join(errors)}")
        return True
    print(f"FAIL {path.name}: expected valid={expected}, observed valid={valid}")
    for error in errors:
        print(f"  - {error}")
    return False


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--fixtures-only", action="store_true")
    parser.add_argument("--path")
    parser.add_argument("--corpus-path")
    args = parser.parse_args()

    if args.fixtures_only:
        fixture_dir = ROOT / "tests/fixtures/full_trace"
        results = [validate_file(fixture_dir / name, expect_valid) for name, expect_valid in FIXTURE_EXPECTATIONS.items()]
    elif args.path or args.corpus_path:
        results = [validate_file(Path(args.path or args.corpus_path))]
    else:
        print("Provide --fixtures-only, --path, or --corpus-path")
        return 2
    ok = all(results)
    print("FINAL:", "PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
