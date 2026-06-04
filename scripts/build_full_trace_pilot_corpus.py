#!/usr/bin/env python3
"""Build a non-final Journal-v1 full-trace pilot corpus.

This pilot is diagnostic and non-evidential. It does not generate the full
420-trace corpus, implement CCT scoring, calibration, refinement variants,
ablations, or paper-ready result tables.
"""

from __future__ import annotations

import json
import sys
from copy import deepcopy
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from cctdiag.schema.full_trace_contracts import DATASET_VERSION  # noqa: E402
from cctdiag.schema.full_trace_validators import validate_full_trace_schema  # noqa: E402
from cctdiag.io.full_trace_views import make_full_trace_prediction_view  # noqa: E402

OUT_DIR = ROOT / "data/interim/journal_v1_full_trace_pilot"
CLEAN_PATH = OUT_DIR / "full_trace_pilot_clean.jsonl"
PERTURBED_PATH = OUT_DIR / "full_trace_pilot_perturbed.jsonl"
ALL_PATH = OUT_DIR / "full_trace_pilot_all.jsonl"

SCENARIOS = [
    "clean_broken_handoff",
    "tool_evidence_usage",
    "same_agent_continuation",
    "cross_agent_propagation",
    "recoverable_irreversible_failure",
    "semantic_collision",
    "complex_collaboration",
]
PERTURBATIONS = [
    "paraphrase",
    "tool_output_truncation",
    "partial_observability",
    "non_causal_textual_distraction",
    "paraphrase",
    "tool_output_truncation",
    "partial_observability",
]
GOLD_STEPS = ["s2", "s3", "s4", "s5", "s2", "s3", "s4"]
H6_LABELS = [
    (True, True, False),
    (False, False, True),
    (True, False, False),
    (False, True, True),
    (True, True, False),
    (False, False, True),
    (True, False, False),
]

PHASES = {
    "s1": "task intake and plan framing",
    "s2": "handoff review and constraint alignment",
    "s3": "evidence integration and execution planning",
    "s4": "verification and transfer review",
    "s5": "final response assembly and delivery check",
}
ROLES = {"s1": "planner", "s2": "analyst", "s3": "executor", "s4": "reviewer", "s5": "coordinator"}


def _short(scenario: str) -> str:
    return "".join(part[0:3].upper() for part in scenario.split("_")[:2])


def make_step(step_index: int, scenario: str, gold_step: str) -> dict[str, Any]:
    step_id = f"s{step_index}"
    agent_id = f"a{step_index}"
    next_agent = f"a{step_index + 1}" if step_index < 5 else None
    prev_agent = f"a{step_index - 1}" if step_index > 1 else None
    scenario_text = scenario.replace("_", " ")
    local_topic = PHASES[step_id]
    evidence_items = [f"ev{step_index}a", f"ev{step_index}b"]
    evidence_used = [evidence_items[0]]
    if step_id == gold_step:
        input_message = f"{scenario_text}: inspect {local_topic} with competing signals and prior context."
        output_message = f"{local_topic.capitalize()} leaves a material ambiguity that later work must handle carefully."
        tool_output = f"audit note {step_id}: signal set includes one unresolved ambiguity and one confirming observation."
        visible_note = "candidate event with detailed context and downstream relevance"
    else:
        input_message = f"{scenario_text}: process {local_topic} using available context and routine checks."
        output_message = f"{local_topic.capitalize()} records assumptions, alternatives, and a normal handoff summary."
        tool_output = f"audit note {step_id}: routine observation list includes context, constraints, and cross-check notes."
        visible_note = "candidate event with neutral context and routine detail"
    return {
        "step_id": step_id,
        "agent_id": agent_id,
        "agent_role": ROLES[step_id],
        "input_message": input_message,
        "output_message": output_message,
        "tool_call": f"inspect_{step_id}_context",
        "tool_output": tool_output,
        "handoff_from": prev_agent,
        "handoff_to": next_agent,
        "evidence_items": evidence_items,
        "evidence_used": evidence_used,
        "visible_step_notes": visible_note,
    }


