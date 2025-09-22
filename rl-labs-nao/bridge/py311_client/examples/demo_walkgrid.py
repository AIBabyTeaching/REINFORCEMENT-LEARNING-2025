from __future__ import annotations

import random
import time

from send_action import send_head, send_posture, send_say, send_walk

HOST = "http://localhost:8000"
GRID_ACTIONS = [
    (0.1, 0.0, 0.0, "Forward"),
    (-0.1, 0.0, 0.0, "Backward"),
    (0.0, 0.1, 0.0, "Left"),
    (0.0, -0.1, 0.0, "Right"),
]

if __name__ == "__main__":
    send_posture("StandInit", HOST)
    time.sleep(2.0)
    for _ in range(4):
        dx, dy, dtheta, label = random.choice(GRID_ACTIONS)
        send_say(f"Moving {label}", HOST)
        send_head(0.0, -0.1, HOST)
        send_walk(dx, dy, dtheta, HOST)
        time.sleep(3.0)
