#!/usr/bin/env python3
"""Build representation-only redesigned CCT graph artifacts.

Task 24 integrates the three authorized strong causal-flow edge types into
redesigned graph artifacts. It does not score, rank, compare to gold/H6 labels,
calibrate, ablate, run statistical tests, or produce paper-ready result tables.
"""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from cctdiag.cct.redesigned_builder import (  # noqa: E402
    STRONG_CAUSAL_EDGE_TYPES,
    base_graph_signature,
    build_redesigned_cct_graph,
    redesigned_graph_signature,
)
from cctdiag.cct.redesigned_validation import redesigned_graph_leakage_findings, validate_redesigned_graph  # noqa: E402
from cctdiag.io.full_trace_views import make_full_trace_prediction_view  # noqa: E402

INPUT_PATH = ROOT / "data/processed/journal_v1_full_trace/main_full_trace_all.jsonl"
OUTPUT_DIR = ROOT / "data/interim/journal_v1_full_trace_cct_redesigned"
GRAPH_OUTPUT_PATH = OUTPUT_DIR / "cct_redesigned_graphs.jsonl"
SAMPLE_GRAPH_OUTPUT_PATH = OUTPUT_DIR / "sample_cct_redesigned_graphs.jsonl"
INVENTORY_JSON_PATH = OUTPUT_DIR / "cct_redesigned_graph_inventory.json"
MANIFEST_PATH = ROOT / "docs/artifact_manifests/cct_redesigned_graphs_manifest.md"
REPORT_DIR = ROOT / "results/reports/journal_v1_full_trace_cct_redesigned"


def run_git(args: list[str]) -> str:
    result = subprocess.run(["git", *args], cwd=ROOT, check=False, text=True, capture_output=True)
    return result.stdout.strip()


