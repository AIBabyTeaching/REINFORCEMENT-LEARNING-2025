# Lab 04 – Dynamic Programming for Policy Evaluation

## Overview
Introduce iterative policy evaluation and improvement for tabular MDPs using dynamic programming. Students reuse the Lab 03 environment to compute value functions numerically and visualize convergence.

## Learning Objectives
- Implement policy evaluation via iterative Bellman updates.
- Apply policy improvement to derive a better policy from value estimates.
- Visualize convergence diagnostics and discuss stopping criteria.

## Prerequisites
- Completed Lab 03 with an MDP environment in code.
- Familiarity with matrix/vector operations in NumPy.

## Pre-Lab Preparation
- Review the dynamic programming sections in [`old content/Section_3_MC.pdf`](../../old%20content/Section_3_MC.pdf), focusing on Bellman expectation and optimality equations.
- Skim iterative update examples in [`old content/RL Solved Example - Updated.pdf`](../../old%20content/RL%20Solved%20Example%20-%20Updated.pdf).

## In-Lab Activities
1. Port your Lab 03 MDP into a notebook or script that supports vectorized value updates.
2. Implement iterative policy evaluation until the max value change drops below a tolerance.
3. Integrate a policy improvement loop to derive a better policy.
4. Plot the evolution of value estimates or residuals across iterations.

## Post-Lab Deliverables
- Notebook or script containing policy evaluation/improvement implementations.
- Short commentary on convergence speed and the impact of tolerance settings.

## Resources
- [`old content/optimal.png`](../../old%20content/optimal.png) to discuss optimal policies visually.
- Instructor-supplied starter code for tabular value iteration (optional).
