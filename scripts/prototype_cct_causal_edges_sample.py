#!/usr/bin/env python3
"""Build a compact sample-only CCT causal-flow edge prototype artifact."""

from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from cctdiag.cct.causal_edges import (
    FORBIDDEN_OUTPUT_FIELDS,
    IMPLEMENTED_EDGE_TYPES,
    audit_edges_for_private_leakage,
    extract_causal_edges_from_prediction_view,
)
from cctdiag.io.full_trace_views import make_full_trace_prediction_view
from cctdiag.schema.full_trace_contracts import SCENARIO_GROUPS

INPUT_PATH = ROOT / "data/processed/journal_v1_full_trace/main_full_trace_all.jsonl"
RAW_OUTPUT_PATH = ROOT / "results/raw/journal_v1_full_trace_cct/cct_causal_edge_sample_prototype.json"
GRAPH_OUTPUT_PATH = ROOT / "data/interim/journal_v1_full_trace_cct/sample_cct_causal_edge_augmented_graphs.jsonl"
REPORT_DIR = ROOT / "results/reports/journal_v1_full_trace_cct"
MAX_SAMPLE_TRACES = 20
TARGET_VARIANTS = ("clean", "perturbed")


def iter_records(path: Path):
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                yield json.loads(line)


def select_sample_records(path: Path = INPUT_PATH) -> list[dict[str, Any]]:
    """Select first clean and first perturbed trace per scenario without gold fields."""

    selected: dict[tuple[str, str], dict[str, Any]] = {}
    target_keys = {(scenario, variant) for scenario in sorted(SCENARIO_GROUPS) for variant in TARGET_VARIANTS}
    for record in iter_records(path):
        key = (record.get("scenario_group"), record.get("case_variant"))
        if key in target_keys and key not in selected:
            selected[key] = record
        if len(selected) == len(target_keys) or len(selected) >= MAX_SAMPLE_TRACES:
            break
    return [selected[key] for key in sorted(selected)]


def build_sample_payload(records: list[dict[str, Any]]) -> dict[str, Any]:
    trace_payloads = []
    all_edges = []
    composition = []
    for record in records:
        prediction_view = make_full_trace_prediction_view(record)
        # Extraction receives only the sanitized prediction view.
        edges = extract_causal_edges_from_prediction_view(prediction_view)
        all_edges.extend(edges)
        trace_payloads.append({"trace_id": prediction_view["trace_id"], "edge_count": len(edges), "edges": edges})
        composition.append(
            {
                "trace_id": record["trace_id"],
                "scenario_group_audit_metadata": record["scenario_group"],
                "case_variant_audit_metadata": record["case_variant"],
            }
        )
    return {
        "artifact_type": "cct_causal_edge_sample_prototype",
        "extraction_scope": "sample_only_not_full_corpus",
        "sample_selection_rule": "first clean and first perturbed trace per scenario group, deterministic sorted scenario order, maximum 20 traces, no gold-label selection",
        "sample_trace_count": len(records),
        "implemented_edge_types": sorted(IMPLEMENTED_EDGE_TYPES),
        "non_implemented_edge_types": {
            "evidence_conflict_edge": "not in Task 20A required subset",
            "evidence_omission_edge": "absence-sensitive; deferred until stronger audit design",
            "correction_opportunity_edge": "diagnostic-only in Task 20 spec; deferred",
            "correction_attempt_edge": "diagnostic-only in Task 20 spec; deferred",
            "unresolved_caveat_edge": "absence-sensitive; deferred",
        },
        "sample_composition_audit_metadata": composition,
        "edge_counts_by_type": dict(Counter(edge["edge_type"] for edge in all_edges)),
        "total_edge_count": len(all_edges),
        "traces": trace_payloads,
    }


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2, sort_keys=True)
        handle.write("\n")


