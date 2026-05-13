#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = [
    "data/interim/journal_v1_pilot/pilot_all_traces.jsonl",
    "data/interim/journal_v1_pilot/pilot_clean_traces.jsonl",
    "data/interim/journal_v1_pilot/pilot_perturbed_traces.jsonl",
    "results/reports/journal_v1_pilot/pilot_audit_report.md",
    "results/reports/journal_v1_pilot/pilot_semantic_audit.md",
    "results/reports/journal_v1_pilot/pilot_lessons_learned.md",
    "configs/corpus_plan.yaml",
    "configs/label_rubric.yaml",
    "docs/12_journal_v1_main_corpus_generation_readiness.md",
]

def main():
    fail = False
    for rel in REQUIRED:
        if not (ROOT / rel).is_file():
            print(f"FAIL missing: {rel}")
            fail = True
    text = (ROOT / "docs/12_journal_v1_main_corpus_generation_readiness.md").read_text(encoding="utf-8")
    if "## Readiness blockers" not in text:
        print("FAIL missing readiness blockers section")
        fail = True
    elif "- none" not in text.lower():
        print("FAIL unresolved readiness blockers")
        fail = True
    print("FINAL:", "FAIL" if fail else "PASS")
    return 1 if fail else 0

if __name__ == "__main__":
    raise SystemExit(main())
