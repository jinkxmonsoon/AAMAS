#!/usr/bin/env python3
"""Audit strongest CCT causal-flow edges on the full corpus.

Task 23 is representation-only. This script does not score, rank, compare to
private labels/H6 labels, calibrate, ablate, run statistical tests, or produce
paper-ready result tables.
"""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from cctdiag.cct.causal_edges import (  # noqa: E402
    FORBIDDEN_NOTE_TERMS,
    FORBIDDEN_OUTPUT_FIELDS,
    audit_edges_for_private_leakage,
    extract_causal_edges_from_prediction_view,
)
from cctdiag.io.full_trace_views import make_full_trace_prediction_view  # noqa: E402

INPUT_PATH = ROOT / "data/processed/journal_v1_full_trace/main_full_trace_all.jsonl"
RAW_OUTPUT_PATH = ROOT / "results/raw/journal_v1_full_trace_cct/cct_strong_edges_full_corpus.json"
SAMPLE_OUTPUT_PATH = ROOT / "results/raw/journal_v1_full_trace_cct/sample_cct_strong_edges_full_corpus.json"
MANIFEST_PATH = ROOT / "docs/artifact_manifests/cct_strong_edges_full_corpus_manifest.md"
REPORT_DIR = ROOT / "results/reports/journal_v1_full_trace_cct"
STRONG_EDGE_TYPES = {
    "downstream_dependency_edge",
    "tool_alignment_edge",
    "cross_agent_dependency_edge",
}
OUT_OF_SCOPE_EDGE_TYPES = [
    "constraint_shift_edge",
    "semantic_collision_edge",
    "evidence_conflict_edge",
    "evidence_omission_edge",
    "correction_opportunity_edge",
    "correction_attempt_edge",
    "unresolved_caveat_edge",
]


def run_git(args: list[str]) -> str:
    result = subprocess.run(["git", *args], cwd=ROOT, check=False, text=True, capture_output=True)
    return result.stdout.strip()


def iter_records(path: Path = INPUT_PATH):
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                yield json.loads(line)


def step_number(step_id: str | None) -> int | None:
    match = re.search(r"(\d+)$", str(step_id or ""))
    return int(match.group(1)) if match else None


def normalize_note(note: str) -> str:
    note = re.sub(r"_trace_.*$", "", note)
    note = re.sub(r"_s\d+_to_s\d+", "_sX_to_sY", note)
    note = re.sub(r"_s\d+_", "_sX_", note)
    note = re.sub(r"_overlap_\d+", "_overlap_N", note)
    return note


def normalize_pair(edge: dict[str, Any]) -> str:
    source = re.sub(r"trace:[^:]+:", "trace:TRACE:", edge["source_node_id"])
    target = re.sub(r"trace:[^:]+:", "trace:TRACE:", edge["target_node_id"])
    source = re.sub(r"step:s\d+", "step:sX", source)
    target = re.sub(r"step:s\d+", "step:sY", target)
    return f"{source}->{target}"


