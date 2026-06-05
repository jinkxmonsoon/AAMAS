#!/usr/bin/env python3
"""Validate or report blocked recovery for the frozen CCT scoring config.

Task 20C is protocol-recovery only. This script does not run scoring, ranking,
calibration, grid search, LOSO, refinement, ablation, or statistical tests.
"""

from __future__ import annotations

import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = ROOT / "configs/cct_scoring.yaml"
EXPECTED_SHA256 = "053f19066923d8d22d27b22727e75876f939f2a60480484c4028eabd07ad0855"
REQUIRED_VARIANTS = (
    "cct_primary_no_position",
    "cct_flow_only",
    "cct_context_only",
    "cct_with_position_features",
)
FORBIDDEN_ENABLED_PATTERNS = (
    "calibration_enabled: true",
    "calibration: true",
    "grid_search_enabled: true",
    "grid_search: true",
    "learned_weights: true",
    "learned: true",
    "loso_enabled: true",
    "ablation_enabled: true",
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    print("=== CCT Scoring Config Presence Validation ===")
    print(f"Path: {CONFIG_PATH.relative_to(ROOT)}")
    print(f"Expected SHA256: {EXPECTED_SHA256}")

    if not CONFIG_PATH.exists():
        print("Status: RECOVERY_BLOCKED")
        print("Reason: configs/cct_scoring.yaml is absent from this checkout.")
        print("Action: recover only from an authoritative frozen source in a separate protocol-recovery task.")
        print("FINAL: BLOCKED_NO_LOCAL_CONFIG")
        return 0

    observed = sha256(CONFIG_PATH)
    print(f"Observed SHA256: {observed}")
    if observed != EXPECTED_SHA256:
        print("Status: FAIL")
        print("Reason: SHA256 does not match the expected frozen Task 17/18 config hash.")
        print("FINAL: FAIL")
        return 1

    text = CONFIG_PATH.read_text(encoding="utf-8")
    missing = [variant for variant in REQUIRED_VARIANTS if variant not in text]
    forbidden = [pattern for pattern in FORBIDDEN_ENABLED_PATTERNS if pattern in text.lower()]

    if missing:
        print("Status: FAIL")
        print("Missing required variants:")
        for variant in missing:
            print(f"  - {variant}")
        print("FINAL: FAIL")
        return 1

    if forbidden:
        print("Status: FAIL")
        print("Forbidden learned/calibration/grid-search settings detected:")
        for pattern in forbidden:
            print(f"  - {pattern}")
        print("FINAL: FAIL")
        return 1

    print("Status: PASS")
    print("Required variants: PASS")
    print("Learned/calibration/grid-search disabled check: PASS")
    print("FINAL: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
