# Lab 10 – NAO Simulator & SDK Warm-Up

## Overview
Transition from simulation-only exercises to NAO robot experimentation. Students will install NAOqi tooling, connect to the simulator or a virtual robot, and execute basic motion/speech routines.

## Learning Objectives
- Install and configure the NAOqi SDK and simulator dependencies.
- Connect to a virtual NAO and execute sample behaviors.
- Capture telemetry and debug connection issues.

## Prerequisites
- Completion of Labs 01–09 to build RL background.
- Access to a machine that supports the NAOqi environment (Python 2.7 requirements noted below).

## Pre-Lab Preparation
- Read the setup checklist in [`old content/howto.txt`](../../old%20content/howto.txt), including environment variables, Python 2.7 installation, and simulator download links.
- Review the NAO lab overview in [`old content/NAO_LAB_REBIRTH.pdf`](../../old%20content/NAO_LAB_REBIRTH.pdf).

## In-Lab Activities
1. Install NAOqi Python 2.7 bindings using the provided archive [`old content/pynaoqi-python2.7-2.5.5.5-win32-vs2013.zip`](../../old%20content/pynaoqi-python2.7-2.5.5.5-win32-vs2013.zip) or platform-specific resources.
2. Configure `PYTHONPATH` and confirm `naoqi` imports in a Python 2.7 shell.
3. Launch Choregraphe or the NAO simulator and establish a network connection.
4. Run starter scripts for speech, posture, and simple motions; log console output and screenshots.

## Post-Lab Deliverables
- Setup log capturing installation steps, environment variables, and troubleshooting notes.
- Minimal example scripts (e.g., wave, introduce itself) committed to the lab folder.
- Simulator screenshots or screen recordings demonstrating successful execution.

## Resources
- [`old content/notepad.txt`](../../old%20content/notepad.txt) for quick reminders compiled from previous NAO sessions.
- Aldebaran/SoftBank official documentation (links curated by instructors).
