#!/usr/bin/env python3
"""Validate required repository structure for initialization task."""

from pathlib import Path

REQUIRED_FILES = [
    "README.md",
    "AGENTS.md",
    "PROTOCOL_LOCK.md",
    "EXPERIMENT_CHANGELOG.md",
    "RESEARCH_LOG.md",
    "docs/00_project_scope.md",
    "docs/01_research_questions.md",
    "docs/02_claims_allowed_forbidden.md",
    "docs/03_cct_formal_schema.md",
    "docs/04_metrics_definition.md",
    "docs/05_reproducibility_checklist.md",
    "docs/06_journal_positioning.md",
    "src/cctdiag/__init__.py",
    "src/cctdiag/io.py",
    "src/cctdiag/schema.py",
    "configs/protocol.yaml",
    "configs/metrics.yaml",
    "configs/seeds.yaml",
    "tests/test_placeholder.py",
    "scripts/validate_repo.py",
]

REQUIRED_DIRS = [
    "docs",
    "src",
    "src/cctdiag",
    "configs",
    "tests",
    "scripts",
]


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    missing_files = [p for p in REQUIRED_FILES if not (root / p).is_file()]
    missing_dirs = [p for p in REQUIRED_DIRS if not (root / p).is_dir()]

    print("=== Repository Validation Report ===")
    print(f"Root: {root}")

    if missing_dirs:
        print("\nMissing directories:")
        for d in missing_dirs:
            print(f"  - {d}")
    else:
        print("\nDirectories: PASS")

    if missing_files:
        print("\nMissing files:")
        for f in missing_files:
            print(f"  - {f}")
    else:
        print("\nFiles: PASS")

    if missing_dirs or missing_files:
        print("\nFINAL: FAIL")
        return 1

    print("\nFINAL: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
