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
    "s1": "intake review",
    "s2": "handoff alignment",
    "s3": "evidence synthesis",
    "s4": "verification pass",
    "s5": "delivery review",
}
ROLES = {"s1": "planner", "s2": "analyst", "s3": "executor", "s4": "reviewer", "s5": "coordinator"}


def _short(scenario: str) -> str:
    return "".join(part[0:3].upper() for part in scenario.split("_")[:2])


BASE_STEP_CONTENT: dict[str, dict[str, str]] = {
    "s1": {
        "input": "Review the incoming request, timing notes, policy checklist, and prior context before assigning work.",
        "output": "Frames the task with two viable interpretations, records the shared constraints, and asks the next agent to compare them.",
        "tool": "Context check lists request terms, timing notes, policy cues, and a cross-check item for downstream review.",
        "note": "neutral intake candidate with relevant context and comparable detail",
    },
    "s2": {
        "input": "Compare the intake packet with transfer notes, constraints, and open assumptions before forwarding the work.",
        "output": "Summarizes the handoff, identifies competing interpretations, and records which constraint details are carried forward.",
        "tool": "Transfer check lists handoff terms, constraint notes, policy cues, and one cross-check item for downstream review.",
        "note": "neutral handoff candidate with relevant context and comparable detail",
    },
    "s3": {
        "input": "Combine visible evidence, tool output, and the received packet into an execution plan with explicit assumptions.",
        "output": "Builds the action plan, notes alternate interpretations, and records which evidence is treated as controlling.",
        "tool": "Evidence check lists source reliability, measurement caveats, context notes, and one cross-check item for downstream review.",
        "note": "neutral evidence candidate with relevant context and comparable detail",
    },
    "s4": {
        "input": "Review the action plan against visible constraints, prior notes, and expected downstream dependencies.",
        "output": "Confirms several details, leaves one interpretation active, and writes the review note used by final assembly.",
        "tool": "Review check lists consistency observations, dependency notes, policy cues, and one cross-check item for downstream review.",
        "note": "neutral review candidate with relevant context and comparable detail",
    },
    "s5": {
        "input": "Assemble the response from prior notes, verify delivery constraints, and record the final operational outcome.",
        "output": "Delivers the final packet, names the assumption followed, and records whether the expected operational condition was met.",
        "tool": "Delivery check lists final packet contents, observed outcome, residual caveats, and one cross-check item for downstream review.",
        "note": "neutral delivery candidate with relevant context and comparable detail",
    },
}

