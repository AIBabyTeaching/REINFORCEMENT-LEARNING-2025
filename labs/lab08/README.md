# Lab 08 – Function Approximation & Deep Q-Networks

## Overview
Move beyond tabular methods by implementing a lightweight Deep Q-Network (DQN) for environments where state spaces are large or continuous. Students will focus on network design, replay buffers, and training stability.

## Learning Objectives
- Configure a neural network to approximate action-value functions.
- Implement experience replay and target network updates.
- Monitor training curves and diagnose divergence or instability.

## Prerequisites
- Working knowledge of PyTorch or TensorFlow from prior coursework.
- Completion of Lab 07 for familiarity with value-based control concepts.

## Pre-Lab Preparation
- Watch a short DQN explainer video (instructor curated) to preview architecture choices.
- Review the comparative figure [`old content/DQN_vs_Q.png`](../../old%20content/DQN_vs_Q.png) to recall tabular vs. deep approaches.

## In-Lab Activities
1. Set up the CartPole-v1 environment (or similar) using Gymnasium.
2. Implement a minimal DQN with replay buffer, target network, and ε-greedy exploration.
3. Train the agent for several episodes while logging loss, rewards, and ε schedule.
4. Experiment with hyperparameters (learning rate, batch size, target update frequency) and document findings.

## Post-Lab Deliverables
- Notebook detailing the DQN implementation, training curves, and tuning experiments.
- Reflection on stabilization tricks (replay, target networks) and remaining challenges.

## Resources
- [`old content/optimal.png`](../../old%20content/optimal.png) to connect deep RL performance with optimal policy intuition.
- Links to PyTorch/TensorFlow quickstarts for neural network setup.
