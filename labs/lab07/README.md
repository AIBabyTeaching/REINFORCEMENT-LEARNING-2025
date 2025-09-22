# Lab 07 – Value-Based Control (SARSA & Q-Learning)

## Overview
Dive into control with temporal-difference methods by implementing SARSA and Q-learning on discrete environments. Students will analyze on-policy vs. off-policy behavior and exploration strategies.

## Learning Objectives
- Implement SARSA and Q-learning algorithms with ε-greedy exploration.
- Compare learning curves and policy quality under different exploration rates.
- Discuss stability considerations for on-policy vs. off-policy methods.

## Prerequisites
- Completion of Lab 06 to build on TD learning insights.
- Experience with OpenAI Gymnasium environments or equivalent simulations.

## Pre-Lab Preparation
- Review SARSA vs. Q-learning visual comparisons in [`old content/DQN_vs_Q.png`](../../old%20content/DQN_vs_Q.png).
- Revisit control sections within [`old content/ALL_WEEKS_V5 - Student.ipynb`](../../old%20content/ALL_WEEKS_V5%20-%20Student.ipynb).

## In-Lab Activities
1. Select a benchmark environment (e.g., CliffWalking-v0, Taxi-v3) and reset seeds for reproducibility.
2. Implement SARSA with decaying ε-greedy exploration; log episodic returns.
3. Implement Q-learning with the same environment for comparison.
4. Analyze stability, convergence speed, and sensitivity to hyperparameters.

## Post-Lab Deliverables
- Consolidated notebook summarizing SARSA and Q-learning implementations.
- Short memo contrasting exploration/exploitation trade-offs observed.

## Resources
- [`old content/optimal.png`](../../old%20content/optimal.png) for discussing optimal policy structures.
- Links to Gymnasium documentation for environment-specific APIs.
