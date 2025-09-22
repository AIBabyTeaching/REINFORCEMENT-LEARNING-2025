"""Reference implementations for multi-armed bandits."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import List, Tuple

import numpy as np

ROOT = Path(__file__).resolve().parents[3]
if str(ROOT) not in __import__("sys").path:
    __import__("sys").path.insert(0, str(ROOT))

from common import utils  # noqa: E402


@dataclass
class BanditArm:
    mean: float
    std: float = 1.0

    def pull(self, rng: np.random.Generator) -> float:
        return rng.normal(self.mean, self.std)


class EpsilonGreedyAgent:
    def __init__(self, n_arms: int, epsilon: float, optimistic: float = 0.0, seed: int = 0) -> None:
        self.n_arms = n_arms
        self.epsilon = epsilon
        self.q_values = np.full(n_arms, optimistic, dtype=float)
        self.counts = np.zeros(n_arms, dtype=int)
        self.rng = np.random.default_rng(seed)

    def select_action(self, step: int) -> int:
        if self.rng.random() < self.epsilon:
            return int(self.rng.integers(self.n_arms))
        return int(np.argmax(self.q_values))

    def update(self, arm: int, reward: float) -> None:
        self.counts[arm] += 1
        step_size = 1.0 / self.counts[arm]
        self.q_values[arm] += step_size * (reward - self.q_values[arm])


class UCBAgent:
    def __init__(self, n_arms: int, c: float = 2.0, seed: int = 0) -> None:
        self.n_arms = n_arms
        self.c = c
        self.q_values = np.zeros(n_arms, dtype=float)
        self.counts = np.ones(n_arms, dtype=int)
        self.rng = np.random.default_rng(seed)

    def select_action(self, step: int) -> int:
        bonuses = self.c * np.sqrt(np.log(step + 1) / self.counts)
        return int(np.argmax(self.q_values + bonuses))

    def update(self, arm: int, reward: float) -> None:
        self.counts[arm] += 1
        step_size = 1.0 / self.counts[arm]
        self.q_values[arm] += step_size * (reward - self.q_values[arm])


def run_bandit(
    arms: List[BanditArm],
    agent,
    steps: int = 200,
    seed: int = 0,
) -> Tuple[np.ndarray, np.ndarray]:
    rng = np.random.default_rng(seed)
    rewards = np.zeros(steps)
    optimal = np.zeros(steps)
    optimal_arm = int(np.argmax([arm.mean for arm in arms]))

    for step in range(steps):
        action = agent.select_action(step + 1)
        reward = arms[action].pull(rng)
        agent.update(action, reward)
        rewards[step] = reward
        optimal[step] = 1.0 if action == optimal_arm else 0.0
    return rewards, optimal
