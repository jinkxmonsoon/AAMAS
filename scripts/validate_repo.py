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
    "docs/08_artifact_recovery_or_reconstruction_decision.md",
    "docs/09_journal_v1_reconstruction_protocol.md",
    "docs/10_journal_v1_operational_contracts.md",
    "docs/11_journal_v1_corpus_plan_and_label_rubric.md",
    "docs/12_journal_v1_main_corpus_generation_readiness.md",
    "src/cctdiag/__init__.py",
    "src/cctdiag/schema/__init__.py",
    "src/cctdiag/schema/errors.py",
    "src/cctdiag/schema/validators.py",
    "src/cctdiag/schema/contracts.py",
    "src/cctdiag/io/__init__.py",
    "src/cctdiag/io/loaders.py",
    "src/cctdiag/cct/__init__.py",
    "src/cctdiag/features/__init__.py",
    "src/cctdiag/baselines/__init__.py",
    "src/cctdiag/diagnosis/__init__.py",
    "src/cctdiag/perturbations/__init__.py",
    "src/cctdiag/metrics/__init__.py",
    "src/cctdiag/stats/__init__.py",
    "src/cctdiag/reporting/__init__.py",
    "src/cctdiag/audit/splits.py",
    "src/cctdiag/audit/integrity.py",
    "src/cctdiag/audit/leakage.py",
    "src/cctdiag/audit/__init__.py",
    "configs/protocol.yaml",
    "configs/metrics.yaml",
    "configs/seeds.yaml",
    "configs/baselines.yaml",
    "configs/ablations.yaml",
    "configs/robustness.yaml",
    "configs/label_rubric.yaml",
    "configs/corpus_plan.yaml",
    "tests/test_placeholder.py",
    "scripts/validate_repo.py",
    "scripts/validate_protocol.py",
    "data/raw/.gitkeep",
    "data/interim/.gitkeep",
    "data/interim/journal_v1_pilot/pilot_all_traces.jsonl",
    "data/interim/journal_v1_pilot/pilot_perturbed_traces.jsonl",
    "data/interim/journal_v1_pilot/pilot_clean_traces.jsonl",
    "data/processed/.gitkeep",
    "data/external/.gitkeep",
    "results/raw/.gitkeep",
    "results/tables/.gitkeep",
    "results/figures/.gitkeep",
    "results/reports/.gitkeep",
    "results/reports/bracis_v0_reported_results.md",
    "notebooks/exploratory/.gitkeep",
    "results/raw/bracis_v0/README.md",
    "data/raw/bracis_v0/README.md",
    "tests/test_artifact_import.py",
    "tests/test_contracts.py",
    "tests/fixtures/journal_v1/minimal_invalid_label_reference.json",
    "tests/fixtures/journal_v1/minimal_invalid_trace_missing_field.json",
    "tests/fixtures/journal_v1/minimal_valid_trace.json",
    "tests/fixtures/journal_v1/minimal_corpus_duplicate_trace_id.jsonl",
    "tests/fixtures/journal_v1/minimal_corpus_bad_parent_link.jsonl",
    "tests/fixtures/journal_v1/minimal_corpus_leakage.jsonl",
    "tests/fixtures/journal_v1/minimal_corpus_valid.jsonl",
    "tests/test_label_consistency.py",
    "tests/test_schema_validation.py",
    "tests/test_split_safety.py",
    "tests/test_corpus_integrity_audit.py",
    "tests/test_leakage_audit.py",
    "tests/test_corpus_plan.py",
    "tests/test_pilot_corpus_audit.py",
    "tests/test_pilot_corpus_builder.py",
    "tests/test_main_corpus_readiness.py",
    "scripts/make_artifact_manifest.py",
    "scripts/validate_contracts.py",
    "scripts/validate_label_consistency.py",
    "scripts/validate_corpus_schema.py",
    "scripts/validate_corpus_plan.py",
    "scripts/audit_leakage.py",
    "scripts/audit_corpus_integrity.py",
    "scripts/audit_pilot_corpus.py",
    "scripts/build_pilot_corpus.py",
    "scripts/check_main_corpus_readiness.py",
    "results/reports/bracis_v0_artifact_inventory.md",
    "results/reports/journal_v1_pilot/pilot_audit_report.md",
    "results/reports/journal_v1_pilot/pilot_lessons_learned.md",
    "results/reports/journal_v1_pilot/pilot_semantic_audit.md",
    "results/reports/journal_v1_pilot/pilot_corpus_inventory.md",
    "results/reports/journal_v1/main_generation_risk_report.md",
    "results/reports/journal_v1/main_h6_semantic_consistency_audit.md",
    "results/reports/journal_v1/main_h6_label_correction_plan.md",
    "results/reports/journal_v1/main_h6_label_consistency_diagnosis.md",
    "scripts/audit_h6_semantic_consistency.py",
    "scripts/audit_label_position_bias.py",
    "results/reports/journal_v1/main_label_position_bias_report.md",
    "results/reports/journal_v1/main_trivial_baseline_risk_report.md",
    "results/reports/journal_v1/main_label_position_bias_correction_plan.md",
    "results/reports/journal_v1/main_failure_step_revision_plan.md",
    "results/reports/journal_v1/main_failure_step_distribution_after_revision.md",
    "results/reports/journal_v1/main_label_distribution_report.md",
    "results/reports/journal_v1/main_semantic_spotcheck_report.md",
    "docs/artifact_manifests/journal_v1_main_corpus_manifest.md",
    "scripts/audit_main_corpus_semantics.py",
    "scripts/make_journal_v1_manifest.py",
    "docs/artifact_manifests/bracis_v0_import_manifest.md",
    "docs/artifact_manifests/bracis_v0_missing_artifacts.md",
    "docs/artifact_manifests/bracis_v0_recovery_attempt.md",
]

REQUIRED_DIRS = [
    "docs",
    "docs/artifact_manifests",
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
    "data/raw/bracis_v0",
    "data/interim",
    "data/interim/journal_v1_pilot",
    "data/processed",
    "data/external",
    "results",
    "results/raw",
    "results/raw/bracis_v0",
    "results/tables",
    "results/figures",
    "results/reports",
    "results/reports/journal_v1_pilot",
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
