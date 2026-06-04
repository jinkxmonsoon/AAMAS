#!/usr/bin/env python3
"""Build the Journal-v1 full-trace main corpus.

This task generates the full ordered multi-step corpus only. It does not
implement CCT graph construction/scoring, calibration, refinement variants,
ablations, empirical hypothesis tests, or paper-ready result tables.
"""

from __future__ import annotations

import json
import sys
from copy import deepcopy
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from cctdiag.io.full_trace_views import make_full_trace_prediction_view  # noqa: E402
from cctdiag.schema.full_trace_contracts import DATASET_VERSION  # noqa: E402
from cctdiag.schema.full_trace_validators import validate_full_trace_schema  # noqa: E402

OUT_DIR = ROOT / "data/processed/journal_v1_full_trace"
CLEAN_PATH = OUT_DIR / "main_full_trace_clean.jsonl"
PERTURBED_PATH = OUT_DIR / "main_full_trace_perturbed.jsonl"
ALL_PATH = OUT_DIR / "main_full_trace_all.jsonl"

SCENARIOS = [
    "clean_broken_handoff",
    "tool_evidence_usage",
    "same_agent_continuation",
    "cross_agent_propagation",
    "recoverable_irreversible_failure",
    "semantic_collision",
    "complex_collaboration",
]
PERTURBATIONS = ["paraphrase", "tool_output_truncation", "partial_observability", "non_causal_textual_distraction"]
GOLD_STEPS = ["s2", "s3", "s4", "s5"]
ROLES = {"s1": "planner", "s2": "analyst", "s3": "executor", "s4": "reviewer", "s5": "coordinator"}
PHASES = {
    "s1": "intake review",
    "s2": "handoff alignment",
    "s3": "evidence synthesis",
    "s4": "verification pass",
    "s5": "delivery review",
}
CONSTRAINTS = ["budget cap", "privacy flag", "time window", "format rule", "access limit", "priority tier"]
EVIDENCE_TYPES = ["coverage reading", "source confidence", "timestamp check", "policy match", "measurement note", "case marker"]
CHANNELS = ["external portal", "client digest", "shared queue", "regional handoff", "review mailbox", "service desk"]
DATES = [("renewal date", "review date"), ("activation date", "archive date"), ("service date", "survey date")]
SOURCES = [("source A", "source B"), ("draft feed", "verified feed"), ("regional note", "central note")]

FORBIDDEN_VISIBLE = (
    "gold",
    "label",
    "failure marker",
    "failing step",
    "root cause",
    "ground truth",
    "known failure",
    "decisive error",
    "culprit",
    "target step",
)


def _short(scenario: str) -> str:
    return "".join(part[:3].upper() for part in scenario.split("_")[:2])


def _pick(items: list[Any], case_index: int, offset: int = 0) -> Any:
    return items[(case_index + offset) % len(items)]


def _base_step(step_index: int, case_index: int) -> dict[str, Any]:
    step_id = f"s{step_index}"
    return {
        "step_id": step_id,
        "agent_id": f"a{step_index}",
        "agent_role": ROLES[step_id],
        "input_message": (
            f"Perform {PHASES[step_id]} for case variant {case_index + 1}, considering the request packet, "
            "visible constraints, alternate interpretations, and handoff notes."
        ),
        "output_message": (
            f"Records {PHASES[step_id]} observations with a comparable amount of operational detail, "
            "including one retained caveat and one downstream note."
        ),
        "tool_call": f"inspect_{step_id}_case_{case_index + 1}",
        "tool_output": (
            f"Check {step_id} returns case-specific context, a relevant caveat, a confirming observation, "
            "and a downstream cross-check item."
        ),
        "handoff_from": f"a{step_index - 1}" if step_index > 1 else None,
        "handoff_to": f"a{step_index + 1}" if step_index < 5 else None,
        "evidence_items": [f"ev{step_index}a_case{case_index + 1}", f"ev{step_index}b_case{case_index + 1}"],
        "evidence_used": [f"ev{step_index}a_case{case_index + 1}"],
        "visible_step_notes": f"neutral {PHASES[step_id]} candidate with concrete case context and comparable detail",
    }


