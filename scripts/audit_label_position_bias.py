#!/usr/bin/env python3
"""Audit Journal-v1 corpus label-position and trivial-shortcut risk.

This script is intentionally diagnostic only: it does not implement evaluation
metrics, baseline models, CCT scoring, calibration, or result tables.
"""

import json
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CORPUS = ROOT / "data/processed/journal_v1/main_all_traces.jsonl"
REPORT_DIR = ROOT / "results/reports/journal_v1"
LABEL_REPORT = REPORT_DIR / "main_label_position_bias_report.md"
BASELINE_REPORT = REPORT_DIR / "main_trivial_baseline_risk_report.md"
CORRECTION_PLAN = REPORT_DIR / "main_label_position_bias_correction_plan.md"

STEP_DOMINANCE_THRESHOLD = 0.50
TRIVIAL_RISK_BLOCK_THRESHOLD = 0.50


def load_rows(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def pct(count: int, total: int) -> float:
    return (count / total * 100.0) if total else 0.0


def md_table(counter: Counter, total: int, key_name: str) -> list[str]:
    lines = [f"| {key_name} | count | percentage |", "|---|---:|---:|"]
    for key, count in counter.most_common():
        lines.append(f"| {key} | {count} | {pct(count, total):.2f}% |")
    return lines


def nested_md_table(rows: list[dict], row_key: str, value_key: str, value_name: str) -> list[str]:
    grouped: dict[str, Counter] = defaultdict(Counter)
    totals: Counter = Counter()
    for row in rows:
        group = str(row.get(row_key))
        value = str(row.get(value_key))
        grouped[group][value] += 1
        totals[group] += 1

    lines = [f"| {row_key} | {value_name} | count | within-group percentage |", "|---|---|---:|---:|"]
    for group in sorted(grouped):
        for value, count in grouped[group].most_common():
            lines.append(f"| {group} | {value} | {count} | {pct(count, totals[group]):.2f}% |")
    return lines


def expected_accuracy(rows: list[dict], predictor) -> tuple[int, float]:
    correct = 0
    computable = 0
    for row in rows:
        prediction = predictor(row)
        if prediction is None:
            continue
        computable += 1
        if prediction == row.get("gold_failure_agent") or prediction == row.get("gold_failure_step"):
            correct += 1
    return correct, (correct / computable if computable else 0.0)


def main() -> int:
    rows = load_rows(CORPUS)
    total = len(rows)
    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    step_counts = Counter(str(row.get("gold_failure_step")) for row in rows)
    agent_counts = Counter(str(row.get("gold_failure_agent")) for row in rows)
    top_step, top_step_count = step_counts.most_common(1)[0]
    top_agent, top_agent_count = agent_counts.most_common(1)[0]

    majority_step_accuracy = top_step_count / total if total else 0.0
    majority_agent_accuracy = top_agent_count / total if total else 0.0
    always_s2_count = sum(1 for row in rows if row.get("gold_failure_step") == "s2")
    always_s2_accuracy = always_s2_count / total if total else 0.0
    most_common_agent_accuracy = majority_agent_accuracy

    first_active_correct = 0
    first_active_computable = 0
    for row in rows:
        catalog = row.get("agent_catalog") or []
        if catalog:
            first_active_computable += 1
            if catalog[0] == row.get("gold_failure_agent"):
                first_active_correct += 1
    first_active_accuracy = first_active_correct / first_active_computable if first_active_computable else None

    step_dominates = majority_step_accuracy > STEP_DOMINANCE_THRESHOLD
    trivial_risks = {
        "majority_step": majority_step_accuracy,
        "majority_agent": majority_agent_accuracy,
        "always_s2": always_s2_accuracy,
        "first_active_agent": first_active_accuracy,
        "most_common_agent": most_common_agent_accuracy,
    }
    high_trivial_risks = {
        name: value for name, value in trivial_risks.items()
        if value is not None and value > TRIVIAL_RISK_BLOCK_THRESHOLD
    }
    evaluation_blocked = bool(step_dominates or high_trivial_risks)

    label_lines = [
        "# Journal-v1 Main Label-Position Bias Report",
        "",
        "## Scope",
        "- Corpus: `data/processed/journal_v1/main_all_traces.jsonl`.",
        f"- Total traces audited: {total}.",
        "- Diagnostic status: corpus-risk audit only; no evaluation metrics, baseline implementations, CCT scoring, calibration, or result tables were added.",
        "",
        "## Acceptance thresholds",
        f"- No single `gold_failure_step` should exceed {STEP_DOMINANCE_THRESHOLD:.0%} of all traces unless explicitly justified.",
        "- No single `gold_failure_agent` should dominate unless scenario-specific and documented.",
        "- Semantic spot-check coverage must include positive and negative H6 examples and at least 3 different `gold_failure_step` values if available.",
        f"- If any trivial shortcut diagnostic exceeds {TRIVIAL_RISK_BLOCK_THRESHOLD:.0%}, evaluation remains blocked pending corpus revision or explicit justification.",
        "",
        "## Overall `gold_failure_step` distribution",
        *md_table(step_counts, total, "gold_failure_step"),
        "",
        "## Overall `gold_failure_agent` distribution",
        *md_table(agent_counts, total, "gold_failure_agent"),
        "",
        "## `gold_failure_step` by `scenario_group`",
        *nested_md_table(rows, "scenario_group", "gold_failure_step", "gold_failure_step"),
        "",
        "## `gold_failure_step` by `perturbation_type`",
        *nested_md_table(rows, "perturbation_type", "gold_failure_step", "gold_failure_step"),
        "",
        "## `gold_failure_agent` by `scenario_group`",
        *nested_md_table(rows, "scenario_group", "gold_failure_agent", "gold_failure_agent"),
        "",
        "## `gold_failure_agent` by `perturbation_type`",
        *nested_md_table(rows, "perturbation_type", "gold_failure_agent", "gold_failure_agent"),
        "",
        "## Bias finding",
        f"- Top `gold_failure_step`: `{top_step}` = {top_step_count}/{total} ({pct(top_step_count, total):.2f}%).",
        f"- Top `gold_failure_agent`: `{top_agent}` = {top_agent_count}/{total} ({pct(top_agent_count, total):.2f}%).",
        f"- Label-position bias detected: {'yes' if step_dominates else 'no'}.",
        f"- Evaluation blocked: {'yes' if evaluation_blocked else 'no'}.",
    ]
    if step_dominates:
        label_lines.append(f"- Blocking reason: `{top_step}` exceeds the {STEP_DOMINANCE_THRESHOLD:.0%} step-dominance threshold.")
    LABEL_REPORT.write_text("\n".join(label_lines) + "\n", encoding="utf-8")

    baseline_lines = [
        "# Journal-v1 Main Trivial-Baseline Risk Report",
        "",
        "## Scope and guardrails",
        "- These values are corpus-risk diagnostics only, not method results.",
        "- No evaluation metric, baseline implementation, CCT scoring, calibration, or result table is introduced by this report.",
        "",
        "## Diagnostic shortcut estimates",
        "| diagnostic shortcut | expected accuracy | numerator / denominator | status |",
        "|---|---:|---:|---|",
        f"| majority_step (`{top_step}`) | {majority_step_accuracy:.4f} ({majority_step_accuracy*100:.2f}%) | {top_step_count}/{total} | {'BLOCKS evaluation' if majority_step_accuracy > TRIVIAL_RISK_BLOCK_THRESHOLD else 'below block threshold'} |",
        f"| majority_agent (`{top_agent}`) | {majority_agent_accuracy:.4f} ({majority_agent_accuracy*100:.2f}%) | {top_agent_count}/{total} | {'BLOCKS evaluation' if majority_agent_accuracy > TRIVIAL_RISK_BLOCK_THRESHOLD else 'below block threshold'} |",
        f"| always_s2 | {always_s2_accuracy:.4f} ({always_s2_accuracy*100:.2f}%) | {always_s2_count}/{total} | {'BLOCKS evaluation' if always_s2_accuracy > TRIVIAL_RISK_BLOCK_THRESHOLD else 'below block threshold'} |",
        (
            f"| first_active_agent | {first_active_accuracy:.4f} ({first_active_accuracy*100:.2f}%) | {first_active_correct}/{first_active_computable} | "
            f"{'BLOCKS evaluation' if first_active_accuracy and first_active_accuracy > TRIVIAL_RISK_BLOCK_THRESHOLD else 'below block threshold'} |"
            if first_active_accuracy is not None else
            "| first_active_agent | not computable | 0/0 | unavailable |"
        ),
        f"| most_common_agent (`{top_agent}`) | {most_common_agent_accuracy:.4f} ({most_common_agent_accuracy*100:.2f}%) | {top_agent_count}/{total} | {'BLOCKS evaluation' if most_common_agent_accuracy > TRIVIAL_RISK_BLOCK_THRESHOLD else 'below block threshold'} |",
        "",
        "## Evaluation gate",
        f"- Evaluation blocked: {'yes' if evaluation_blocked else 'no'}.",
    ]
    if high_trivial_risks:
        baseline_lines.append("- Blocking trivial-risk diagnostics: " + ", ".join(f"{k}={v*100:.2f}%" for k, v in high_trivial_risks.items()) + ".")
    else:
        baseline_lines.append("- No trivial-risk diagnostic exceeded the 50% block threshold.")
    BASELINE_REPORT.write_text("\n".join(baseline_lines) + "\n", encoding="utf-8")

    if evaluation_blocked:
        plan_lines = [
            "# Journal-v1 Main Label-Position Bias Correction Plan",
            "",
            "## Status",
            "- Evaluation remains blocked.",
            f"- Exact blocking reason: `gold_failure_step={top_step}` appears in {top_step_count}/{total} traces ({pct(top_step_count, total):.2f}%), causing `majority_step` and `always_s2` shortcut diagnostics to exceed 50%.",
            "",
            "## Non-action taken in this task",
            "- The corpus was not silently edited.",
            "- Gold labels were not changed.",
            "- No metrics, baselines, CCT scoring, calibration, or result tables were implemented.",
            "",
            "## Required before evaluation can proceed",
            "1. Obtain explicit authorization for corpus revision or a written scientific justification for the observed step-position concentration.",
            "2. If revision is authorized, revise generation/labeling procedures so failure-step positions are structurally diversified without changing the protected protocol silently.",
            "3. Regenerate or relabel only under the approved correction task, then rerun the full audit suite including this script.",
            "4. Keep `EXPERIMENT_CHANGELOG.md`, `RESEARCH_LOG.md`, and `PROTOCOL_LOCK.md` synchronized with the gate status.",
        ]
        CORRECTION_PLAN.write_text("\n".join(plan_lines) + "\n", encoding="utf-8")

    print(f"Top gold_failure_step: {top_step} {top_step_count}/{total} ({pct(top_step_count, total):.2f}%)")
    print(f"Top gold_failure_agent: {top_agent} {top_agent_count}/{total} ({pct(top_agent_count, total):.2f}%)")
    print(f"always_s2 expected accuracy: {always_s2_accuracy:.4f} ({always_s2_accuracy*100:.2f}%)")
    print(f"majority_step expected accuracy: {majority_step_accuracy:.4f} ({majority_step_accuracy*100:.2f}%)")
    print(f"majority_agent expected accuracy: {majority_agent_accuracy:.4f} ({majority_agent_accuracy*100:.2f}%)")
    print("Evaluation blocked:", "yes" if evaluation_blocked else "no")
    if evaluation_blocked:
        print(f"Blocking reason: gold_failure_step={top_step} concentration and trivial shortcut risk exceed 50%.")
    print("FINAL: AUDIT_COMPLETE_BLOCKED" if evaluation_blocked else "FINAL: AUDIT_COMPLETE_CLEARED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
