"""Expected SARSA control."""
from __future__ import annotations

from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[3]
if str(ROOT) not in __import__("sys").path:
    __import__("sys").path.insert(0, str(ROOT))

from common import policies  # noqa: E402


def expected_sarsa(env, episodes: int, alpha: float, gamma: float, epsilon: float) -> np.ndarray:
    n_states = env.observation_space.n
    n_actions = env.action_space.n
    q_table = np.zeros((n_states, n_actions))

    rng = np.random.default_rng(1)

    for episode in range(episodes):
        state, _ = env.reset()
        done = False
        while not done:
            if rng.random() < epsilon:
                action = int(rng.integers(n_actions))
            else:
                action = int(np.argmax(q_table[state]))
            next_state, reward, terminated, truncated, _ = env.step(action)
            greedy_action = int(np.argmax(q_table[next_state]))
            probs = np.full(n_actions, epsilon / n_actions)
            probs[greedy_action] += 1.0 - epsilon
            expected_value = np.dot(probs, q_table[next_state])
            td_target = reward + gamma * expected_value
            q_table[state, action] += alpha * (td_target - q_table[state, action])
            state = next_state
            done = terminated or truncated
    return q_table
