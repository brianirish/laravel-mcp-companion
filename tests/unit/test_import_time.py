"""Importing the server must not touch the network.

Version discovery used to run at import: on a cold or expired cache,
`import laravel_mcp_companion` asked GitHub for the branch list, could block
for the length of the request timeout, and rewrote the checked-in versions
cache as a side effect. The import now reads the cache only. The network
lookup is an explicit call made once at server startup.
"""

import os
import subprocess
import sys

import pytest

from laravel_mcp_companion import docs_updater
from laravel_mcp_companion import mcp_tools
@pytest.fixture
def restore_versions():
    saved = list(docs_updater.SUPPORTED_VERSIONS)
    yield
    docs_updater.SUPPORTED_VERSIONS[:] = saved


def test_import_opens_no_socket_even_when_the_cache_has_expired(tmp_path):
    # The old lookup caught its own network errors and fell back to the stale
    # cache, so a socket that merely raises would go unnoticed. Count attempts.
    probe = tmp_path / "import_probe.py"
    probe.write_text(
        "import socket\n"
        "attempts = []\n"
        "class NoSocket(socket.socket):\n"
        "    def __init__(self, *a, **k):\n"
        "        attempts.append('socket')\n"
        "        raise OSError('network disabled for this test')\n"
        "def no_lookup(*a, **k):\n"
        "    attempts.append('getaddrinfo')\n"
        "    raise OSError('network disabled for this test')\n"
        "socket.socket = NoSocket\n"
        "socket.getaddrinfo = no_lookup\n"
        # Make the versions cache read as long expired, whatever its real age.
        "import json\n"
        "_loads = json.loads\n"
        "def aged(*a, **k):\n"
        "    data = _loads(*a, **k)\n"
        "    if isinstance(data, dict) and 'versions' in data and 'updated_at' in data:\n"
        "        data['updated_at'] = '2020-01-01T00:00:00+00:00'\n"
        "    return data\n"
        "json.loads = aged\n"
        "import laravel_mcp_companion.server\n"
        "print('NETWORK-ATTEMPTS', len(attempts))\n"
    )
    result = subprocess.run(
        [sys.executable, "-c", "import import_probe"], capture_output=True, text=True, timeout=120,
        env={**os.environ, "PYTHONPATH": f"{tmp_path}{os.pathsep}{os.getcwd()}"},
    )

    assert "NETWORK-ATTEMPTS 0" in result.stdout, (result.stdout[-500:], result.stderr[-1500:])


def test_refresh_updates_the_list_every_module_already_holds(monkeypatch, restore_versions):
    shared = docs_updater.SUPPORTED_VERSIONS
    monkeypatch.setattr(docs_updater, "get_supported_versions", lambda cache_file=None: ["6.x", "12.x", "99.x"])

    result = docs_updater.refresh_supported_versions()

    assert result == ["6.x", "12.x", "99.x"]
    assert docs_updater.SUPPORTED_VERSIONS is shared
    assert mcp_tools.SUPPORTED_VERSIONS is shared


def test_the_default_version_follows_a_refresh(monkeypatch, restore_versions):
    monkeypatch.setattr(docs_updater, "get_supported_versions", lambda cache_file=None: ["12.x", "98.x"])
    docs_updater.refresh_supported_versions()

    assert docs_updater.get_default_version() == "98.x"
    assert mcp_tools.get_version_from_path("blade.md")[0] == "98.x"


def test_a_failed_refresh_keeps_the_versions_already_loaded(monkeypatch, restore_versions):
    before = list(docs_updater.SUPPORTED_VERSIONS)

    def offline(cache_file=None):
        raise OSError("github is unreachable")

    monkeypatch.setattr(docs_updater, "get_supported_versions", offline)

    assert docs_updater.refresh_supported_versions() == before
    assert docs_updater.SUPPORTED_VERSIONS == before
