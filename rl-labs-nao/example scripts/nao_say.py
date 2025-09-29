# -*- coding: utf-8 -*-
"""Thin wrappers around NAOqi primitives."""
from __future__ import unicode_literals

try:
    from naoqi import ALProxy
    print("ALProxy Loaded Successfully at:", ALProxy)
except ImportError:
    ALProxy = None  # type: ignore

# --- Helpers (safe under unicode_literals) ---
def to_bytes(s):
    # In Py2.7: unicode -> UTF-8 bytes; str stays str; ints stay ints
    try:
        # unicode type exists in Py2
        unicode  # noqa
        if isinstance(s, unicode):
            return s.encode('utf-8')
    except NameError:
        pass
    return s if isinstance(s, str) else str(s)

def make_proxy(module, ip, port, keep_alive=True):
    module_b = to_bytes(module)
    ip_b = to_bytes(ip)
    port_i = int(port)
    try:
        return ALProxy(module_b, ip_b, port_i, bool(keep_alive))
    except NotImplementedError:
        # Fall back to the 3-arg overload if 4-arg is unavailable
        return ALProxy(module_b, ip_b, port_i)

# --- Your parameters (bytes are safest with unicode_literals present) ---
name = 'ALTextToSpeech'
ip   = '1.1.1.21'   # replace with your robot's IPv4
port = 9559
text = 'say hello'

# --- Build proxy and speak ---
tts = make_proxy(name, ip, port)
print(tts)
tts.say(to_bytes(text))
