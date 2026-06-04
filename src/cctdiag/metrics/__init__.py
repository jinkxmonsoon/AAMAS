"""Metric interfaces for diagnostic attribution sanity checks."""

from cctdiag.metrics.attribution import (
    agent_accuracy,
    irreversibility_accuracy,
    macro_accuracy_by_perturbation,
    macro_accuracy_by_scenario,
    propagation_accuracy,
    recoverability_accuracy,
    step_accuracy,
    tuple_accuracy_step_agent,
)
from cctdiag.metrics.sanity import interpret_shortcut_risk

__all__ = [
    "agent_accuracy",
    "irreversibility_accuracy",
    "interpret_shortcut_risk",
    "macro_accuracy_by_perturbation",
    "macro_accuracy_by_scenario",
    "propagation_accuracy",
    "recoverability_accuracy",
    "step_accuracy",
    "tuple_accuracy_step_agent",
]
