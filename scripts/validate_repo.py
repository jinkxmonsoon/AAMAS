#!/usr/bin/env python3
"""Validate required repository structure for protocol-first scaffold hardening."""

from pathlib import Path

REQUIRED_FILES = [
    "README.md",
    "AGENTS.md",
    "PROTOCOL_LOCK.md",
    "EXPERIMENT_CHANGELOG.md",
    "RESEARCH_LOG.md",
    "requirements.txt",
    "pyproject.toml",
    ".gitignore",
    "CITATION.cff",
    "docs/00_project_scope.md",
    "docs/01_research_questions.md",
    "docs/02_claims_allowed_forbidden.md",
    "docs/03_cct_formal_schema.md",
    "docs/04_metrics_definition.md",
    "docs/05_reproducibility_checklist.md",
    "docs/06_journal_positioning.md",
    "docs/07_desk_reject_artifact_audit.md",
    "src/cctdiag/__init__.py",
    "src/cctdiag/schema/__init__.py",
    "src/cctdiag/io/__init__.py",
    "src/cctdiag/cct/__init__.py",
    "src/cctdiag/features/__init__.py",
    "src/cctdiag/baselines/__init__.py",
    "src/cctdiag/diagnosis/__init__.py",
    "src/cctdiag/perturbations/__init__.py",
    "src/cctdiag/metrics/__init__.py",
    "src/cctdiag/stats/__init__.py",
    "src/cctdiag/reporting/__init__.py",
    "configs/protocol.yaml",
    "configs/metrics.yaml",
    "configs/seeds.yaml",
    "configs/baselines.yaml",
    "configs/ablations.yaml",
    "configs/robustness.yaml",
    "tests/test_placeholder.py",
    "scripts/validate_repo.py",
    "scripts/validate_protocol.py",
    "data/raw/.gitkeep",
    "data/interim/.gitkeep",
    "data/processed/.gitkeep",
    "data/external/.gitkeep",
    "results/raw/.gitkeep",
    "results/tables/.gitkeep",
    "results/figures/.gitkeep",
    "results/reports/.gitkeep",
    "results/reports/bracis_v0_reported_results.md",
    "notebooks/exploratory/.gitkeep",
]

REQUIRED_DIRS = [
    "docs",
    "src",
    "src/cctdiag",
    "src/cctdiag/schema",
    "src/cctdiag/io",
    "src/cctdiag/cct",
    "src/cctdiag/features",
    "src/cctdiag/baselines",
    "src/cctdiag/diagnosis",
    "src/cctdiag/perturbations",
    "src/cctdiag/metrics",
    "src/cctdiag/stats",
    "src/cctdiag/reporting",
    "configs",
    "tests",
    "scripts",
    "data",
    "data/raw",
    "data/interim",
    "data/processed",
    "data/external",
    "results",
    "results/raw",
    "results/tables",
    "results/figures",
    "results/reports",
    "notebooks",
    "notebooks/exploratory",
]



AMBIGUOUS_NAMES = [
    "io",
    "schema",
    "metrics",
    "stats",
    "reporting",
    "baselines",
    "diagnosis",
    "perturbations",
    "features",
    "cct",
]

def main() -> int:
    root = Path(__file__).resolve().parents[1]
    missing_files = [p for p in REQUIRED_FILES if not (root / p).is_file()]
    missing_dirs = [p for p in REQUIRED_DIRS if not (root / p).is_dir()]

    ambiguous = []
    for name in AMBIGUOUS_NAMES:
        mod = root / "src" / "cctdiag" / f"{name}.py"
        pkg = root / "src" / "cctdiag" / name
        if mod.exists() and pkg.is_dir():
            ambiguous.append(name)

    print("=== Repository Validation Report ===")
    print(f"Root: {root}")
    print(f"Checked directories: {len(REQUIRED_DIRS)}")
    print(f"Checked files: {len(REQUIRED_FILES)}")

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

    if ambiguous:
        print("\nAmbiguous module/package names:")
        for name in ambiguous:
            print(f"  - {name}")
    else:
        print("\nAmbiguity check: PASS")

    if missing_dirs or missing_files or ambiguous:
        print("\nFINAL: FAIL")
        return 1

    print("\nFINAL: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
