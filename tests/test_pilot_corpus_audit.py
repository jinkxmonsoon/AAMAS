from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]

def test_pilot_audit_passes():
    subprocess.run(["python", str(ROOT/"scripts/build_pilot_corpus.py")], check=True)
    subprocess.run(["python", str(ROOT/"scripts/audit_pilot_corpus.py")], check=True)
    assert (ROOT/"results/reports/journal_v1_pilot/pilot_audit_report.md").is_file()
