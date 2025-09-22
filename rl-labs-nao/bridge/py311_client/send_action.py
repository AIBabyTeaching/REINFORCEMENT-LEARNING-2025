"""Python 3.11 helper for sending actions to the NAO bridge."""
from __future__ import annotations

import argparse
import queue
import threading
import time
from dataclasses import dataclass
from typing import Any, Dict, Optional

import requests

RATE_LIMIT_SECONDS = 1.0


@dataclass
class PendingCommand:
    endpoint: str
    payload: Dict[str, Any]


class CommandSender:
    def __init__(self, host: str, rate_limit: float = RATE_LIMIT_SECONDS) -> None:
        self.host = host.rstrip("/")
        self.rate_limit = rate_limit
        self._queue: "queue.Queue[PendingCommand]" = queue.Queue()
        self._last_sent = 0.0
        self._thread = threading.Thread(target=self._worker, daemon=True)
        self._thread.start()

    def enqueue(self, endpoint: str, payload: Dict[str, Any]) -> None:
        self._queue.put(PendingCommand(endpoint, payload))

    def _worker(self) -> None:
        last_payload: Optional[PendingCommand] = None
        while True:
            cmd = self._queue.get()
            if last_payload and last_payload.endpoint == cmd.endpoint and last_payload.payload == cmd.payload:
                # Drop duplicate command
                continue
            now = time.time()
            sleep_time = max(0.0, self.rate_limit - (now - self._last_sent))
            if sleep_time:
                time.sleep(sleep_time)
            try:
                response = requests.post(f"{self.host}/{cmd.endpoint}", json=cmd.payload, timeout=5)
                response.raise_for_status()
                print(f"Sent {cmd.endpoint}: {response.json()}")
            except Exception as exc:  # pragma: no cover - network errors
                print(f"Failed to send {cmd.endpoint}: {exc}")
            self._last_sent = time.time()
            last_payload = cmd
            self._queue.task_done()


_sender: Optional[CommandSender] = None


def get_sender(host: str) -> CommandSender:
    global _sender
    if _sender is None:
        _sender = CommandSender(host)
    return _sender


def send_say(text: str, host: str) -> None:
    get_sender(host).enqueue("say", {"text": text})


def send_wave(host: str) -> None:
    get_sender(host).enqueue("wave", {})


def send_head(yaw: float, pitch: float, host: str) -> None:
    get_sender(host).enqueue("head", {"yaw": yaw, "pitch": pitch})


def send_posture(name: str, host: str) -> None:
    get_sender(host).enqueue("posture", {"name": name})


def send_walk(dx: float, dy: float, dtheta: float, host: str) -> None:
    get_sender(host).enqueue("walk", {"dx": dx, "dy": dy, "dtheta": dtheta})


def main() -> None:
    parser = argparse.ArgumentParser(description="Send a single NAO action over HTTP")
    parser.add_argument("--host", required=True, help="Base URL of the NAO bridge, e.g. http://192.168.1.2:8000")
    parser.add_argument("--action", choices=["say", "wave", "head", "posture", "walk"], required=True)
    parser.add_argument("--payload", help="Payload for the action")
    args = parser.parse_args()

    host = args.host
    action = args.action
    payload = args.payload

    if action == "say":
        send_say(payload or "Hello!", host)
    elif action == "wave":
        send_wave(host)
    elif action == "head":
        if payload is None:
            raise SystemExit("--payload must be yaw,pitch for head action")
        yaw, pitch = map(float, payload.split(","))
        send_head(yaw, pitch, host)
    elif action == "posture":
        send_posture(payload or "StandInit", host)
    elif action == "walk":
        if payload is None:
            raise SystemExit("--payload must be dx,dy,dtheta for walk action")
        dx, dy, dtheta = map(float, payload.split(","))
        send_walk(dx, dy, dtheta, host)

    # Allow background thread to flush queue
    time.sleep(RATE_LIMIT_SECONDS + 0.5)


if __name__ == "__main__":
    main()
