#!/usr/bin/env python3
"""Run the final minimal deterministic CCT rescue evaluation.

This script performs the Task 30 fixed-formula evaluation only. It does not
learn weights, tune thresholds, calibrate, grid search, run LOSO, ablate, modify
corpus/gold labels, restore scoring config, or produce paper-ready claims.
"""

from __future__ import annotations

import json
import random
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Callable

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from cctdiag.io.full_trace_views import make_full_trace_prediction_view  # noqa: E402

CORPUS_PATH = ROOT / "data/processed/journal_v1_full_trace/main_full_trace_all.jsonl"
FEATURE_PATH = ROOT / "results/raw/journal_v1_rescue/rescue_candidate_step_features.json"
PREDICTION_PATH = ROOT / "results/raw/journal_v1_rescue/final_rescue_predictions.json"
REPORT_DIR = ROOT / "results/reports/journal_v1_rescue"
AMENDMENT_REPORT = REPORT_DIR / "rescue_protocol_amendment_for_intratrace_ranking.md"
EVALUATION_REPORT = REPORT_DIR / "final_rescue_evaluation_report.md"
ERROR_REPORT = REPORT_DIR / "final_rescue_error_analysis.md"
DECISION_REPORT = REPORT_DIR / "final_rescue_hypothesis_decision.md"
SEED = 20260605
STEP_IDS = ["s1", "s2", "s3", "s4", "s5"]
CCT_VARIANTS = [
    "cct_candidate_step_structural_sum",
    "cct_candidate_step_flow_only",
    "cct_candidate_step_tool_alignment_only",
    "cct_candidate_step_cross_agent_only",
    "cct_candidate_step_visible_relation_overlap",
]
BASELINES = [
    "majority_step",
    "always_s2",
    "random_step_seeded",
    "first_step",
    "last_step",
    "flat_log_lexical_baseline",
    "non_cct_visible_heuristic_baseline",
]
ALL_METHODS = BASELINES + CCT_VARIANTS


def load_records() -> list[dict[str, Any]]:
    return [json.loads(line) for line in CORPUS_PATH.read_text().splitlines() if line.strip()]


def load_features_by_trace() -> dict[str, list[dict[str, Any]]]:
    rows = json.loads(FEATURE_PATH.read_text())
    by_trace: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        by_trace[str(row["trace_id"])].append(row)
    for trace_rows in by_trace.values():
        trace_rows.sort(key=lambda row: STEP_IDS.index(row["candidate_step_id"]))
    return dict(by_trace)


def step_text(step: dict[str, Any]) -> str:
    fields = ["input_message", "output_message", "tool_call", "tool_output", "visible_step_notes"]
    return " ".join(str(step.get(field) or "") for field in fields).lower()


def choose_by_score(scores: dict[str, float]) -> tuple[str, list[str]]:
    ordered = sorted(scores, key=lambda step_id: (-scores[step_id], STEP_IDS.index(step_id)))
    return ordered[0], ordered[:2]


def cct_scores(rows: list[dict[str, Any]], variant: str) -> dict[str, float]:
    scores: dict[str, float] = {}
    for row in rows:
        step_id = row["candidate_step_id"]
        if variant == "cct_candidate_step_structural_sum":
            value = (
                row["incoming_strong_edge_count"]
                + row["outgoing_strong_edge_count"]
                + row["non_adjacent_dependency_involvement_count"]
                + row["relation_type_diversity_count"]
                + row["visible_tool_output_alignment_indicator"]
                + row["visible_dependency_carryover_indicator"]
            )
        elif variant == "cct_candidate_step_flow_only":
            value = (
                row["incoming_strong_edge_count"]
                + row["outgoing_strong_edge_count"]
                + row["non_adjacent_dependency_involvement_count"]
                + row["relation_type_diversity_count"]
            )
        elif variant == "cct_candidate_step_tool_alignment_only":
            value = (
                row["tool_alignment_incoming_count"]
                + row["tool_alignment_outgoing_count"]
                + row["visible_tool_output_alignment_indicator"]
            )
        elif variant == "cct_candidate_step_cross_agent_only":
            value = row["cross_agent_dependency_incoming_count"] + row["cross_agent_dependency_outgoing_count"]
        elif variant == "cct_candidate_step_visible_relation_overlap":
            value = (
                row["downstream_dependency_incoming_count"]
                + row["downstream_dependency_outgoing_count"]
                + row["visible_dependency_carryover_indicator"]
                + row["relation_type_diversity_count"]
            )
        else:
            raise ValueError(f"unknown CCT variant: {variant}")
        scores[step_id] = float(value)
    return scores


