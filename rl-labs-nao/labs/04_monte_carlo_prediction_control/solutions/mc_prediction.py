"""First-visit Monte Carlo prediction for Blackjack."""
from __future__ import annotations

from collections import defaultdict
from pathlib import Path
from typing import Dict, Iterable, Tuple

import numpy as np

ROOT = Path(__file__).resolve().parents[3]
if str(ROOT) not in __import__("sys").path:
    __import__("sys").path.insert(0, str(ROOT))

from common import utils  # noqa: E402

State = Tuple[int, int, bool]


def generate_episode(env, policy) -> Iterable[Tuple[State, int]]:
    episode = []
    state, _ = env.reset()
    done = False
    while not done:
        action = policy(state)
        next_state, reward, terminated, truncated, _ = env.step(action)
        episode.append((state, action, reward))
        state = next_state
        done = terminated or truncated
    return episode


def mc_prediction(env, policy, episodes: int, gamma: float = 1.0) -> Dict[State, float]:
    returns_sum = defaultdict(float)
    returns_count = defaultdict(float)
    value_table: Dict[State, float] = {}

    for _ in range(episodes):
        episode = list(generate_episode(env, policy))
        G = 0.0
        visited = set()
        for state, _, reward in reversed(episode):
            G = gamma * G + reward
            if state not in visited:
                visited.add(state)
                returns_sum[state] += G
                returns_count[state] += 1.0
                value_table[state] = returns_sum[state] / returns_count[state]
    return value_table