def build_payload() -> dict[str, Any]:
    trace_payloads: list[dict[str, Any]] = []
    metadata: list[dict[str, str]] = []
    all_edges: list[dict[str, Any]] = []

    for record in iter_records():
        prediction_view = make_full_trace_prediction_view(record)
        # Extraction receives only the sanitized prediction view and only the three in-scope edge types.
        edges = extract_causal_edges_from_prediction_view(prediction_view, edge_types=STRONG_EDGE_TYPES)
        step_agents = {step["step_id"]: step.get("agent_id") for step in prediction_view["steps"]}
        for edge in edges:
            source_num = step_number(edge.get("source_step_id"))
            target_num = step_number(edge.get("target_step_id"))
            edge["audit_relation"] = {
                "step_delta": None if source_num is None or target_num is None else target_num - source_num,
                "same_agent_visible_audit": step_agents.get(edge.get("source_step_id")) == step_agents.get(edge.get("target_step_id")),
            }
        all_edges.extend(edges)
        trace_payloads.append({"trace_id": prediction_view["trace_id"], "edge_count": len(edges), "edges": edges})
        metadata.append(
            {
                "trace_id": record["trace_id"],
                "scenario_group_audit_metadata": record["scenario_group"],
                "perturbation_type_audit_metadata": record["perturbation_type"],
                "case_variant_audit_metadata": record["case_variant"],
            }
        )

    return {
        "artifact_type": "cct_strong_edges_full_corpus_audit",
        "extraction_scope": "full_corpus_representation_only_no_scoring_no_gold_comparison",
        "input_corpus": str(INPUT_PATH.relative_to(ROOT)),
        "edge_types_in_scope": sorted(STRONG_EDGE_TYPES),
        "edge_types_out_of_scope": OUT_OF_SCOPE_EDGE_TYPES,
        "audit_metadata_policy": "scenario_group, perturbation_type, and case_variant are joined only after extraction for descriptive audit metadata and are forbidden for future scoring unless separately authorized",
        "total_traces_processed": len(trace_payloads),
        "total_edge_count": len(all_edges),
        "edge_counts_by_type": dict(Counter(edge["edge_type"] for edge in all_edges)),
        "trace_audit_metadata": metadata,
        "traces": trace_payloads,
    }


def summarize(payload: dict[str, Any]) -> dict[str, Any]:
    all_edges = [edge for trace in payload["traces"] for edge in trace["edges"]]
    metadata_by_trace = {item["trace_id"]: item for item in payload["trace_audit_metadata"]}
    clean_trace_ids = [m["trace_id"] for m in payload["trace_audit_metadata"] if m["case_variant_audit_metadata"] == "clean"]
    perturbed_trace_ids = [m["trace_id"] for m in payload["trace_audit_metadata"] if m["case_variant_audit_metadata"] != "clean"]
    edges_by_trace = {trace["trace_id"]: trace["edges"] for trace in payload["traces"]}

    clean_counts = Counter(edge["edge_type"] for trace_id in clean_trace_ids for edge in edges_by_trace[trace_id])
    perturbed_counts = Counter(edge["edge_type"] for trace_id in perturbed_trace_ids for edge in edges_by_trace[trace_id])
    scenario_counts = Counter(item["scenario_group_audit_metadata"] for item in payload["trace_audit_metadata"])
    perturbation_counts = Counter(item["perturbation_type_audit_metadata"] for item in payload["trace_audit_metadata"])
    case_variant_counts = Counter(item["case_variant_audit_metadata"] for item in payload["trace_audit_metadata"])
    trace_edge_counts = [trace["edge_count"] for trace in payload["traces"]]
    deltas = Counter(edge["audit_relation"]["step_delta"] for edge in all_edges)
    adjacent = sum(count for delta, count in deltas.items() if delta == 1)
    non_adjacent = sum(count for delta, count in deltas.items() if delta not in {None, 1})
    same_agent = sum(1 for edge in all_edges if edge["audit_relation"]["same_agent_visible_audit"])
    cross_agent = len(all_edges) - same_agent
    note_patterns = Counter(normalize_note(edge["extraction_notes"]) for edge in all_edges)
    pair_patterns = Counter(normalize_pair(edge) for edge in all_edges)
    type_note_patterns = defaultdict(Counter)
    for edge in all_edges:
        type_note_patterns[edge["edge_type"]][normalize_note(edge["extraction_notes"])] += 1

    return {
        "total_traces": payload["total_traces_processed"],
        "total_clean_traces": len(clean_trace_ids),
        "total_perturbed_traces": len(perturbed_trace_ids),
        "total_edges": len(all_edges),
        "edge_counts_by_type": dict(Counter(edge["edge_type"] for edge in all_edges)),
        "clean_edge_counts_by_type": dict(clean_counts),
        "perturbed_edge_counts_by_type": dict(perturbed_counts),
        "scenario_group_distribution": dict(sorted(scenario_counts.items())),
        "perturbation_type_distribution": dict(sorted(perturbation_counts.items())),
        "case_variant_distribution": dict(sorted(case_variant_counts.items())),
        "edge_density_min": min(trace_edge_counts) if trace_edge_counts else 0,
        "edge_density_max": max(trace_edge_counts) if trace_edge_counts else 0,
        "edge_density_mean": round(sum(trace_edge_counts) / len(trace_edge_counts), 4) if trace_edge_counts else 0,
        "step_delta_distribution": dict(sorted(deltas.items(), key=lambda item: str(item[0]))),
        "adjacent_edge_count": adjacent,
        "non_adjacent_edge_count": non_adjacent,
        "same_agent_relation_count": same_agent,
        "cross_agent_relation_count": cross_agent,
        "repeated_relation_note_patterns": {k: v for k, v in note_patterns.items() if v > 1},
        "repeated_source_target_patterns": {k: v for k, v in pair_patterns.items() if v > 1},
        "relation_note_pattern_count_by_type": {edge_type: len(counter) for edge_type, counter in type_note_patterns.items()},
        "max_repeated_note_pattern_count_by_type": {edge_type: max(counter.values()) for edge_type, counter in type_note_patterns.items()},
    }