def flat_log_lexical_scores(prediction_view: dict[str, Any]) -> dict[str, float]:
    keywords = {
        "failure": 3,
        "risk": 2,
        "missing": 2,
        "conflict": 2,
        "ambiguous": 2,
        "required": 1,
        "constraint": 1,
        "handoff": 1,
        "tool": 1,
        "evidence": 1,
        "irreversible": 2,
        "recover": 1,
        "alternate": 1,
    }
    scores: dict[str, float] = {}
    for step in prediction_view["steps"]:
        text = step_text(step)
        scores[step["step_id"]] = float(sum(weight for term, weight in keywords.items() if term in text))
    return scores


def non_cct_visible_heuristic_scores(prediction_view: dict[str, Any]) -> dict[str, float]:
    scores: dict[str, float] = {}
    for step in prediction_view["steps"]:
        score = 0.0
        if step.get("tool_output"):
            score += 1.0
        if step.get("handoff_from"):
            score += 0.5
        if step.get("handoff_to"):
            score += 0.5
        text = step_text(step)
        if "required" in text or "constraint" in text:
            score += 1.0
        if "alternate" in text or "conflict" in text:
            score += 1.0
        scores[step["step_id"]] = score
    return scores


def generate_predictions(records: list[dict[str, Any]], features_by_trace: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    rng = random.Random(SEED)
    predictions: list[dict[str, Any]] = []
    for record in records:
        prediction_view = make_full_trace_prediction_view(record)
        trace_id = str(prediction_view["trace_id"])
        candidate_steps = list(prediction_view["candidate_steps"])
        feature_rows = features_by_trace[trace_id]
        method_predictions: dict[str, dict[str, Any]] = {}

        fixed = {
            "majority_step": "s2",
            "always_s2": "s2",
            "first_step": candidate_steps[0],
            "last_step": candidate_steps[-1],
            "random_step_seeded": rng.choice(candidate_steps),
        }
        for method, step_id in fixed.items():
            method_predictions[method] = {"predicted_step": step_id, "top2_steps": [step_id]}

        for method, score_fn in {
            "flat_log_lexical_baseline": flat_log_lexical_scores,
            "non_cct_visible_heuristic_baseline": non_cct_visible_heuristic_scores,
        }.items():
            predicted, top2 = choose_by_score(score_fn(prediction_view))
            method_predictions[method] = {"predicted_step": predicted, "top2_steps": top2}

        for variant in CCT_VARIANTS:
            predicted, top2 = choose_by_score(cct_scores(feature_rows, variant))
            method_predictions[variant] = {"predicted_step": predicted, "top2_steps": top2}

        predictions.append({"trace_id": trace_id, "predictions": method_predictions})
    return predictions


def evaluate(records: list[dict[str, Any]], predictions: list[dict[str, Any]]) -> dict[str, Any]:
    labels_by_trace = {
        str(record["trace_id"]): {
            "gold_step": record["private_labels"]["gold_failure_step"],
            "scenario_group": record["scenario_group"],
            "perturbation_type": record["perturbation_type"],
        }
        for record in records
    }
    totals = {method: Counter() for method in ALL_METHODS}
    scenario = {method: defaultdict(Counter) for method in ALL_METHODS}
    perturbation = {method: defaultdict(Counter) for method in ALL_METHODS}
    clean_perturbed = {method: defaultdict(Counter) for method in ALL_METHODS}
    confusion = {method: {gold: Counter() for gold in STEP_IDS} for method in ALL_METHODS}
    predicted_steps = {method: Counter() for method in ALL_METHODS}
    errors = {method: [] for method in ALL_METHODS}

    for item in predictions:
        trace_id = item["trace_id"]
        meta = labels_by_trace[trace_id]
        gold = meta["gold_step"]
        clean_key = "clean" if meta["perturbation_type"] == "none" else "perturbed"
        for method, prediction in item["predictions"].items():
            pred = prediction["predicted_step"]
            top2 = set(prediction.get("top2_steps") or [])
            correct = pred == gold
            totals[method]["n"] += 1
            totals[method]["correct"] += int(correct)
            totals[method]["top2"] += int(gold in top2)
            scenario[method][meta["scenario_group"]]["n"] += 1
            scenario[method][meta["scenario_group"]]["correct"] += int(correct)
            perturbation[method][meta["perturbation_type"]]["n"] += 1
            perturbation[method][meta["perturbation_type"]]["correct"] += int(correct)
            clean_perturbed[method][clean_key]["n"] += 1
            clean_perturbed[method][clean_key]["correct"] += int(correct)
            confusion[method][gold][pred] += 1
            predicted_steps[method][pred] += 1
            if not correct and len(errors[method]) < 5:
                errors[method].append({"trace_id": trace_id, "gold_step": gold, "predicted_step": pred})

    results: dict[str, Any] = {}
    for method in ALL_METHODS:
        n = totals[method]["n"]
        acc = totals[method]["correct"] / n if n else 0.0
        top2 = totals[method]["top2"] / n if n else 0.0
        scenario_acc = _group_accuracy(scenario[method])
        perturbation_acc = _group_accuracy(perturbation[method])
        cp_acc = _group_accuracy(clean_perturbed[method])
        macro_scenario = sum(scenario_acc.values()) / len(scenario_acc) if scenario_acc else 0.0
        macro_perturbation = sum(perturbation_acc.values()) / len(perturbation_acc) if perturbation_acc else 0.0
        results[method] = {
            "accuracy": acc,
            "top2_containment": top2,
            "macro_scenario_accuracy": macro_scenario,
            "macro_perturbation_accuracy": macro_perturbation,
            "scenario_accuracy": scenario_acc,
            "perturbation_accuracy": perturbation_acc,
            "clean_vs_perturbed_accuracy": cp_acc,
            "confusion_matrix": {gold: dict(confusion[method][gold]) for gold in STEP_IDS},
            "predicted_step_counts": dict(predicted_steps[method]),
            "sample_errors": errors[method],
        }
    return results


def _group_accuracy(groups: dict[str, Counter]) -> dict[str, float]:
    return {key: counts["correct"] / counts["n"] for key, counts in sorted(groups.items()) if counts["n"]}


def pct(value: float) -> str:
    return f"{value:.2%}"


def write_reports(predictions: list[dict[str, Any]], results: dict[str, Any]) -> None:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    PREDICTION_PATH.parent.mkdir(parents=True, exist_ok=True)
    PREDICTION_PATH.write_text("[\n" + ",\n".join(json.dumps(item, sort_keys=True) for item in predictions) + "\n]\n")

    best_cct = max(CCT_VARIANTS, key=lambda m: (results[m]["accuracy"], results[m]["macro_scenario_accuracy"], -CCT_VARIANTS.index(m)))
    trivial_order = ["majority_step", "always_s2", "random_step_seeded", "first_step", "last_step"]
    strongest_trivial = max(trivial_order, key=lambda m: (results[m]["accuracy"], -trivial_order.index(m)))
    non_cct_order = [strongest_trivial, "flat_log_lexical_baseline", "non_cct_visible_heuristic_baseline"]
    strongest_non_cct = max(non_cct_order, key=lambda m: (results[m]["accuracy"], -non_cct_order.index(m)))
    h1_margin = results[best_cct]["accuracy"] - results[strongest_non_cct]["accuracy"]
    h2_order = ["flat_log_lexical_baseline", "non_cct_visible_heuristic_baseline"]
    h2_reference = max(h2_order, key=lambda m: (results[m]["accuracy"], -h2_order.index(m)))
    h2_margin = results[best_cct]["accuracy"] - results[h2_reference]["accuracy"]
    h1_supported = h1_margin >= 0.10
    h2_supported = h2_margin >= 0.10

    AMENDMENT_REPORT.write_text(_amendment_text())
    EVALUATION_REPORT.write_text(_evaluation_text(results, best_cct, strongest_trivial, strongest_non_cct, h2_reference))
    ERROR_REPORT.write_text(_error_text(results, best_cct))
    DECISION_REPORT.write_text(_decision_text(best_cct, strongest_non_cct, h2_reference, h1_margin, h2_margin, h1_supported, h2_supported))


def _amendment_text() -> str:
    return """# Rescue Protocol Amendment for Intratrace Ranking

## Scope
- This amendment authorizes one final minimal deterministic rescue evaluation only.
- It does not authorize calibration, weight tuning, grid search, LOSO, ablation, corpus/gold-label changes, scoring-config restoration, or paper-ready performance claims.

## Rationale
- Global candidate-step feature-vector duplication remains a severe limitation: Task 29 reported 99.19% duplicate candidate-step feature vectors.
- Task 29 also reported within-trace duplicate candidate-step rows = 0, meaning each trace's five candidate steps are distinguishable by the current feature representation.
- Because failure-step attribution is an intra-trace selection problem, this amendment permits one high-risk fixed-formula intra-trace evaluation despite global degeneracy.

## Boundary
- Predictions must be generated before private labels are read for evaluation.
- Scenario and perturbation metadata may be used only after prediction for stratified reporting.
- If CCT does not exceed the strongest baseline by the pre-specified margin, H1-R/H2-R are closed as unsupported and the rescue path stops.
"""


def _evaluation_text(results: dict[str, Any], best_cct: str, strongest_trivial: str, strongest_non_cct: str, h2_reference: str) -> str:
    lines = [
        "# Final Rescue Evaluation Report",
        "",
        "## Scope",
        "- Final minimal deterministic rescue evaluation under `configs/rescue_experiment_v1.yaml`.",
        "- No tuning, calibration, grid search, LOSO, ablation, corpus/gold-label change, or paper-ready performance claim is performed.",
        "- `flat_log_text_similarity_baseline` is omitted because the prediction view does not expose terminal outcome text; adding it would require a new input contract.",
        "",
        "## Method accuracy summary",
        "| method | family | step accuracy | macro scenario accuracy | macro perturbation accuracy | top-2 containment |",
        "|---|---|---:|---:|---:|---:|",
    ]
    for method in ALL_METHODS:
        family = "CCT" if method in CCT_VARIANTS else "baseline"
        res = results[method]
        lines.append(
            f"| {method} | {family} | {pct(res['accuracy'])} | {pct(res['macro_scenario_accuracy'])} | {pct(res['macro_perturbation_accuracy'])} | {pct(res['top2_containment'])} |"
        )
    lines.extend([
        "",
        "## Strongest references",
        f"- Best CCT variant: `{best_cct}` with step accuracy {pct(results[best_cct]['accuracy'])}.",
        f"- Strongest trivial baseline: `{strongest_trivial}` with step accuracy {pct(results[strongest_trivial]['accuracy'])}.",
        f"- Strongest non-CCT baseline overall: `{strongest_non_cct}` with step accuracy {pct(results[strongest_non_cct]['accuracy'])}.",
        f"- H2 flat/non-CCT reference: `{h2_reference}` with step accuracy {pct(results[h2_reference]['accuracy'])}.",
        "",
        "## Clean vs perturbed accuracy",
    ])
    for method in ALL_METHODS:
        cp = results[method]["clean_vs_perturbed_accuracy"]
        lines.append(f"- {method}: clean={pct(cp.get('clean', 0.0))}; perturbed={pct(cp.get('perturbed', 0.0))}")
    lines.extend(["", "## Confusion matrices over s1-s5"])
    for method in ALL_METHODS:
        lines.append(f"### {method}")
        for gold in STEP_IDS:
            row = results[method]["confusion_matrix"][gold]
            compact = ", ".join(f"{pred}:{row.get(pred, 0)}" for pred in STEP_IDS)
            lines.append(f"- gold {gold}: {compact}")
    return "\n".join(lines) + "\n"


def _error_text(results: dict[str, Any], best_cct: str) -> str:
    res = results[best_cct]
    scenario_items = sorted(res["scenario_accuracy"].items(), key=lambda item: item[1])
    perturb_items = sorted(res["perturbation_accuracy"].items(), key=lambda item: item[1])
    most_common_pred = Counter(res["predicted_step_counts"]).most_common(1)[0]
    lines = [
        "# Final Rescue Error Analysis",
        "",
        f"- Best evaluated CCT variant: `{best_cct}`",
        f"- Most common predicted step: {most_common_pred[0]} ({most_common_pred[1]} traces)",
        f"- Prediction collapse to one position: {'yes' if most_common_pred[1] > 0.80 * 420 else 'no'}",
        f"- Behaves like first/last/majority baseline: {'yes' if most_common_pred[1] > 0.80 * 420 else 'partial/no'}",
        "",
        "## Best scenario groups",
    ]
    for key, value in reversed(scenario_items[-3:]):
        lines.append(f"- {key}: {pct(value)}")
    lines.append("")
    lines.append("## Worst scenario groups")
    for key, value in scenario_items[:3]:
        lines.append(f"- {key}: {pct(value)}")
    lines.append("")
    lines.append("## Perturbation accuracy")
    for key, value in perturb_items:
        lines.append(f"- {key}: {pct(value)}")
    lines.append("")
    lines.append("## Example failure modes")
    if res["sample_errors"]:
        for error in res["sample_errors"]:
            lines.append(f"- trace `{error['trace_id']}`: predicted {error['predicted_step']} but gold step was {error['gold_step']} (reported after prediction freeze).")
    else:
        lines.append("- none recorded")
    return "\n".join(lines) + "\n"


def _decision_text(best_cct: str, strongest_non_cct: str, h2_reference: str, h1_margin: float, h2_margin: float, h1_supported: bool, h2_supported: bool) -> str:
    continue_rescue = h1_supported and h2_supported
    return f"""# Final Rescue Hypothesis Decision

## Decisions
- H1-R: {'preliminary_supported' if h1_supported else 'unsupported'}
- H2-R: {'preliminary_supported' if h2_supported else 'unsupported'}
- Rescue path continues: {'yes; only to future robustness/statistical validation, not immediate paper claim' if continue_rescue else 'no; return to Path B negative-evidence framing'}

## Basis
- Best CCT variant: `{best_cct}`.
- Strongest non-CCT baseline for H1-R: `{strongest_non_cct}`.
- H2-R flat/non-CCT reference: `{h2_reference}`.
- H1-R margin over strongest non-CCT baseline: {h1_margin:.3f}.
- H2-R margin over flat/non-CCT reference: {h2_margin:.3f}.
- Required margin: 0.100.

## Interpretation
{'The CCT rescue variant cleared the pre-specified margin. This is preliminary support only and would require a future robustness/statistical validation task before any paper claim.' if continue_rescue else 'The CCT rescue variant did not clear the pre-specified margin. H1-R/H2-R remain unsupported, and the rescue path stops under the current feature representation.'}

## Non-action confirmation
- No tuning, calibration, grid search, LOSO, ablation, corpus/gold-label change, scoring-config restoration, or paper-ready performance claim was performed.
"""


def main() -> None:
    records = load_records()
    features_by_trace = load_features_by_trace()
    predictions = generate_predictions(records, features_by_trace)
    # Private labels are read only inside evaluate(), after predictions exist.
    results = evaluate(records, predictions)
    write_reports(predictions, results)
    best_cct = max(CCT_VARIANTS, key=lambda m: (results[m]["accuracy"], results[m]["macro_scenario_accuracy"], -CCT_VARIANTS.index(m)))
    strongest_non_cct = max(BASELINES, key=lambda m: (results[m]["accuracy"], -BASELINES.index(m)))
    print(
        "final_rescue_evaluation "
        f"best_cct={best_cct} acc={results[best_cct]['accuracy']:.3f} "
        f"strongest_baseline={strongest_non_cct} baseline_acc={results[strongest_non_cct]['accuracy']:.3f}"
    )


if __name__ == "__main__":
    main()