def _apply_scenario(steps: list[dict[str, Any]], scenario: str, case_index: int, gold_step: str) -> None:
    constraint = _pick(CONSTRAINTS, case_index)
    evidence = _pick(EVIDENCE_TYPES, case_index)
    channel = _pick(CHANNELS, case_index)
    operative_date, nearby_date = _pick(DATES, case_index)
    source_primary, source_confirmed = _pick(SOURCES, case_index)
    alternate = _pick(CONSTRAINTS, case_index, 2)
    s = {step["step_id"]: step for step in steps}

    if scenario == "clean_broken_handoff":
        s["s1"].update(
            output_message=f"Identifies {constraint} as required and asks that it travel with the timing note and route summary.",
            tool_output=f"Context check marks {constraint} as required, with timing and route notes also relevant for the transfer.",
        )
        s[gold_step].update(
            input_message=f"Prepare the transfer note from intake details, including {constraint}, timing, and route assumptions.",
            output_message=f"Forwards timing and route details but restates {constraint} as optional background rather than a required condition.",
            tool_output=f"Transfer check shows {constraint} required in intake while the forwarded packet lists it as optional context.",
            visible_step_notes="neutral handoff candidate where a required condition is softened while other details remain available",
        )
        for step_id in GOLD_STEPS:
            if step_id != gold_step:
                s[step_id]["output_message"] += f" The note remains plausible and references {constraint} only through the received packet."
        s["s5"]["output_message"] = f"Delivers a result that follows timing and route notes but does not enforce {constraint}."
    elif scenario == "tool_evidence_usage":
        s["s1"].update(output_message=f"Asks downstream work to compare {evidence} with sample coverage before selecting an option.")
        s["s2"].update(
            output_message=f"Records a broad noisy reading and a narrower reading with stronger support for {evidence}.",
            tool_output=f"Collection check returns a broad noisy reading plus a narrower reading with stronger support for {evidence}.",
        )
        s[gold_step].update(
            input_message=f"Choose an execution option from the collected readings, confidence note, and {evidence} caveat.",
            output_message=f"Treats the broad noisy reading as controlling and leaves the stronger {evidence} caveat out of the plan.",
            tool_output=f"Evidence check states the broad reading is weak for this case while the narrower reading has stronger support.",
            visible_step_notes="neutral evidence candidate where a visible caveat is not carried into the plan",
        )
        s["s5"]["output_message"] = f"Delivers the selected option and observes it aligns with the broad reading rather than the stronger {evidence} cue."
    elif scenario == "same_agent_continuation":
        s["s1"].update(output_message=f"Frames an internal-use assumption and asks later review to confirm whether {channel} is permitted.")
        s["s2"].update(
            output_message=f"Records that {channel} requires an additional confirmation step before delivery.",
            tool_output=f"Policy check allows internal reuse but says {channel} needs additional confirmation before release.",
        )
        s["s3"].update(output_message=f"Drafts internal content and keeps the {channel} confirmation caveat visible for review.")
        s[gold_step].update(
            input_message=f"Review the draft, confirmation caveat, and {channel} before authorizing the response path.",
            output_message=f"Carries the internal-use assumption into {channel} authorization and does not request the extra confirmation.",
            tool_output=f"Review check repeats the {channel} confirmation caveat while the review note treats internal permission as sufficient.",
            visible_step_notes="neutral continuation candidate where an earlier assumption is carried into a broader channel decision",
        )
        s["s5"]["output_message"] = f"Assembles the response for {channel} and records that no extra confirmation was obtained."
    elif scenario == "cross_agent_propagation":
        s["s1"].update(output_message=f"Asks downstream agents to preserve the confidence qualifier attached to {source_primary}.")
        s["s2"].update(
            output_message=f"Sends {source_primary} with a low-confidence qualifier and {source_confirmed} as a stable reference.",
            tool_output=f"Source check reports {source_primary} as low confidence and {source_confirmed} as stable for comparison.",
        )
        s["s3"].update(output_message=f"Builds an intermediate calculation while keeping the {source_primary} qualifier visible.")
        s["s4"].update(output_message=f"Marks {source_confirmed} suitable for comparison while leaving final value selection to delivery.")
        s[gold_step].update(
            input_message=f"Prepare delivery using the intermediate calculation, qualifier, and {source_confirmed} reference.",
            output_message=f"Uses the low-confidence {source_primary} estimate as the delivered value despite the visible stable reference.",
            tool_output=f"Delivery check shows the final value depends on low-confidence {source_primary} while {source_confirmed} remains visible.",
            visible_step_notes="neutral propagation candidate where downstream output relies on an earlier weak estimate",
        )
    elif scenario == "recoverable_irreversible_failure":
        s["s1"].update(output_message=f"Asks later agents to use the correction window if {alternate} and draft terms diverge.")
        s[gold_step].update(
            input_message=f"Compare checklist, draft terms, and correction-window instructions before forwarding the packet.",
            output_message=f"Finds that the draft omits {alternate} but forwards the packet without using the available correction window.",
            tool_output=f"Checklist check shows {alternate} is required and the same-turn correction path is still open.",
            visible_step_notes="neutral recovery candidate where a visible correction opportunity is available but not used",
        )
        s["s3"]["output_message"] = f"Builds execution steps from the forwarded packet and notes that {alternate} is absent from the working draft."
        s["s4"]["output_message"] = "Reviews the draft after the correction window has closed and can only add a caveat."
        s["s5"]["output_message"] = "Delivers the packet with the caveat and the terminal state remains degraded."
    elif scenario == "semantic_collision":
        s["s1"].update(output_message=f"Frames two close terms, {operative_date} and {nearby_date}, and asks that delivery use {operative_date}.")
        s["s2"].update(
            output_message=f"Records {operative_date} separately from {nearby_date} and keeps the operational distinction visible.",
            tool_output=f"Term check distinguishes {operative_date} as operative and {nearby_date} as an internal planning term.",
        )
        s[gold_step].update(
            input_message=f"Prepare execution notes from {operative_date}, {nearby_date}, and the delivery requirement.",
            output_message=f"Uses {nearby_date} as if it were {operative_date} in the execution note.",
            tool_output=f"Evidence check shows {nearby_date} belongs to planning while {operative_date} controls delivery.",
            visible_step_notes="neutral semantic candidate where close alternatives are visible and one is used in the wrong role",
        )
        s["s5"]["output_message"] = f"Delivers an outcome tied to {nearby_date}, creating a mismatch with the requested {operative_date} operation."
    elif scenario == "complex_collaboration":
        s["s1"].update(output_message=f"Frames a collaborative task requiring handoff continuity, {source_confirmed} ranking, and a correction window.")
        s["s2"].update(
            output_message=f"Sends {source_primary} and {source_confirmed} forward and asks execution to preserve which source is confirmed.",
            tool_output=f"Handoff check records {source_primary} as preliminary, {source_confirmed} as confirmed, and a correction window after review.",
        )
        s["s3"].update(output_message=f"Builds the plan using {source_confirmed} and notes that source ranking must remain attached to the handoff.")
        s[gold_step].update(
            input_message=f"Review source ranking, handoff summary, and correction-window status before final assembly.",
            output_message=f"Collapses the summary so {source_primary} appears confirmed and closes the correction window without requesting a source check.",
            tool_output=f"Review check shows {source_confirmed} remains confirmed and the correction window is still available at review time.",
            visible_step_notes="neutral collaboration candidate where handoff summary, evidence ranking, and correction timing interact visibly",
        )
        s["s5"]["output_message"] = f"Delivers from the collapsed summary and records that final assembly followed {source_primary} as if confirmed."


