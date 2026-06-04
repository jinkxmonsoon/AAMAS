#!/usr/bin/env python3
import json
import random
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/processed/journal_v1"

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
ROLES = ["planner", "reviewer", "executor", "analyst", "coordinator"]
TOOL_CALLS = ["lookup_context", "fetch_trace", "retrieve_policy", "query_incident_log"]

SCENARIO_CONTEXTS = {
    "clean_broken_handoff": ["handoff packet omitted critical constraints", "transition note missed dependency checkpoint"],
    "tool_evidence_usage": ["tool evidence list had conflicting entries", "retrieved evidence required reconciliation"],
    "same_agent_continuation": ["same agent resumed after interruption", "continuation resumed with partial notes"],
    "cross_agent_propagation": ["upstream artifact propagated downstream", "dependent agent reused unresolved output"],
    "recoverable_irreversible_failure": ["recovery path existed but was delayed", "correction window was present but narrow"],
    "semantic_collision": ["terms overlapped but meanings diverged", "similar phrasing masked distinct failure cause"],
    "complex_collaboration": ["multi-agent coordination had competing priorities", "parallel threads converged with conflicting assumptions"],
}

RATIONALES = [
    "metadata rationale: {step} assigned to {agent} because the {phase} action created the documented failure path",
    "non-visible rationale: {step}/{agent} anchors dependency, propagation, and correction evidence for the {phase} fault",
    "rationale stored in metadata: {step} is the structurally grounded {phase} failure point for {agent}",
]

FAILURE_STEP_PHASES = {
    "s2": "handoff-intake",
    "s3": "evidence-integration",
    "s4": "verification-transfer",
    "s5": "final-adjudication",
}

FAILURE_STEP_INPUTS = {
    "s2": "handoff intake contained an unresolved constraint mismatch",
    "s3": "evidence integration combined incompatible observations",
    "s4": "verification transfer accepted an unchecked dependency",
    "s5": "final adjudication closed while a correction cue remained unresolved",
}

FAILURE_STEP_OUTPUTS = {
    "s2": "Intake summary moved forward with an unresolved constraint gap",
    "s3": "Integrated evidence bundle preserved an unresolved contradiction",
    "s4": "Verification note advanced without completing dependency validation",
    "s5": "Final adjudication recorded a degraded conclusion after missed correction",
}

FAILURE_STEP_TOOL_OUTPUTS = {
    "s2": "handoff-audit: constraint mismatch remained open",
    "s3": "evidence-merge: incompatible observation pair retained",
    "s4": "verification-log: dependency check incomplete",
    "s5": "adjudication-log: closure note retained unresolved correction cue",
}

FAILURE_STEPS = ["s2", "s3", "s4", "s5"]


def write_jsonl(path: Path, rows):
    path.write_text("\n".join(json.dumps(r, sort_keys=True) for r in rows) + "\n", encoding="utf-8")


