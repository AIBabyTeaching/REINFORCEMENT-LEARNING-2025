from __future__ import annotations

import time

from send_action import send_posture, send_wave

HOST = "http://localhost:8000"

if __name__ == "__main__":
    send_posture("StandInit", HOST)
    time.sleep(2.0)
    send_wave(HOST)
    time.sleep(5.0)
