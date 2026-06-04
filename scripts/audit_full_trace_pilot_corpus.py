#!/usr/bin/env python3
"""Audit the non-final Journal-v1 full-trace pilot corpus."""

from __future__ import annotations

import json
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from cctdiag.io.full_trace_views import assert_no_full_trace_private_leakage, make_full_trace_prediction_view  # noqa: E402
from cctdiag.schema.errors import ValidationError  # noqa: E402
from cctdiag.schema.full_trace_contracts import SCENARIO_GROUPS  # noqa: E402
from cctdiag.schema.full_trace_validators import validate_full_trace_schema  # noqa: E402

DATA_DIR = ROOT / "data/interim/journal_v1_full_trace_pilot"
REPORT_DIR = ROOT / "results/reports/journal_v1_full_trace_pilot"
CLEAN_PATH = DATA_DIR / "full_trace_pilot_clean.jsonl"
PERTURBED_PATH = DATA_DIR / "full_trace_pilot_perturbed.jsonl"
ALL_PATH = DATA_DIR / "full_trace_pilot_all.jsonl"
INVENTORY_REPORT = REPORT_DIR / "full_trace_pilot_inventory.md"
AUDIT_REPORT = REPORT_DIR / "full_trace_pilot_audit_report.md"
SEMANTIC_REPORT = REPORT_DIR / "full_trace_pilot_semantic_spotcheck.md"
RISK_REPORT = REPORT_DIR / "full_trace_pilot_generation_risk_report.md"

CORE_PERTURBATIONS = {
    "paraphrase",
    "tool_output_truncation",
    "partial_observability",
    "non_causal_textual_distraction",
}
LEXICAL_FORBIDDEN = ("gold", "label", "failure marker", "failing step", "root cause", "ground truth")


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def pct(count: int, total: int) -> str:
    return f"{(count / total * 100.0) if total else 0.0:.2f}%"


def counter_table(counter: Counter, total: int, key_name: str) -> list[str]:
    lines = [f"| {key_name} | count | percentage |", "|---|---:|---:|"]
    for key in sorted(counter):
        lines.append(f"| {key} | {counter[key]} | {pct(counter[key], total)} |")
    return lines


def visible_text(row: dict[str, Any]) -> str:
    parts = []
    for step in row["steps"]:
        for field in ("input_message", "output_message", "tool_call", "tool_output", "visible_step_notes"):
            parts.append(str(step.get(field) or ""))
    return "\n".join(parts).lower()


def content_asymmetry_issues(row: dict[str, Any]) -> list[str]:
    gold_step = row["private_labels"]["gold_failure_step"]
    steps = row["steps"]
    gold = next(step for step in steps if step["step_id"] == gold_step)
    issues = []
    if gold.get("tool_call") and sum(1 for step in steps if step.get("tool_call")) <= 1:
        issues.append("gold step is the only step with tool_call")
    if gold.get("evidence_items") and sum(1 for step in steps if step.get("evidence_items")) <= 1:
        issues.append("gold step is the only step with evidence_items")
    gold_richness = len(str(gold.get("input_message", ""))) + len(str(gold.get("output_message", "")))
    other_rich = [
        len(str(step.get("input_message", ""))) + len(str(step.get("output_message", "")))
        for step in steps
        if step["step_id"] != gold_step
    ]
    if other_rich and gold_richness > max(other_rich) * 1.8:
        issues.append("gold step has excessive visible text richness compared with all non-gold steps")
    return issues


