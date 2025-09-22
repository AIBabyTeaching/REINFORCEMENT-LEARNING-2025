# -*- coding: utf-8 -*-
"""Thin wrappers around NAOqi primitives."""
from __future__ import unicode_literals

try:
    from naoqi import ALProxy
except ImportError:
    ALProxy = None  # type: ignore


def _proxy(name, ip, port):
    if ALProxy is None:
        raise RuntimeError("NAOqi SDK not available")
    return ALProxy(name, ip, port)


def say(ip, port, text):
    proxy = _proxy("ALTextToSpeech", ip, port)
    proxy.say(text)


def wave(ip, port):
    motion = _proxy("ALMotion", ip, port)
    posture = _proxy("ALRobotPosture", ip, port)
    if not motion.robotIsWakeUp():
        motion.wakeUp()
    posture.goToPosture("StandInit", 0.5)
    names = ["RShoulderPitch", "RShoulderRoll", "RElbowYaw", "RElbowRoll", "RWristYaw"]
    angles = [1.5, -0.3, 0.0, 1.0, 0.0]
    times = [1.0, 1.0, 1.0, 1.0, 1.0]
    motion.angleInterpolation(names, angles, times, True)


def head(ip, port, yaw, pitch):
    motion = _proxy("ALMotion", ip, port)
    motion.setAngles(["HeadYaw", "HeadPitch"], [yaw, pitch], 0.1)


def posture(ip, port, name):
    proxy = _proxy("ALRobotPosture", ip, port)
    proxy.goToPosture(name, 0.5)


def walk(ip, port, dx, dy, dtheta):
    motion = _proxy("ALMotion", ip, port)
    motion.moveToward(dx, dy, dtheta)
