"""Deterministic tests for policy and value iteration."""
from __future__ import annotations

import importlib.util
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[4]
if str(ROOT) not in __import__("sys").path:
    __import__("sys").path.insert(0, str(ROOT))

from common import mdp  # noqa: E402


def _load_module(name: str, relative: str):
    path = ROOT / relative
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)  # type: ignore[attr-defined]
    return module


policy_iteration = _load_module(
    "policy_iteration",
    "labs/03_dynamic_programming_pi_vi/solutions/policy_iteration.py",
)
value_iteration = _load_module(
    "value_iteration",
    "labs/03_dynamic_programming_pi_vi/solutions/value_iteration.py",
)


def build_world() -> mdp.Gridworld:
    return mdp.Gridworld(
        width=4,
        height=4,
        terminal_states=[(0, 0), (3, 3)],
        reward_map={(3, 3): 0.0},
        step_reward=-1.0,
    )


EXPECTED_VALUES = np.array([
    [0.0, -1.0, -2.0, -3.0],
    [-1.0, -2.0, -3.0, -2.0],
    [-2.0, -3.0, -2.0, -1.0],
    [-3.0, -2.0, -1.0, 0.0],
])


def test_value_iteration_converges():
    world = build_world()
    values, policy = value_iteration.value_iteration(world, gamma=1.0, tolerance=1e-8)
    assert np.allclose(values.reshape(4, 4), EXPECTED_VALUES, atol=1e-6)
    assert policy.shape == (16, 4)
    assert np.isclose(policy.sum(axis=1), 1.0).all()


def test_policy_iteration_matches_value_iteration():
    world = build_world()
    v_vi, policy_vi = value_iteration.value_iteration(world, gamma=0.9)
    v_pi, policy_pi = policy_iteration.policy_iteration(world, gamma=0.9)
    assert np.allclose(v_vi, v_pi, atol=1e-4)
    assert np.allclose(policy_vi, policy_pi, atol=1e-4)