def make_steps(scenario: str, case_index: int, gold_step: str) -> list[dict[str, Any]]:
    steps = [_base_step(step_index, case_index) for step_index in range(1, 6)]
    _apply_scenario(steps, scenario, case_index, gold_step)
    text = " ".join(str(step.get(field, "")) for step in steps for field in ("input_message", "output_message", "tool_output", "visible_step_notes")).lower()
    leaked = [term for term in FORBIDDEN_VISIBLE if term in text]
    if leaked:
        raise ValueError(f"visible leakage terms in generated trace: {leaked}")
    return steps


def h6_labels(scenario_index: int, case_index: int) -> tuple[bool, bool, bool]:
    propagation = (scenario_index + case_index) % 2 == 0
    irreversibility = (scenario_index * 2 + case_index) % 3 != 0
    recoverability = (scenario_index + case_index * 2) % 3 == 0
    return propagation, irreversibility, recoverability


def make_clean_trace(scenario_index: int, case_index: int, scenario: str) -> dict[str, Any]:
    gold_step = GOLD_STEPS[case_index % len(GOLD_STEPS)]
    gold_agent = f"a{gold_step[1:]}"
    propagation, irreversibility, recoverability = h6_labels(scenario_index, case_index)
    steps = make_steps(scenario, case_index, gold_step)
    case_id = f"FTMAIN_{_short(scenario)}_C{case_index + 1:02d}"
    return {
        "trace_id": f"JV1FTMAIN_{_short(scenario)}_C{case_index + 1:02d}_clean",
        "dataset_version": DATASET_VERSION,
        "scenario_group": scenario,
        "case_id": case_id,
        "case_variant": "clean",
        "perturbation_type": "none",
        "perturbation_intensity": None,
        "steps": steps,
        "terminal_outcome": "recovered_execution" if recoverability else "degraded_execution",
        "private_labels": {
            "gold_failure_step": gold_step,
            "gold_failure_agent": gold_agent,
            "gold_irreversibility": irreversibility,
            "gold_propagation": propagation,
            "gold_recoverability": recoverability,
            "label_rationale": f"Private main-corpus rationale: {gold_step}/{gold_agent} is supported by visible diagnostic evidence for {scenario} case {case_index + 1}.",
            "label_confidence": 0.9,
            "label_source": "journal_v1_full_trace_main_controlled_builder",
            "propagation_evidence": "Private H6 note: downstream dependency status assigned by controlled main-corpus design.",
            "irreversibility_evidence": "Private H6 note: outcome reversibility assigned by controlled main-corpus design.",
            "recovery_opportunity": "available" if recoverability else "unavailable_or_missed",
            "primary_labeler": "main_full_trace_builder_rule",
            "secondary_labeler": "main_fixture_review",
            "adjudicator": "not_required",
            "disagreement_type": "none",
            "adjudication_decision": "builder_rule",
            "manual_audit_status": "accepted",
        },
        "provenance": {
            "annotator_or_generator": "build_full_trace_main_corpus.py",
            "provenance_notes": "Task 15 full-trace main corpus generation; not evaluation results",
            "synthetic_control_rule": "task15_full_trace_main_controlled_generation",
        },
    }


