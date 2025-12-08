"""Minimal Markov Decision Process helpers for tabular environments."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Iterable, List, Tuple

import numpy as np


@dataclass(frozen=True)
class State:
    """Immutable representation of a state."""

    name: Tuple[int, int]
    terminal: bool = False


@dataclass(frozen=True)
class Action:
    """Immutable representation of an action."""

    name: str


@dataclass(frozen=True)
class Transition:
    """State transition with probability and reward."""

    next_state: State
    probability: float
    reward: float


class Gridworld:
    """Deterministic gridworld with optional terminal and obstacle states."""

    def __init__(
        self,
        width: int,
        height: int,
        terminal_states: Iterable[Tuple[int, int]] | None = None,
        reward_map: Dict[Tuple[int, int], float] | None = None,
        step_reward: float = -1.0,
    ) -> None:
        self.width = width
        self.height = height
        self.states: Dict[Tuple[int, int], State] = {}
        self.terminal_states = set(terminal_states or [])
        self.reward_map = reward_map or {}
        self.step_reward = step_reward
        for y in range(height):
            for x in range(width):
                coord = (x, y)
                self.states[coord] = State(coord, terminal=coord in self.terminal_states)
        self.actions = [Action("UP"), Action("DOWN"), Action("LEFT"), Action("RIGHT")]

    def state_index(self, coord: Tuple[int, int]) -> int:
        x, y = coord
        return y * self.width + x

    def transitions(self, state: State, action: Action) -> List[Transition]:
        if state.terminal:
            return [Transition(state, 1.0, 0.0)]
        x, y = state.name
        dx, dy = {
            "UP": (0, -1),
            "DOWN": (0, 1),
            "LEFT": (-1, 0),
            "RIGHT": (1, 0),
        }[action.name]
        nx, ny = min(max(x + dx, 0), self.width - 1), min(max(y + dy, 0), self.height - 1)
        next_state = self.states[(nx, ny)]
        reward = self.reward_map.get(next_state.name, self.step_reward)
        return [Transition(next_state, 1.0, reward)]

    def as_transition_matrices(self, gamma: float) -> Tuple[np.ndarray, np.ndarray]:
        """Return transition probability and reward matrices."""

        n_states = len(self.states)
        n_actions = len(self.actions)
        p = np.zeros((n_actions, n_states, n_states))
        r = np.zeros((n_actions, n_states, n_states))
        for a_idx, action in enumerate(self.actions):
            for state in self.states.values():
                s_idx = self.state_index(state.name)
                for transition in self.transitions(state, action):
                    ns_idx = self.state_index(transition.next_state.name)
                    p[a_idx, s_idx, ns_idx] += transition.probability
                    r[a_idx, s_idx, ns_idx] = transition.reward
        return p, r * gamma


def policy_evaluation(
    policy: np.ndarray,
    transition_probabilities: np.ndarray,
    rewards: np.ndarray,
    gamma: float,
    tolerance: float = 1e-6,
) -> np.ndarray:
    """Evaluate a policy for a finite MDP."""

    n_states = policy.shape[0]
    value = np.zeros(n_states)
    delta = np.inf
    while delta > tolerance:
        delta = 0.0
        for s in range(n_states):
            v = value[s]
            new_v = 0.0
            for a in range(policy.shape[1]):
                new_v += policy[s, a] * np.sum(
                    transition_probabilities[a, s] * (rewards[a, s] + gamma * value)
                )
            value[s] = new_v
            delta = max(delta, abs(v - new_v))
    return value
