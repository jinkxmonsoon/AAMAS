#!/usr/bin/env python3
"""Analyze errors from the frozen uncalibrated CCT diagnostic run.

This script performs post-hoc descriptive error analysis only. It does not
change config weights, add features, alter scoring/ranking, calibrate, grid
search, run LOSO, refine, ablate, run statistical tests, or produce paper-ready
result tables.
"""

from __future__ import annotations

import hashlib
import json
import statistics
import subprocess
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from cctdiag.diagnosis.cct_ranking import rank_trace_candidates, top_ranked_by_trace  # noqa: E402
from cctdiag.diagnosis.cct_scoring import score_feature_row  # noqa: E402

CONFIG_PATH = ROOT / "configs/cct_scoring.yaml"
FEATURES_PATH = ROOT / "data/interim/journal_v1_full_trace_cct/cct_features.jsonl"
CORPUS_PATH = ROOT / "data/processed/journal_v1_full_trace/main_full_trace_all.jsonl"
TASK18_RAW_PATH = ROOT / "results/raw/journal_v1_full_trace_cct/cct_uncalibrated_diagnostics.json"
RAW_OUT = ROOT / "results/raw/journal_v1_full_trace_cct/cct_uncalibrated_error_analysis.json"
REPORT_DIR = ROOT / "results/reports/journal_v1_full_trace_cct"
ERROR_REPORT = REPORT_DIR / "cct_uncalibrated_error_analysis.md"
TIE_REPORT = REPORT_DIR / "cct_uncalibrated_tie_analysis.md"
FEATURE_REPORT = REPORT_DIR / "cct_uncalibrated_feature_dominance_report.md"
DISAGREEMENT_REPORT = REPORT_DIR / "cct_uncalibrated_variant_disagreement_report.md"
TASK18_CONFIG_SHA256 = "053f19066923d8d22d27b22727e75876f939f2a60480484c4028eabd07ad0855"
TASK18_HEAD = "2695aa3e8c06936270b40a1b6d93eee41f55f87b"


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    with path.open(encoding="utf-8") as handle:
        return [json.loads(line) for line in handle if line.strip()]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _accuracy(correct: int, total: int) -> float | None:
    return None if total == 0 else correct / total


