import json
from pathlib import Path

from scripts import build_cct_descriptor_augmented_features as builder


def test_descriptor_augmented_rows_are_reproducible_from_full_trace_corpus():
    traces = builder.read_traces(builder.INPUT_PATH)
    rows = builder.build_rows(traces)

    assert len(traces) == builder.EXPECTED_TRACE_COUNT
    assert len(rows) == builder.EXPECTED_ROW_COUNT
    assert builder.leakage_status(rows)[0] == "PASS"
    assert set(builder.DESCRIPTOR_COLUMNS).issubset(rows[0])


def test_tracked_sample_contains_clean_and_perturbed_full_step_sets():
    sample_path = Path("results/raw/journal_v1_full_trace_cct/sample_cct_descriptor_augmented_features.json")
    sample_rows = json.loads(sample_path.read_text(encoding="utf-8"))

    variants = {row["case_variant"] for row in sample_rows}
    trace_ids = {row["trace_id"] for row in sample_rows}

    assert variants == {"clean", "perturbed"}
    assert len(trace_ids) == 2
    assert len(sample_rows) == 10
    for trace_id in trace_ids:
        steps = [row["step_id"] for row in sample_rows if row["trace_id"] == trace_id]
        assert steps == ["s1", "s2", "s3", "s4", "s5"]
    for row in sample_rows:
        for column in builder.DESCRIPTOR_COLUMNS:
            assert row[column]