SCENARIO_STEP_OVERRIDES: dict[str, dict[str, dict[str, str]]] = {
    "clean_broken_handoff": {
        "s1": {
            "tool": "Context check records a requester cap, timing note, and compliance cue; both cap and timing are marked relevant.",
            "output": "Frames two scheduling options and asks that the cap travel with the timing note during transfer.",
        },
        "s2": {
            "input": "Prepare the transfer note from intake details, including the cap, timing note, and routing assumptions.",
            "output": "Forwards the timing note and route, but converts the cap into a general preference rather than a required constraint.",
            "tool": "Transfer check shows the cap as required in intake while the forwarded packet lists it as optional background context.",
            "note": "handoff candidate where a required constraint is softened while other details remain available",
        },
        "s3": {
            "output": "Builds the schedule from the forwarded packet and treats the cap as optional because the transfer note presented it that way.",
            "tool": "Evidence check confirms timing feasibility but shows the cap was not applied in the scheduling calculation.",
        },
        "s4": {
            "output": "Verifies the schedule math and route order, while noting that the cap status depends on the earlier transfer wording.",
        },
        "s5": {
            "output": "Delivers a schedule that follows timing and route notes but misses the required cap from the original request.",
        },
    },
    "tool_evidence_usage": {
        "s1": {
            "output": "Frames the task and asks that tool confidence and sample coverage both be considered before selecting an option.",
        },
        "s2": {
            "tool": "Collection check returns two candidate readings, one broad but noisy and one narrower with stronger coverage.",
            "output": "Records both readings and sends both forward as competing evidence rather than selecting one prematurely.",
        },
        "s3": {
            "input": "Choose an execution option from the collected readings, confidence note, and sample-coverage caveat.",
            "output": "Treats the broad noisy reading as the controlling value and leaves the stronger coverage caveat out of the action plan.",
            "tool": "Evidence check states the broad reading has weak coverage while the narrower reading has stronger support for this case.",
            "note": "evidence candidate where a visible tool caveat is available but not carried into the plan",
        },
        "s4": {
            "output": "Reviews the plan for formatting and timing while noting that evidence weighting was already chosen upstream.",
        },
        "s5": {
            "output": "Delivers the selected option and observes that the result matches the noisy broad reading rather than the stronger case-specific cue.",
        },
    },
    "same_agent_continuation": {
        "s1": {
            "output": "Frames the task with an internal-only assumption and asks later agents to confirm whether external sharing is permitted.",
        },
        "s2": {
            "tool": "Policy check states internal notes may be reused, but external sharing requires an additional confirmation step.",
            "output": "Records the external-sharing caveat and sends it forward with the rest of the packet.",
        },
        "s3": {
            "output": "Drafts an internal summary and keeps the external-sharing caveat visible for review.",
        },
        "s4": {
            "input": "Review the draft, prior caveat, and delivery channel before authorizing the response path.",
            "output": "Carries forward the earlier internal-use assumption as if it covered the external channel and authorizes that channel.",
            "tool": "Review check repeats the external-confirmation caveat, but the review note treats internal permission as sufficient.",
            "note": "continuation candidate where an earlier assumption is carried into a broader channel decision",
        },
        "s5": {
            "output": "Assembles the response using the authorized external channel and records that no extra confirmation was obtained.",
        },
    },
    "cross_agent_propagation": {
        "s1": {
            "output": "Frames the task and asks each downstream agent to preserve the confidence qualifier attached to the source estimate.",
        },
        "s2": {
            "tool": "Source check reports an estimate with a low-confidence qualifier and a separate stable reference value.",
            "output": "Sends both values forward and notes that confidence should be checked before final use.",
        },
        "s3": {
            "output": "Builds an intermediate calculation and keeps the low-confidence qualifier visible in the working notes.",
        },
        "s4": {
            "output": "Reviews the calculation and marks the stable reference as suitable for comparison, while leaving final choice to delivery.",
        },
        "s5": {
            "input": "Prepare delivery using the intermediate calculation, confidence qualifier, and stable reference value.",
            "output": "Uses the low-confidence estimate as the delivered value and states that later formatting followed that earlier estimate.",
            "tool": "Delivery check shows the final value depends on the low-confidence estimate even though the stable reference remained visible.",
            "note": "propagation candidate where a downstream output visibly relies on an earlier weak estimate",
        },
    },
    "recoverable_irreversible_failure": {
        "s1": {
            "output": "Frames the task and asks later agents to use the correction window if the checklist and draft diverge.",
        },
        "s2": {
            "input": "Compare checklist, draft terms, and correction-window instructions before forwarding the operational packet.",
            "output": "Finds that the draft omits the cancellation window but forwards the packet without opening the available correction window.",
            "tool": "Checklist check shows the cancellation window is required and that a same-turn correction path is still available.",
            "note": "recovery candidate where a visible correction opportunity is available but not used",
        },
        "s3": {
            "output": "Builds execution steps from the forwarded packet and notes that the cancellation window is absent from the working draft.",
        },
        "s4": {
            "output": "Reviews the draft after the correction window has closed and can only add a caveat rather than restore the omitted term.",
        },
        "s5": {
            "output": "Delivers the packet with the caveat, and the terminal state remains degraded because the earlier window was not used.",
        },
    },
    "semantic_collision": {
        "s1": {
            "output": "Frames two close terms, renewal date and review date, and asks that the terminal outcome use the operational renewal date.",
        },
        "s2": {
            "tool": "Term check distinguishes renewal date as the operative date and review date as an internal planning date.",
            "output": "Records both terms separately and keeps the operative date distinction visible for execution.",
        },
        "s3": {
            "input": "Prepare execution notes from the two close terms and the terminal-outcome requirement.",
            "output": "Uses the internal review date as the operational renewal date in the execution note.",
            "tool": "Evidence check shows the review date belongs to planning while the renewal date controls the delivered outcome.",
            "note": "semantic candidate where two close alternatives are visible and one is selected for the wrong operational role",
        },
        "s4": {
            "output": "Checks formatting and confirms both dates appear, but does not revisit which date controls the delivered outcome.",
        },
        "s5": {
            "output": "Delivers an outcome tied to the review date, creating a mismatch with the requested renewal-date operation.",
        },
    },
    "complex_collaboration": {
        "s1": {
            "output": "Frames a collaborative task requiring handoff continuity, source ranking, and a brief correction window before delivery.",
        },
        "s2": {
            "tool": "Handoff check records source A as preliminary, source B as confirmed, and a correction window after review.",
            "output": "Sends both sources forward and asks execution to keep the confirmed source attached to the handoff note.",
        },
        "s3": {
            "output": "Builds the plan using source B but notes that a handoff summary must still preserve the source ranking.",
        },
        "s4": {
            "input": "Review source ranking, handoff summary, and correction-window status before final assembly.",
            "output": "Collapses the handoff summary so source A appears confirmed and closes the correction window without requesting a source check.",
            "tool": "Review check shows source B remains confirmed and the correction window is still available at review time.",
            "note": "collaboration candidate where handoff summary, evidence ranking, and correction timing interact visibly",
        },
        "s5": {
            "output": "Delivers from the collapsed summary and records that final assembly followed source A as if it were confirmed.",
        },
    },
}


def _merge_step_content(scenario: str, step_id: str) -> dict[str, str]:
    content = dict(BASE_STEP_CONTENT[step_id])
    content.update(SCENARIO_STEP_OVERRIDES.get(scenario, {}).get(step_id, {}))
    return content


def make_step(step_index: int, scenario: str, gold_step: str) -> dict[str, Any]:
    step_id = f"s{step_index}"
    agent_id = f"a{step_index}"
    next_agent = f"a{step_index + 1}" if step_index < 5 else None
    prev_agent = f"a{step_index - 1}" if step_index > 1 else None
    evidence_items = [f"ev{step_index}a", f"ev{step_index}b"]
    evidence_used = [evidence_items[0]]
    content = _merge_step_content(scenario, step_id)
    return {
        "step_id": step_id,
        "agent_id": agent_id,
        "agent_role": ROLES[step_id],
        "input_message": content["input"],
        "output_message": content["output"],
        "tool_call": f"inspect_{step_id}_context",
        "tool_output": content["tool"],
        "handoff_from": prev_agent,
        "handoff_to": next_agent,
        "evidence_items": evidence_items,
        "evidence_used": evidence_used,
        "visible_step_notes": content["note"],
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
