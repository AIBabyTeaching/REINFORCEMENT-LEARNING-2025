"""Value iteration implementation."""
from __future__ import annotations

from pathlib import Path
from typing import Tuple

import numpy as np

ROOT = Path(__file__).resolve().parents[3]
if str(ROOT) not in __import__("sys").path:
    __import__("sys").path.insert(0, str(ROOT))

from common import mdp, policies  # noqa: E402


def value_iteration(
    world: mdp.Gridworld,
    gamma: float = 0.9,
    tolerance: float = 1e-6,
) -> Tuple[np.ndarray, np.ndarray]:
    transitions, rewards = world.as_transition_matrices(gamma=gamma)
    n_states = len(world.states)
    n_actions = len(world.actions)
    values = np.zeros(n_states)
    delta = np.inf
    while delta > tolerance:
        delta = 0.0
        for s in range(n_states):
            v = values[s]
            q_values = [
                np.sum(transitions[a, s] * (rewards[a, s] + gamma * values))
                for a in range(n_actions)
            ]
            values[s] = max(q_values)
            delta = max(delta, abs(v - values[s]))
    q_table = np.zeros((n_states, n_actions))
    for s in range(n_states):
        for a in range(n_actions):
            q_table[s, a] = np.sum(transitions[a, s] * (rewards[a, s] + gamma * values))
    policy = policies.deterministic_policy_from_q(q_table)
    return values, policy
