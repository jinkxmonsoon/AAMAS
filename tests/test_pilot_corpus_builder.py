from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]

def test_build_pilot_creates_expected_files():
    subprocess.run(["python", str(ROOT/"scripts/build_pilot_corpus.py")], check=True)
    assert (ROOT/"data/interim/journal_v1_pilot/pilot_all_traces.jsonl").is_file()
