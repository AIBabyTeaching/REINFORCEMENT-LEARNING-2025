# NAO Bridge

The bridge enables Python 3.11 notebooks to communicate with NAO's Python 2.7 runtime. A lightweight HTTP server exposes NAOqi actions while the Python 3.11 client throttles and queues outgoing commands.

## Components

- `py27_nao_service/`: Python 2.7 HTTP server wrapping NAOqi primitives.
- `py311_client/`: Python 3.11 helper functions and examples to send JSON commands.

## Quick start

1. **Python 2.7 service**
   ```bash
   cd bridge/py27_nao_service
   pip install -r requirements.txt
   python server.py --host 0.0.0.0 --port 8000 --nao-ip 192.168.1.10
   ```
   This launches an HTTP service that forwards `/say`, `/wave`, `/head`, `/posture`, and `/walk` requests to NAOqi.

2. **Python 3.11 client**
   ```bash
   cd bridge/py311_client
   python send_action.py --host http://192.168.1.10:8000 --action say --payload "Hello class!"
   ```
   The client enforces a configurable rate limit (`RATE_LIMIT_SECONDS`) and deduplicates consecutive commands to protect the robot.

## Integration in notebooks

Lab 10 demonstrates mapping gridworld actions to NAO behaviours by importing `send_action.py` and calling `send_wave()` or `send_posture("StandInit")`. The helper automatically serialises payloads, handles HTTP errors, and logs results for reproducibility.

> For offline development, the client can be pointed at `http://localhost:8000` and the service run on the same workstation with `--dry-run` to print commands instead of sending them to NAOqi.