def write_graph_preview(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        for trace in payload["traces"]:
            handle.write(json.dumps({"trace_id": trace["trace_id"], "edges": trace["edges"]}, sort_keys=True) + "\n")


def leakage_findings(payload: dict[str, Any]) -> list[str]:
    findings = []
    all_edges = [edge for trace in payload["traces"] for edge in trace["edges"]]
    findings.extend(audit_edges_for_private_leakage(all_edges))
    serialized_edges = json.dumps(all_edges, sort_keys=True).lower()
    for forbidden in sorted(FORBIDDEN_OUTPUT_FIELDS):
        if f'"{forbidden}"' in serialized_edges:
            findings.append(f"forbidden_output_key:{forbidden}")
    return sorted(set(findings))


def template_sensitivity(payload: dict[str, Any]) -> dict[str, Any]:
    all_edges = [edge for trace in payload["traces"] for edge in trace["edges"]]
    note_counts = Counter(edge["extraction_notes"] for edge in all_edges)
    pair_counts = Counter(f"{edge['source_node_id']}->{edge['target_node_id']}" for edge in all_edges)
    type_counts = Counter(edge["edge_type"] for edge in all_edges)
    trace_edge_counts = [trace["edge_count"] for trace in payload["traces"]]
    fixed_word_edges = [edge for edge in all_edges if edge["edge_type"] == "constraint_shift_edge"]
    return {
        "repeated_extraction_notes": {k: v for k, v in note_counts.items() if v > 1},
        "repeated_source_target_patterns": {k: v for k, v in pair_counts.items() if v > 1},
        "edge_counts_by_type": dict(type_counts),
        "sample_trace_edge_count_min": min(trace_edge_counts) if trace_edge_counts else 0,
        "sample_trace_edge_count_max": max(trace_edge_counts) if trace_edge_counts else 0,
        "constraint_shift_fixed_word_edge_count": len(fixed_word_edges),
        "sparse_edge_types": sorted(edge_type for edge_type in IMPLEMENTED_EDGE_TYPES if type_counts.get(edge_type, 0) == 0),
        "dense_edge_types": sorted(edge_type for edge_type, count in type_counts.items() if count > len(payload["traces"]) * 3),
    }


def write_reports(payload: dict[str, Any]) -> None:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    findings = leakage_findings(payload)
    sensitivity = template_sensitivity(payload)
    counts = payload["edge_counts_by_type"]
    count_lines = "\n".join(f"- {edge_type}: {counts[edge_type]}" for edge_type in sorted(counts))
    visible_fields = {
        "constraint_shift_edge": "input_message, output_message, tool_output, visible_step_notes",
        "downstream_dependency_edge": "input_message, output_message, tool_output",
        "tool_alignment_edge": "tool_call, tool_output, output_message",
        "cross_agent_dependency_edge": "handoff_from, handoff_to, input_message, output_message, tool_output",
        "semantic_collision_edge": "input_message, output_message, tool_output, visible_step_notes",
    }
    visible_lines = "\n".join(f"- {edge_type}: {fields}" for edge_type, fields in sorted(visible_fields.items()))

    (REPORT_DIR / "cct_causal_edge_sample_inventory.md").write_text(
        "# CCT Causal Edge Sample Inventory\n\n"
        f"- Input corpus: `{INPUT_PATH.relative_to(ROOT)}`\n"
        f"- Sampling rule: {payload['sample_selection_rule']}\n"
        f"- Sample trace count: {payload['sample_trace_count']}\n"
        f"- Total edge count: {payload['total_edge_count']}\n"
        "- Edge counts by type:\n"
        f"{count_lines}\n\n"
        "## Visible fields used by edge type\n"
        f"{visible_lines}\n\n"
        "## Non-implemented edge types\n"
        + "\n".join(f"- {k}: {v}" for k, v in sorted(payload["non_implemented_edge_types"].items()))
        + "\n",
        encoding="utf-8",
    )

    (REPORT_DIR / "cct_causal_edge_sample_leakage_audit.md").write_text(
        "# CCT Causal Edge Sample Leakage Audit\n\n"
        f"- Leakage status: {'PASS' if not findings else 'FAIL'}\n"
        "- Extraction input: `make_full_trace_prediction_view(record)` only.\n"
        "- Raw private/provenance fields are not passed to edge extraction.\n"
        "- Scenario and perturbation metadata are used only for sample-selection/audit composition, not as extraction inputs.\n"
        f"- Findings: {len(findings)}\n"
        + ("" if not findings else "\n".join(f"  - {finding}" for finding in findings) + "\n"),
        encoding="utf-8",
    )

    (REPORT_DIR / "cct_causal_edge_sample_template_sensitivity_report.md").write_text(
        "# CCT Causal Edge Sample Template Sensitivity Report\n\n"
        f"- Sample trace edge-count min: {sensitivity['sample_trace_edge_count_min']}\n"
        f"- Sample trace edge-count max: {sensitivity['sample_trace_edge_count_max']}\n"
        f"- Sparse implemented edge types: {', '.join(sensitivity['sparse_edge_types']) or 'none'}\n"
        f"- Dense edge types: {', '.join(sensitivity['dense_edge_types']) or 'none'}\n"
        f"- Constraint-shift fixed-word edge count: {sensitivity['constraint_shift_fixed_word_edge_count']}\n"
        f"- Repeated extraction-note patterns: {len(sensitivity['repeated_extraction_notes'])}\n"
        f"- Repeated source-target patterns: {len(sensitivity['repeated_source_target_patterns'])}\n"
        "- Finding: prototype remains template-sensitive and requires a larger full-audit design before any scoring consideration.\n",
        encoding="utf-8",
    )

    (REPORT_DIR / "cct_causal_edge_sample_readiness_gate.md").write_text(
        "# CCT Causal Edge Sample Readiness Gate\n\n"
        f"- Sample trace count: {payload['sample_trace_count']}\n"
        f"- Leakage status: {'PASS' if not findings else 'FAIL'}\n"
        "- CCT_CAUSAL_FLOW_EDGE_SAMPLE_PROTOTYPE_READY_FOR_FULL_AUDIT = no\n"
        "- CCT_CAUSAL_FLOW_EDGES_READY_FOR_SCORING = no\n"
        "- Decision rationale: sample-only extraction is feasible and reviewable, but template sensitivity and limited sample scope require a stronger audit design before full-audit expansion.\n"
        "- Recommended next task: refine deterministic rules and audit criteria on sample artifacts before any full-corpus audit; scoring remains blocked.\n",
        encoding="utf-8",
    )

    if findings:
        raise RuntimeError(f"leakage audit failed: {findings}")


def main() -> int:
    records = select_sample_records()
    if len(records) > MAX_SAMPLE_TRACES:
        raise RuntimeError(f"sample exceeds max traces: {len(records)} > {MAX_SAMPLE_TRACES}")
    payload = build_sample_payload(records)
    write_json(RAW_OUTPUT_PATH, payload)
    write_graph_preview(GRAPH_OUTPUT_PATH, payload)
    write_reports(payload)
    print("Built sample-only CCT causal edge prototype")
    print(f"sample_traces={payload['sample_trace_count']} total_edges={payload['total_edge_count']}")
    print("edge_counts_by_type=" + json.dumps(payload["edge_counts_by_type"], sort_keys=True))
    print(f"raw_output={RAW_OUTPUT_PATH.relative_to(ROOT)}")
    print(f"graph_preview={GRAPH_OUTPUT_PATH.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
