"""MCP Registry metadata (server.json) and its Docker counterpart.

The registry validates OCI ownership through an image label, so server.json
and the Dockerfile have to agree on the server name — these tests pin both
sides to the same literal.
"""

import json
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]

SERVER_NAME = "io.github.brianirish/laravel-mcp-companion"


def server_json() -> dict:
    return json.loads((REPO_ROOT / "server.json").read_text(encoding="utf-8"))


def test_server_json_exists_and_names_the_server():
    data = server_json()
    assert data["name"] == SERVER_NAME
    # Reverse-DNS with exactly one slash, per the registry schema
    assert re.fullmatch(r"[a-zA-Z0-9.-]+/[a-zA-Z0-9._-]+", data["name"])
    assert data["description"]
    # The registry rejects a description longer than this.
    assert len(data["description"]) <= 100
    assert data["$schema"].endswith("/server.schema.json")


def package(registry_type: str) -> dict:
    found = [pkg for pkg in server_json()["packages"] if pkg["registryType"] == registry_type]
    assert len(found) == 1, f"expected one {registry_type} package"
    return found[0]


def test_server_json_declares_the_image_and_the_pypi_package_and_nothing_else():
    assert sorted(pkg["registryType"] for pkg in server_json()["packages"]) == ["oci", "pypi"]


def test_server_json_declares_the_oci_package():
    pkg = package("oci")
    assert pkg["identifier"].startswith("ghcr.io/brianirish/laravel-mcp-companion:")
    assert pkg["transport"]["type"] == "stdio"
    assert pkg["runtimeHint"] == "docker"


def test_server_json_declares_the_pypi_package():
    pkg = package("pypi")
    assert pkg["identifier"] == "laravel-mcp-companion"
    assert pkg["transport"]["type"] == "stdio"
    assert pkg["runtimeHint"] == "uvx"


def test_readme_carries_the_line_the_registry_checks_pypi_ownership_by():
    # The registry reads the package's README from PyPI, which is this file.
    text = (REPO_ROOT / "README.md").read_text(encoding="utf-8")
    assert f"mcp-name: {SERVER_NAME}" in text


def test_dockerfile_carries_registry_ownership_label():
    text = (REPO_ROOT / "Dockerfile").read_text(encoding="utf-8")
    assert f'io.modelcontextprotocol.server.name="{SERVER_NAME}"' in text
