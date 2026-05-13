
def check_split_safety(records, assignments=None, family_level_split=True, loso_groups_defined=True):
    issues = []
    if not loso_groups_defined:
        issues.append("loso_groups_not_defined")
    if assignments and family_level_split:
        fam_to_split = {}
        for r in records:
            fam = r.get("clean_parent_trace_id") or r.get("trace_id")
            sp = assignments.get(r.get("trace_id"))
            if fam in fam_to_split and fam_to_split[fam] != sp:
                issues.append(f"family_split_violation:{fam}")
            fam_to_split[fam] = sp
    return issues
