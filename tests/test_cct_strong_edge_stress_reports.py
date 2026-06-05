from pathlib import Path

REPORT_DIR = Path("results/reports/journal_v1_full_trace_cct")


def test_strong_edge_stress_plan_limits_scope_to_three_edges():
    text = (REPORT_DIR / "cct_strong_edge_stress_test_plan.md").read_text(encoding="utf-8")

    assert "downstream_dependency_edge" in text
    assert "tool_alignment_edge" in text
    assert "cross_agent_dependency_edge" in text
    assert "constraint_shift_edge`: remains sparse" in text
    assert "semantic_collision_edge`: remains highly lexical" in text
    assert "gold_failure_step" in text


def test_strong_edge_stress_report_records_subset_counts_and_no_statistics():
    text = (REPORT_DIR / "cct_strong_edge_stress_test_report.md").read_text(encoding="utf-8")

    assert "Sample trace count: 14" in text
    assert "In-scope edge count: 78" in text
    assert "`downstream_dependency_edge` | 11 | 11" in text
    assert "`tool_alignment_edge` | 14 | 14" in text
    assert "`cross_agent_dependency_edge` | 14 | 14" in text
    assert "not statistical tests" in text


def test_strong_edge_readiness_authorizes_only_narrow_audit_not_scoring():
    recommendation = (REPORT_DIR / "cct_strong_edge_rule_revision_recommendation.md").read_text(encoding="utf-8")
    readiness = (REPORT_DIR / "cct_strong_edge_readiness_gate.md").read_text(encoding="utf-8")

    assert "narrowed representation-only full-corpus audit" in recommendation
    assert "STRONG_CAUSAL_FLOW_EDGES_READY_FOR_NARROW_FULL_CORPUS_AUDIT = yes" in readiness
    assert "CCT_CAUSAL_FLOW_EDGES_READY_FOR_SCORING = no" in readiness
    assert "It may extract only `downstream_dependency_edge`, `tool_alignment_edge`, and `cross_agent_dependency_edge`" in readiness
