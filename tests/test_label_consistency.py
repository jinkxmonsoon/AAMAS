import json
from pathlib import Path
import pytest
from cctdiag.schema.validators import validate_label_consistency
from cctdiag.schema.errors import ValidationError

ROOT = Path(__file__).resolve().parents[1]


def test_label_consistency_valid_fixture_passes():
    data = json.loads((ROOT / "tests/fixtures/journal_v1/minimal_valid_trace.json").read_text())
    validate_label_consistency(data["record"], data["trace_steps"])


def test_label_consistency_invalid_reference_fails():
    data = json.loads((ROOT / "tests/fixtures/journal_v1/minimal_invalid_label_reference.json").read_text())
    with pytest.raises(ValidationError):
        validate_label_consistency(data["record"], data["trace_steps"])
