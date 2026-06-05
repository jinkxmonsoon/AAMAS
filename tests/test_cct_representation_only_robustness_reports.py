from pathlib import Path


REPORT_DIR = Path("results/reports/journal_v1_full_trace_cct")


def test_representation_only_status_preserves_scoring_blocker():
    text = (REPORT_DIR / "cct_representation_only_status_after_config_blocker.md").read_text(encoding="utf-8")

    assert "configs/cct_scoring.yaml` remains absent" in text
    assert "NOT_REPRODUCIBLE_FROM_CURRENT_CHECKOUT" in text
    assert "Scoring and calibration remain blocked" in text


def test_causal_edge_robustness_audit_records_sample_counts_without_scoring():
    text = (REPORT_DIR / "cct_causal_edge_sample_robustness_audit.md").read_text(encoding="utf-8")

    assert "Sample trace count: 14" in text
    assert "Clean sampled traces: 7" in text
    assert "Perturbed sampled traces: 7" in text
    assert "Total sample edge count: 102" in text
    assert "not a statistical test" in text


def test_rule_limitations_and_next_readiness_remain_conservative():
    limitations = (REPORT_DIR / "cct_causal_edge_sample_rule_limitations.md").read_text(encoding="utf-8")
    readiness = (REPORT_DIR / "cct_causal_edge_next_readiness_decision.md").read_text(encoding="utf-8")

    assert "downstream_dependency_edge" in limitations
    assert "tool_alignment_edge" in limitations
    assert "cross_agent_dependency_edge" in limitations
    assert "constraint_shift_edge" in limitations
    assert "semantic_collision_edge" in limitations
    assert "REPRESENTATION_ONLY_EDGE_ROBUSTNESS_READY_FOR_FULL_CORPUS_AUDIT = no" in readiness
    assert "CCT_CAUSAL_FLOW_EDGES_READY_FOR_SCORING = no" in readiness
    assert "No config restoration/recreation" in readiness
