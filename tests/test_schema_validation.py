import json
from pathlib import Path
import pytest
from cctdiag.schema.validators import validate_record_schema
from cctdiag.schema.errors import ValidationError

ROOT = Path(__file__).resolve().parents[1]


def test_schema_valid_fixture_passes():
    data = json.loads((ROOT / "tests/fixtures/journal_v1/minimal_valid_trace.json").read_text())
    validate_record_schema(data["record"])


def test_schema_missing_field_fails():
    rec = json.loads((ROOT / "tests/fixtures/journal_v1/minimal_invalid_trace_missing_field.json").read_text())
    with pytest.raises(ValidationError):
        validate_record_schema(rec)