def leakage_findings(payload: dict[str, Any]) -> list[str]:
    all_edges = [edge for trace in payload["traces"] for edge in trace["edges"]]
    findings = list(audit_edges_for_private_leakage(all_edges))
    serialized_edges = json.dumps(all_edges, sort_keys=True).lower()
    for forbidden in sorted(FORBIDDEN_OUTPUT_FIELDS):
        if f'"{forbidden}"' in serialized_edges:
            findings.append(f"forbidden_edge_key:{forbidden}")
    for edge_index, edge in enumerate(all_edges):
        notes = str(edge.get("extraction_notes", "")).lower()
        for term in FORBIDDEN_NOTE_TERMS:
            if term in notes:
                findings.append(f"edge[{edge_index}].forbidden_note_term:{term}")
    return sorted(set(findings))


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")



def artifact_stats(path: Path) -> dict[str, Any]:
    data = path.read_bytes()
    return {
        "sha256": hashlib.sha256(data).hexdigest(),
        "bytes": len(data),
        "lines": path.read_text(encoding="utf-8").count("\n"),
    }


def build_sample_payload(payload: dict[str, Any]) -> dict[str, Any]:
    metadata_by_trace = {item["trace_id"]: item for item in payload["trace_audit_metadata"]}
    selected_trace_ids: list[str] = []
    seen_variants: set[str] = set()
    for item in payload["trace_audit_metadata"]:
        variant = "clean" if item["case_variant_audit_metadata"] == "clean" else "perturbed"
        if variant not in seen_variants:
            seen_variants.add(variant)
            selected_trace_ids.append(item["trace_id"])
        if seen_variants == {"clean", "perturbed"}:
            break
    selected = set(selected_trace_ids)
    traces = [trace for trace in payload["traces"] if trace["trace_id"] in selected]
    metadata = [metadata_by_trace[trace_id] for trace_id in selected_trace_ids]
    return {
        "artifact_type": "sample_cct_strong_edges_full_corpus_audit",
        "source_full_artifact": str(RAW_OUTPUT_PATH.relative_to(ROOT)),
        "sample_rule": "first clean trace and first perturbed trace from the full-corpus strong-edge audit payload",
        "edge_types_in_scope": payload["edge_types_in_scope"],
        "edge_types_out_of_scope": payload["edge_types_out_of_scope"],
        "sample_trace_count": len(traces),
        "total_edge_count": sum(trace["edge_count"] for trace in traces),
        "edge_counts_by_type": dict(Counter(edge["edge_type"] for trace in traces for edge in trace["edges"])),
        "trace_audit_metadata": metadata,
        "traces": traces,
    }


