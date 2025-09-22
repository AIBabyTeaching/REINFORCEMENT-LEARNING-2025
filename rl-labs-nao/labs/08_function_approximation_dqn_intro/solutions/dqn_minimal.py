"""Minimal DQN components for educational use."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Tuple

import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim

ROOT = Path(__file__).resolve().parents[3]
if str(ROOT) not in __import__("sys").path:
    __import__("sys").path.insert(0, str(ROOT))

from common import utils  # noqa: E402


class QNetwork(nn.Module):
    def __init__(self, state_dim: int, action_dim: int, hidden_dim: int = 64) -> None:
        super().__init__()
        self.layers = nn.Sequential(
            nn.Linear(state_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, action_dim),
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:  # type: ignore[override]
        return self.layers(x)


@dataclass
class DQNConfig:
    gamma: float = 0.99
    lr: float = 1e-3
    batch_size: int = 32
    target_update: int = 100
    replay_size: int = 10000
    start_training: int = 1000
    epsilon_start: float = 1.0
    epsilon_end: float = 0.05
    epsilon_decay: int = 10000


def linear_decay(step: int, start: float, end: float, decay: int) -> float:
    fraction = min(1.0, step / decay)
    return start + fraction * (end - start)


def train_dqn(env, episodes: int, config: DQNConfig) -> Tuple[list[float], QNetwork]:
    utils.set_global_seeds(42)
    device = torch.device("cpu")
    state_dim = env.observation_space.shape[0]
    action_dim = env.action_space.n

    policy_net = QNetwork(state_dim, action_dim).to(device)
    target_net = QNetwork(state_dim, action_dim).to(device)
    target_net.load_state_dict(policy_net.state_dict())
    optimizer = optim.Adam(policy_net.parameters(), lr=config.lr)
    replay = utils.ReplayBuffer(config.replay_size)

    rewards_history: list[float] = []
    global_step = 0

    for episode in range(episodes):
        state, _ = env.reset()
        state = np.asarray(state, dtype=np.float32)
        done = False
        episode_reward = 0.0
        while not done:
            epsilon = linear_decay(global_step, config.epsilon_start, config.epsilon_end, config.epsilon_decay)
            if np.random.rand() < epsilon:
                action = env.action_space.sample()
            else:
                with torch.no_grad():
                    q_values = policy_net(torch.tensor(state).to(device))
                    action = int(torch.argmax(q_values).item())
            next_state, reward, terminated, truncated, _ = env.step(action)
            next_state = np.asarray(next_state, dtype=np.float32)
            replay.push(
                utils.Transition(state=state, action=action, reward=reward, next_state=next_state, done=terminated or truncated)
            )
            state = next_state
            episode_reward += reward
            done = terminated or truncated
            global_step += 1

            if len(replay) >= config.start_training:
                batch = replay.sample(config.batch_size)
                batch_state = torch.tensor(np.array([b.state for b in batch]), dtype=torch.float32, device=device)
                batch_next = torch.tensor(np.array([b.next_state for b in batch]), dtype=torch.float32, device=device)
                batch_reward = torch.tensor([b.reward for b in batch], dtype=torch.float32, device=device)
                batch_action = torch.tensor([b.action for b in batch], dtype=torch.int64, device=device)
                batch_done = torch.tensor([b.done for b in batch], dtype=torch.float32, device=device)

                q_values = policy_net(batch_state).gather(1, batch_action.unsqueeze(1)).squeeze(1)
                with torch.no_grad():
                    next_q = target_net(batch_next).max(1)[0]
                    target = batch_reward + config.gamma * next_q * (1.0 - batch_done)
                loss = nn.functional.mse_loss(q_values, target)

                optimizer.zero_grad()
                loss.backward()
                nn.utils.clip_grad_norm_(policy_net.parameters(), 1.0)
                optimizer.step()

            if global_step % config.target_update == 0:
                target_net.load_state_dict(policy_net.state_dict())
        rewards_history.append(episode_reward)
    return rewards_history, policy_net
