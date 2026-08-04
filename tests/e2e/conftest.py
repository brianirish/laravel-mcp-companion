"""Fixtures for the e2e suite: a real docs tree and a real server process.

Everything here spawns `laravel_mcp_companion.py` the way Docker's ENTRYPOINT
does. No fixed sleeps: HTTP readiness is polled, and every test carries a
hard timeout so a wedged subprocess fails fast instead of hanging CI.
"""

import json
import os
import socket
import subprocess
import sys
import time
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
SERVER_SCRIPT = REPO_ROOT / "laravel_mcp_companion.py"


def build_docs_tree(root: Path) -> Path:
    docs = root / "docs"
    for version in ("11.x", "12.x"):
        vdir = docs / version
        vdir.mkdir(parents=True)
        (vdir / "installation.md").write_text(
            "# Installation\n\n## Requirements\n\nPHP and Composer.\n"
        )
        (vdir / "routing.md").write_text(
            "# Routing\n\n## Basic Routing\n\nRoutes live in routes/web.php. "
            "Define them with Route::get and friends.\n\n"
            "## Route Parameters\n\nCapture URI segments with braces.\n"
        )
        meta = vdir / ".metadata"
        meta.mkdir()
        (meta / "sync_info.json").write_text(json.dumps({
            "version": version,
            "commit_sha": "e2efixture",
            "commit_date": "2026-08-01T00:00:00Z",
            "commit_message": "e2e fixture",
            "sync_time": "2026-08-01T00:00:00Z",
        }))

    # A nested service file, exercising both the unified fan-out and the
    # recursive enumeration that most service docs depend on.
    daemons = docs / "external" / "forge" / "servers"
    daemons.mkdir(parents=True)
    (daemons / "daemons.md").write_text(
        "# Daemons\n\n## Supervisor Daemons\n\nForge manages supervisor daemon "
        "processes that keep workers alive across restarts.\n"
    )
    return docs


@pytest.fixture(scope="session")
def e2e_docs(tmp_path_factory):
    return build_docs_tree(tmp_path_factory.mktemp("e2e"))


def server_args(docs: Path, *extra: str) -> list[str]:
    return [
        str(SERVER_SCRIPT),
        "--docs-path", str(docs),
        "--version", "12.x",
        *extra,
    ]


def free_port() -> int:
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


@pytest.fixture
def http_server(e2e_docs):
    """The real server over HTTP on an ephemeral port. Yields the base URL."""
    procs = []

    def start(*extra_args: str, env_extra: dict | None = None) -> str:
        port = free_port()
        env = {**os.environ, **(env_extra or {})}
        proc = subprocess.Popen(
            [sys.executable, *server_args(e2e_docs, "--transport", "http",
                                          "--port", str(port))] + list(extra_args),
            cwd=REPO_ROOT, env=env,
            stdout=subprocess.DEVNULL, stderr=subprocess.PIPE,
        )
        procs.append(proc)
        deadline = time.monotonic() + 20
        while time.monotonic() < deadline:
            if proc.poll() is not None:
                stderr = proc.stderr.read().decode(errors="replace")[-2000:] if proc.stderr else ""
                raise RuntimeError(f"server exited early:\n{stderr}")
            try:
                with socket.create_connection(("127.0.0.1", port), timeout=0.2):
                    return f"http://127.0.0.1:{port}"
            except OSError:
                time.sleep(0.1)
        raise RuntimeError("server never opened its port")

    yield start

    for proc in procs:
        proc.terminate()
        try:
            proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            proc.kill()
            proc.wait(timeout=5)
