#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REQUIRED = {
    "configs/protocol.yaml": ["journal_v1_dataset_version:", "scenario_groups:", "case_schema_required_keys:", "acceptance_gate:"],
    "configs/metrics.yaml": ["metric_interfaces:"],
    "configs/baselines.yaml": ["baseline_registry:"],
    "configs/ablations.yaml": ["ablation_registry:"],
    "configs/robustness.yaml": ["perturbation_taxonomy:", "analysis_requirements:"],
    "configs/seeds.yaml": ["seed_policy:", "seed_registry_placeholder:"],
    "configs/corpus_plan.yaml": ["dataset_version:", "counts:", "scenario_groups:"],
    "configs/label_rubric.yaml": ["label_semantics:", "label_provenance_fields:", "anti_leakage_rules:", "acceptance_criteria:"],
}

def main() -> int:
    failed = False
    print("=== Contract Validation ===")
    for rel, keys in REQUIRED.items():
        p = ROOT / rel
        if not p.is_file():
            print(f"FAIL missing file: {rel}")
            failed = True
            continue
        text = p.read_text(encoding="utf-8")
        missing = [k for k in keys if k not in text]
        if missing:
            print(f"FAIL {rel}: missing keys {missing}")
            failed = True
        else:
            print(f"PASS {rel}")
    print("FINAL:", "FAIL" if failed else "PASS")
    return 1 if failed else 0

if __name__ == "__main__":
    raise SystemExit(main())
