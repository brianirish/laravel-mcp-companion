"""A running server asks nothing of the network but GitHub's list of versions.

The README promises that questions go nowhere and that no documentation
service is called while you work. The one request it owns up to is the
startup check of which Laravel versions exist. This starts the server the way
a client does, over stdio, from a directory with no project in it, with every
name lookup and every outbound connection refused and recorded. The versions
cache is made to look expired so that the GitHub request is always made: it
shows the recording works.
"""

import os
import sys
from pathlib import Path

from fastmcp import Client
from fastmcp.client.transports import StdioTransport

REPO_ROOT = Path(__file__).resolve().parents[2]

PROBE = """
import json
import os
import socket

LOG = os.environ["NETWORK_PROBE_LOG"]


def record(host):
    with open(LOG, "a") as log:
        log.write(f"{host}\\n")


def no_lookup(host, *args, **kwargs):
    record(host)
    raise socket.gaierror("network disabled for this test")


real_connect = socket.socket.connect


def no_connect(self, address):
    if self.family in (socket.AF_INET, socket.AF_INET6):
        record(address[0])
        raise OSError("network disabled for this test")
    return real_connect(self, address)


socket.getaddrinfo = no_lookup
socket.socket.connect = no_connect

real_loads = json.loads


def aged(*args, **kwargs):
    data = real_loads(*args, **kwargs)
    if isinstance(data, dict) and "versions" in data and "updated_at" in data:
        data["updated_at"] = "2020-01-01T00:00:00+00:00"
    return data


json.loads = aged

import sys

from laravel_mcp_companion import server

sys.argv = ["laravel-mcp-companion"]
server.main()
"""


async def test_a_stdio_session_reaches_only_github(tmp_path):
    (tmp_path / "network_probe.py").write_text(PROBE)
    log = tmp_path / "hosts.log"
    no_project = tmp_path / "no-project"
    no_project.mkdir()
    env = {
        **os.environ,
        "PYTHONPATH": f"{tmp_path}{os.pathsep}{REPO_ROOT}",
        "NETWORK_PROBE_LOG": str(log),
        # Empty homes, so nothing either library cached earlier hides a request.
        "FASTMCP_HOME": str(tmp_path / "fastmcp"),
        "LARAVEL_MCP_COMPANION_HOME": str(tmp_path / "companion"),
    }
    transport = StdioTransport(
        sys.executable, ["-c", "import network_probe"], env=env, cwd=str(no_project),
    )

    async with Client(transport) as client:
        search = await client.call_tool(
            "search_laravel_docs", {"query": "retry a failed queue job", "sources": ["core"]},
        )
        hits = search.structured_content["results"]
        assert hits, search.structured_content
        version, filename = hits[0]["file"].split("/", 1)
        section = await client.call_tool(
            "read_laravel_doc_section",
            {"filename": filename, "section": hits[0]["section"], "version": version},
        )
        assert section.content[0].text

    hosts = set(log.read_text().split()) if log.exists() else set()
    assert hosts, "the probe recorded nothing; it is not catching requests"
    assert hosts == {"api.github.com"}
