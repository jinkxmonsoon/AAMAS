#!/usr/bin/env python3
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from cctdiag.io.loaders import load_jsonl
from cctdiag.schema.validators import validate_record_schema, validate_label_consistency
from cctdiag.schema.errors import ValidationError
from cctdiag.audit.leakage import find_leakage
from cctdiag.audit.integrity import audit_integrity


def main():
    p = ROOT / "data/interim/journal_v1_pilot/pilot_all_traces.jsonl"
    rows = load_jsonl(str(p))
    errs=[]
    for r in rows:
        try:
            validate_record_schema(r)
            trace_steps=[{"step_id": s, "agent_id": r["agent_catalog"][min(i, len(r["agent_catalog"])-1)]} for i,s in enumerate(r["step_catalog"])]
            validate_label_consistency(r, trace_steps)
        except ValidationError as e:
            errs.append(f"{r.get('trace_id')}: {e}")
    leak = find_leakage(rows)
    integ = audit_integrity(rows)
    clean=[r for r in rows if r.get("case_variant")=="clean"]
    pert=[r for r in rows if r.get("case_variant")!="clean"]
    scenario_count=len(set(r["scenario_group"] for r in clean))
    coverage_ok = len(rows)==14 and len(clean)==7 and len(pert)==7 and scenario_count==7

    # H6-oriented counts
    prop_true = sum(1 for r in rows if r.get("gold_propagation") is True)
    irrev_true = sum(1 for r in rows if r.get("gold_irreversibility") is True)
    recov_true = sum(1 for r in rows if r.get("gold_recoverability") is True)
    recovered_intermediate = sum(1 for r in rows if str(r.get("gold_recoverability", "")).lower() == "recovered_intermediate_error")
    uncertain_or_borderline = sum(1 for r in rows if any(str(r.get(k, "")).lower() in {"uncertain", "borderline", "unknown"} for k in ["gold_irreversibility", "gold_propagation", "gold_recoverability"]))

    rationale_prop = all(r.get("label_rationale") for r in rows if r.get("gold_propagation") is True)
    rationale_irrev = all(r.get("label_rationale") for r in rows if r.get("gold_irreversibility") is True)
    rationale_recov = all(r.get("label_rationale") for r in rows if r.get("gold_recoverability") is True)

    h6_ok = (
        prop_true >= 2 and irrev_true >= 2 and (recov_true >= 2 or recovered_intermediate >= 2)
        and rationale_prop and rationale_irrev and rationale_recov
    )

    out = ROOT / "results/reports/journal_v1_pilot/pilot_audit_report.md"
    out.write_text(
        "# Pilot Audit Report\n\n"
        "- Non-final, non-evidential pilot only.\n"
        f"- Schema/label errors: {len(errs)}\n"
        f"- Leakage issues: {len(leak)}\n"
        f"- Integrity issues: {len(integ)}\n"
        f"- Coverage check (14/7/7/all-scenarios): {'PASS' if coverage_ok else 'FAIL'}\n"
        f"- H6 coverage: propagation_true={prop_true}, irreversibility_true={irrev_true}, recoverability_true={recov_true}, recovered_intermediate={recovered_intermediate}, uncertain_or_borderline={uncertain_or_borderline}\n"
        f"- H6 acceptance check: {'PASS' if h6_ok else 'FAIL'}\n"
        f"- Rationale checks for true labels: propagation={rationale_prop}, irreversibility={rationale_irrev}, recoverability={rationale_recov}\n",
        encoding="utf-8",
    )
    final_fail = bool(errs or leak or integ or not coverage_ok or not h6_ok)
    print("FINAL:", "FAIL" if final_fail else "PASS")
    return 1 if final_fail else 0

if __name__ == "__main__":
    raise SystemExit(main())
