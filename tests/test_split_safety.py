from cctdiag.audit.splits import check_split_safety

def test_split_safety_family_violation_detected():
    recs=[{"trace_id":"c1","clean_parent_trace_id":None},{"trace_id":"p1","clean_parent_trace_id":"c1"}]
    assign={"c1":"train","p1":"test"}
    issues=check_split_safety(recs,assignments=assign,family_level_split=True,loso_groups_defined=True)
    assert any('family_split_violation' in i for i in issues)

def test_split_safety_loso_missing_detected():
    issues=check_split_safety([],assignments=None,loso_groups_defined=False)
    assert 'loso_groups_not_defined' in issues
