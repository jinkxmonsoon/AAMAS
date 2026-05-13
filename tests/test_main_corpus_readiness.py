from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]

def test_main_readiness_script_passes():
    subprocess.run(["python", str(ROOT / "scripts/check_main_corpus_readiness.py")], check=True)
