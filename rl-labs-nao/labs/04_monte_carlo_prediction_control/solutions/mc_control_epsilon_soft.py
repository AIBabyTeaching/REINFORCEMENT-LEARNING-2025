"""ε-soft Monte Carlo control."""
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


def epsilon_soft_policy(q_table: Dict[State, np.ndarray], epsilon: float, n_actions: int):
    def policy(state: State) -> int:
        if state not in q_table:
            return int(np.random.randint(n_actions))
        greedy_action = int(np.argmax(q_table[state]))
        probs = np.full(n_actions, epsilon / n_actions)
        probs[greedy_action] += 1.0 - epsilon
        return int(np.random.choice(n_actions, p=probs))

    return policy


def mc_control_epsilon_soft(env, episodes: int, epsilon: float = 0.1, gamma: float = 1.0):
    n_actions = env.action_space.n
    returns_sum = defaultdict(lambda: np.zeros(n_actions))
    returns_count = defaultdict(lambda: np.zeros(n_actions))
    q_table = defaultdict(lambda: np.zeros(n_actions))

    rng = np.random.default_rng(1)

    for episode_idx in range(episodes):
        policy = epsilon_soft_policy(q_table, epsilon, n_actions)
        state, _ = env.reset()
        done = False
        trajectory = []
        while not done:
            action = policy(state)
            next_state, reward, terminated, truncated, _ = env.step(action)
            trajectory.append((state, action, reward))
            state = next_state
            done = terminated or truncated
        G = 0.0
        visited = set()
        for state, action, reward in reversed(trajectory):
            G = gamma * G + reward
            if (state, action) not in visited:
                visited.add((state, action))
                returns_sum[state][action] += G
                returns_count[state][action] += 1.0
                q_table[state][action] = returns_sum[state][action] / returns_count[state][action]
    return q_table