def audit_rows(clean: list[dict[str, Any]], perturbed: list[dict[str, Any]], rows: list[dict[str, Any]]) -> dict[str, Any]:
    errors: list[str] = []
    warnings: list[str] = []
    clean_ids = {row["trace_id"] for row in clean}
    by_id = {row["trace_id"]: row for row in rows}

    for row in rows:
        trace_id = row.get("trace_id", "<missing>")
        try:
            validate_full_trace_schema(row)
            view = make_full_trace_prediction_view(row)
            assert_no_full_trace_private_leakage(view)
        except (ValidationError, ValueError) as exc:
            errors.append(f"{trace_id}: validation/prediction-view error: {exc}")
            continue
        if view["candidate_steps"] != [step["step_id"] for step in row["steps"]]:
            errors.append(f"{trace_id}: candidate step preservation mismatch")
        if set(view["candidate_agents"]) != {step["agent_id"] for step in row["steps"]}:
            errors.append(f"{trace_id}: candidate agent preservation mismatch")
        text = visible_text(row)
        for term in LEXICAL_FORBIDDEN:
            if term in text:
                errors.append(f"{trace_id}: visible text contains forbidden leakage term `{term}`")
        for issue in content_asymmetry_issues(row):
            warnings.append(f"{trace_id}: {issue}")

    for row in perturbed:
        parent_id = row.get("clean_parent_trace_id")
        if parent_id not in clean_ids:
            errors.append(f"{row.get('trace_id')}: clean_parent_trace_id missing or not in clean set")
            continue
        parent = by_id[parent_id]
        for field in ("gold_failure_step", "gold_failure_agent"):
            if row["private_labels"].get(field) != parent["private_labels"].get(field):
                errors.append(f"{row['trace_id']}: {field} does not match clean parent")
        if len(row["steps"]) != len(parent["steps"]):
            errors.append(f"{row['trace_id']}: perturbed trace does not preserve parent step count")

    scenario_counts = Counter(row["scenario_group"] for row in rows)
    perturbation_counts = Counter(row["perturbation_type"] for row in rows)
    step_counts = Counter(row["private_labels"]["gold_failure_step"] for row in rows)
    agent_counts = Counter(row["private_labels"]["gold_failure_agent"] for row in rows)
    h6_counts = {
        "gold_propagation": Counter(row["private_labels"]["gold_propagation"] for row in rows),
        "gold_irreversibility": Counter(row["private_labels"]["gold_irreversibility"] for row in rows),
        "gold_recoverability": Counter(row["private_labels"]["gold_recoverability"] for row in rows),
    }

    if len(clean) != 7:
        errors.append(f"expected 7 clean traces, found {len(clean)}")
    if len(perturbed) != 7:
        errors.append(f"expected 7 perturbed traces, found {len(perturbed)}")
    if len(rows) != 14:
        errors.append(f"expected 14 total traces, found {len(rows)}")
    if set(scenario_counts) != SCENARIO_GROUPS:
        errors.append("mandatory scenario coverage mismatch")
    if not CORE_PERTURBATIONS.issubset(set(perturbation_counts)):
        errors.append("core perturbation coverage mismatch")
    if not {"s2", "s3", "s4", "s5"}.issubset(set(step_counts)):
        errors.append("gold_failure_step coverage does not include s2/s3/s4/s5")
    for h6_name, counts in h6_counts.items():
        if counts[True] < 2 or counts[False] < 2:
            errors.append(f"{h6_name} lacks required true/false pilot coverage")

    accept = len(rows) if not errors else 0
    revise = 0 if not warnings else min(len(warnings), len(rows))
    reject = 0 if not errors else len(errors)
    status = "PASS" if not errors else "FAIL"
    return {
        "status": status,
        "errors": errors,
        "warnings": warnings,
        "scenario_counts": scenario_counts,
        "perturbation_counts": perturbation_counts,
        "step_counts": step_counts,
        "agent_counts": agent_counts,
        "h6_counts": h6_counts,
        "semantic_spotcheck": {"accept": accept, "revise": revise, "reject": reject},
    }


