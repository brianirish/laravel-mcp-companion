"""The README's one-click install links, decoded.

Each link carries a server configuration that nobody reads once it is encoded.
These tests decode the links as the clients do and check what they would
install, and check them against scripts/install_links.py, which produces them.

Formats:
  Cursor   https://cursor.com/docs/context/mcp/install-links
           https://cursor.com/docs/reference/deeplinks (the https://cursor.com/link/ form)
  VS Code  https://code.visualstudio.com/api/extension-guides/ai/mcp
           ("Install an MCP server from configuration", "Shareable web badges
           and redirect wrapper")
"""

import base64
import importlib.util
import json
import re
from pathlib import Path
from urllib.parse import parse_qs, unquote, urlsplit

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]

SERVER_NAME = "laravel-mcp-companion"
COMMAND = "uvx"
ARGS = ["laravel-mcp-companion"]

CURSOR_PREFIX = "https://cursor.com/link/mcp/install?"
VSCODE_PREFIX = "https://vscode.dev/redirect?"


def installation_section() -> str:
    text = (REPO_ROOT / "README.md").read_text(encoding="utf-8")
    match = re.search(r"^## Installation\n(.*?)(?=^## )", text, re.DOTALL | re.MULTILINE)
    assert match, "README has no Installation section"
    return match.group(1)


def links(prefix: str) -> list[str]:
    """Every Markdown link target in the Installation section starting with `prefix`."""
    targets = re.findall(r"\]\((https://[^)\s]+)\)", installation_section())
    return [target for target in targets if target.startswith(prefix)]


def vscode_link(scheme: str) -> str:
    """The redirect link whose wrapped URL uses `scheme` ("vscode" or "vscode-insiders")."""
    found = [link for link in links(VSCODE_PREFIX) if wrapped_url(link).startswith(f"{scheme}:")]
    assert len(found) == 1, f"expected one {scheme}: install link in the README, found {len(found)}"
    return found[0]


def wrapped_url(link: str) -> str:
    """The vscode: URL that vscode.dev/redirect sends the browser to."""
    return parse_qs(urlsplit(link).query)["url"][0]


def generator():
    spec = importlib.util.spec_from_file_location("install_links", REPO_ROOT / "scripts" / "install_links.py")
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_cursor_link_installs_the_uvx_server():
    found = links(CURSOR_PREFIX)
    assert len(found) == 1, f"expected one Cursor install link in the README, found {len(found)}"
    query = parse_qs(urlsplit(found[0]).query, strict_parsing=True)
    assert query["name"] == [SERVER_NAME]
    # Cursor takes the server's own configuration, without the name wrapping it.
    config = json.loads(base64.b64decode(query["config"][0], validate=True))
    assert config == {"command": COMMAND, "args": ARGS}


@pytest.mark.parametrize("scheme", ["vscode", "vscode-insiders"])
def test_vscode_link_installs_the_uvx_server(scheme):
    target = wrapped_url(vscode_link(scheme))
    prefix = f"{scheme}:mcp/install?"
    assert target.startswith(prefix), target
    # VS Code takes one JSON object that carries the name beside the configuration.
    config = json.loads(unquote(target[len(prefix) :]))
    assert config == {"name": SERVER_NAME, "command": COMMAND, "args": ARGS}


def test_links_are_the_ones_the_script_produces():
    produced = generator().install_links()
    in_readme = {
        "cursor": links(CURSOR_PREFIX)[0],
        "vscode": vscode_link("vscode"),
        "vscode-insiders": vscode_link("vscode-insiders"),
    }
    assert in_readme == produced, "README install links are out of date. Run: python scripts/install_links.py"