def main():
    per_group, per_clean_pert = 12, 4
    expected_clean, expected_pert, expected_total = 84, 336, 420
    OUT.mkdir(parents=True, exist_ok=True)

    clean_rows, pert_rows = [], []
    global_case = 1
    for sg_idx, sg in enumerate(SCENARIOS):
        for group_case in range(1, per_group + 1):
            seed = 10000 + sg_idx * 100 + group_case
            rnd = random.Random(seed)
            agent_catalog = [f"a{rnd.randint(1,4)}", f"a{rnd.randint(5,8)}", f"a{rnd.randint(9,12)}"]
            role = ROLES[rnd.randrange(len(ROLES))]
            tool_call = TOOL_CALLS[rnd.randrange(len(TOOL_CALLS))]
            context = SCENARIO_CONTEXTS[sg][rnd.randrange(len(SCENARIO_CONTEXTS[sg]))]
            fail_step = FAILURE_STEPS[(global_case - 1) % len(FAILURE_STEPS)]
            step_count = 5 if fail_step == "s5" else 4 + rnd.randrange(2)  # 4 or 5, with s5 supported when selected
            steps = [f"s{i}" for i in range(1, step_count + 1)]
            step_agents = {step: agent_catalog[idx % len(agent_catalog)] for idx, step in enumerate(steps)}
            fail_agent = step_agents[fail_step]
            fail_step_index = steps.index(fail_step)
            handoff_from = step_agents[steps[max(0, fail_step_index - 1)]]
            handoff_to = fail_agent
            phase = FAILURE_STEP_PHASES[fail_step]
            evidence_pool = [f"ev{rnd.randint(1,20)}" for _ in range(4)]
            evidence_used = sorted(set(evidence_pool[:2]))
            base = {
                "trace_id": f"JV1_{sg}_C{global_case:03d}_clean",
                "dataset_version": "BRACIS-Journal-v1",
                "scenario_group": sg,
                "case_id": f"SG_{sg[:3].upper()}_C{global_case:03d}",
                "case_variant": "clean",
                "perturbation_type": "none",
                "perturbation_intensity": None,
                "step_id": fail_step,
                "agent_id": fail_agent,
                "agent_role": role,
                "input_message": f"Case {global_case}: {context}; phase={phase}; event={FAILURE_STEP_INPUTS[fail_step]}; constraints={rnd.choice(['timebound','safety','consistency'])}",
                "output_message": FAILURE_STEP_OUTPUTS[fail_step],
                "tool_call": tool_call,
                "tool_output": f"{FAILURE_STEP_TOOL_OUTPUTS[fail_step]}; record={rnd.randint(100,999)}; signal={rnd.choice(['weak','mixed','partial'])}",
                "handoff_from": handoff_from,
                "handoff_to": handoff_to,
                "evidence_items": evidence_pool,
                "evidence_used": evidence_used,
                "terminal_outcome": "failed_execution" if global_case % 2 == 0 else "degraded_execution",
                "gold_failure_step": fail_step,
                "gold_failure_agent": fail_agent,
                "gold_irreversibility": (global_case % 4 in {0, 1}),
                "gold_propagation": (global_case % 4 in {1, 2}),
                "gold_recoverability": (global_case % 4 in {2, 3}),
                "label_source": "journal_v1_main_controlled",
                "label_confidence": rnd.choice([0.86, 0.9, 0.93]),
                "annotator_or_generator": "main_corpus_builder",
                "provenance_notes": f"seed={seed}; deterministic diversified main corpus; non-evidential without downstream experiments",
                "label_rationale": rnd.choice(RATIONALES).format(step=fail_step, agent=fail_agent, phase=phase),
                "step_catalog": steps,
                "agent_catalog": agent_catalog,
                "synthetic_control_rule": "task10_main_controlled",
                "primary_labeler": "generator_rule",
                "secondary_labeler": "review_pending",
                "adjudicator": "pending",
                "manual_audit_status": "pending",
                "disagreement_type": "none",
                "adjudication_decision": "auto_rule",
                "generation_seed": seed,
            }
            # Enforce H6 semantic consistency constraints
            if base["gold_irreversibility"]:
                base["irreversibility_evidence"] = rnd.choice([
                    f"no successful correction after {fail_step} before terminal outcome",
                    f"failure consequence from {fail_step} persisted to terminal state without neutralization",
                    f"mitigation attempt after {fail_step} was insufficient to neutralize terminal failure",
                ])
            else:
                base["irreversibility_evidence"] = rnd.choice([
                    f"later correction at {steps[-1]} successfully corrected the effect from {fail_step}",
                    f"repair after {fail_step} successfully corrected the error trajectory",
                    f"terminal impact from {fail_step} was recovered before completion",
                ])

            if base["gold_recoverability"]:
                base["recovery_opportunity"] = rnd.choice(["available_and_used", "available_but_missed"])
            else:
                base["recovery_opportunity"] = "not_applicable_or_unavailable"

            if base["gold_propagation"]:
                base["propagation_evidence"] = rnd.choice([
                    f"downstream {steps[min(fail_step_index + 1, len(steps)-1)]} consumed faulty artifact from {fail_step}",
                    f"dependent agent reused unresolved output from {fail_step}",
                    f"handoff recipient integrated incorrect evidence originating at {fail_step}",
                ])
            else:
                base["propagation_evidence"] = rnd.choice([
                    f"error remained local to {fail_step} with isolated impact",
                    f"later steps used independent evidence channels and isolated the {fail_step} fault",
                    f"fault impact stayed confined to originating step {fail_step} context",
                ])

            clean_rows.append(base)
            for p_idx, pert in enumerate(PERTURBATIONS[:per_clean_pert], start=1):
                pr = dict(base)
                pr["trace_id"] = f"JV1_{sg}_C{global_case:03d}_{pert}_P{p_idx:02d}"
                pr["case_variant"] = "perturbed"
                pr["perturbation_type"] = pert
                pr["perturbation_intensity"] = rnd.choice(["low", "medium"])
                pr["clean_parent_trace_id"] = base["trace_id"]
                pr["input_message"] = base["input_message"] + f" :: variant={pert}"
                pr["degraded_observability_note"] = "none"
                pert_rows.append(pr)
            global_case += 1

    all_rows = clean_rows + pert_rows
    assert len(clean_rows) == expected_clean and len(pert_rows) == expected_pert and len(all_rows) == expected_total
    write_jsonl(OUT / "main_clean_traces.jsonl", clean_rows)
    write_jsonl(OUT / "main_perturbed_traces.jsonl", pert_rows)
    write_jsonl(OUT / "main_all_traces.jsonl", all_rows)
    print(f"Built main corpus: clean={len(clean_rows)} perturbed={len(pert_rows)} total={len(all_rows)}")


if __name__ == "__main__":
    main()
