"""Ranking helpers for frozen uncalibrated CCT diagnostics."""

from __future__ import annotations

from collections import defaultdict
from collections.abc import Mapping, Sequence
from typing import Any


def rank_trace_candidates(scored_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    """Rank candidates within each trace by descending score.

    Ties preserve the input feature-row order within each trace. This is a
    deterministic diagnostic convention, not a learned or tuned tie-breaker.
    """

    grouped: dict[str, list[tuple[int, Mapping[str, Any]]]] = defaultdict(list)
    for index, row in enumerate(scored_rows):
        grouped[str(row["trace_id"])].append((index, row))

    ranked_rows: list[dict[str, Any]] = []
    for trace_id in sorted(grouped):
        ordered = sorted(grouped[trace_id], key=lambda item: (-float(item[1]["score"]), item[0]))
        top_score = float(ordered[0][1]["score"]) if ordered else 0.0
        tie_count = sum(1 for _, row in ordered if float(row["score"]) == top_score)
        for rank_index, (_, row) in enumerate(ordered, start=1):
            ranked_rows.append(
                {
                    "trace_id": trace_id,
                    "step_id": row["step_id"],
                    "agent_id": row["agent_id"],
                    "score": float(row["score"]),
                    "rank": rank_index,
                    "top_score_tie_count": tie_count,
                }
            )
    return ranked_rows


def top_ranked_by_trace(ranked_rows: Sequence[Mapping[str, Any]]) -> dict[str, dict[str, Any]]:
    """Return the top-ranked diagnostic candidate for each trace."""

    top: dict[str, dict[str, Any]] = {}
    for row in ranked_rows:
        if int(row["rank"]) == 1:
            top[str(row["trace_id"])] = dict(row)
    return top
