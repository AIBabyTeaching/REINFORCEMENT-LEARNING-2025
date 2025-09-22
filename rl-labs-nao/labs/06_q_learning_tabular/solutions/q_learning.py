"""Tabular Q-learning implementation."""
from __future__ import annotations

from pathlib import Path
from typing import Callable

import numpy as np

ROOT = Path(__file__).resolve().parents[3]
if str(ROOT) not in __import__("sys").path:
    __import__("sys").path.insert(0, str(ROOT))

from common import policies  # noqa: E402


def q_learning(
    env,
    episodes: int,
    alpha: float,
    gamma: float,
    epsilon_start: float,
    epsilon_end: float,
) -> np.ndarray:
    n_states = env.observation_space.n
    n_actions = env.action_space.n
    q_table = np.zeros((n_states, n_actions))
    eps_schedule = np.linspace(epsilon_start, epsilon_end, episodes)
    rng = np.random.default_rng(2)

    for episode in range(episodes):
        epsilon = eps_schedule[episode]
        state, _ = env.reset()
        done = False
        while not done:
            if rng.random() < epsilon:
                action = int(rng.integers(n_actions))
            else:
                action = int(np.argmax(q_table[state]))
            next_state, reward, terminated, truncated, _ = env.step(action)
            td_target = reward + gamma * np.max(q_table[next_state])
            q_table[state, action] += alpha * (td_target - q_table[state, action])
            state = next_state
            done = terminated or truncated
    return q_table
