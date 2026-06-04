"""Baseline interfaces for diagnostic sanity checks."""

from cctdiag.baselines.trivial import (
    TRIVIAL_BASELINES,
    always_s2,
    first_active_agent,
    last_active_agent,
    majority_agent,
    majority_step,
    random_agent_seeded,
    random_step_seeded,
    same_as_parent_for_perturbations,
)

__all__ = [
    "TRIVIAL_BASELINES",
    "always_s2",
    "first_active_agent",
    "last_active_agent",
    "majority_agent",
    "majority_step",
    "random_agent_seeded",
    "random_step_seeded",
    "same_as_parent_for_perturbations",
]
