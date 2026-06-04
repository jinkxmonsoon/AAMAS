import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FORBIDDEN_PRIVATE_FIELDS = {
    "private_labels",
    "provenance",
    "gold_failure_step",
    "gold_failure_agent",
    "gold_irreversibility",
    "gold_propagation",
    "gold_recoverability",
    "label_rationale",
    "label_confidence",
    "label_source",
    "propagation_evidence",
    "irreversibility_evidence",
    "recovery_opportunity",
    "primary_labeler",
    "secondary_labeler",
    "adjudicator",
    "disagreement_type",
    "adjudication_decision",
    "manual_audit_status",
    "synthetic_control_rule",
    "annotator_or_generator",
    "provenance_notes",
}


def _forbidden_paths(value, path=""):
    found = []
    if isinstance(value, dict):
        for key, nested in value.items():
            nested_path = f"{path}.{key}" if path else str(key)
            if key in FORBIDDEN_PRIVATE_FIELDS:
                found.append(nested_path)
            found.extend(_forbidden_paths(nested, nested_path))
    elif isinstance(value, list):
        for index, item in enumerate(value):
            found.extend(_forbidden_paths(item, f"{path}[{index}]"))
    return found


def test_tracked_cct_feature_sample_contains_no_private_fields():
    sample_path = ROOT / "data/interim/journal_v1_full_trace_cct/sample_cct_features.jsonl"
    rows = [json.loads(line) for line in sample_path.read_text().splitlines() if line]

    assert rows
    assert not [path for row in rows for path in _forbidden_paths(row)]
    assert "scenario_group" not in rows[0]
    assert "perturbation_type" not in rows[0]


def test_tracked_cct_graph_sample_contains_no_private_fields():
    sample_path = ROOT / "data/interim/journal_v1_full_trace_cct/sample_cct_graphs.jsonl"
    rows = [json.loads(line) for line in sample_path.read_text().splitlines() if line]

    assert rows
    assert not [path for row in rows for path in _forbidden_paths(row)]
