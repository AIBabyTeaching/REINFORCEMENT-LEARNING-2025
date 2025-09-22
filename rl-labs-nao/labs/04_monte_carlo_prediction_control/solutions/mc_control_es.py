"""Exploring starts Monte Carlo control."""
from __future__ import annotations

from collections import defaultdict
from pathlib import Path
from typing import Dict, Tuple

import numpy as np

ROOT = Path(__file__).resolve().parents[3]
if str(ROOT) not in __import__("sys").path:
    __import__("sys").path.insert(0, str(ROOT))

from common import policies  # noqa: E402

State = Tuple[int, int, bool]


def mc_control_es(env, episodes: int, gamma: float = 1.0) -> Dict[State, np.ndarray]:
    returns_sum = defaultdict(lambda: np.zeros(env.action_space.n))
    returns_count = defaultdict(lambda: np.zeros(env.action_space.n))
    q_table = defaultdict(lambda: np.zeros(env.action_space.n))

    rng = np.random.default_rng(0)

    for _ in range(episodes):
        state, _ = env.reset()
        action = int(rng.integers(env.action_space.n))
        episode = []
        done = False
        while not done:
            next_state, reward, terminated, truncated, _ = env.step(action)
            episode.append((state, action, reward))
            state = next_state
            if terminated or truncated:
                done = True
            else:
                greedy_action = int(np.argmax(q_table[state]))
                action = greedy_action

        G = 0.0
        visited = set()
        for state, action, reward in reversed(episode):
            G = gamma * G + reward
            if (state, action) not in visited:
                visited.add((state, action))
                returns_sum[state][action] += G
                returns_count[state][action] += 1.0
                q_table[state][action] = (
                    returns_sum[state][action] / returns_count[state][action]
                )
    return q_table
