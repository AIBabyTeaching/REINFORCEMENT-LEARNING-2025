# -*- coding: utf-8 -*-
"""Python 2.7 Flask server bridging HTTP commands to NAOqi."""
from __future__ import unicode_literals

import argparse
import logging

from flask import Flask, jsonify, request

import nao_actions

app = Flask(__name__)
LOGGER = logging.getLogger("nao_bridge")


@app.route("/say", methods=["POST"])
def route_say():
    payload = request.get_json(force=True)
    text = payload.get("text", "Hello")
    nao_actions.say(app.config["NAO_IP"], app.config["NAO_PORT"], text)
    return jsonify({"status": "ok", "text": text})


@app.route("/wave", methods=["POST"])
def route_wave():
    nao_actions.wave(app.config["NAO_IP"], app.config["NAO_PORT"])
    return jsonify({"status": "ok"})


@app.route("/head", methods=["POST"])
def route_head():
    payload = request.get_json(force=True)
    yaw = float(payload.get("yaw", 0.0))
    pitch = float(payload.get("pitch", 0.0))
    nao_actions.head(app.config["NAO_IP"], app.config["NAO_PORT"], yaw, pitch)
    return jsonify({"status": "ok", "yaw": yaw, "pitch": pitch})


@app.route("/posture", methods=["POST"])
def route_posture():
    payload = request.get_json(force=True)
    name = payload.get("name", "StandInit")
    nao_actions.posture(app.config["NAO_IP"], app.config["NAO_PORT"], name)
    return jsonify({"status": "ok", "name": name})


@app.route("/walk", methods=["POST"])
def route_walk():
    payload = request.get_json(force=True)
    dx = float(payload.get("dx", 0.0))
    dy = float(payload.get("dy", 0.0))
    dtheta = float(payload.get("dtheta", 0.0))
    nao_actions.walk(app.config["NAO_IP"], app.config["NAO_PORT"], dx, dy, dtheta)
    return jsonify({"status": "ok", "dx": dx, "dy": dy, "dtheta": dtheta})


def main():
    parser = argparse.ArgumentParser(description="NAO bridge HTTP service")
    parser.add_argument("--host", default="0.0.0.0")
    parser.add_argument("--port", type=int, default=8000)
    parser.add_argument("--nao-ip", required=True)
    parser.add_argument("--nao-port", type=int, default=9559)
    parser.add_argument("--debug", action="store_true")
    args = parser.parse_args()

    logging.basicConfig(level=logging.DEBUG if args.debug else logging.INFO)
    app.config["NAO_IP"] = args.nao_ip
    app.config["NAO_PORT"] = args.nao_port

    LOGGER.info("Starting NAO bridge on %s:%s targeting %s:%s", args.host, args.port, args.nao_ip, args.nao_port)
    app.run(host=args.host, port=args.port, threaded=True)


if __name__ == "__main__":
    main()
