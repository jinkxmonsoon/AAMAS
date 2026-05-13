from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]


def test_main_audit_passes():
    subprocess.run(["python", str(ROOT / "scripts/build_main_corpus.py")], check=True)
    subprocess.run(["python", str(ROOT / "scripts/audit_main_corpus.py")], check=True)
