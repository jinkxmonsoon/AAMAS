#!/usr/bin/env python3
"""Validate the frozen uncalibrated CCT scoring protocol config.

This validator checks protocol guardrails only. It does not score, rank,
evaluate, calibrate, refine, ablate, compare against gold labels, or produce
paper-ready result tables.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = ROOT / "configs/cct_scoring.yaml"

REQUIRED_VARIANTS = {
    "cct_primary_no_position",
    "cct_flow_only",
    "cct_context_only",
}
OPTIONAL_HIGH_RISK_VARIANTS = {"cct_with_position_features"}
FORBIDDEN_CONFIG_FLAGS = {
    "learned_parameters",
    "loso",
    "grid_search",
    "calibration",
    "post_performance_adjustment",
}


def load_config(path: Path = CONFIG_PATH) -> dict[str, Any]:
    """Load the JSON-compatible YAML config without external dependencies."""

    return json.loads(path.read_text(encoding="utf-8"))


def _variant_features(config: dict[str, Any], variant_name: str) -> set[str]:
    variant = config.get("variants", {}).get(variant_name, {})
    features = variant.get("features", {})
    if not isinstance(features, dict):
        return set()
    return set(features)


def validate_config(config: dict[str, Any]) -> list[str]:
    """Return protocol violations for the frozen scoring configuration."""

    violations: list[str] = []
    variants = config.get("variants", {})
    if not isinstance(variants, dict):
        return ["variants must be a mapping"]

    missing = sorted(REQUIRED_VARIANTS - set(variants))
    if missing:
        violations.append("missing required variants: " + ", ".join(missing))

    formula = config.get("formula", {})
    if formula.get("type") != "transparent_weighted_sum":
        violations.append("formula.type must be transparent_weighted_sum")
    if formula.get("weights_fixed_before_execution") is not True:
        violations.append("weights must be fixed before execution")
    for flag in FORBIDDEN_CONFIG_FLAGS:
        if formula.get(flag) is not False:
            violations.append(f"formula.{flag} must be false")

    if config.get("execution_enabled") is not False:
        violations.append("execution_enabled must remain false for protocol-only freeze")

    forbidden_fields = set(config.get("forbidden_score_fields", []))
    high_risk = set(config.get("restricted_high_risk_features", []))
    primary_features = _variant_features(config, "cct_primary_no_position")
    forbidden_in_primary = sorted(primary_features & forbidden_fields)
    if forbidden_in_primary:
        violations.append("primary variant uses forbidden fields: " + ", ".join(forbidden_in_primary))
    high_risk_in_primary = sorted(primary_features & high_risk)
    if high_risk_in_primary:
        violations.append("primary variant uses high-risk fields: " + ", ".join(high_risk_in_primary))

    primary = variants.get("cct_primary_no_position", {})
    if primary.get("uses_position_or_identity_features") is not False:
        violations.append("primary variant must declare uses_position_or_identity_features=false")
    if primary.get("status") != "primary_frozen":
        violations.append("primary variant status must be primary_frozen")

    for variant_name, variant in variants.items():
        features = variant.get("features", {})
        if not isinstance(features, dict) or not features:
            violations.append(f"{variant_name} must define non-empty fixed feature weights")
            continue
        for feature, weight in features.items():
            if not isinstance(weight, int | float):
                violations.append(f"{variant_name}.{feature} weight must be numeric and fixed")
            elif weight < 0:
                violations.append(f"{variant_name}.{feature} weight must be non-negative")
        if any(feature in forbidden_fields for feature in features):
            blocked = sorted(set(features) & forbidden_fields)
            violations.append(f"{variant_name} uses forbidden score fields: " + ", ".join(blocked))

    for variant_name in OPTIONAL_HIGH_RISK_VARIANTS & set(variants):
        variant = variants[variant_name]
        if variant.get("uses_position_or_identity_features") is not True:
            violations.append(f"{variant_name} must explicitly declare high-risk position/identity use")
        if "not_primary" not in str(variant.get("status", "")):
            violations.append(f"{variant_name} must be marked not primary")

    disallowed_top_level = {"calibration_settings", "learned_weights", "training", "grid_search", "loso"}
    present_disallowed = sorted(disallowed_top_level & set(config))
    if present_disallowed:
        violations.append("config contains learned/calibration settings: " + ", ".join(present_disallowed))

    return violations


def main() -> int:
    config = load_config()
    violations = validate_config(config)
    print("=== CCT Scoring Protocol Validation ===")
    print(f"Config: {CONFIG_PATH.relative_to(ROOT)}")
    print("Required variants: " + ", ".join(sorted(REQUIRED_VARIANTS)))
    print("Primary variant: cct_primary_no_position")
    if violations:
        for violation in violations:
            print(f"FAIL: {violation}")
        print("FINAL: FAIL")
        return 1
    print("Forbidden/high-risk primary-feature checks: PASS")
    print("Learned/calibration settings check: PASS")
    print("FINAL: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
