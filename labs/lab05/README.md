# Lab 05 – Monte Carlo Methods

## Overview
Explore Monte Carlo prediction and control techniques for episodic tasks. Students will build or reuse a simulator (e.g., Blackjack) to estimate value functions from sampled returns.

## Learning Objectives
- Implement first-visit and every-visit Monte Carlo estimators.
- Compare exploring starts with ε-greedy behavior policies.
- Track policy improvement over episodes.

## Prerequisites
- Understanding of episodic MDPs from Labs 03–04.
- Familiarity with Python data handling (lists, dictionaries, NumPy arrays).

## Pre-Lab Preparation
- Review the Monte Carlo lecture decks [`old content/Section_10_MonteCarlo_Dynamic_1.pdf`](../../old%20content/Section_10_MonteCarlo_Dynamic_1.pdf) and [`old content/Section_10_MonteCarlo_Example_1.pdf`](../../old%20content/Section_10_MonteCarlo_Example_1.pdf).
- Revisit relevant segments in the legacy notebook [`old content/ALL_WEEKS_V5 - Student.ipynb`](../../old%20content/ALL_WEEKS_V5%20-%20Student.ipynb).

## In-Lab Activities
1. Implement Monte Carlo prediction for state values using first-visit returns.
2. Extend to action-value estimation with exploring starts.
3. Introduce ε-greedy action selection and observe policy evolution.
4. Discuss sample efficiency compared to dynamic programming.

## Post-Lab Deliverables
- Notebook with Monte Carlo code, learning curves, and commentary.
- Brief reflection on trade-offs between Monte Carlo and DP methods.

## Resources
- [`old content/UpdateRuleExample.png`](../../old%20content/UpdateRuleExample.png) to visualize incremental averaging.
- OpenAI Gymnasium environments for quick experimentation (e.g., Blackjack-v1).
