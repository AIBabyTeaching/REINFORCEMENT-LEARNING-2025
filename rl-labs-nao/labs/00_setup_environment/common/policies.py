"""Policy utilities."""
from __future__ import annotations

import math
import random
from typing import Iterable, List

import numpy as np


def epsilon_greedy(q_values: np.ndarray, epsilon: float) -> int:
    if random.random() < epsilon:
        return random.randrange(len(q_values))
    return int(np.argmax(q_values))


def softmax(q_values: np.ndarray, temperature: float) -> np.ndarray:
    scaled = q_values / max(temperature, 1e-8)
    scaled -= np.max(scaled)
    probs = np.exp(scaled)
    probs /= np.sum(probs)
    return probs


def deterministic_policy_from_q(q_table: np.ndarray) -> np.ndarray:
    greedy_actions = np.argmax(q_table, axis=1)
    policy = np.zeros_like(q_table)
    for state, action in enumerate(greedy_actions):
        policy[state, action] = 1.0
    return policy


def schedule_linear(start: float, end: float, steps: int) -> List[float]:
    if steps <= 1:
        return [end]
    delta = (end - start) / (steps - 1)
    return [start + i * delta for i in range(steps)]


def ucb_action(q_values: np.ndarray, counts: Iterable[int], step: int, c: float = 2.0) -> int:
    counts = np.array(counts, dtype=float)
    counts[counts == 0] = 1e-6
    bonuses = c * np.sqrt(math.log(step + 1) / counts)
    return int(np.argmax(q_values + bonuses))
