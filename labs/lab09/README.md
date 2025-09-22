# Lab 09 – Policy Gradient & Actor-Critic Methods

## Overview
Introduce policy gradient techniques for problems where value-based methods struggle. Students will implement REINFORCE and add baselines or simple actor-critic variants to reduce variance.

## Learning Objectives
- Derive and implement the REINFORCE algorithm with softmax policies.
- Incorporate baseline functions to reduce gradient variance.
- Extend to an actor-critic architecture with shared parameters.

## Prerequisites
- Completion of Lab 08 with experience training neural networks for control.
- Comfort with automatic differentiation frameworks (PyTorch preferred).

## Pre-Lab Preparation
- Study [`old content/RL_Section8_pdf.pdf`](../../old%20content/RL_Section8_pdf.pdf) for policy gradient theorem derivations.
- Review any policy gradient code snippets archived in [`old content/ALL_WEEKS_V5 - Student.ipynb`](../../old%20content/ALL_WEEKS_V5%20-%20Student.ipynb).

## In-Lab Activities
1. Implement the REINFORCE algorithm for a discrete-action environment (e.g., CartPole with softmax policy).
2. Add a learned baseline or value function to create a variance-reduced estimator.
3. Explore an actor-critic setup with simultaneous policy and value updates.
4. Compare learning curves with and without baselines.

## Post-Lab Deliverables
- Notebook containing REINFORCE and actor-critic implementations, plus comparison plots.
- Reflection on variance sources and strategies for stabilization.

## Resources
- [`old content/optimal.png`](../../old%20content/optimal.png) for visual discussion on optimal policies.
- Suggested reading: Sutton & Barto Chapter 13 or equivalent policy gradient tutorials.
