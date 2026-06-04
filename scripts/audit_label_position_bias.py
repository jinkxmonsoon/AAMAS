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

STEP_DOMINANCE_THRESHOLD = 0.40
STEP_SHORTCUT_RISK_THRESHOLD = 0.40
OTHER_TRIVIAL_RISK_BLOCK_THRESHOLD = 0.50
MIN_DISTINCT_STEP_SHARE = 0.15
MIN_DISTINCT_STEPS_AT_SHARE = 3


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
    step_values_meeting_min_share = sum(1 for count in step_counts.values() if (count / total if total else 0.0) >= MIN_DISTINCT_STEP_SHARE)
    step_diversity_ok = step_values_meeting_min_share >= MIN_DISTINCT_STEPS_AT_SHARE
    high_trivial_risks = {}
    if majority_step_accuracy > STEP_SHORTCUT_RISK_THRESHOLD:
        high_trivial_risks["majority_step"] = majority_step_accuracy
    if always_s2_accuracy > STEP_SHORTCUT_RISK_THRESHOLD:
        high_trivial_risks["always_s2"] = always_s2_accuracy
    for name, value in {
        "majority_agent": majority_agent_accuracy,
        "first_active_agent": first_active_accuracy,
        "most_common_agent": most_common_agent_accuracy,
    }.items():
        if value is not None and value > OTHER_TRIVIAL_RISK_BLOCK_THRESHOLD:
            high_trivial_risks[name] = value
    evaluation_blocked = bool(step_dominates or not step_diversity_ok or high_trivial_risks)

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
        f"- At least {MIN_DISTINCT_STEPS_AT_SHARE} distinct `gold_failure_step` values should each appear in at least {MIN_DISTINCT_STEP_SHARE:.0%} of traces.",
        "- No single `gold_failure_agent` should dominate unless scenario-specific and documented.",
        "- Semantic spot-check coverage must include positive and negative H6 examples and at least 3 different `gold_failure_step` values if available.",
        f"- `majority_step` and `always_s2` diagnostics must not exceed {STEP_SHORTCUT_RISK_THRESHOLD:.0%}; other trivial agent diagnostics remain blocked above {OTHER_TRIVIAL_RISK_BLOCK_THRESHOLD:.0%}.",
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
        f"- Distinct step values meeting >=15% share: {step_values_meeting_min_share}.",
        f"- Label-position bias detected: {'yes' if step_dominates or not step_diversity_ok else 'no'}.",
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
        f"| majority_step (`{top_step}`) | {majority_step_accuracy:.4f} ({majority_step_accuracy*100:.2f}%) | {top_step_count}/{total} | {'BLOCKS evaluation' if majority_step_accuracy > STEP_SHORTCUT_RISK_THRESHOLD else 'below block threshold'} |",
        f"| majority_agent (`{top_agent}`) | {majority_agent_accuracy:.4f} ({majority_agent_accuracy*100:.2f}%) | {top_agent_count}/{total} | {'BLOCKS evaluation' if majority_agent_accuracy > OTHER_TRIVIAL_RISK_BLOCK_THRESHOLD else 'below block threshold'} |",
        f"| always_s2 | {always_s2_accuracy:.4f} ({always_s2_accuracy*100:.2f}%) | {always_s2_count}/{total} | {'BLOCKS evaluation' if always_s2_accuracy > STEP_SHORTCUT_RISK_THRESHOLD else 'below block threshold'} |",
        (
            f"| first_active_agent | {first_active_accuracy:.4f} ({first_active_accuracy*100:.2f}%) | {first_active_correct}/{first_active_computable} | "
            f"{'BLOCKS evaluation' if first_active_accuracy and first_active_accuracy > OTHER_TRIVIAL_RISK_BLOCK_THRESHOLD else 'below block threshold'} |"
            if first_active_accuracy is not None else
            "| first_active_agent | not computable | 0/0 | unavailable |"
        ),
        f"| most_common_agent (`{top_agent}`) | {most_common_agent_accuracy:.4f} ({most_common_agent_accuracy*100:.2f}%) | {top_agent_count}/{total} | {'BLOCKS evaluation' if most_common_agent_accuracy > OTHER_TRIVIAL_RISK_BLOCK_THRESHOLD else 'below block threshold'} |",
        "",
        "## Evaluation gate",
        f"- Evaluation blocked: {'yes' if evaluation_blocked else 'no'}.",
    ]
    if high_trivial_risks:
        baseline_lines.append("- Blocking trivial-risk diagnostics: " + ", ".join(f"{k}={v*100:.2f}%" for k, v in high_trivial_risks.items()) + ".")
    else:
        baseline_lines.append("- No trivial-risk diagnostic exceeded its configured block threshold.")
    BASELINE_REPORT.write_text("\n".join(baseline_lines) + "\n", encoding="utf-8")

    if evaluation_blocked:
        status_lines = [
            "- Evaluation remains blocked.",
            f"- Exact blocking reason(s): top step `{top_step}` appears in {top_step_count}/{total} traces ({pct(top_step_count, total):.2f}%); distinct steps meeting >=15% share = {step_values_meeting_min_share}; blocking diagnostics = {', '.join(high_trivial_risks) if high_trivial_risks else 'distribution threshold'}.",
        ]
        required_lines = [
            "1. Obtain explicit authorization for corpus revision or a written scientific justification for the observed step-position concentration.",
            "2. If revision is authorized, revise generation/labeling procedures so failure-step positions are structurally diversified without changing the protected protocol silently.",
            "3. Regenerate or relabel only under the approved correction task, then rerun the full audit suite including this script.",
            "4. Keep `EXPERIMENT_CHANGELOG.md`, `RESEARCH_LOG.md`, and `PROTOCOL_LOCK.md` synchronized with the gate status.",
        ]
    else:
        status_lines = [
            "- Evaluation is cleared by the Task 10F label-position/trivial-shortcut gate.",
            f"- Top step `{top_step}` appears in {top_step_count}/{total} traces ({pct(top_step_count, total):.2f}%), and {step_values_meeting_min_share} step values meet the >=15% diversity threshold.",
        ]
        required_lines = [
            "1. Preserve the corrected corpus hashes in the manifest.",
            "2. Re-run this audit if any corpus-generation logic or gold labels change.",
        ]
    plan_lines = [
        "# Journal-v1 Main Label-Position Bias Correction Plan",
        "",
        "## Status",
        *status_lines,
        "",
        "## Non-action guardrail",
        "- No metrics, baselines, CCT scoring, calibration, or result tables were implemented by this diagnostic script.",
        "",
        "## Required follow-up",
        *required_lines,
    ]
    CORRECTION_PLAN.write_text("\n".join(plan_lines) + "\n", encoding="utf-8")

    print(f"Top gold_failure_step: {top_step} {top_step_count}/{total} ({pct(top_step_count, total):.2f}%)")
    print(f"Top gold_failure_agent: {top_agent} {top_agent_count}/{total} ({pct(top_agent_count, total):.2f}%)")
    print(f"always_s2 expected accuracy: {always_s2_accuracy:.4f} ({always_s2_accuracy*100:.2f}%)")
    print(f"majority_step expected accuracy: {majority_step_accuracy:.4f} ({majority_step_accuracy*100:.2f}%)")
    print(f"majority_agent expected accuracy: {majority_agent_accuracy:.4f} ({majority_agent_accuracy*100:.2f}%)")
    print("Evaluation blocked:", "yes" if evaluation_blocked else "no")
    if evaluation_blocked:
        print(f"Blocking reason: gold_failure_step={top_step} concentration/diversity or trivial shortcut risk exceeds Task 10F thresholds.")
    print("FINAL: AUDIT_COMPLETE_BLOCKED" if evaluation_blocked else "FINAL: AUDIT_COMPLETE_CLEARED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
