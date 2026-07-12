#!/usr/bin/env python3
"""Build descriptor-augmented CCT feature rows for audit/review only.

This script emits one review-layer row per full-trace step. It does not score,
rank, calibrate, search, split, or evaluate models.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
INPUT_PATH = ROOT / "data/processed/journal_v1_full_trace/main_full_trace_all.jsonl"
FULL_OUTPUT_PATH = ROOT / "results/raw/journal_v1_full_trace_cct/cct_descriptor_augmented_features.json"
SAMPLE_OUTPUT_PATH = ROOT / "results/raw/journal_v1_full_trace_cct/sample_cct_descriptor_augmented_features.json"
REPORT_DIR = ROOT / "results/reports/journal_v1_full_trace_cct"
MANIFEST_PATH = ROOT / "docs/artifact_manifests/journal_v1_descriptor_augmented_features_manifest.md"

DESCRIPTOR_COLUMNS = [
    "descriptor_agent_role",
    "descriptor_handoff_context",
    "descriptor_visible_step_evidence",
]

READINESS_PROTOCOL_REVISION = "no"
READINESS_SCORING = "no"
EXPECTED_TRACE_COUNT = 420
EXPECTED_ROW_COUNT = 2100
EXPECTED_STEPS_PER_TRACE = 5


def read_traces(path: Path) -> list[dict[str, Any]]:
    traces: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                traces.append(json.loads(line))
    return traces


def descriptor_handoff_context(step: dict[str, Any]) -> str:
    source = step.get("handoff_from") or "trace_start"
    target = step.get("handoff_to") or "trace_end"
    return f"handoff_from={source};handoff_to={target}"


def descriptor_visible_step_evidence(step: dict[str, Any]) -> str:
    evidence_items = step.get("evidence_items") or []
    evidence_used = step.get("evidence_used") or []
    note_token_count = len((step.get("visible_step_notes") or "").split())
    return (
        f"evidence_items={len(evidence_items)};"
        f"evidence_used={len(evidence_used)};"
        f"visible_note_tokens={note_token_count}"
    )


def build_rows(traces: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for trace in traces:
        for position, step in enumerate(trace.get("steps", []), start=1):
            rows.append(
                {
                    "trace_id": trace["trace_id"],
                    "case_id": trace["case_id"],
                    "case_variant": trace["case_variant"],
                    "dataset_version": trace["dataset_version"],
                    "scenario_group": trace["scenario_group"],
                    "perturbation_type": trace.get("perturbation_type"),
                    "perturbation_intensity": trace.get("perturbation_intensity"),
                    "terminal_outcome": trace.get("terminal_outcome"),
                    "step_id": step["step_id"],
                    "step_position": position,
                    "agent_id": step["agent_id"],
                    "agent_role": step["agent_role"],
                    "handoff_from": step.get("handoff_from"),
                    "handoff_to": step.get("handoff_to"),
                    "input_message": step.get("input_message"),
                    "output_message": step.get("output_message"),
                    "tool_call": step.get("tool_call"),
                    "tool_output": step.get("tool_output"),
                    "visible_step_notes": step.get("visible_step_notes"),
                    "descriptor_agent_role": f"role={step['agent_role']}",
                    "descriptor_handoff_context": descriptor_handoff_context(step),
                    "descriptor_visible_step_evidence": descriptor_visible_step_evidence(step),
                }
            )
    return rows


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2, sort_keys=True)
        handle.write("\n")


def file_stats(path: Path) -> dict[str, Any]:
    data = path.read_bytes()
    return {
        "path": path.relative_to(ROOT).as_posix(),
        "sha256": hashlib.sha256(data).hexdigest(),
        "bytes": len(data),
        "lines": path.read_text(encoding="utf-8").count("\n"),
    }


def select_sample_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    clean_trace_id = next(row["trace_id"] for row in rows if row["case_variant"] == "clean")
    perturbed_trace_id = next(row["trace_id"] for row in rows if row["case_variant"] == "perturbed")
    selected = {clean_trace_id, perturbed_trace_id}
    return [row for row in rows if row["trace_id"] in selected]


def leakage_status(rows: list[dict[str, Any]]) -> tuple[str, list[str]]:
    forbidden_terms = ["gold", "label", "failure", "failed", "correct", "incorrect"]
    hits: list[str] = []
    for row in rows:
        for column in DESCRIPTOR_COLUMNS:
            value = str(row.get(column, "")).lower()
            for term in forbidden_terms:
                if term in value:
                    hits.append(f"{row['trace_id']}:{row['step_id']}:{column}:{term}")
    return ("PASS" if not hits else "FAIL", hits)


def compact_counts(rows: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "row_count": len(rows),
        "trace_count": len({row["trace_id"] for row in rows}),
        "case_variant_counts": dict(Counter(row["case_variant"] for row in rows)),
        "scenario_group_counts": dict(Counter(row["scenario_group"] for row in rows)),
        "descriptor_columns": DESCRIPTOR_COLUMNS,
    }


def write_reports(rows: list[dict[str, Any]], sample_rows: list[dict[str, Any]], full_stats: dict[str, Any], sample_stats: dict[str, Any]) -> None:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    counts = compact_counts(rows)
    status, hits = leakage_status(rows)
    join_complete = len(rows) == EXPECTED_ROW_COUNT
    traces_with_all_steps = sum(
        1
        for trace_id in {row["trace_id"] for row in rows}
        if sum(1 for row in rows if row["trace_id"] == trace_id) == EXPECTED_STEPS_PER_TRACE
    )

    (REPORT_DIR / "cct_descriptor_augmented_feature_inventory.md").write_text(
        "# CCT Descriptor-Augmented Feature Inventory\n\n"
        "Scope: descriptor-only review artifact for the Journal-v1 full-trace corpus.\n\n"
        f"- Source traces: `{INPUT_PATH.relative_to(ROOT)}`\n"
        f"- Trace count: {counts['trace_count']}\n"
        f"- Expected row count: {EXPECTED_ROW_COUNT}\n"
        f"- Observed row count: {counts['row_count']}\n"
        f"- Join completeness: {counts['row_count']}/{EXPECTED_ROW_COUNT}\n"
        f"- Traces with {EXPECTED_STEPS_PER_TRACE} rows: {traces_with_all_steps}/{EXPECTED_TRACE_COUNT}\n"
        f"- Descriptor columns: {', '.join(DESCRIPTOR_COLUMNS)}\n"
        f"- Full artifact policy: regenerated locally; excluded from normal Git review.\n"
        f"- Tracked sample artifact: `{SAMPLE_OUTPUT_PATH.relative_to(ROOT)}` ({len(sample_rows)} rows)\n",
        encoding="utf-8",
    )

    (REPORT_DIR / "cct_descriptor_augmented_feature_leakage_audit.md").write_text(
        "# CCT Descriptor-Augmented Feature Leakage Audit\n\n"
        f"- Leakage status: {status}\n"
        f"- Descriptor columns checked: {', '.join(DESCRIPTOR_COLUMNS)}\n"
        "- Forbidden audit terms: gold, label, failure, failed, correct, incorrect\n"
        f"- Hits: {len(hits)}\n"
        "- Scope: descriptor text only; no private label fields are emitted.\n",
        encoding="utf-8",
    )

    variant_lines = "\n".join(f"- {k}: {v}" for k, v in sorted(counts["case_variant_counts"].items()))
    scenario_lines = "\n".join(f"- {k}: {v}" for k, v in sorted(counts["scenario_group_counts"].items()))
    (REPORT_DIR / "cct_descriptor_augmented_feature_variance_report.md").write_text(
        "# CCT Descriptor-Augmented Feature Variance Report\n\n"
        "This compact report records coverage variance only; it is not a statistical test.\n\n"
        f"## Case variants\n{variant_lines}\n\n"
        f"## Scenario groups\n{scenario_lines}\n",
        encoding="utf-8",
    )

    (REPORT_DIR / "cct_descriptor_augmented_shortcut_risk_report.md").write_text(
        "# CCT Descriptor-Augmented Shortcut Risk Report\n\n"
        "- Risk posture: conservative.\n"
        "- Descriptor layer includes role, handoff-neighborhood, and visible evidence-count context.\n"
        "- Descriptor layer intentionally excludes private labels, gold failure fields, scoring outputs, rankings, and evaluation metrics.\n"
        "- Residual risk: descriptors could still encode corpus-construction regularities; future protocol revision remains locked pending explicit authorization.\n",
        encoding="utf-8",
    )

    (REPORT_DIR / "cct_descriptor_augmented_readiness_gate.md").write_text(
        "# CCT Descriptor-Augmented Readiness Gate\n\n"
        f"- Join completeness: {counts['row_count']}/{EXPECTED_ROW_COUNT}\n"
        f"- Leakage status: {status}\n"
        f"- AUGMENTED_FEATURE_LAYER_READY_FOR_PROTOCOL_REVISION = {READINESS_PROTOCOL_REVISION}\n"
        f"- AUGMENTED_FEATURE_LAYER_READY_FOR_SCORING = {READINESS_SCORING}\n"
        "- Decision rationale: conservative hold; this task is artifact reviewability only.\n",
        encoding="utf-8",
    )

    (REPORT_DIR / "cct_descriptor_augmented_artifact_size_report.md").write_text(
        "# CCT Descriptor-Augmented Artifact Size Report\n\n"
        "## Diff size diagnosis\n"
        "The full descriptor-augmented JSON contains 2,100 row objects and is a generated artifact. Keeping it in normal Git can make pull requests unreviewable.\n\n"
        "## Artifact sizes\n"
        f"- Full local artifact: `{full_stats['path']}`\n"
        f"  - SHA256: `{full_stats['sha256']}`\n"
        f"  - Lines: {full_stats['lines']}\n"
        f"  - Bytes: {full_stats['bytes']}\n"
        f"- Tracked sample artifact: `{sample_stats['path']}`\n"
        f"  - SHA256: `{sample_stats['sha256']}`\n"
        f"  - Lines: {sample_stats['lines']}\n"
        f"  - Bytes: {sample_stats['bytes']}\n\n"
        "## Policy\n"
        "- Keep source code, scripts, tests, compact reports, readiness reports, and manifests in Git.\n"
        "- Keep only compact sample augmented feature artifacts in Git.\n"
        "- Regenerate the full augmented feature artifact locally with `python scripts/build_cct_descriptor_augmented_features.py`.\n"
        "- Do not track large full JSON artifacts in normal Git when they make reviews unmanageable.\n"
        "- Use Git LFS or release artifacts if full generated artifacts must later be versioned.\n",
        encoding="utf-8",
    )

    MANIFEST_PATH.parent.mkdir(parents=True, exist_ok=True)
    MANIFEST_PATH.write_text(
        "# Journal-v1 Descriptor-Augmented Features Manifest\n\n"
        "## Generation command\n"
        "```bash\npython scripts/build_cct_descriptor_augmented_features.py\n```\n\n"
        "## Expected outputs\n"
        f"- Full local artifact: `{full_stats['path']}` (generated, ignored for normal Git review)\n"
        f"- Tracked sample artifact: `{sample_stats['path']}`\n"
        f"- Compact reports: `results/reports/journal_v1_full_trace_cct/*descriptor_augmented*.md`\n\n"
        "## Expected counts\n"
        f"- Source trace count: {EXPECTED_TRACE_COUNT}\n"
        f"- Expected row count: {EXPECTED_ROW_COUNT}\n"
        f"- Join completeness: {counts['row_count']}/{EXPECTED_ROW_COUNT}\n"
        f"- Descriptor columns: {', '.join(DESCRIPTOR_COLUMNS)}\n"
        f"- Leakage status: {status}\n"
        f"- AUGMENTED_FEATURE_LAYER_READY_FOR_PROTOCOL_REVISION = {READINESS_PROTOCOL_REVISION}\n"
        f"- AUGMENTED_FEATURE_LAYER_READY_FOR_SCORING = {READINESS_SCORING}\n\n"
        "## Artifact hashes and sizes\n"
        f"| Artifact | SHA256 | Lines | Bytes | Git policy |\n"
        f"| --- | --- | ---: | ---: | --- |\n"
        f"| `{full_stats['path']}` | `{full_stats['sha256']}` | {full_stats['lines']} | {full_stats['bytes']} | regenerate locally; ignored |\n"
        f"| `{sample_stats['path']}` | `{sample_stats['sha256']}` | {sample_stats['lines']} | {sample_stats['bytes']} | tracked compact sample |\n\n"
        "## Review policy\n"
        "Keep code, tests, compact reports, readiness gates, and manifests in Git. Keep only compact sample augmented feature artifacts in Git. If full generated artifacts need archival/versioning later, use Git LFS or release artifact handling rather than normal Git diffs.\n\n"
        "## Non-actions\n"
        "No scoring, ranking, protocol revision, calibration, grid search, LOSO, refinement, ablation, statistical test, empirical hypothesis test, or paper-ready result table is produced by this artifact build.\n",
        encoding="utf-8",
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=INPUT_PATH)
    parser.add_argument("--full-output", type=Path, default=FULL_OUTPUT_PATH)
    parser.add_argument("--sample-output", type=Path, default=SAMPLE_OUTPUT_PATH)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    traces = read_traces(args.input)
    rows = build_rows(traces)
    if len(traces) != EXPECTED_TRACE_COUNT:
        raise RuntimeError(f"expected {EXPECTED_TRACE_COUNT} traces, observed {len(traces)}")
    if len(rows) != EXPECTED_ROW_COUNT:
        raise RuntimeError(f"expected {EXPECTED_ROW_COUNT} rows, observed {len(rows)}")

    write_json(args.full_output, rows)
    sample_rows = select_sample_rows(rows)
    write_json(args.sample_output, sample_rows)
    full_stats = file_stats(args.full_output)
    sample_stats = file_stats(args.sample_output)
    write_reports(rows, sample_rows, full_stats, sample_stats)
    status, hits = leakage_status(rows)
    if status != "PASS":
        raise RuntimeError(f"descriptor leakage audit failed: {hits[:5]}")
    print("Built descriptor-augmented feature artifacts")
    print(f"rows={len(rows)} join_completeness={len(rows)}/{EXPECTED_ROW_COUNT} leakage={status}")
    print(f"full={full_stats['path']} sha256={full_stats['sha256']} bytes={full_stats['bytes']} lines={full_stats['lines']}")
    print(f"sample={sample_stats['path']} sha256={sample_stats['sha256']} bytes={sample_stats['bytes']} lines={sample_stats['lines']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
