"""Double Q-learning reference implementation."""
from __future__ import annotations

from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[3]
if str(ROOT) not in __import__("sys").path:
    __import__("sys").path.insert(0, str(ROOT))


def double_q_learning(
    env,
    episodes: int,
    alpha: float,
    gamma: float,
    epsilon: float,
) -> tuple[np.ndarray, np.ndarray]:
    n_states = env.observation_space.n
    n_actions = env.action_space.n
    q1 = np.zeros((n_states, n_actions))
    q2 = np.zeros((n_states, n_actions))
    rng = np.random.default_rng(3)

    for episode in range(episodes):
        state, _ = env.reset()
        done = False
        while not done:
            if rng.random() < epsilon:
                action = int(rng.integers(n_actions))
            else:
                action = int(np.argmax(q1[state] + q2[state]))
            next_state, reward, terminated, truncated, _ = env.step(action)
            if rng.random() < 0.5:
                best_next = int(np.argmax(q1[next_state]))
                td_target = reward + gamma * q2[next_state, best_next]
                q1[state, action] += alpha * (td_target - q1[state, action])
            else:
                best_next = int(np.argmax(q2[next_state]))
                td_target = reward + gamma * q1[next_state, best_next]
                q2[state, action] += alpha * (td_target - q2[state, action])
            state = next_state
            done = terminated or truncated
    return q1, q2
