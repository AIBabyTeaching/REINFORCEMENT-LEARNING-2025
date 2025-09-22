"""Policy iteration implementation."""
from __future__ import annotations

from pathlib import Path
from typing import Tuple

import numpy as np

ROOT = Path(__file__).resolve().parents[3]
if str(ROOT) not in __import__("sys").path:
    __import__("sys").path.insert(0, str(ROOT))

from common import mdp  # noqa: E402


def policy_iteration(
    world: mdp.Gridworld,
    gamma: float = 0.9,
    tolerance: float = 1e-6,
) -> Tuple[np.ndarray, np.ndarray]:
    transitions, rewards = world.as_transition_matrices(gamma=gamma)
    n_states = len(world.states)
    n_actions = len(world.actions)
    policy = np.full((n_states, n_actions), 1.0 / n_actions)

    stable = False
    iteration = 0
    while not stable:
        iteration += 1
        values = mdp.policy_evaluation(policy, transitions, rewards, gamma, tolerance)
        stable = True
        for s in range(n_states):
            action_returns = []
            for a in range(n_actions):
                action_returns.append(
                    np.sum(transitions[a, s] * (rewards[a, s] + gamma * values))
                )
            best_action = int(np.argmax(action_returns))
            if policy[s].argmax() != best_action:
                stable = False
            policy[s] = 0.0
            policy[s, best_action] = 1.0
        if iteration > 1000:
            break
    return values, policy
