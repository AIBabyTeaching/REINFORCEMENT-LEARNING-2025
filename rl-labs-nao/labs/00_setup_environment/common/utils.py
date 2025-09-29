"""Miscellaneous utilities for reproducibility and buffers."""
from __future__ import annotations

import collections
import random
from dataclasses import dataclass
from typing import Deque, Iterable, Iterator, List, Sequence, Tuple

import numpy as np

try:
    import torch
except Exception:  # pragma: no cover
    torch = None  # type: ignore


def set_global_seeds(seed: int) -> None:
    random.seed(seed)
    np.random.seed(seed)
    if torch is not None:
        torch.manual_seed(seed)
        if torch.cuda.is_available():
            torch.cuda.manual_seed_all(seed)


@dataclass
class Transition:
    state: np.ndarray
    action: int
    reward: float
    next_state: np.ndarray
    done: bool


class ReplayBuffer:
    def __init__(self, capacity: int) -> None:
        self.capacity = capacity
        self.buffer: Deque[Transition] = collections.deque(maxlen=capacity)

    def push(self, transition: Transition) -> None:
        self.buffer.append(transition)

    def sample(self, batch_size: int) -> List[Transition]:
        indices = np.random.choice(len(self.buffer), batch_size, replace=False)
        return [self.buffer[i] for i in indices]

    def __len__(self) -> int:
        return len(self.buffer)


def moving_average(sequence: Sequence[float], window: int) -> np.ndarray:
    sequence = np.asarray(sequence)
    if window <= 1:
        return sequence
    kernel = np.ones(window) / window
    return np.convolve(sequence, kernel, mode="valid")


def discounted_returns(rewards: Iterable[float], gamma: float) -> List[float]:
    returns: List[float] = []
    g = 0.0
    for reward in reversed(list(rewards)):
        g = reward + gamma * g
        returns.append(g)
    returns.reverse()
    return returns


def chunk_iterator(iterable: Iterable, batch_size: int) -> Iterator[Tuple]:
    batch: List = []
    for item in iterable:
        batch.append(item)
        if len(batch) == batch_size:
            yield tuple(batch)
            batch = []
    if batch:
        yield tuple(batch)
