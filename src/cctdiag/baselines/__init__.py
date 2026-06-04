"""Baseline interfaces for diagnostic sanity checks."""

from cctdiag.baselines.flat_log import flat_log_keyword_agent, flat_log_keyword_step, flat_log_role_agent
from cctdiag.baselines.spectrum import spectrum_inspired_agent, spectrum_inspired_step
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
    "flat_log_keyword_agent",
    "flat_log_keyword_step",
    "flat_log_role_agent",
    "last_active_agent",
    "majority_agent",
    "majority_step",
    "random_agent_seeded",
    "random_step_seeded",
    "same_as_parent_for_perturbations",
    "spectrum_inspired_agent",
    "spectrum_inspired_step",
]
