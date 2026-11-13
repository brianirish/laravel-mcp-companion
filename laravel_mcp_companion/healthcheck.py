#!/usr/bin/env python3
"""Container health check: exit 0 when the server is healthy, 1 when it is not.

Run by the image's HEALTHCHECK. Over HTTP it asks the server's own /healthz,
which answers 200 while the server can serve documentation and 503 when it
cannot. Over stdio there is no port to ask; the process being alive is all a
check can establish, and Docker already knows that, so the check passes.

The transport, port and bind address are read the way the server reads them:
the command line of PID 1 first, then the environment.
"""

import os
import sys
import urllib.error
import urllib.request
from typing import Mapping, Optional, Sequence

DEFAULT_HTTP_PORT = 8081
TIMEOUT_SECONDS = 4


def _option(argv: Sequence[str], name: str) -> Optional[str]:
    """The value of `--name value` or `--name=value` in argv, if present."""
    for i, arg in enumerate(argv):
        if arg == name and i + 1 < len(argv):
            return argv[i + 1]
        if arg.startswith(name + "="):
            return arg.split("=", 1)[1]
    return None


def target(argv: Sequence[str], env: Mapping[str, str]) -> Optional[str]:
    """The /healthz URL to ask, or None when the server is on stdio."""
    transport = _option(argv, "--transport") or env.get("TRANSPORT") or "stdio"
    if transport != "http":
        return None

    port = _option(argv, "--port") or env.get("PORT") or str(DEFAULT_HTTP_PORT)
    host = _option(argv, "--host") or env.get("HOST") or "127.0.0.1"
    # A wildcard bind address is not one to connect to.
    if host in ("0.0.0.0", "::", ""):
        host = "127.0.0.1"
    return f"http://{host}:{port}/healthz"


def check(url: str) -> int:
    try:
        with urllib.request.urlopen(url, timeout=TIMEOUT_SECONDS) as response:
            return 0 if response.status == 200 else 1
    except (urllib.error.URLError, OSError, ValueError):
        return 1


def run(argv: Sequence[str], env: Mapping[str, str]) -> int:
    url = target(argv, env)
    return 0 if url is None else check(url)


def _pid1_argv() -> list[str]:
    try:
        with open("/proc/1/cmdline", "rb") as f:
            return [part.decode(errors="replace") for part in f.read().split(b"\0") if part]
    except OSError:
        return []


if __name__ == "__main__":
    sys.exit(run(_pid1_argv(), os.environ))
