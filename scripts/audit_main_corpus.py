#!/usr/bin/env python3
import json
import subprocess
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CORPUS = ROOT / "data/processed/journal_v1/main_all_traces.jsonl"
REPORTS = ROOT / "results/reports/journal_v1"


def run_cmd(cmd):
    proc = subprocess.run(cmd, text=True, capture_output=True)
    return proc.returncode, (proc.stdout + proc.stderr).strip()


def load_rows(path):
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def main():
    REPORTS.mkdir(parents=True, exist_ok=True)
    rows = load_rows(CORPUS)
    clean = [r for r in rows if r.get("case_variant") == "clean"]
    pert = [r for r in rows if r.get("case_variant") == "perturbed"]

    scenario_counts = Counter(r["scenario_group"] for r in clean)
    parent_counts = Counter(r.get("clean_parent_trace_id") for r in pert)

    h6 = {
        "propagation_true": sum(1 for r in rows if r.get("gold_propagation") is True),
        "propagation_false": sum(1 for r in rows if r.get("gold_propagation") is False),
        "irreversibility_true": sum(1 for r in rows if r.get("gold_irreversibility") is True),
        "irreversibility_false": sum(1 for r in rows if r.get("gold_irreversibility") is False),
        "recoverability_true": sum(1 for r in rows if r.get("gold_recoverability") is True),
        "recoverability_false": sum(1 for r in rows if r.get("gold_recoverability") is False),
        "uncertain_or_borderline": sum(1 for r in rows if any(str(r.get(k, "")).lower() in {"uncertain", "borderline"} for k in ["gold_propagation", "gold_irreversibility", "gold_recoverability"])),
    }

    checks = {
        "schema": run_cmd(["python", str(ROOT / "scripts/validate_corpus_schema.py"), "--corpus-path", str(CORPUS)]),
        "label": run_cmd(["python", str(ROOT / "scripts/validate_label_consistency.py"), "--corpus-path", str(CORPUS)]),
        "leakage": run_cmd(["python", str(ROOT / "scripts/audit_leakage.py"), "--corpus-path", str(CORPUS)]),
        "integrity": run_cmd(["python", str(ROOT / "scripts/audit_corpus_integrity.py"), "--corpus-path", str(CORPUS), "--complete-corpus-check"]),
    }

    split_ok = "PASS" if run_cmd(["python", str(ROOT / "scripts/audit_corpus_integrity.py"), "--corpus-path", str(CORPUS), "--complete-corpus-check"])[0] == 0 else "FAIL"
    h6_ok = all(h6[k] >= 20 for k in ["propagation_true", "propagation_false", "irreversibility_true", "irreversibility_false", "recoverability_true", "recoverability_false"])

    (REPORTS / "main_corpus_inventory.md").write_text(
        "# Main Corpus Inventory\n\n"
        f"- Clean traces: {len(clean)}\n"
        f"- Perturbed traces: {len(pert)}\n"
        f"- Total traces: {len(rows)}\n"
        f"- Scenario groups: {len(scenario_counts)}\n",
        encoding="utf-8",
    )

    (REPORTS / "main_h6_distribution_report.md").write_text(
        "# Main H6 Distribution Report\n\n" + "\n".join([f"- {k}: {v}" for k, v in h6.items()]) + f"\n- H6 minimum-count gate: {'PASS' if h6_ok else 'FAIL'}\n",
        encoding="utf-8",
    )

    (REPORTS / "main_leakage_report.md").write_text(
        "# Main Leakage Report\n\n" + checks["leakage"][1] + "\n",
        encoding="utf-8",
    )
    (REPORTS / "main_integrity_report.md").write_text(
        "# Main Integrity Report\n\n" + checks["integrity"][1] + "\n",
        encoding="utf-8",
    )

    scenario_ok = len(scenario_counts) == 7 and all(v == 12 for v in scenario_counts.values())
    pert_ok = all(v == 4 for v in parent_counts.values()) and len(pert) == 336
    all_ok = (
        len(clean) == 84 and len(pert) == 336 and len(rows) == 420 and scenario_ok and pert_ok and h6_ok
        and all(code == 0 for code, _ in checks.values())
    )

    (REPORTS / "main_corpus_audit_report.md").write_text(
        "# Main Corpus Audit Report\n\n"
        + f"- Schema validation: {'PASS' if checks['schema'][0] == 0 else 'FAIL'}\n"
        + f"- Label consistency validation: {'PASS' if checks['label'][0] == 0 else 'FAIL'}\n"
        + f"- Leakage audit: {'PASS' if checks['leakage'][0] == 0 else 'FAIL'}\n"
        + f"- Integrity audit: {'PASS' if checks['integrity'][0] == 0 else 'FAIL'}\n"
        + f"- Scenario count audit (7 groups x 12 clean): {'PASS' if scenario_ok else 'FAIL'}\n"
        + f"- Perturbation count audit (4 per clean): {'PASS' if pert_ok else 'FAIL'}\n"
        + f"- Parent-child linkage audit: {'PASS' if pert_ok else 'FAIL'}\n"
        + f"- Split-safety interface audit: {split_ok}\n"
        + f"- H6 distribution audit: {'PASS' if h6_ok else 'FAIL'}\n"
        + f"- FINAL: {'PASS' if all_ok else 'FAIL'}\n",
        encoding="utf-8",
    )

    print("FINAL:", "PASS" if all_ok else "FAIL")
    return 0 if all_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
