# Reinforcement Learning 2025 Resources

## Notebooks
- `notebooks/q_learning_gym.ipynb` – Demonstrates tabular and deep Q-learning on Gymnasium's FrozenLake environment using Stable-Baselines3. The notebook includes explanatory markdown cells, plots of training dynamics, and a comparative discussion of algorithm variants.

## Dependencies
To execute the new notebook locally, install:

```bash
pip install gymnasium==0.29.1 stable-baselines3==2.7.0 sb3-contrib==2.7.0 matplotlib numpy pandas
```

Stable-Baselines3 and sb3-contrib must be installed at matching versions—`2.7.0` in this repository—to avoid import errors such as missing `FloatSchedule`. The pins above mirror the canonical list in [`rl-labs-nao/requirements.txt`](rl-labs-nao/requirements.txt). These packages complement the existing Python tooling in the repository and provide the Gym environment along with plotting utilities.
