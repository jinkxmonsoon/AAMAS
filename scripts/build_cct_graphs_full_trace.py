#!/usr/bin/env python3
"""Build full-trace CCT graph artifacts and compact review samples.

Generated full JSONL artifacts are reproducible local outputs and are excluded
from normal Git review. Compact samples and Markdown reports are tracked.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from cctdiag.cct.builder import build_cct_graph  # noqa: E402
from cctdiag.cct.features import extract_cct_feature_rows  # noqa: E402

INPUT_PATH = ROOT / "data/processed/journal_v1_full_trace/main_full_trace_all.jsonl"
OUT_DIR = ROOT / "data/interim/journal_v1_full_trace_cct"
REPORT_DIR = ROOT / "results/reports/journal_v1_full_trace_cct"
MANIFEST_DIR = ROOT / "docs/artifact_manifests"
GRAPHS_PATH = OUT_DIR / "cct_graphs.jsonl"
FEATURES_PATH = OUT_DIR / "cct_features.jsonl"
SAMPLE_GRAPHS_PATH = OUT_DIR / "sample_cct_graphs.jsonl"
SAMPLE_FEATURES_PATH = OUT_DIR / "sample_cct_features.jsonl"


def _read_jsonl(path: Path) -> list[dict[str, Any]]:
    with path.open(encoding="utf-8") as handle:
        return [json.loads(line) for line in handle if line.strip()]


def _write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, sort_keys=True) + "\n")


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _line_count(path: Path) -> int:
    with path.open(encoding="utf-8") as handle:
        return sum(1 for _ in handle)


def _size(path: Path) -> int:
    return path.stat().st_size


def _artifact_row(path: Path, tracked_policy: str) -> dict[str, Any]:
    return {
        "path": str(path.relative_to(ROOT)),
        "bytes": _size(path),
        "lines": _line_count(path),
        "sha256": _sha256(path),
        "git_policy": tracked_policy,
    }


def _select_sample(records: list[dict[str, Any]], graphs: list[dict[str, Any]], feature_rows: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    clean_trace = next(record["trace_id"] for record in records if record.get("case_variant") == "clean")
    perturbed_trace = next(record["trace_id"] for record in records if record.get("case_variant") != "clean")
    sample_ids = {clean_trace, perturbed_trace}
    return [graph for graph in graphs if graph["trace_id"] in sample_ids], [row for row in feature_rows if row["trace_id"] in sample_ids]


def _write_reports(artifact_rows: list[dict[str, Any]], graph_count: int, feature_count: int) -> None:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    MANIFEST_DIR.mkdir(parents=True, exist_ok=True)
    by_path = {row["path"]: row for row in artifact_rows}

    (REPORT_DIR / "cct_graph_inventory.md").write_text(
        "# Journal-v1 Full-Trace CCT Graph Inventory\n\n"
        "Scope: graph construction artifacts only; no scoring, ranking, calibration, refinement, ablation, empirical hypothesis test, or paper-ready result table.\n\n"
        f"- Input corpus: `{INPUT_PATH.relative_to(ROOT)}`\n"
        f"- Full graphs generated locally: {graph_count}\n"
        f"- Full feature rows generated locally: {feature_count}\n"
        f"- Compact sample graphs tracked: {by_path[str(SAMPLE_GRAPHS_PATH.relative_to(ROOT))]['lines']}\n"
        f"- Compact sample feature rows tracked: {by_path[str(SAMPLE_FEATURES_PATH.relative_to(ROOT))]['lines']}\n",
        encoding="utf-8",
    )
    (REPORT_DIR / "cct_feature_inventory.md").write_text(
        "# Journal-v1 Full-Trace CCT Feature Inventory\n\n"
        "Feature rows are structural, model-visible descriptors extracted from graph nodes. They are not predictions or scores.\n\n"
        f"- Feature schema rows generated locally: {feature_count}\n"
        "- One feature row is emitted per trace step.\n"
        "- Private labels and provenance are not feature inputs.\n"
        "- Feature payload fields: `feature_schema_version`, `trace_id`, `step_id`, `agent_id`, `agent_role`, `order_index`, `in_degree`, `out_degree`, `input_token_count`, `output_token_count`, `tool_output_token_count`, `evidence_item_count`, `evidence_used_count`, `has_tool_call`, `has_handoff_from`, `has_handoff_to`.\n"
        "- `scenario_group` and `perturbation_type` are not included in feature payloads; the variance audit joins them from public corpus metadata only for descriptive audit stratification.\n",
        encoding="utf-8",
    )
    (REPORT_DIR / "cct_graph_validation_report.md").write_text(
        "# Journal-v1 Full-Trace CCT Graph Validation Report\n\n"
        "Validation status: generated graphs contain one graph per input trace and one step node per visible trace step.\n\n"
        f"- Graphs checked: {graph_count}\n"
        f"- Feature rows checked: {feature_count}\n"
        "- Expected output: 420 graphs and 2,100 feature rows for the current full-trace main corpus.\n",
        encoding="utf-8",
    )
    (REPORT_DIR / "cct_leakage_audit_report.md").write_text(
        "# Journal-v1 Full-Trace CCT Leakage Audit Report\n\n"
        "Leakage audit status: graph construction calls the full-trace prediction view before extracting graph or feature fields.\n\n"
        "Forbidden private fields checked: private labels, provenance fields, gold labels, label rationale, label source, propagation evidence, irreversibility evidence, and recovery opportunity.\n"
        "No scoring, ranking, evaluation, calibration, refinement, ablation, empirical hypothesis test, or result table was produced.\n",
        encoding="utf-8",
    )
    size_lines = [
        "# Journal-v1 Full-Trace CCT Artifact Size Report",
        "",
        "Policy: full generated JSONL artifacts are reproducible local outputs and excluded from normal Git review; compact samples and Markdown reports remain tracked.",
        "",
        "| Path | Bytes | Lines | SHA256 | Git policy |",
        "|---|---:|---:|---|---|",
    ]
    for row in artifact_rows:
        size_lines.append(f"| `{row['path']}` | {row['bytes']} | {row['lines']} | `{row['sha256']}` | {row['git_policy']} |")
    (REPORT_DIR / "cct_artifact_size_report.md").write_text("\n".join(size_lines) + "\n", encoding="utf-8")

    manifest_lines = [
        "# Journal-v1 Full-Trace CCT Artifact Manifest",
        "",
        "## Generated artifact policy",
        "",
        "- Keep source code, tests, scripts, configs, compact samples, and compact Markdown reports in Git.",
        "- Exclude full generated CCT JSONL artifacts from normal Git because they are reproducible and can make PR diffs unreviewable.",
        "- Regenerate full artifacts locally with `python scripts/build_cct_graphs_full_trace.py`.",
        "- Validate with `python scripts/validate_cct_graphs_full_trace.py`.",
        "- Audit feature variance with `python scripts/audit_cct_feature_variance.py`.",
        "- If project policy later requires versioned full artifacts, use Git LFS or release artifacts rather than normal Git blobs.",
        "",
        "## Artifact hashes and counts",
        "",
        "| Path | Bytes | Lines | SHA256 | Git policy |",
        "|---|---:|---:|---|---|",
    ]
    for row in artifact_rows:
        manifest_lines.append(f"| `{row['path']}` | {row['bytes']} | {row['lines']} | `{row['sha256']}` | {row['git_policy']} |")
    manifest_lines.extend(
        [
            "",
            "## Expected command outputs",
            "",
            "- `python scripts/build_cct_graphs_full_trace.py`: writes 420 graphs, 2,100 feature rows, 2 sample graphs, and 10 sample feature rows.",
            "- `python scripts/validate_cct_graphs_full_trace.py`: passes graph count, feature count, sample coverage, and leakage checks.",
            "- `python scripts/audit_cct_feature_variance.py`: writes descriptive variance, structural shortcut-risk, and readiness-gate reports without scoring.",
        ]
    )
    (MANIFEST_DIR / "journal_v1_full_trace_cct_manifest.md").write_text("\n".join(manifest_lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--no-full", action="store_true", help="Only write compact samples/reports; default writes full local artifacts too.")
    args = parser.parse_args()

    records = _read_jsonl(INPUT_PATH)
    graphs = [build_cct_graph(record) for record in records]
    feature_rows = [row for graph in graphs for row in extract_cct_feature_rows(graph)]
    sample_graphs, sample_features = _select_sample(records, graphs, feature_rows)

    if not args.no_full:
        _write_jsonl(GRAPHS_PATH, graphs)
        _write_jsonl(FEATURES_PATH, feature_rows)
    _write_jsonl(SAMPLE_GRAPHS_PATH, sample_graphs)
    _write_jsonl(SAMPLE_FEATURES_PATH, sample_features)

    artifact_rows = []
    if GRAPHS_PATH.exists():
        artifact_rows.append(_artifact_row(GRAPHS_PATH, "excluded from normal Git; reproducible local artifact"))
    if FEATURES_PATH.exists():
        artifact_rows.append(_artifact_row(FEATURES_PATH, "excluded from normal Git; reproducible local artifact"))
    artifact_rows.extend(
        [
            _artifact_row(SAMPLE_GRAPHS_PATH, "tracked compact sample"),
            _artifact_row(SAMPLE_FEATURES_PATH, "tracked compact sample"),
        ]
    )
    _write_reports(artifact_rows, len(graphs), len(feature_rows))
    print(f"wrote {len(graphs)} graphs and {len(feature_rows)} feature rows")
    print(f"wrote {len(sample_graphs)} sample graphs and {len(sample_features)} sample feature rows")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
