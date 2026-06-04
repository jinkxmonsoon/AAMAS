import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "scripts/validate_cct_scoring_protocol.py"


def _load_validator():
    spec = importlib.util.spec_from_file_location("validate_cct_scoring_protocol", VALIDATOR)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_cct_scoring_protocol_config_passes_guardrails():
    module = _load_validator()
    config = module.load_config()

    assert module.validate_config(config) == []
    assert {"cct_primary_no_position", "cct_flow_only", "cct_context_only"}.issubset(config["variants"])
    assert config["execution_enabled"] is False


def test_primary_cct_scoring_variant_excludes_forbidden_and_high_risk_fields():
    module = _load_validator()
    config = module.load_config()
    primary_features = set(config["variants"]["cct_primary_no_position"]["features"])

    assert not primary_features & set(config["forbidden_score_fields"])
    assert not primary_features & set(config["restricted_high_risk_features"])
    assert config["formula"]["learned_parameters"] is False
    assert config["formula"]["calibration"] is False
    assert config["formula"]["grid_search"] is False