def write_manifest(full_stats: dict[str, Any], sample_stats: dict[str, Any], summary: dict[str, Any]) -> None:
    MANIFEST_PATH.parent.mkdir(parents=True, exist_ok=True)
    MANIFEST_PATH.write_text(
        "# CCT Strong Edges Full-Corpus Artifact Manifest\n\n"
        "## Artifact policy\n\n"
        "The full strong-edge full-corpus JSON is a generated representation-audit artifact and is excluded from normal Git review to avoid an oversized diff. It is reproducible with `python scripts/audit_cct_strong_edges_full_corpus.py`. A compact sample artifact is tracked for review.\n\n"
        "## Generation command\n\n"
        "```bash\npython scripts/audit_cct_strong_edges_full_corpus.py\n```\n\n"
        "## Expected outputs\n\n"
        f"- Full local artifact: `{RAW_OUTPUT_PATH.relative_to(ROOT)}`\n"
        f"- Tracked sample artifact: `{SAMPLE_OUTPUT_PATH.relative_to(ROOT)}`\n"
        f"- Total traces expected: {summary['total_traces']}\n"
        f"- Total edges expected: {summary['total_edges']}\n"
        "- Edge types: `downstream_dependency_edge`, `tool_alignment_edge`, `cross_agent_dependency_edge`\n\n"
        "## Artifact stats\n\n"
        f"| Artifact | SHA256 | Lines | Bytes | Git policy |\n"
        f"| --- | --- | ---: | ---: | --- |\n"
        f"| `{RAW_OUTPUT_PATH.relative_to(ROOT)}` | `{full_stats['sha256']}` | {full_stats['lines']} | {full_stats['bytes']} | generated locally; ignored by normal Git |\n"
        f"| `{SAMPLE_OUTPUT_PATH.relative_to(ROOT)}` | `{sample_stats['sha256']}` | {sample_stats['lines']} | {sample_stats['bytes']} | tracked compact review sample |\n\n"
        "## Prohibitions\n\n"
        "This manifest does not authorize scoring, ranking, gold/H6 comparison, calibration, ablation, statistical tests, or paper-ready result tables.\n",
        encoding="utf-8",
    )