def make_clean_trace(index: int, scenario: str) -> dict[str, Any]:
    gold_step = GOLD_STEPS[index]
    gold_agent = f"a{int(gold_step[1:])}"
    propagation, irreversibility, recoverability = H6_LABELS[index]
    steps = [make_step(i, scenario, gold_step) for i in range(1, 6)]
    return {
        "trace_id": f"JV1FT_{_short(scenario)}_C{index + 1:03d}_clean",
        "dataset_version": DATASET_VERSION,
        "scenario_group": scenario,
        "case_id": f"FT_{_short(scenario)}_C{index + 1:03d}",
        "case_variant": "clean",
        "perturbation_type": "none",
        "perturbation_intensity": None,
        "steps": steps,
        "terminal_outcome": "degraded_execution" if not recoverability else "recovered_execution",
        "private_labels": {
            "gold_failure_step": gold_step,
            "gold_failure_agent": gold_agent,
            "gold_irreversibility": irreversibility,
            "gold_propagation": propagation,
            "gold_recoverability": recoverability,
            "label_rationale": f"Private pilot rationale: {gold_step}/{gold_agent} is the controlled attribution point for {scenario}.",
            "label_confidence": 0.9,
            "label_source": "journal_v1_full_trace_pilot_controlled",
            "propagation_evidence": "Private H6 note: downstream dependency status is controlled for pilot coverage.",
            "irreversibility_evidence": "Private H6 note: correction availability is controlled for pilot coverage.",
            "recovery_opportunity": "available" if recoverability else "unavailable_or_missed",
            "primary_labeler": "pilot_builder_rule",
            "secondary_labeler": "pilot_fixture_review",
            "adjudicator": "not_required",
            "disagreement_type": "none",
            "adjudication_decision": "pilot_rule",
            "manual_audit_status": "pending",
        },
        "provenance": {
            "annotator_or_generator": "build_full_trace_pilot_corpus.py",
            "provenance_notes": "Task 14 non-final non-evidential full-trace pilot; not paper evidence",
            "synthetic_control_rule": "task14_full_trace_pilot",
        },
    }


def make_perturbed_trace(clean_trace: dict[str, Any], perturbation: str, index: int) -> dict[str, Any]:
    trace = deepcopy(clean_trace)
    trace["trace_id"] = clean_trace["trace_id"].replace("_clean", f"_{perturbation}_P01")
    trace["case_variant"] = "perturbed"
    trace["perturbation_type"] = perturbation
    trace["perturbation_intensity"] = "medium"
    trace["clean_parent_trace_id"] = clean_trace["trace_id"]
    trace["provenance"]["provenance_notes"] = (
        "Task 14 perturbed pilot preserving parent structure and private labels; not paper evidence"
    )
    if perturbation == "paraphrase":
        trace["steps"][0]["input_message"] += " The request wording is restated with the same visible facts."
        trace["steps"][0]["visible_step_notes"] = "candidate event with neutral paraphrased wording"
    elif perturbation == "tool_output_truncation":
        trace["steps"][2]["tool_output"] = "audit note s3: routine observation list includes context ... [truncated]"
        trace["steps"][2]["visible_step_notes"] = "candidate event with neutral truncated tool output"
    elif perturbation == "partial_observability":
        trace["steps"][3]["evidence_used"] = trace["steps"][3]["evidence_used"][:1]
        trace["steps"][3]["visible_step_notes"] = "candidate event with neutral partial-observability condition"
    elif perturbation == "non_causal_textual_distraction":
        trace["steps"][1]["output_message"] += " A scheduling aside is included but is unrelated to the task state."
        trace["steps"][1]["visible_step_notes"] = "candidate event with neutral unrelated text"
    return trace


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.write_text("".join(json.dumps(row, sort_keys=True) + "\n" for row in rows), encoding="utf-8")


def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    clean = [make_clean_trace(index, scenario) for index, scenario in enumerate(SCENARIOS)]
    perturbed = [make_perturbed_trace(trace, PERTURBATIONS[index], index) for index, trace in enumerate(clean)]
    all_rows = clean + perturbed
    for row in all_rows:
        validate_full_trace_schema(row)
        make_full_trace_prediction_view(row)
    write_jsonl(CLEAN_PATH, clean)
    write_jsonl(PERTURBED_PATH, perturbed)
    write_jsonl(ALL_PATH, all_rows)
    print("=== Full-Trace Pilot Build ===")
    print(f"clean: {len(clean)} -> {CLEAN_PATH.relative_to(ROOT)}")
    print(f"perturbed: {len(perturbed)} -> {PERTURBED_PATH.relative_to(ROOT)}")
    print(f"all: {len(all_rows)} -> {ALL_PATH.relative_to(ROOT)}")
    print("FINAL: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
