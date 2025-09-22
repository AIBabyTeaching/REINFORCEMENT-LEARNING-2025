# Reinforcement Learning Laboratory Journey

This repository hosts a 12-lab, hands-on reinforcement learning (RL) pathway for AASTMT students. The experience moves from probability refreshers and tabular control to deep RL and NAO robot deployment, enabling students to build intuition, code fluency, and hardware confidence step by step.

## How to Use This Repository
1. **Start with Lab 01** to configure your environment and understand how the materials are organized.
2. **Work through each lab sequentially**—later activities depend on artifacts you create earlier.
3. **Consult the `old content/` archive** whenever you need background theory, solved examples, or NAO setup notes.
4. **Document your progress** in each lab folder, committing notebooks, scripts, and reports as you go.

## Lab Roadmap
| Lab | Title | Highlights |
| --- | --- | --- |
| 01 | [Orientation & Tooling](labs/lab01/README.md) | Environment setup, repository tour, and personal RL goals. |
| 02 | [Probability & Simulation Warm-Up](labs/lab02/README.md) | Random processes, empirical statistics, and visualization practice. |
| 03 | [Markov Decision Processes](labs/lab03/README.md) | Model sequential problems as MDPs and validate with simulations. |
| 04 | [Dynamic Programming for Policy Evaluation](labs/lab04/README.md) | Bellman updates, policy evaluation, and improvement loops. |
| 05 | [Monte Carlo Methods](labs/lab05/README.md) | Episodic prediction/control with exploring starts and ε-greedy exploration. |
| 06 | [Temporal-Difference Learning](labs/lab06/README.md) | TD(0), eligibility traces, and bias–variance reflections. |
| 07 | [Value-Based Control (SARSA & Q-Learning)](labs/lab07/README.md) | On-policy vs. off-policy control and exploration schedules. |
| 08 | [Function Approximation & DQN](labs/lab08/README.md) | Deep Q-Network implementation with replay buffers and target networks. |
| 09 | [Policy Gradient & Actor-Critic Methods](labs/lab09/README.md) | REINFORCE, baselines, and introductory actor-critic workflows. |
| 10 | [NAO Simulator & SDK Warm-Up](labs/lab10/README.md) | NAOqi setup, simulator connectivity, and baseline robot behaviors. |
| 11 | [Learning-Driven NAO Behaviors](labs/lab11/README.md) | Deploy RL-informed policies on the NAO simulator and hardware. |
| 12 | [Capstone Demo & Reflection](labs/lab12/README.md) | Final project showcase, retrospective, and future directions. |

## Key Reference Materials
- **Legacy Notebook:** [`old content/ALL_WEEKS_V5 - Student.ipynb`](old%20content/ALL_WEEKS_V5%20-%20Student.ipynb)
- **Lecture Slides:** [`old content/Lec/intro_RL.pdf`](old%20content/Lec/intro_RL.pdf)
- **Solved Examples & Theory PDFs:**
  - [`old content/RL Solved Example - Updated.pdf`](old%20content/RL%20Solved%20Example%20-%20Updated.pdf)
  - [`old content/Section_3_MC.pdf`](old%20content/Section_3_MC.pdf)
  - [`old content/Section_10_MonteCarlo_Dynamic_1.pdf`](old%20content/Section_10_MonteCarlo_Dynamic_1.pdf)
  - [`old content/Section_10_MonteCarlo_Example_1.pdf`](old%20content/Section_10_MonteCarlo_Example_1.pdf)
  - [`old content/RL_Section8_pdf.pdf`](old%20content/RL_Section8_pdf.pdf)
- **Visual Aids:** [`old content/DQN_vs_Q.png`](old%20content/DQN_vs_Q.png), [`old content/optimal.png`](old%20content/optimal.png), [`old content/UpdateRuleExample.png`](old%20content/UpdateRuleExample.png)
- **NAO Resources:** [`old content/howto.txt`](old%20content/howto.txt), [`old content/NAO_LAB_REBIRTH.pdf`](old%20content/NAO_LAB_REBIRTH.pdf), [`old content/pynaoqi-python2.7-2.5.5.5-win32-vs2013.zip`](old%20content/pynaoqi-python2.7-2.5.5.5-win32-vs2013.zip)

> 📁 The `old content/` directory is intentionally preserved as an archive. Use it for background reading and supplemental exercises while relying on the new `labs/` structure for graded deliverables.

## Getting Started Checklist
- [ ] Install Python 3.10+ and create a virtual environment.
- [ ] Install required libraries (`numpy`, `matplotlib`, `pandas`, `gymnasium`, `torch`, etc.).
- [ ] Verify GPU availability (if applicable) with the Lab 01 environment check notebook.
- [ ] Review upcoming lab objectives to plan time for NAO hardware access.

## Contribution & Feedback
Instructors and teaching assistants are encouraged to open issues or pull requests to iterate on lab instructions, starter code, and grading rubrics. Students should report broken links or unclear steps via the course communication channel.

## Author

**Ahmed Métwalli** – [LinkedIn](https://www.linkedin.com/in/ahmed-m%C3%A9twalli/) | [ResearchGate](https://www.researchgate.net/profile/Ahmed-Metwalli)

Assistant Lecturer (MSc) at AASTMT focused on AI and Data Science. With over 15 publications and multidisciplinary projects spanning sign language, agriculture, surgery, textiles, accounting, signals, embedded systems, IoT, and optical and RF communications, he is now pursuing a Ph.D. on machine-learning-based wireless channel identification.
