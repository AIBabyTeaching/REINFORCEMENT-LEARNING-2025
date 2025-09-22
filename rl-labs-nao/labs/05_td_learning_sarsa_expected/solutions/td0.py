"""TD(0) prediction."""
from __future__ import annotations

from pathlib import Path
from typing import Callable

import numpy as np

ROOT = Path(__file__).resolve().parents[3]
if str(ROOT) not in __import__("sys").path:
    __import__("sys").path.insert(0, str(ROOT))

from common import utils  # noqa: E402


def td0_prediction(env, policy: Callable, episodes: int, alpha: float, gamma: float) -> np.ndarray:
    n_states = env.observation_space.n
    values = np.zeros(n_states)
    for episode in range(episodes):
        state, _ = env.reset()
        done = False
        while not done:
            action = policy(state)
            next_state, reward, terminated, truncated, _ = env.step(action)
            td_target = reward + gamma * values[next_state]
            values[state] += alpha * (td_target - values[state])
            state = next_state
            done = terminated or truncated
    return values
