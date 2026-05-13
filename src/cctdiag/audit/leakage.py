LEAKAGE_TERMS = {
    "gold_failure_step", "gold_failure_agent", "irreversible", "propagation", "recoverability",
    "failing step", "root cause step", "decisive error", "label rationale", "ground truth", "gold label"
}

VISIBLE_FIELDS = ["input_message", "output_message", "tool_call", "tool_output", "evidence_items", "evidence_used", "handoff_from", "handoff_to", "provenance_notes"]


def find_leakage(records):
    issues = []
    for r in records:
        rid = r.get("trace_id", "unknown")
        for f in VISIBLE_FIELDS:
            txt = str(r.get(f, "")).lower()
            for t in LEAKAGE_TERMS:
                if t in txt:
                    issues.append((rid, f, t))
        if "label_rationale" in str(r).lower() and any("label_rationale" in str(r.get(f, "")).lower() for f in VISIBLE_FIELDS):
            issues.append((rid, "model_visible", "label_rationale_exposed"))
    return issues
