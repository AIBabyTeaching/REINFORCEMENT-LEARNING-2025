"""Reference policy evaluation routine."""
from __future__ import annotations

from pathlib import Path
from typing import Tuple

import numpy as np

ROOT = Path(__file__).resolve().parents[3]
if str(ROOT) not in __import__("sys").path:
    __import__("sys").path.insert(0, str(ROOT))

from common import mdp  # noqa: E402


def make_gridworld() -> Tuple[mdp.Gridworld, np.ndarray, np.ndarray]:
    world = mdp.Gridworld(
        width=4,
        height=4,
        terminal_states=[(0, 0), (3, 3)],
        reward_map={(3, 3): 0.0},
        step_reward=-1.0,
    )
    transitions, rewards = world.as_transition_matrices(gamma=1.0)
    return world, transitions, rewards


def evaluate_uniform_policy(gamma: float = 0.9) -> np.ndarray:
    world, transitions, rewards = make_gridworld()
    policy = np.full((len(world.states), len(world.actions)), 1.0 / len(world.actions))
    values = mdp.policy_evaluation(policy, transitions, rewards, gamma)
    return values.reshape((world.height, world.width))
