from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_contract_keys_present() -> None:
    checks = {
        "configs/protocol.yaml": ["scenario_groups:", "case_schema_required_keys:"],
        "configs/metrics.yaml": ["metric_interfaces:"],
        "configs/baselines.yaml": ["baseline_registry:"],
        "configs/seeds.yaml": ["seed_policy:"],
    }
    for rel, keys in checks.items():
        text = (ROOT / rel).read_text(encoding="utf-8")
        for k in keys:
            assert k in text