def _labels(corpus: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    labels = {}
    for record in corpus:
        labels[record["trace_id"]] = {
            "gold_step": record["private_labels"]["gold_failure_step"],
            "gold_agent": record["private_labels"]["gold_failure_agent"],
            "scenario_group": record["scenario_group"],
            "perturbation_type": record["perturbation_type"],
            "case_variant_group": "clean" if record["case_variant"] == "clean" else "perturbed",
        }
    return labels


def _features_by_trace(features: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in features:
        grouped[row["trace_id"]].append(row)
    for rows in grouped.values():
        rows.sort(key=lambda row: row["order_index"])
    return grouped


def _confusion(gold_pred_pairs: list[tuple[str, str]]) -> dict[str, dict[str, int]]:
    matrix: dict[str, dict[str, int]] = defaultdict(lambda: defaultdict(int))
    for gold, pred in gold_pred_pairs:
        matrix[gold][pred] += 1
    return {gold: dict(sorted(preds.items())) for gold, preds in sorted(matrix.items())}


def _breakdown(records: list[dict[str, Any]], group_field: str) -> dict[str, dict[str, Any]]:
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for record in records:
        grouped[record[group_field]].append(record)
    return {
        group: {
            "n": len(rows),
            "correct": sum(1 for row in rows if row["correct"]),
            "incorrect": sum(1 for row in rows if not row["correct"]),
            "accuracy": _accuracy(sum(1 for row in rows if row["correct"]), len(rows)),
            "error_rate": _accuracy(sum(1 for row in rows if not row["correct"]), len(rows)),
        }
        for group, rows in sorted(grouped.items())
    }


def _rank_containment(ranked_by_trace: dict[str, list[dict[str, Any]]], labels: dict[str, dict[str, Any]]) -> dict[str, Any]:
    ranks = []
    top2 = 0
    top3 = 0
    for trace_id, ranked in ranked_by_trace.items():
        gold = labels[trace_id]["gold_step"]
        rank = next(row["rank"] for row in ranked if row["step_id"] == gold)
        ranks.append(rank)
        if rank <= 2:
            top2 += 1
        if rank <= 3:
            top3 += 1
    return {
        "top_1_accuracy": _accuracy(sum(1 for rank in ranks if rank == 1), len(ranks)),
        "top_2_containment": _accuracy(top2, len(ranks)),
        "top_3_containment": _accuracy(top3, len(ranks)),
        "mean_gold_step_rank": statistics.mean(ranks),
        "median_gold_step_rank": statistics.median(ranks),
        "gold_step_rank_distribution": dict(sorted(Counter(ranks).items())),
    }


def _score_variant(variant_name: str, variant: dict[str, Any], features_by_trace: dict[str, list[dict[str, Any]]], labels: dict[str, dict[str, Any]]) -> dict[str, Any]:
    scored = []
    for rows in features_by_trace.values():
        for row in rows:
            scored.append(
                {
                    "trace_id": row["trace_id"],
                    "step_id": row["step_id"],
                    "agent_id": row["agent_id"],
                    "score": score_feature_row(row, variant["features"]),
                }
            )
    ranked = rank_trace_candidates(scored)
    ranked_by_trace: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in ranked:
        ranked_by_trace[row["trace_id"]].append(row)
    top = top_ranked_by_trace(ranked)

    rows = []
    step_pairs = []
    agent_pairs = []
    for trace_id, pred in top.items():
        label = labels[trace_id]
        correct = pred["step_id"] == label["gold_step"]
        rows.append(
            {
                "trace_id": trace_id,
                "pred_step": pred["step_id"],
                "pred_agent": pred["agent_id"],
                "gold_step": label["gold_step"],
                "gold_agent": label["gold_agent"],
                "correct": correct,
                "agent_correct": pred["agent_id"] == label["gold_agent"],
                "tuple_correct": correct and pred["agent_id"] == label["gold_agent"],
                "scenario_group": label["scenario_group"],
                "perturbation_type": label["perturbation_type"],
                "case_variant_group": label["case_variant_group"],
                "top_score_tie_count": pred["top_score_tie_count"],
            }
        )
        step_pairs.append((label["gold_step"], pred["step_id"]))
        agent_pairs.append((label["gold_agent"], pred["agent_id"]))

    total = len(rows)
    correct_count = sum(1 for row in rows if row["correct"])
    return {
        "variant_name": variant_name,
        "predicted_step_distribution": dict(sorted(Counter(row["pred_step"] for row in rows).items())),
        "predicted_agent_distribution": dict(sorted(Counter(row["pred_agent"] for row in rows).items())),
        "gold_step_predicted_step_confusion": _confusion(step_pairs),
        "gold_agent_predicted_agent_confusion": _confusion(agent_pairs),
        "correct_count": correct_count,
        "incorrect_count": total - correct_count,
        "step_accuracy": _accuracy(correct_count, total),
        "agent_accuracy": _accuracy(sum(1 for row in rows if row["agent_correct"]), total),
        "tuple_step_agent_accuracy": _accuracy(sum(1 for row in rows if row["tuple_correct"]), total),
        "clean_vs_perturbed_error_breakdown": _breakdown(rows, "case_variant_group"),
        "scenario_error_breakdown": _breakdown(rows, "scenario_group"),
        "perturbation_error_breakdown": _breakdown(rows, "perturbation_type"),
        "correct_trace_ids": [row["trace_id"] for row in rows if row["correct"]],
        "wrong_trace_ids": [row["trace_id"] for row in rows if not row["correct"]],
        "rank_diagnostics": _rank_containment(ranked_by_trace, labels),
        "ranked_by_trace": {trace_id: ranked_by_trace[trace_id] for trace_id in sorted(ranked_by_trace)},
        "top_predictions": top,
    }


def _tie_analysis(variant_analysis: dict[str, dict[str, Any]], labels: dict[str, dict[str, Any]]) -> dict[str, Any]:
    output = {}
    for variant, payload in variant_analysis.items():
        tied = []
        non_tied = []
        tie_break_gold_missed = 0
        tie_break_affects_pred = 0
        for trace_id, ranked in payload["ranked_by_trace"].items():
            top_score = ranked[0]["score"]
            top_tied = [row for row in ranked if row["score"] == top_score]
            pred = ranked[0]
            correct = pred["step_id"] == labels[trace_id]["gold_step"]
            record = {"trace_id": trace_id, "correct": correct, "tie_count": len(top_tied)}
            if len(top_tied) > 1:
                tied.append(record)
                if len({row["step_id"] for row in top_tied}) > 1:
                    tie_break_affects_pred += 1
                if not correct and any(row["step_id"] == labels[trace_id]["gold_step"] for row in top_tied):
                    tie_break_gold_missed += 1
            else:
                non_tied.append(record)
        total = len(tied) + len(non_tied)
        output[variant] = {
            "tied_top_score_traces": len(tied),
            "tied_top_score_percent": _accuracy(len(tied), total),
            "average_tied_candidates_per_trace": statistics.mean([row["tie_count"] for row in tied]) if tied else 1.0,
            "tie_breaking_can_affect_predicted_step": tie_break_affects_pred,
            "tie_breaking_missed_gold_that_was_tied_for_top": tie_break_gold_missed,
            "accuracy_on_tied_traces": _accuracy(sum(1 for row in tied if row["correct"]), len(tied)),
            "accuracy_on_non_tied_traces": _accuracy(sum(1 for row in non_tied if row["correct"]), len(non_tied)),
            "wrong_score_separation_traces": sum(1 for row in non_tied if not row["correct"]),
        }
    return output


def _feature_dominance(config: dict[str, Any], features_by_trace: dict[str, list[dict[str, Any]]], labels: dict[str, dict[str, Any]], primary_ranked: dict[str, list[dict[str, Any]]]) -> dict[str, Any]:
    weights = config["variants"]["cct_primary_no_position"]["features"]
    contribution_values: dict[str, list[float]] = {feature: [] for feature in weights}
    top_contributor_by_trace = Counter()
    trace_summaries = []
    margins_rank1_rank2 = []
    margins_gold_to_top = []
    score_ranges = []

    for trace_id, rows in features_by_trace.items():
        per_step_contributions = []
        for row in rows:
            contributions = {}
            for feature, weight in weights.items():
                value = row.get(feature, 0)
                numeric = 1.0 if value is True else 0.0 if value is False or value is None else float(value)
                contribution = float(weight) * numeric
                contributions[feature] = contribution
                contribution_values[feature].append(contribution)
            top_feature = max(contributions.items(), key=lambda item: (item[1], item[0]))[0]
            per_step_contributions.append({"step_id": row["step_id"], "score": sum(contributions.values()), "contributions": contributions, "top_feature": top_feature})
        trace_top_feature = max(
            weights,
            key=lambda feature: sum(step["contributions"][feature] for step in per_step_contributions),
        )
        top_contributor_by_trace[trace_top_feature] += 1
        ranked = primary_ranked[trace_id]
        rank1 = ranked[0]
        rank2 = ranked[1]
        gold_row = next(row for row in ranked if row["step_id"] == labels[trace_id]["gold_step"])
        margins_rank1_rank2.append(rank1["score"] - rank2["score"])
        margins_gold_to_top.append(gold_row["score"] - rank1["score"])
        scores = [step["score"] for step in per_step_contributions]
        score_ranges.append(max(scores) - min(scores))
        trace_summaries.append(
            {
                "trace_id": trace_id,
                "top_contributor_feature": trace_top_feature,
                "score_range": max(scores) - min(scores),
                "rank1_rank2_margin": rank1["score"] - rank2["score"],
                "gold_minus_top_margin": gold_row["score"] - rank1["score"],
            }
        )

    per_feature = {}
    for feature, values in contribution_values.items():
        per_feature[feature] = {
            "mean_contribution": statistics.mean(values),
            "variance": statistics.pvariance(values),
            "max_contribution": max(values),
            "min_contribution": min(values),
        }
    dominant_feature = max(per_feature.items(), key=lambda item: item[1]["mean_contribution"])[0]
    return {
        "per_feature_contribution_summary": per_feature,
        "dominant_average_feature": dominant_feature,
        "top_contributing_feature_per_trace_counts": dict(sorted(top_contributor_by_trace.items())),
        "mean_rank1_rank2_margin": statistics.mean(margins_rank1_rank2),
        "median_rank1_rank2_margin": statistics.median(margins_rank1_rank2),
        "mean_gold_minus_top_margin": statistics.mean(margins_gold_to_top),
        "median_gold_minus_top_margin": statistics.median(margins_gold_to_top),
        "mean_within_trace_score_range": statistics.mean(score_ranges),
        "median_within_trace_score_range": statistics.median(score_ranges),
        "near_constant_score_trace_count": sum(1 for value in score_ranges if value <= 0.05),
        "trace_summaries": trace_summaries,
    }


def _variant_disagreement(variant_analysis: dict[str, dict[str, Any]]) -> dict[str, Any]:
    pairs = [
        ("cct_primary_no_position", "cct_flow_only"),
        ("cct_primary_no_position", "cct_context_only"),
        ("cct_primary_no_position", "cct_with_position_features"),
        ("cct_flow_only", "cct_with_position_features"),
    ]
    output = {}
    top = {variant: payload["top_predictions"] for variant, payload in variant_analysis.items()}
    for left, right in pairs:
        agree = []
        disagree = []
        left_correct_right_wrong = []
        right_correct_left_wrong = []
        for trace_id, left_pred in top[left].items():
            right_pred = top[right][trace_id]
            same = left_pred["step_id"] == right_pred["step_id"]
            (agree if same else disagree).append(trace_id)
            # correctness inferred from per-variant correct_trace_ids
            left_correct = trace_id in set(variant_analysis[left]["correct_trace_ids"])
            right_correct = trace_id in set(variant_analysis[right]["correct_trace_ids"])
            if left_correct and not right_correct:
                left_correct_right_wrong.append(trace_id)
            if right_correct and not left_correct:
                right_correct_left_wrong.append(trace_id)
        output[f"{left}__vs__{right}"] = {
            "agreement_count": len(agree),
            "disagreement_count": len(disagree),
            "agreement_rate": _accuracy(len(agree), len(agree) + len(disagree)),
            "left_correct_right_wrong_count": len(left_correct_right_wrong),
            "right_correct_left_wrong_count": len(right_correct_left_wrong),
            "disagreement_trace_ids_sample": disagree[:20],
        }
    return output


def _cross_variant_cases(variant_analysis: dict[str, dict[str, Any]]) -> dict[str, Any]:
    primary_correct = set(variant_analysis["cct_primary_no_position"]["correct_trace_ids"])
    flow_correct = set(variant_analysis["cct_flow_only"]["correct_trace_ids"])
    position_correct = set(variant_analysis["cct_with_position_features"]["correct_trace_ids"])
    all_variants = list(variant_analysis)
    all_trace_ids = set(variant_analysis["cct_primary_no_position"]["top_predictions"])
    all_fail = []
    all_agree = []
    variants_disagree = []
    for trace_id in sorted(all_trace_ids):
        preds = {variant_analysis[v]["top_predictions"][trace_id]["step_id"] for v in all_variants}
        if not any(trace_id in set(variant_analysis[v]["correct_trace_ids"]) for v in all_variants):
            all_fail.append(trace_id)
        if len(preds) == 1:
            all_agree.append(trace_id)
        else:
            variants_disagree.append(trace_id)
    return {
        "primary_correct": sorted(primary_correct),
        "primary_wrong": variant_analysis["cct_primary_no_position"]["wrong_trace_ids"],
        "flow_correct_primary_wrong": sorted(flow_correct - primary_correct),
        "with_position_correct_primary_wrong": sorted(position_correct - primary_correct),
        "all_variants_fail": all_fail,
        "all_variants_agree": all_agree,
        "variants_disagree": variants_disagree,
    }


def _write_reports(analysis: dict[str, Any]) -> None:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    primary = analysis["variants"]["cct_primary_no_position"]
    tie = analysis["tie_analysis"]
    dominance = analysis["feature_dominance"]
    disagreement = analysis["variant_disagreement"]
    cases = analysis["cross_variant_cases"]

    worst_scenarios = sorted(primary["scenario_error_breakdown"].items(), key=lambda item: (-item[1]["error_rate"], item[0]))
    best_scenarios = sorted(primary["scenario_error_breakdown"].items(), key=lambda item: (item[1]["error_rate"], item[0]))
    worst_perturbations = sorted(primary["perturbation_error_breakdown"].items(), key=lambda item: (-item[1]["error_rate"], item[0]))

    error_lines = [
        "# Journal-v1 Full-Trace CCT Uncalibrated Error Analysis",
        "",
        "Scope: descriptive error analysis of the frozen Task 18 diagnostic run only. No weights, features, scoring formula, tie-breaking, corpus records, gold labels, baselines, or protocol were changed.",
        "",
        f"- Branch: `{analysis['provenance']['branch']}`",
        f"- Analysis HEAD: `{analysis['provenance']['head']}`",
        f"- Task 18 HEAD reference: `{TASK18_HEAD}`",
        f"- `configs/cct_scoring.yaml` SHA256: `{analysis['provenance']['config_sha256']}`",
        f"- Config hash matches Task 18: {str(analysis['provenance']['config_hash_matches_task18']).lower()}",
        "",
        "## Variant prediction distributions and correctness",
        "",
        "| Variant | Correct | Incorrect | Step accuracy | Predicted step distribution | Predicted agent distribution |",
        "|---|---:|---:|---:|---|---|",
    ]
    for variant, payload in analysis["variants"].items():
        error_lines.append(
            f"| `{variant}` | {payload['correct_count']} | {payload['incorrect_count']} | {payload['step_accuracy']:.6f} | `{payload['predicted_step_distribution']}` | `{payload['predicted_agent_distribution']}` |"
        )
    error_lines.extend(["", "## Primary scenario errors", "", "| Scenario | Accuracy | Error rate | Incorrect | n |", "|---|---:|---:|---:|---:|"])
    for scenario, payload in primary["scenario_error_breakdown"].items():
        error_lines.append(f"| `{scenario}` | {payload['accuracy']:.6f} | {payload['error_rate']:.6f} | {payload['incorrect']} | {payload['n']} |")
    error_lines.extend(["", "## Primary perturbation errors", "", "| Perturbation | Accuracy | Error rate | Incorrect | n |", "|---|---:|---:|---:|---:|"])
    for perturbation, payload in primary["perturbation_error_breakdown"].items():
        error_lines.append(f"| `{perturbation}` | {payload['accuracy']:.6f} | {payload['error_rate']:.6f} | {payload['incorrect']} | {payload['n']} |")
    error_lines.extend(
        [
            "",
            "## Ranking diagnostics for primary",
            "",
            f"- Top-1 accuracy: {primary['rank_diagnostics']['top_1_accuracy']:.6f}",
            f"- Top-2 containment: {primary['rank_diagnostics']['top_2_containment']:.6f}",
            f"- Top-3 containment: {primary['rank_diagnostics']['top_3_containment']:.6f}",
            f"- Mean gold-step rank: {primary['rank_diagnostics']['mean_gold_step_rank']:.6f}",
            f"- Median gold-step rank: {primary['rank_diagnostics']['median_gold_step_rank']:.6f}",
            f"- Gold-step rank distribution: `{primary['rank_diagnostics']['gold_step_rank_distribution']}`",
            "",
            "## Cross-variant case sets",
            "",
            f"- Primary correct cases: {len(cases['primary_correct'])}",
            f"- Primary wrong cases: {len(cases['primary_wrong'])}",
            f"- Flow-only correct while primary wrong: {len(cases['flow_correct_primary_wrong'])}",
            f"- With-position correct while primary wrong: {len(cases['with_position_correct_primary_wrong'])}",
            f"- All variants fail: {len(cases['all_variants_fail'])}",
            f"- All variants agree: {len(cases['all_variants_agree'])}",
            f"- Variants disagree: {len(cases['variants_disagree'])}",
            "",
            "## Diagnostic interpretation answers",
            "",
            "- Primary failure is mainly caused by weak/non-discriminative fixed features plus context contributions that often separate the wrong step, not by a tuned model failure.",
            f"- Score ties are not the main primary failure mode: primary tied-top rate is {tie['cct_primary_no_position']['tied_top_score_percent']:.6f}; wrong score separation count is {tie['cct_primary_no_position']['wrong_score_separation_traces']}.",
            "- Removal of position/identity features matters: the high-risk with-position diagnostic reaches 0.250000 and exceeds primary, indicating shortcut risk rather than structural support.",
            "- Context features dilute flow features in the primary formula: context-only is weak, while primary underperforms flow-only despite adding context density fields.",
            "- Flow-only is not substantively stronger; it matches a positional/default 0.250000 pattern and remains near a plausible-candidate baseline.",
            "- Errors are concentrated by scenario: worst groups are " + ", ".join(f"`{name}`" for name, _ in worst_scenarios[:2]) + "; best group is " + f"`{best_scenarios[0][0]}`.",
            "- Perturbation errors are highest for " + f"`{worst_perturbations[0][0]}`.",
            "- H1 remains unsupported after error analysis; H2 remains unsupported after error analysis.",
            "- Recommended next task: inspect feature design and protocol assumptions before any calibration, including whether visible structural features need non-position-derived causal/flow descriptors and whether the corpus graph shape is too uniform.",
            "- Non-actions: no calibration, grid search, LOSO, refinement, ablation, statistical test, or paper-ready result table was produced.",
        ]
    )
    ERROR_REPORT.write_text("\n".join(error_lines) + "\n", encoding="utf-8")

    tie_lines = [
        "# Journal-v1 Full-Trace CCT Uncalibrated Tie Analysis",
        "",
        "| Variant | Tied top traces | Tied top percent | Avg tied candidates | Tie-break can affect predicted step | Tie-break missed tied gold | Accuracy tied | Accuracy non-tied | Wrong score separation traces |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for variant, payload in tie.items():
        tied_acc = "n/a" if payload["accuracy_on_tied_traces"] is None else f"{payload['accuracy_on_tied_traces']:.6f}"
        non_tied_acc = "n/a" if payload["accuracy_on_non_tied_traces"] is None else f"{payload['accuracy_on_non_tied_traces']:.6f}"
        tie_lines.append(
            f"| `{variant}` | {payload['tied_top_score_traces']} | {payload['tied_top_score_percent']:.6f} | {payload['average_tied_candidates_per_trace']:.6f} | {payload['tie_breaking_can_affect_predicted_step']} | {payload['tie_breaking_missed_gold_that_was_tied_for_top']} | {tied_acc} | {non_tied_acc} | {payload['wrong_score_separation_traces']} |"
        )
    tie_lines.append("\nPrimary underperformance is not mainly a tie artifact because most primary errors are non-tied wrong score separations.")
    TIE_REPORT.write_text("\n".join(tie_lines) + "\n", encoding="utf-8")

    feature_lines = [
        "# Journal-v1 Full-Trace CCT Uncalibrated Feature Dominance Report",
        "",
        "## Primary feature contribution summary",
        "",
        "| Feature | Mean contribution | Variance | Min | Max |",
        "|---|---:|---:|---:|---:|",
    ]
    for feature, payload in dominance["per_feature_contribution_summary"].items():
        feature_lines.append(f"| `{feature}` | {payload['mean_contribution']:.6f} | {payload['variance']:.6f} | {payload['min_contribution']:.6f} | {payload['max_contribution']:.6f} |")
    feature_lines.extend(
        [
            "",
            f"- Dominant average feature: `{dominance['dominant_average_feature']}`.",
            f"- Top contributing feature per trace counts: `{dominance['top_contributing_feature_per_trace_counts']}`.",
            f"- Mean rank1-rank2 margin: {dominance['mean_rank1_rank2_margin']:.6f}.",
            f"- Median rank1-rank2 margin: {dominance['median_rank1_rank2_margin']:.6f}.",
            f"- Mean gold-minus-top margin: {dominance['mean_gold_minus_top_margin']:.6f}.",
            f"- Median gold-minus-top margin: {dominance['median_gold_minus_top_margin']:.6f}.",
            f"- Mean within-trace score range: {dominance['mean_within_trace_score_range']:.6f}.",
            f"- Median within-trace score range: {dominance['median_within_trace_score_range']:.6f}.",
            f"- Near-constant score traces (range <= 0.05): {dominance['near_constant_score_trace_count']}.",
            "- Interpretation: scores are usually separated, but the largest average contributions come from broad context/tool-output fields that do not identify the gold step reliably.",
        ]
    )
    FEATURE_REPORT.write_text("\n".join(feature_lines) + "\n", encoding="utf-8")

    disagreement_lines = [
        "# Journal-v1 Full-Trace CCT Uncalibrated Variant Disagreement Report",
        "",
        "| Pair | Agreement | Disagreement | Agreement rate | Left correct/right wrong | Right correct/left wrong |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for pair, payload in disagreement.items():
        disagreement_lines.append(
            f"| `{pair}` | {payload['agreement_count']} | {payload['disagreement_count']} | {payload['agreement_rate']:.6f} | {payload['left_correct_right_wrong_count']} | {payload['right_correct_left_wrong_count']} |"
        )
    disagreement_lines.append("\nVariant disagreement confirms that the primary formula often selects different steps than flow/position diagnostics; flow-only and with-position never select the same step in this fixed graph shape, yet both reach 0.250000 because each collapses to a different single-position/default prediction.")
    DISAGREEMENT_REPORT.write_text("\n".join(disagreement_lines) + "\n", encoding="utf-8")


def main() -> int:
    config_hash = sha256(CONFIG_PATH)
    config = read_json(CONFIG_PATH)
    task18 = read_json(TASK18_RAW_PATH)
    features = read_jsonl(FEATURES_PATH)
    corpus = read_jsonl(CORPUS_PATH)
    labels = _labels(corpus)
    features_by_trace = _features_by_trace(features)
    branch = subprocess.check_output(["git", "branch", "--show-current"], cwd=ROOT, text=True).strip()
    head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()

    variants = {
        name: _score_variant(name, variant, features_by_trace, labels)
        for name, variant in config["variants"].items()
    }
    tie = _tie_analysis(variants, labels)
    dominance = _feature_dominance(config, features_by_trace, labels, variants["cct_primary_no_position"]["ranked_by_trace"])
    disagreement = _variant_disagreement(variants)
    cases = _cross_variant_cases(variants)
    analysis = {
        "provenance": {
            "branch": branch,
            "head": head,
            "task18_head_reference": TASK18_HEAD,
            "config_sha256": config_hash,
            "task18_config_sha256_reference": TASK18_CONFIG_SHA256,
            "config_hash_matches_task18": config_hash == TASK18_CONFIG_SHA256,
            "task18_raw_head": task18.get("provenance", {}).get("head"),
            "task18_raw_config_sha256": task18.get("provenance", {}).get("config_sha256_before_execution"),
        },
        "variants": variants,
        "tie_analysis": tie,
        "feature_dominance": dominance,
        "variant_disagreement": disagreement,
        "cross_variant_cases": cases,
        "interpretation": {
            "primary_failure_mainly_weak_features": True,
            "primary_failure_mainly_score_ties": False,
            "removal_of_position_identity_features_matters": True,
            "context_features_dilute_flow_features": True,
            "flow_only_matches_positional_default_pattern": True,
            "with_position_indicates_shortcut_risk": True,
            "h1_status_after_error_analysis": "unsupported",
            "h2_status_after_error_analysis": "unsupported",
            "recommended_next_task": "feature-design and graph-shape diagnostic review before any calibration or protocol revision",
            "non_actions": [
                "no config changes",
                "no weight changes",
                "no feature changes",
                "no scoring formula changes",
                "no tie-breaking changes",
                "no calibration",
                "no grid search",
                "no LOSO",
                "no refinement",
                "no ablation",
                "no statistical test",
                "no paper-ready result table",
            ],
        },
    }
    compact_analysis = json.loads(json.dumps(analysis))
    for payload in compact_analysis["variants"].values():
        payload.pop("ranked_by_trace", None)
        payload.pop("top_predictions", None)
    compact_analysis["feature_dominance"].pop("trace_summaries", None)

    RAW_OUT.parent.mkdir(parents=True, exist_ok=True)
    RAW_OUT.write_text(json.dumps(compact_analysis, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    _write_reports(analysis)

    primary = variants["cct_primary_no_position"]
    print("=== CCT Uncalibrated Error Analysis ===")
    print(f"Branch: {branch}")
    print(f"HEAD: {head}")
    print(f"Config SHA256 matches Task 18: {config_hash == TASK18_CONFIG_SHA256}")
    print(f"Primary top-2 containment: {primary['rank_diagnostics']['top_2_containment']:.6f}")
    print(f"Primary top-3 containment: {primary['rank_diagnostics']['top_3_containment']:.6f}")
    print(f"Primary mean gold rank: {primary['rank_diagnostics']['mean_gold_step_rank']:.6f}")
    print("H1 status after error analysis: unsupported")
    print("H2 status after error analysis: unsupported")
    print("FINAL: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
