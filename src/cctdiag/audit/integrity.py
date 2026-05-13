from cctdiag.schema.contracts import DATASET_VERSION, SCENARIO_GROUPS, PERTURBATION_TYPES


def audit_integrity(records, complete_corpus_check=False, expected_counts=None, core_perturbations=None):
    issues = []
    ids = [r.get("trace_id") for r in records]
    if len(ids) != len(set(ids)):
        issues.append("duplicate_trace_id")
    by_id = {r.get("trace_id"): r for r in records}
    for r in records:
        if r.get("dataset_version") != DATASET_VERSION:
            issues.append(f"bad_dataset_version:{r.get('trace_id')}")
        if r.get("scenario_group") not in SCENARIO_GROUPS:
            issues.append(f"bad_scenario_group:{r.get('trace_id')}")
        if r.get("perturbation_type") not in PERTURBATION_TYPES:
            issues.append(f"bad_perturbation_type:{r.get('trace_id')}")
        if r.get("case_variant") == "clean" and r.get("perturbation_type") != "none":
            issues.append(f"clean_not_none:{r.get('trace_id')}")
        if r.get("perturbation_type") != "none":
            p = r.get("clean_parent_trace_id")
            if not p or p not in by_id or by_id[p].get("case_variant") != "clean":
                issues.append(f"bad_parent_link:{r.get('trace_id')}")
            if r.get("trace_id") == p:
                issues.append(f"overwrite_clean:{r.get('trace_id')}")
    if complete_corpus_check and expected_counts:
        from collections import Counter
        c = Counter(r.get("scenario_group") for r in records if r.get("case_variant") == "clean")
        for sg, n in expected_counts.items():
            if c.get(sg, 0) != n:
                issues.append(f"scenario_count_mismatch:{sg}:{c.get(sg,0)}!={n}")
    return issues
