"""Validation checks for BRACIS v0 artifact import scaffold."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_artifact_dirs_and_manifest_exist() -> None:
    assert (ROOT / "data/raw/bracis_v0").is_dir()
    assert (ROOT / "results/raw/bracis_v0").is_dir()
    assert (ROOT / "docs/artifact_manifests/bracis_v0_import_manifest.md").is_file()


def test_no_zero_byte_imported_artifacts_and_duplicate_names_reported() -> None:
    scan_roots = [ROOT / "data/raw/bracis_v0", ROOT / "results/raw/bracis_v0"]
    files = [p for r in scan_roots for p in r.rglob("*") if p.is_file()]

    zero = [str(p) for p in files if p.stat().st_size == 0]
    assert not zero, f"Zero-byte artifacts found: {zero}"

    names = {}
    duplicates = set()
    for p in files:
        if p.name in names:
            duplicates.add(p.name)
        names[p.name] = str(p)

    manifest_text = (ROOT / "docs/artifact_manifests/bracis_v0_import_manifest.md").read_text(encoding="utf-8")
    if duplicates:
        for name in sorted(duplicates):
            assert name in manifest_text or "duplicate" in manifest_text.lower()
