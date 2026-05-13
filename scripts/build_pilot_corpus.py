#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/interim/journal_v1_pilot"

SCENARIOS = [
    "clean_broken_handoff",
    "tool_evidence_usage",
    "same_agent_continuation",
    "cross_agent_propagation",
    "recoverable_irreversible_failure",
    "semantic_collision",
    "complex_collaboration",
]
PERTS = ["paraphrase", "tool_output_truncation", "partial_observability", "non_causal_textual_distraction"]


def make_clean(i, sg):
    steps=["s1","s2","s3"]
    agents=["a1","a2"]
    return {
        "trace_id": f"JV1_{sg}_C{i:03d}_clean",
        "dataset_version": "BRACIS-Journal-v1",
        "scenario_group": sg,
        "case_id": f"SG_{i:03d}",
        "case_variant": "clean",
        "perturbation_type": "none",
        "perturbation_intensity": None,
        "step_id": "s2",
        "agent_id": "a2",
        "agent_role": "reviewer",
        "input_message": f"Case {i} task handoff context",
        "output_message": "Intermediate response with unresolved error",
        "tool_call": "lookup_context",
        "tool_output": "context snippet",
        "handoff_from": "a1",
        "handoff_to": "a2",
        "evidence_items": ["ev1", "ev2"],
        "evidence_used": ["ev2"],
        "terminal_outcome": "failed_execution",
        "gold_failure_step": "s2",
        "gold_failure_agent": "a2",
        "gold_irreversibility": i in {1,4,6},
        "gold_propagation": i in {2,4,7},
        "gold_recoverability": i in {3,5,7},
        "label_source": "pilot_controlled",
        "label_confidence": 0.85,
        "annotator_or_generator": "pilot_builder",
        "provenance_notes": "journal_v1 pilot non-evidential fixture-like corpus",
        "label_rationale": "stored as non-model-visible metadata",
        "step_catalog": steps,
        "agent_catalog": agents,
    }


def make_perturbed(clean, pert, j):
    r=dict(clean)
    r["trace_id"]=clean["trace_id"].replace("_clean", f"_{pert}_P{j:02d}")
    r["case_variant"]="perturbed"
    r["perturbation_type"]=pert
    r["perturbation_intensity"]="medium"
    r["clean_parent_trace_id"]=clean["trace_id"]
    r["input_message"]=clean["input_message"]+" variant"
    return r


def write_jsonl(path, rows):
    path.write_text("\n".join(json.dumps(r) for r in rows)+"\n", encoding="utf-8")


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    clean=[make_clean(i+1, sg) for i,sg in enumerate(SCENARIOS)]
    pert=[make_perturbed(c, PERTS[i % len(PERTS)], i+1) for i,c in enumerate(clean)]
    all_rows=clean+pert
    write_jsonl(OUT / "pilot_clean_traces.jsonl", clean)
    write_jsonl(OUT / "pilot_perturbed_traces.jsonl", pert)
    write_jsonl(OUT / "pilot_all_traces.jsonl", all_rows)
    inv = ROOT / "results/reports/journal_v1_pilot/pilot_corpus_inventory.md"
    inv.write_text("# Pilot Corpus Inventory\n\n- Non-final, non-evidential pilot corpus.\n- Clean traces: 7\n- Perturbed traces: 7\n- Total traces: 14\n", encoding="utf-8")
    print("Pilot corpus built: 14 traces")

if __name__ == "__main__":
    main()
