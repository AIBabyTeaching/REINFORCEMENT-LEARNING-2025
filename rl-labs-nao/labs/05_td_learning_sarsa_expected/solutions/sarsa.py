"""SARSA control implementation."""
from __future__ import annotations

from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[3]
if str(ROOT) not in __import__("sys").path:
    __import__("sys").path.insert(0, str(ROOT))

from common import policies  # noqa: E402


def sarsa_control(env, episodes: int, alpha: float, gamma: float, epsilon: float) -> np.ndarray:
    n_states = env.observation_space.n
    n_actions = env.action_space.n
    q_table = np.zeros((n_states, n_actions))

    rng = np.random.default_rng(0)

    def policy(state: int) -> int:
        if rng.random() < epsilon:
            return int(rng.integers(n_actions))
        return int(np.argmax(q_table[state]))

    for episode in range(episodes):
        state, _ = env.reset()
        action = policy(state)
        done = False
        while not done:
            next_state, reward, terminated, truncated, _ = env.step(action)
            next_action = policy(next_state)
            td_target = reward + gamma * q_table[next_state, next_action]
            q_table[state, action] += alpha * (td_target - q_table[state, action])
            state, action = next_state, next_action
            done = terminated or truncated
    return q_table