def iter_records():
    with INPUT_PATH.open("r", encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                yield json.loads(line)


def build_graphs() -> tuple[list[dict[str, Any]], list[dict[str, str]]]:
    graphs = []
    metadata = []
    for record in iter_records():
        prediction_view = make_full_trace_prediction_view(record)
        graph = build_redesigned_cct_graph(prediction_view)
        validate_redesigned_graph(graph)
        graphs.append(graph)
        metadata.append(
            {
                "trace_id": record["trace_id"],
                "scenario_group_audit_metadata": record["scenario_group"],
                "perturbation_type_audit_metadata": record["perturbation_type"],
                "case_variant_audit_metadata": record["case_variant"],
            }
        )
    return graphs, metadata


def summarize(graphs: list[dict[str, Any]], metadata: list[dict[str, str]]) -> dict[str, Any]:
    base_signatures = Counter(base_graph_signature(graph) for graph in graphs)
    redesigned_signatures = Counter(redesigned_graph_signature(graph) for graph in graphs)
    node_counts = Counter(graph["node_count"] for graph in graphs)
    base_edge_counts = Counter(graph["base_edge_count"] for graph in graphs)
    causal_edge_counts = Counter(graph["causal_flow_edge_count"] for graph in graphs)
    total_edge_counts = Counter(graph["total_edge_count"] for graph in graphs)
    edge_type_counts = Counter()
    for graph in graphs:
        edge_type_counts.update(graph["edge_type_counts"])
    clean_ids = {item["trace_id"] for item in metadata if item["case_variant_audit_metadata"] == "clean"}
    clean_signatures = Counter(redesigned_graph_signature(graph) for graph in graphs if graph["trace_id"] in clean_ids)
    perturbed_signatures = Counter(redesigned_graph_signature(graph) for graph in graphs if graph["trace_id"] not in clean_ids)
    scenario_counts = Counter(item["scenario_group_audit_metadata"] for item in metadata)
    perturbation_counts = Counter(item["perturbation_type_audit_metadata"] for item in metadata)
    return {
        "total_traces_processed": len(graphs),
        "total_redesigned_graphs": len(graphs),
        "node_count_distribution": dict(sorted(node_counts.items())),
        "base_edge_count_distribution": dict(sorted(base_edge_counts.items())),
        "causal_flow_edge_count_distribution": dict(sorted(causal_edge_counts.items())),
        "total_edge_count_distribution": dict(sorted(total_edge_counts.items())),
        "edge_counts_by_type": dict(sorted(edge_type_counts.items())),
        "base_graph_signature_unique_count": len(base_signatures),
        "redesigned_graph_signature_unique_count": len(redesigned_signatures),
        "base_duplicate_graph_signature_count": sum(count - 1 for count in base_signatures.values() if count > 1),
        "redesigned_duplicate_graph_signature_count": sum(count - 1 for count in redesigned_signatures.values() if count > 1),
        "clean_redesigned_signature_unique_count": len(clean_signatures),
        "perturbed_redesigned_signature_unique_count": len(perturbed_signatures),
        "scenario_group_distribution": dict(sorted(scenario_counts.items())),
        "perturbation_type_distribution": dict(sorted(perturbation_counts.items())),
        "template_sensitivity_carryover": {
            "from_task23_repeated_relation_note_patterns": 74,
            "from_task23_repeated_source_target_patterns": 3,
            "carryover_status": "present_audit_condition",
        },
    }


def write_jsonl(path: Path, graphs: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        for graph in graphs:
            handle.write(json.dumps(graph, sort_keys=True) + "\n")


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def sample_graphs(graphs: list[dict[str, Any]], metadata: list[dict[str, str]]) -> list[dict[str, Any]]:
    selected = []
    seen = set()
    graph_by_trace = {graph["trace_id"]: graph for graph in graphs}
    for item in metadata:
        variant = "clean" if item["case_variant_audit_metadata"] == "clean" else "perturbed"
        if variant not in seen:
            seen.add(variant)
            selected.append(graph_by_trace[item["trace_id"]])
        if seen == {"clean", "perturbed"}:
            break
    return selected


def artifact_stats(path: Path) -> dict[str, Any]:
    data = path.read_bytes()
    return {"sha256": hashlib.sha256(data).hexdigest(), "bytes": len(data), "lines": path.read_text(encoding="utf-8").count("\n")}


def write_manifest(full_stats: dict[str, Any], sample_stats: dict[str, Any], inventory_stats: dict[str, Any], summary: dict[str, Any]) -> None:
    MANIFEST_PATH.parent.mkdir(parents=True, exist_ok=True)
    MANIFEST_PATH.write_text(
        "# CCT Redesigned Graph Artifact Manifest\n\n"
        "## Artifact policy\n\n"
        "The full redesigned graph JSONL is a generated representation artifact and is excluded from normal Git review to avoid oversized diffs. It is reproducible with `python scripts/build_cct_redesigned_graphs.py`. The compact sample graph JSONL, inventory JSON, reports, and manifest are tracked.\n\n"
        "## Generation command\n\n```bash\npython scripts/build_cct_redesigned_graphs.py\n```\n\n"
        "## Expected outputs\n\n"
        f"- Full local graphs: `{GRAPH_OUTPUT_PATH.relative_to(ROOT)}`\n"
        f"- Tracked sample graphs: `{SAMPLE_GRAPH_OUTPUT_PATH.relative_to(ROOT)}`\n"
        f"- Tracked inventory JSON: `{INVENTORY_JSON_PATH.relative_to(ROOT)}`\n"
        f"- Total redesigned graphs expected: {summary['total_redesigned_graphs']}\n"
        "- Causal-flow edge types: `downstream_dependency_edge`, `tool_alignment_edge`, `cross_agent_dependency_edge`\n\n"
        "## Artifact stats\n\n"
        "| Artifact | SHA256 | Lines | Bytes | Git policy |\n"
        "| --- | --- | ---: | ---: | --- |\n"
        f"| `{GRAPH_OUTPUT_PATH.relative_to(ROOT)}` | `{full_stats['sha256']}` | {full_stats['lines']} | {full_stats['bytes']} | generated locally; ignored by normal Git |\n"
        f"| `{SAMPLE_GRAPH_OUTPUT_PATH.relative_to(ROOT)}` | `{sample_stats['sha256']}` | {sample_stats['lines']} | {sample_stats['bytes']} | tracked compact review sample |\n"
        f"| `{INVENTORY_JSON_PATH.relative_to(ROOT)}` | `{inventory_stats['sha256']}` | {inventory_stats['lines']} | {inventory_stats['bytes']} | tracked compact inventory |\n\n"
        "## Prohibitions\n\nThis manifest does not authorize scoring, ranking, gold/H6 comparison, calibration, ablation, statistical tests, or paper-ready result tables.\n",
        encoding="utf-8",
    )


def dist_lines(distribution: dict[Any, int]) -> str:
    return "\n".join(f"- {key}: {value}" for key, value in distribution.items())


def write_reports(summary: dict[str, Any], leakage_findings: list[str]) -> None:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    edge_lines = dist_lines(summary["edge_counts_by_type"])
    scenario_lines = dist_lines(summary["scenario_group_distribution"])
    perturbation_lines = dist_lines(summary["perturbation_type_distribution"])
    (REPORT_DIR / "cct_redesigned_graph_inventory.md").write_text(
        "# CCT Redesigned Graph Inventory\n\n"
        f"- Branch: `{run_git(['branch', '--show-current'])}`\n"
        f"- HEAD before build: `{run_git(['rev-parse', 'HEAD'])}`\n"
        f"- `configs/cct_scoring.yaml` exists: {(ROOT / 'configs/cct_scoring.yaml').exists()}\n"
        "- Task 18 reproducibility status: `NOT_REPRODUCIBLE_FROM_CURRENT_CHECKOUT`\n"
        "- Scope: representation-only graph integration; no scoring dependency.\n"
        f"- Total traces processed: {summary['total_traces_processed']}\n"
        f"- Total redesigned graphs: {summary['total_redesigned_graphs']}\n"
        f"- Full local graphs: `{GRAPH_OUTPUT_PATH.relative_to(ROOT)}` (generated, ignored by Git)\n"
        f"- Tracked sample graphs: `{SAMPLE_GRAPH_OUTPUT_PATH.relative_to(ROOT)}`\n"
        f"- Tracked inventory JSON: `{INVENTORY_JSON_PATH.relative_to(ROOT)}`\n\n"
        "## Edge counts by type\n"
        f"{edge_lines}\n",
        encoding="utf-8",
    )
    (REPORT_DIR / "cct_redesigned_graph_leakage_audit.md").write_text(
        "# CCT Redesigned Graph Leakage Audit\n\n"
        f"- Leakage status: {'PASS' if not leakage_findings else 'FAIL'}\n"
        "- Graph construction input: `make_full_trace_prediction_view(record)` only.\n"
        "- No private/gold/H6/provenance/scoring fields are present in graph output.\n"
        "- Scenario, perturbation, and case-variant metadata are not graph construction inputs.\n"
        "- Audit metadata is excluded from future scoring unless separately authorized.\n"
        f"- Findings: {len(leakage_findings)}\n"
        + ("" if not leakage_findings else "\n".join(f"  - {finding}" for finding in leakage_findings) + "\n"),
        encoding="utf-8",
    )
    (REPORT_DIR / "cct_redesigned_graph_diversity_report.md").write_text(
        "# CCT Redesigned Graph Diversity Report\n\n"
        "## Count distributions\n"
        "### Node counts\n"
        f"{dist_lines(summary['node_count_distribution'])}\n\n"
        "### Base edge counts\n"
        f"{dist_lines(summary['base_edge_count_distribution'])}\n\n"
        "### Causal-flow edge counts\n"
        f"{dist_lines(summary['causal_flow_edge_count_distribution'])}\n\n"
        "### Total edge counts\n"
        f"{dist_lines(summary['total_edge_count_distribution'])}\n\n"
        "## Audit-only metadata distributions\n"
        "### Scenario group\n"
        f"{scenario_lines}\n\n"
        "### Perturbation type\n"
        f"{perturbation_lines}\n\n"
        f"- Clean redesigned signature unique count: {summary['clean_redesigned_signature_unique_count']}\n"
        f"- Perturbed redesigned signature unique count: {summary['perturbed_redesigned_signature_unique_count']}\n",
        encoding="utf-8",
    )
    before = summary["base_graph_signature_unique_count"]
    after = summary["redesigned_graph_signature_unique_count"]
    before_dup = summary["base_duplicate_graph_signature_count"]
    after_dup = summary["redesigned_duplicate_graph_signature_count"]
    (REPORT_DIR / "cct_redesigned_graph_degeneracy_report.md").write_text(
        "# CCT Redesigned Graph Degeneracy Report\n\n"
        f"- Graph signature uniqueness before causal-flow edges: {before}\n"
        f"- Graph signature uniqueness after causal-flow edges: {after}\n"
        f"- Duplicate graph signature count before causal-flow edges: {before_dup}\n"
        f"- Duplicate graph signature count after causal-flow edges: {after_dup}\n"
        f"- Strong edges reduce graph degeneracy: {'yes' if after > before and after_dup < before_dup else 'no'}\n"
        f"- Template sensitivity carryover from Task 23 relation-note patterns: {summary['template_sensitivity_carryover']['from_task23_repeated_relation_note_patterns']}\n"
        f"- Template sensitivity carryover from Task 23 source-target patterns: {summary['template_sensitivity_carryover']['from_task23_repeated_source_target_patterns']}\n"
        "- Interpretation: redesigned graphs are more diverse than base sequence/handoff graphs, but repeated templates remain an audit condition before any feature audit.\n",
        encoding="utf-8",
    )
    ready = not leakage_findings and after > before and after_dup < before_dup
    (REPORT_DIR / "cct_redesigned_readiness_gate.md").write_text(
        "# CCT Redesigned Graph Readiness Gate\n\n"
        f"- CCT_REDESIGNED_GRAPHS_READY_FOR_FEATURE_AUDIT = {'yes' if ready else 'no'}\n"
        "- CCT_REDESIGNED_GRAPHS_READY_FOR_SCORING = no\n"
        f"- Leakage status: {'PASS' if not leakage_findings else 'FAIL'}\n"
        f"- Total redesigned graphs: {summary['total_redesigned_graphs']}\n"
        "- Decision rationale: redesigned graphs integrate the three full-corpus-audited strong causal-flow edge types and reduce graph-signature degeneracy under representation-only constraints. This authorizes only a future representation-only feature audit, not scoring.\n"
        "- Remaining blockers before scoring: missing frozen scoring-config provenance, no scoring protocol authorization, and no future feature-validity audit.\n",
        encoding="utf-8",
    )


def main() -> int:
    graphs, metadata = build_graphs()
    findings = redesigned_graph_leakage_findings(graphs)
    summary = summarize(graphs, metadata)
    inventory_payload = {"artifact_type": "cct_redesigned_graph_inventory", "summary": summary, "trace_audit_metadata": metadata}
    write_jsonl(GRAPH_OUTPUT_PATH, graphs)
    write_jsonl(SAMPLE_GRAPH_OUTPUT_PATH, sample_graphs(graphs, metadata))
    write_json(INVENTORY_JSON_PATH, inventory_payload)
    full_stats = artifact_stats(GRAPH_OUTPUT_PATH)
    sample_stats = artifact_stats(SAMPLE_GRAPH_OUTPUT_PATH)
    inventory_stats = artifact_stats(INVENTORY_JSON_PATH)
    write_manifest(full_stats, sample_stats, inventory_stats, summary)
    write_reports(summary, findings)
    if findings:
        raise RuntimeError(f"redesigned graph leakage findings: {findings}")
    print("Built representation-only redesigned CCT graphs")
    print(f"total_graphs={summary['total_redesigned_graphs']}")
    print("edge_counts_by_type=" + json.dumps(summary["edge_counts_by_type"], sort_keys=True))
    print(f"base_unique={summary['base_graph_signature_unique_count']} redesigned_unique={summary['redesigned_graph_signature_unique_count']}")
    print(f"graphs={GRAPH_OUTPUT_PATH.relative_to(ROOT)}")
    print(f"sample={SAMPLE_GRAPH_OUTPUT_PATH.relative_to(ROOT)}")
    print(f"inventory={INVENTORY_JSON_PATH.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
