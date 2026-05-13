#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read_text(p: str) -> str:
    return (ROOT / p).read_text(encoding="utf-8")


def main() -> int:
    cp = read_text("configs/corpus_plan.yaml")
    lr = read_text("configs/label_rubric.yaml")

    checks = [
        ("corpus_plan", "dataset_version: BRACIS-Journal-v1", cp),
        ("corpus_plan", "scenario_group_count: 7", cp),
        ("corpus_plan", "clean_cases_per_group: 12", cp),
        ("corpus_plan", "total_clean_cases: 84", cp),
        ("corpus_plan", "core_perturbations_per_clean_case: 4", cp),
        ("corpus_plan", "total_perturbation_variants: 336", cp),
        ("corpus_plan", "total_main_controlled_traces: 420", cp),
        ("label_rubric", "label_provenance_fields:", lr),
        ("label_rubric", "anti_leakage_rules:", lr),
        ("label_rubric", "acceptance_criteria:", lr),
    ]
    failed = False
    print("=== Corpus Plan Validation ===")
    for group, key, text in checks:
        if key in text:
            print(f"PASS {group}: {key}")
        else:
            print(f"FAIL {group}: missing {key}")
            failed = True
    print("FINAL:", "FAIL" if failed else "PASS")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
