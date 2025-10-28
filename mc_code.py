# -*- coding: utf-8 -*-
"""
Markov posture controller for NAO (Py2.7 + NAOqi 2.x), no speech output.
- States: sitting, staying, standing
- Transition matrix P (rows sum to 1)
- Head-swipe trigger (Front->Middle->Rear OR Rear->Middle->Front within 1.2 s)
- On swipe: steady-state (theoretical) + empirical distribution are PRINTED to terminal
- CSV logs:
    - posture_log.csv               : timestamp, state
    - steady_state_snapshots.csv    : timestamp, total_steps, empirical(*), theoretical(*)

Run:
  export NAO_IP=192.168.1.10
  python2 nao_posture_markov_swipe_stats_nospeech.py --ip $NAO_IP --port 9559
"""

from __future__ import print_function
import qi, argparse, sys, time, os, csv, random
from collections import deque

# ---------- user-tunable parameters ----------
PERIOD_S = 3.0                 # pacing between decision points
SIT_SPEED = 0.6                # ALRobotPosture speed
STAND_SPEED = 0.6              # ALRobotPosture speed
SWIPE_WINDOW_S = 1.2           # window to complete the 3-tap sequence
COOLDOWN_S = 2.0               # suppress repeated triggers within this time
POWER_ITERS = 200              # iterations for stationary distribution power method
POWER_TOL = 1e-10              # early-stop tolerance for power method
# --------------------------------------------

# State order must match matrix indexing
STATES = ["sitting", "staying", "standing"]
IDX = dict((s, i) for i, s in enumerate(STATES))

# Transition matrix P in the above order: rows sum to 1 (example values)
P = [
    [0.70, 0.25, 0.05],  # sitting
    [0.20, 0.60, 0.20],  # staying
    [0.05, 0.25, 0.70],  # standing
]

def now_str():
    return time.strftime("%Y-%m-%d %H:%M:%S")

def csv_append(path, header, row):
    newfile = not os.path.exists(path)
    with open(path, 'ab') as f:  # 'ab' avoids extra blank lines on Win/Py2
        w = csv.writer(f)
        if newfile:
            w.writerow(header)
        w.writerow(row)

def sample_next(current_state):
    row = P[IDX[current_state]]
    r, acc = random.random(), 0.0
    for j, p in enumerate(row):
        acc += p
        if r <= acc:
            return STATES[j]
    return STATES[-1]

def power_stationary(Pmat, iters=POWER_ITERS, tol=POWER_TOL):
    """
    Stationary distribution estimate for an ergodic 3x3 transition matrix:
      pi_{k+1} = pi_k * P
    Starting from uniform; early stop when L1-change < tol.
    """
    n = len(Pmat)
    pi = [1.0 / n] * n
    for _ in range(iters):
        nxt = [0.0] * n
        for j in range(n):          # column index
            colsum = 0.0
            for i in range(n):      # row index
                colsum += pi[i] * Pmat[i][j]
            nxt[j] = colsum
        total = sum(nxt)
        if total > 0:
            nxt = [x / total for x in nxt]
        if sum(abs(nxt[k] - pi[k]) for k in range(n)) < tol:
            pi = nxt
            break
        pi = nxt
    return pi

