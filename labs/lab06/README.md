# Lab 06 – Temporal-Difference Learning

## Overview
Transition from Monte Carlo methods to temporal-difference (TD) learning with incremental updates. Students will implement TD(0) and eligibility traces, comparing performance with Monte Carlo baselines.

## Learning Objectives
- Implement TD(0) prediction for value estimation.
- Understand eligibility traces and TD(λ) intuition.
- Compare convergence speed and sample efficiency versus Monte Carlo approaches.

## Prerequisites
- Completed Lab 05 with Monte Carlo code available for comparison.
- Comfort manipulating NumPy arrays and plotting tools.

## Pre-Lab Preparation
- Revisit the solved examples highlighting TD behavior in [`old content/RL Solved Example - Updated.pdf`](../../old%20content/RL%20Solved%20Example%20-%20Updated.pdf).
- Review any TD-focused notes embedded in [`old content/ALL_WEEKS_V5 - Student.ipynb`](../../old%20content/ALL_WEEKS_V5%20-%20Student.ipynb).

## In-Lab Activities
1. Implement TD(0) for the random walk or Blackjack tasks from prior labs.
2. Add eligibility traces to experiment with TD(λ) variants.
3. Plot learning curves comparing TD and Monte Carlo approaches.
4. Discuss the bias-variance trade-off inherent in TD learning.

## Post-Lab Deliverables
- Notebook showcasing TD implementations, experiments, and plots.
- Short write-up summarizing insights on TD vs. Monte Carlo.

## Resources
- [`old content/DQN_vs_Q.png`](../../old%20content/DQN_vs_Q.png) to preview discussions about value approximation to come.
- Open-source RL textbooks or Sutton & Barto Chapter 6 for supplemental reading.