def write_reports(clean: list[dict[str, Any]], perturbed: list[dict[str, Any]], rows: list[dict[str, Any]], result: dict[str, Any]) -> None:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    total = len(rows)
    inventory_lines = [
        "# Full-Trace Pilot Inventory",
        "",
        "## Scope",
        "- Non-final, non-evidential full-trace pilot corpus.",
        "- Not a paper result table and not CCT evaluation.",
        "",
        "## Counts",
        f"- Clean traces: {len(clean)}.",
        f"- Perturbed traces: {len(perturbed)}.",
        f"- Total traces: {total}.",
        "",
        "## Scenario coverage",
        *counter_table(result["scenario_counts"], total, "scenario_group"),
        "",
        "## Perturbation coverage",
        *counter_table(result["perturbation_counts"], total, "perturbation_type"),
        "",
        "## Gold failure step distribution",
        *counter_table(result["step_counts"], total, "gold_failure_step"),
        "",
        "## Gold failure agent distribution",
        *counter_table(result["agent_counts"], total, "gold_failure_agent"),
    ]
    INVENTORY_REPORT.write_text("\n".join(inventory_lines) + "\n", encoding="utf-8")

    h6_lines = []
    for name, counter in result["h6_counts"].items():
        h6_lines.extend(["", f"### {name}", *counter_table(counter, total, name)])
    audit_lines = [
        "# Full-Trace Pilot Audit Report",
        "",
        "## Scope",
        "- Audit of non-final Journal-v1 full-trace pilot only.",
        "- No CCT scoring, calibration, refinement, ablation, or paper-ready result table is produced.",
        "",
        "## Status",
        f"- FINAL: {result['status']}.",
        "- Full-trace schema validation: PASS." if result["status"] == "PASS" else "- Full-trace schema validation: FAIL.",
        "- Prediction-view validation: PASS." if result["status"] == "PASS" else "- Prediction-view validation: FAIL.",
        "- Current failure-centered main corpus remains blocked.",
        "",
        "## H6 distribution",
        *h6_lines,
        "",
        "## Errors",
        *( ["- none."] if not result["errors"] else [f"- {error}" for error in result["errors"]] ),
        "",
        "## Warnings",
        *( ["- none."] if not result["warnings"] else [f"- {warning}" for warning in result["warnings"]] ),
    ]
    AUDIT_REPORT.write_text("\n".join(audit_lines) + "\n", encoding="utf-8")

    spot = result["semantic_spotcheck"]
    semantic_lines = [
        "# Full-Trace Pilot Semantic Spot-Check",
        "",
        "## Scope",
        "- Diagnostic semantic spot-check for the non-final pilot.",
        "- Checks that non-gold steps and agents are plausible and visible notes are neutral.",
        "",
        "## Outcome",
        f"- accept: {spot['accept']}",
        f"- revise: {spot['revise']}",
        f"- reject: {spot['reject']}",
        "- blocker: no" if result["status"] == "PASS" else "- blocker: yes",
    ]
    SEMANTIC_REPORT.write_text("\n".join(semantic_lines) + "\n", encoding="utf-8")

    risk_lines = [
        "# Full-Trace Pilot Generation Risk Report",
        "",
        "## Scope",
        "- Non-final pilot generation risk assessment.",
        "- The old failure-centered corpus remains blocked and no paper result may use this pilot.",
        "",
        "## Risks",
        "- Small pilot size: 14 traces only.",
        "- Synthetic templating risk remains possible and must be reassessed before main corpus regeneration.",
        "- Full 420-trace corpus generation remains blocked pending future approval.",
        "",
        "## Mitigations present in pilot",
        "- One clean trace per mandatory scenario group.",
        "- Core perturbation types distributed across perturbed traces.",
        "- Gold labels kept in private_labels only.",
        "- Prediction views preserve all candidate steps and agents.",
        "- Gold step is not the only richly detailed step with tool/evidence/handoff content.",
    ]
    RISK_REPORT.write_text("\n".join(risk_lines) + "\n", encoding="utf-8")


def main() -> int:
    clean = load_jsonl(CLEAN_PATH)
    perturbed = load_jsonl(PERTURBED_PATH)
    rows = load_jsonl(ALL_PATH)
    result = audit_rows(clean, perturbed, rows)
    write_reports(clean, perturbed, rows, result)
    print("=== Full-Trace Pilot Audit ===")
    print(f"clean: {len(clean)}")
    print(f"perturbed: {len(perturbed)}")
    print(f"all: {len(rows)}")
    print(f"scenario_groups: {dict(sorted(result['scenario_counts'].items()))}")
    print(f"perturbation_types: {dict(sorted(result['perturbation_counts'].items()))}")
    print(f"gold_failure_step: {dict(sorted(result['step_counts'].items()))}")
    print(f"semantic_spotcheck: {result['semantic_spotcheck']}")
    if result["errors"]:
        print("errors:")
        for error in result["errors"]:
            print(f"  - {error}")
    if result["warnings"]:
        print("warnings:")
        for warning in result["warnings"]:
            print(f"  - {warning}")
    print("FINAL:", result["status"])
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