class PostureMarkov(object):
    def __init__(self, session):
        # Services (no TTS used)
        self.posture = session.service("ALRobotPosture")
        self.motion  = session.service("ALMotion")
        self.memory  = session.service("ALMemory")

        # Head tactile subscriptions
        self._subs = []
        self._events = deque(maxlen=12)
        self._last_trigger_t = 0.0
        self._request_stats = False  # set by swipe callback
        self._wire_head_swipe()

        # Runtime state & stats
        self.current = "staying"
        self.total_steps = 0
        self.counts = dict((s, 0) for s in STATES)

        # File paths
        self.log_path = "posture_log.csv"
        self.snap_path = "steady_state_snapshots.csv"

        # Start posture
        try:
            self.motion.wakeUp()
            self.posture.goToPosture("StandInit", STAND_SPEED)
        except Exception:
            pass

        print("[{}] Controller started. Head swipe to print statistics.".format(now_str()))
        sys.stdout.flush()

    # ---------- tactile wiring ----------
    def _wire_head_swipe(self):
        for key, name in [
            ("FrontTactilTouched",  "Front"),
            ("MiddleTactilTouched", "Middle"),
            ("RearTactilTouched",   "Rear"),
        ]:
            sub = self.memory.subscriber(key)
            sub.signal.connect(self._make_cb(name))
            self._subs.append(sub)

    def _make_cb(self, name):
        def _cb(value):
            try:
                if float(value) >= 0.5:
                    self._record_touch(name)
            except Exception:
                pass
        return _cb

    def _record_touch(self, name):
        t = time.time()
        self._events.append((name, t))
        # prune window
        while self._events and (t - self._events[0][1] > SWIPE_WINDOW_S):
            self._events.popleft()
        self._maybe_request_stats(t)

    def _maybe_request_stats(self, tnow):
        if (tnow - self._last_trigger_t) < COOLDOWN_S:
            return
        seq = [n for (n, _) in self._events]
        if self._has_subsequence(seq, ["Front", "Middle", "Rear"]) \
           or self._has_subsequence(seq, ["Rear", "Middle", "Front"]):
            self._last_trigger_t = tnow
            self._request_stats = True

    @staticmethod
    def _has_subsequence(seq, pattern):
        it = iter(seq)
        try:
            for p in pattern:
                while True:
                    v = next(it)
                    if v == p:
                        break
            return True
        except StopIteration:
            return False

    # ---------- actions ----------
    def _do_action(self, state):
        # Only actions (no speech); logs are printed and written to CSV.
        try:
            if state == "sitting":
                self.posture.goToPosture("Sit", SIT_SPEED)
            elif state == "standing":
                self.posture.goToPosture("StandInit", STAND_SPEED)
            else:
                # 'staying' is a no-op posture-wise
                pass
        except Exception:
            pass

        # Stats + terminal log
        self.total_steps += 1
        self.counts[state] += 1
        msg = "[{}] ACTION: {:>8s} | totals: {}".format(
            now_str(), state, ", ".join("{}={}".format(s, self.counts[s]) for s in STATES)
        )
        print(msg); sys.stdout.flush()

        # CSV log of each executed state
        csv_append(self.log_path, ["timestamp", "state"], [now_str(), state])

    def _print_stats(self, empirical, theoretical):
        # Pretty terminal print for snapshot
        print("\n===== STATS SNAPSHOT @ {} =====".format(now_str()))
        print("Total steps: {}".format(self.total_steps))

        # empirical as counts and percentages
        def pct(x): return "{:6.2f}%".format(100.0 * x)
        emp_line = "Empirical: " + ", ".join(
            "{}={} ({})".format(s, self.counts[s], pct(empirical[IDX[s]])) for s in STATES
        )
        print(emp_line)

        # theoretical pi
        theo_line = "Theoretical steady-state (pi): " + ", ".join(
            "{}={:.6f}".format(s, theoretical[IDX[s]]) for s in STATES
        )
        print(theo_line)
        print("========================================\n")
        sys.stdout.flush()

    def _snapshot(self):
        # Empirical distribution
        if self.total_steps > 0:
            empirical = [self.counts[s] / float(self.total_steps) for s in STATES]
        else:
            empirical = [0.0, 0.0, 0.0]

        # Theoretical steady-state
        theoretical = power_stationary(P)

        # CSV snapshot
        header = ["timestamp", "total_steps"] + \
                 ["emp_"+s for s in STATES] + ["theo_"+s for s in STATES]
        row = [now_str(), self.total_steps] + empirical + theoretical
        csv_append(self.snap_path, header, row)

        # Terminal print
        self._print_stats(empirical, theoretical)

    # ---------- main loop ----------
    def run(self):
        try:
            while True:
                # Action for the current state
                self._do_action(self.current)

                # Swipe-triggered snapshot (if requested)
                if self._request_stats:
                    self._request_stats = False
                    self._snapshot()

                # Next state
                self.current = sample_next(self.current)

                # Loop pacing
                slept = 0.0
                while slept < PERIOD_S:
                    time.sleep(0.1); slept += 0.1
        except KeyboardInterrupt:
            pass
        finally:
            print("[{}] Stopping. Going to rest.".format(now_str()))
            sys.stdout.flush()
            try:
                self.motion.rest()
            except Exception:
                pass

def main(ip, port):
    app = qi.Application(["NAO_Posture_Markov_NoSpeech", "--qi-url", "tcp://%s:%d" % (ip, port)])
    try:
        app.start()
    except RuntimeError:
        print("[ERR] Connection failed. Check NAO_IP/port and network.", file=sys.stderr)
        sys.exit(1)

    session = app.session
    ctrl = PostureMarkov(session)
    ctrl.run()
    app.stop()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip",   type=str, default="1.1.1.21")
    parser.add_argument("--port", type=int, default=9559)
    args = parser.parse_args()
    main(args.ip, args.port)
