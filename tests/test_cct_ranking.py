from cctdiag.diagnosis.cct_ranking import rank_trace_candidates, top_ranked_by_trace


def test_rank_trace_candidates_orders_within_trace_and_preserves_ties_by_input_order():
    scored = [
        {"trace_id": "t1", "step_id": "s1", "agent_id": "a1", "score": 1.0},
        {"trace_id": "t1", "step_id": "s2", "agent_id": "a2", "score": 2.0},
        {"trace_id": "t1", "step_id": "s3", "agent_id": "a3", "score": 2.0},
        {"trace_id": "t2", "step_id": "s1", "agent_id": "a1", "score": 0.5},
    ]

    ranked = rank_trace_candidates(scored)
    top = top_ranked_by_trace(ranked)

    assert top["t1"]["step_id"] == "s2"
    assert top["t1"]["top_score_tie_count"] == 2
    assert top["t2"]["step_id"] == "s1"
