#!/usr/bin/env python3
import json
import random
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PLAN = ROOT / "configs/corpus_plan.yaml"
OUT = ROOT / "data/processed/journal_v1"


def write_jsonl(path: Path, rows):
    path.write_text("\n".join(json.dumps(r, sort_keys=True) for r in rows) + "\n", encoding="utf-8")


def main():
    # Frozen from configs/corpus_plan.yaml (validated separately).
    scenarios = [
        "clean_broken_handoff",
        "tool_evidence_usage",
        "same_agent_continuation",
        "cross_agent_propagation",
        "recoverable_irreversible_failure",
        "semantic_collision",
        "complex_collaboration",
    ]
    per_group = 12
    per_clean_pert = 4
    expected_clean = 84
    expected_pert = 336
    expected_total = 420
    perturbations = ["paraphrase", "tool_output_truncation", "partial_observability", "non_causal_textual_distraction"]

    OUT.mkdir(parents=True, exist_ok=True)

    clean_rows = []
    pert_rows = []
    global_case = 1
    for sg_idx, sg in enumerate(scenarios):
        for group_case in range(1, per_group + 1):
            seed = 10000 + sg_idx * 100 + group_case
            rnd = random.Random(seed)
            base = {
                "trace_id": f"JV1_{sg}_C{global_case:03d}_clean",
                "dataset_version": "BRACIS-Journal-v1",
                "scenario_group": sg,
                "case_id": f"SG_{sg[:3].upper()}_C{global_case:03d}",
                "case_variant": "clean",
                "perturbation_type": "none",
                "perturbation_intensity": None,
                "step_id": "s2",
                "agent_id": "a2",
                "agent_role": "reviewer",
                "input_message": f"Main corpus case {global_case} with controlled collaboration context",
                "output_message": "Intermediate response containing a controlled failure signal",
                "tool_call": "lookup_context",
                "tool_output": f"context snippet {rnd.randint(1, 999)}",
                "handoff_from": "a1",
                "handoff_to": "a2",
                "evidence_items": ["ev1", "ev2", "ev3"],
                "evidence_used": ["ev2"],
                "terminal_outcome": "failed_execution" if global_case % 2 == 0 else "degraded_execution",
                "gold_failure_step": "s2",
                "gold_failure_agent": "a2",
                "gold_irreversibility": (global_case % 4 in {0, 1}),
                "gold_propagation": (global_case % 4 in {1, 2}),
                "gold_recoverability": (global_case % 4 in {2, 3}),
                "label_source": "journal_v1_main_controlled",
                "label_confidence": 0.9,
                "annotator_or_generator": "main_corpus_builder",
                "provenance_notes": f"seed={seed}; deterministic main controlled corpus; non-evidential without downstream experiments",
                "label_rationale": "stored as non-model-visible metadata with explicit dependency/recovery evidence",
                "step_catalog": ["s1", "s2", "s3", "s4"],
                "agent_catalog": ["a1", "a2", "a3"],
                "synthetic_control_rule": "task10_main_controlled",
                "primary_labeler": "generator_rule",
                "secondary_labeler": "review_pending",
                "adjudicator": "pending",
                "manual_audit_status": "pending",
                "disagreement_type": "none",
                "adjudication_decision": "auto_rule",
                "generation_seed": seed,
                "recovery_opportunity": "available_but_missed" if global_case % 4 == 3 else "not_applicable_or_unavailable",
                "propagation_evidence": "downstream step s3 uses faulty s2 artifact for decision",
                "irreversibility_evidence": "no successful correction after s2 before terminal outcome",
            }
            clean_rows.append(base)
            for p_idx, pert in enumerate(perturbations[:per_clean_pert], start=1):
                pr = dict(base)
                pr["trace_id"] = f"JV1_{sg}_C{global_case:03d}_{pert}_P{p_idx:02d}"
                pr["case_variant"] = "perturbed"
                pr["perturbation_type"] = pert
                pr["perturbation_intensity"] = "medium"
                pr["clean_parent_trace_id"] = base["trace_id"]
                pr["input_message"] = base["input_message"] + f" :: {pert} variant"
                pr["degraded_observability_note"] = "none"
                pert_rows.append(pr)
            global_case += 1

    all_rows = clean_rows + pert_rows
    assert len(clean_rows) == expected_clean
    assert len(pert_rows) == expected_pert
    assert len(all_rows) == expected_total

    write_jsonl(OUT / "main_clean_traces.jsonl", clean_rows)
    write_jsonl(OUT / "main_perturbed_traces.jsonl", pert_rows)
    write_jsonl(OUT / "main_all_traces.jsonl", all_rows)
    print(f"Built main corpus: clean={len(clean_rows)} perturbed={len(pert_rows)} total={len(all_rows)}")


if __name__ == "__main__":
    main()