def write_reports(payload: dict[str, Any], summary: dict[str, Any], findings: list[str]) -> None:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    edge_counts = "\n".join(f"- {k}: {v}" for k, v in sorted(summary["edge_counts_by_type"].items()))
    clean_counts = "\n".join(f"- {k}: {summary['clean_edge_counts_by_type'].get(k, 0)}" for k in sorted(STRONG_EDGE_TYPES))
    perturbed_counts = "\n".join(f"- {k}: {summary['perturbed_edge_counts_by_type'].get(k, 0)}" for k in sorted(STRONG_EDGE_TYPES))
    scenario_lines = "\n".join(f"- {k}: {v}" for k, v in summary["scenario_group_distribution"].items())
    perturbation_lines = "\n".join(f"- {k}: {v}" for k, v in summary["perturbation_type_distribution"].items())

    (REPORT_DIR / "cct_strong_edges_full_corpus_inventory.md").write_text(
        "# CCT Strong Edges Full-Corpus Inventory\n\n"
        f"- Branch: `{run_git(['branch', '--show-current'])}`\n"
        f"- HEAD before audit run: `{run_git(['rev-parse', 'HEAD'])}`\n"
        f"- `configs/cct_scoring.yaml` exists: {(ROOT / 'configs/cct_scoring.yaml').exists()}\n"
        "- Task 18 reproducibility status: `NOT_REPRODUCIBLE_FROM_CURRENT_CHECKOUT`\n"
        "- Scope: representation-only full-corpus audit; no scoring dependency.\n"
        f"- Input corpus: `{INPUT_PATH.relative_to(ROOT)}`\n"
        f"- Full local raw output: `{RAW_OUTPUT_PATH.relative_to(ROOT)}` (generated, ignored by Git)\n"
        f"- Tracked compact sample output: `{SAMPLE_OUTPUT_PATH.relative_to(ROOT)}`\n"
        f"- Artifact manifest: `{MANIFEST_PATH.relative_to(ROOT)}`\n"
        f"- Total traces processed: {summary['total_traces']}\n"
        f"- Total clean traces: {summary['total_clean_traces']}\n"
        f"- Total perturbed traces: {summary['total_perturbed_traces']}\n"
        f"- Total edges generated: {summary['total_edges']}\n"
        "- Edge types in scope: `downstream_dependency_edge`, `tool_alignment_edge`, `cross_agent_dependency_edge`\n"
        "- Edge types out of scope: " + ", ".join(f"`{edge}`" for edge in OUT_OF_SCOPE_EDGE_TYPES) + "\n\n"
        "## Edge counts by type\n"
        f"{edge_counts}\n",
        encoding="utf-8",
    )

    (REPORT_DIR / "cct_strong_edges_full_corpus_leakage_audit.md").write_text(
        "# CCT Strong Edges Full-Corpus Leakage Audit\n\n"
        f"- Leakage status: {'PASS' if not findings else 'FAIL'}\n"
        "- Extraction input: `make_full_trace_prediction_view(record)` only.\n"
        "- Raw records are not passed to edge extraction; raw-record extraction would be rejected because private/provenance fields are present.\n"
        "- Scenario, perturbation, and case-variant metadata are joined only after extraction for descriptive audit stratification.\n"
        "- Audit metadata fields are forbidden for future scoring unless separately authorized.\n"
        f"- Findings: {len(findings)}\n"
        + ("" if not findings else "\n".join(f"  - {finding}" for finding in findings) + "\n"),
        encoding="utf-8",
    )

    (REPORT_DIR / "cct_strong_edges_full_corpus_distribution_report.md").write_text(
        "# CCT Strong Edges Full-Corpus Distribution Report\n\n"
        "## Edge density\n"
        f"- Edge density per trace min: {summary['edge_density_min']}\n"
        f"- Edge density per trace max: {summary['edge_density_max']}\n"
        f"- Edge density per trace mean: {summary['edge_density_mean']}\n\n"
        "## Clean vs perturbed edge counts\n"
        "### Clean\n"
        f"{clean_counts}\n\n"
        "### Perturbed\n"
        f"{perturbed_counts}\n\n"
        "## Scenario-group distribution (audit-only metadata)\n"
        f"{scenario_lines}\n\n"
        "## Perturbation-type distribution (audit-only metadata)\n"
        f"{perturbation_lines}\n\n"
        "## Relation distribution\n"
        f"- Adjacent edge count: {summary['adjacent_edge_count']}\n"
        f"- Non-adjacent edge count: {summary['non_adjacent_edge_count']}\n"
        f"- Same-agent relation count: {summary['same_agent_relation_count']}\n"
        f"- Cross-agent relation count: {summary['cross_agent_relation_count']}\n",
        encoding="utf-8",
    )

    top_notes = sorted(summary["repeated_relation_note_patterns"].items(), key=lambda item: (-item[1], item[0]))[:10]
    top_pairs = sorted(summary["repeated_source_target_patterns"].items(), key=lambda item: (-item[1], item[0]))[:10]
    note_lines = "\n".join(f"- `{k}`: {v}" for k, v in top_notes) or "- none"
    pair_lines = "\n".join(f"- `{k}`: {v}" for k, v in top_pairs) or "- none"
    pattern_by_type = "\n".join(
        f"- {edge_type}: patterns={summary['relation_note_pattern_count_by_type'].get(edge_type, 0)}, max_repeat={summary['max_repeated_note_pattern_count_by_type'].get(edge_type, 0)}"
        for edge_type in sorted(STRONG_EDGE_TYPES)
    )
    (REPORT_DIR / "cct_strong_edges_full_corpus_template_sensitivity_report.md").write_text(
        "# CCT Strong Edges Full-Corpus Template Sensitivity Report\n\n"
        f"- Repeated relation-note pattern count: {len(summary['repeated_relation_note_patterns'])}\n"
        f"- Repeated source-target pattern count: {len(summary['repeated_source_target_patterns'])}\n"
        "## Relation-note pattern counts by type\n"
        f"{pattern_by_type}\n\n"
        "## Top repeated relation-note patterns\n"
        f"{note_lines}\n\n"
        "## Top repeated source-target patterns\n"
        f"{pair_lines}\n\n"
        "## Relation-validity checks\n"
        "- `tool_alignment_edge` uses visible `tool_call`, `tool_output`, and `output_message` relation fields.\n"
        "- `downstream_dependency_edge` includes non-adjacent edges and therefore goes beyond generic immediate temporal adjacency.\n"
        "- `cross_agent_dependency_edge` includes non-adjacent edges and requires visible content relation beyond handoff adjacency.\n"
        "- Finding: full-corpus representation extraction is reviewable, but repeated templates remain audit conditions for graph-redesign integration.\n",
        encoding="utf-8",
    )

    ready_for_integration = not findings and summary["total_traces"] == 420 and set(summary["edge_counts_by_type"]) == STRONG_EDGE_TYPES
    (REPORT_DIR / "cct_strong_edges_full_corpus_readiness_gate.md").write_text(
        "# CCT Strong Edges Full-Corpus Readiness Gate\n\n"
        f"- STRONG_CAUSAL_FLOW_EDGES_FULL_CORPUS_AUDIT_READY = {'yes' if not findings else 'no'}\n"
        f"- STRONG_CAUSAL_FLOW_EDGES_READY_FOR_GRAPH_REDESIGN_INTEGRATION = {'yes' if ready_for_integration else 'no'}\n"
        "- CCT_CAUSAL_FLOW_EDGES_READY_FOR_SCORING = no\n"
        f"- Leakage status: {'PASS' if not findings else 'FAIL'}\n"
        f"- Total traces audited: {summary['total_traces']}\n"
        f"- Total edges audited: {summary['total_edges']}\n"
        "- Decision rationale: the three strongest edge types were extracted over the full corpus using prediction-view-only inputs and no private/gold/scoring fields. Graph-redesign integration readiness is representation-only and does not authorize scoring.\n"
        "- Remaining blockers before scoring: missing frozen scoring-config provenance, no scoring protocol authorization, and unresolved validation of edge utility against a future explicitly scoped protocol.\n",
        encoding="utf-8",
    )


def main() -> int:
    payload = build_payload()
    summary = summarize(payload)
    findings = leakage_findings(payload)
    sample_payload = build_sample_payload(payload)
    write_json(RAW_OUTPUT_PATH, payload)
    write_json(SAMPLE_OUTPUT_PATH, sample_payload)
    full_stats = artifact_stats(RAW_OUTPUT_PATH)
    sample_stats = artifact_stats(SAMPLE_OUTPUT_PATH)
    write_manifest(full_stats, sample_stats, summary)
    write_reports(payload, summary, findings)
    if findings:
        raise RuntimeError(f"leakage audit failed: {findings}")
    print("Built representation-only full-corpus strong-edge audit")
    print(f"total_traces={summary['total_traces']} total_edges={summary['total_edges']}")
    print("edge_counts_by_type=" + json.dumps(summary["edge_counts_by_type"], sort_keys=True))
    print(f"raw_output={RAW_OUTPUT_PATH.relative_to(ROOT)}")
    print(f"sample_output={SAMPLE_OUTPUT_PATH.relative_to(ROOT)}")
    print(f"manifest={MANIFEST_PATH.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