def make_perturbed_trace(clean_trace: dict[str, Any], perturbation: str) -> dict[str, Any]:
    trace = deepcopy(clean_trace)
    trace["trace_id"] = clean_trace["trace_id"].replace("_clean", f"_{perturbation}_P01")
    trace["case_variant"] = "perturbed"
    trace["perturbation_type"] = perturbation
    trace["perturbation_intensity"] = "medium"
    trace["clean_parent_trace_id"] = clean_trace["trace_id"]
    trace["provenance"]["provenance_notes"] = "Task 15 perturbed full-trace main record preserving parent labels; not evaluation results"
    if perturbation == "paraphrase":
        trace["steps"][0]["input_message"] += " The wording is restated while preserving the same visible facts."
    elif perturbation == "tool_output_truncation":
        # Truncate a non-gold step when possible; diagnostic evidence remains in visible messages.
        gold = trace["private_labels"]["gold_failure_step"]
        index = 0 if gold != "s1" else 1
        trace["steps"][index]["tool_output"] = trace["steps"][index]["tool_output"][:95] + " ... [truncated]"
    elif perturbation == "partial_observability":
        trace["steps"][3]["evidence_used"] = trace["steps"][3]["evidence_used"][:1]
        trace["steps"][3]["visible_step_notes"] += "; partial observation note retains neutral wording"
    elif perturbation == "non_causal_textual_distraction":
        trace["steps"][1]["output_message"] += " A scheduling aside is present but does not change the operational dependency."
    return trace


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.write_text("".join(json.dumps(row, sort_keys=True) + "\n" for row in rows), encoding="utf-8")


def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    clean: list[dict[str, Any]] = []
    for scenario_index, scenario in enumerate(SCENARIOS):
        clean.extend(make_clean_trace(scenario_index, case_index, scenario) for case_index in range(12))
    perturbed = [make_perturbed_trace(row, perturbation) for row in clean for perturbation in PERTURBATIONS]
    all_rows = clean + perturbed
    for row in all_rows:
        validate_full_trace_schema(row)
        make_full_trace_prediction_view(row)
    write_jsonl(CLEAN_PATH, clean)
    write_jsonl(PERTURBED_PATH, perturbed)
    write_jsonl(ALL_PATH, all_rows)
    print("=== Full-Trace Main Corpus Build ===")
    print(f"clean: {len(clean)} -> {CLEAN_PATH.relative_to(ROOT)}")
    print(f"perturbed: {len(perturbed)} -> {PERTURBED_PATH.relative_to(ROOT)}")
    print(f"all: {len(all_rows)} -> {ALL_PATH.relative_to(ROOT)}")
    print("FINAL: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
