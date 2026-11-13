"""The tool surface, pinned.

`contract.json` records every tool's name, input schema and output schema,
and the resource templates, as a client sees them with `--transform-mode
none`. That file is the interface the versioning policy makes promises about.
A change to it is a change to the public API: this test fails until the file
is regenerated, which puts the change in front of whoever reviews the diff.

    UPDATE_CONTRACT=1 pytest tests/protocol/test_tool_contract.py

Tools marked experimental are recorded too, flagged as such; the policy lets
them change in a minor release, and the diff still shows it happening.
"""

import json
import os
from pathlib import Path

import pytest
from fastmcp import Client

from laravel_mcp_companion.server import create_mcp_server
from laravel_mcp_companion.tools import ERROR_SCHEMA, EXPERIMENTAL_TOOLS, STABLE_TOOLS

CONTRACT = Path(__file__).parent / "contract.json"


async def observed_contract(tmp_path) -> dict:
    (tmp_path / "12.x").mkdir()
    (tmp_path / "12.x" / "routing.md").write_text("# Routing\n\n## Basics\n\nText.\n")
    server = create_mcp_server("Contract", tmp_path, "12.x", transform_mode=None)
    async with Client(server) as client:
        tools = await client.list_tools()
        templates = await client.list_resource_templates()
    return {
        "tools": {
            tool.name: {
                "stable": tool.name in STABLE_TOOLS,
                "input_schema": tool.inputSchema,
                "output_schema": tool.outputSchema,
            }
            for tool in sorted(tools, key=lambda t: t.name)
        },
        "resource_templates": sorted(template.uriTemplate for template in templates),
        "error_schema": ERROR_SCHEMA,
    }


@pytest.mark.asyncio
async def test_the_surface_matches_the_recorded_contract(tmp_path):
    observed = await observed_contract(tmp_path)

    if os.environ.get("UPDATE_CONTRACT"):
        CONTRACT.write_text(json.dumps(observed, indent=2, sort_keys=True) + "\n")

    recorded = json.loads(CONTRACT.read_text())
    assert observed == recorded, (
        "The tool surface differs from tests/protocol/contract.json. If the change is intended, "
        "regenerate the file with UPDATE_CONTRACT=1 and say in the changelog what changed."
    )


@pytest.mark.asyncio
async def test_every_declared_tool_is_served_and_nothing_else(tmp_path):
    observed = await observed_contract(tmp_path)

    assert set(observed["tools"]) == set(STABLE_TOOLS) | set(EXPERIMENTAL_TOOLS)


@pytest.mark.asyncio
async def test_no_tool_takes_the_injected_context_as_an_argument(tmp_path):
    observed = await observed_contract(tmp_path)

    for name, tool in observed["tools"].items():
        assert "ctx" not in tool["input_schema"].get("properties", {}), name


@pytest.mark.asyncio
async def test_the_three_resource_templates_are_part_of_the_contract(tmp_path):
    observed = await observed_contract(tmp_path)

    assert observed["resource_templates"] == [
        "laravel-external://{service}/{path*}",
        "laravel-package://{package}/{path*}",
        "laravel://{path*}",
    ]


@pytest.mark.asyncio
async def test_search_mode_lists_the_two_everyday_tools_and_the_two_meta_tools(tmp_path):
    """The meta-tools belong to the framework and are outside the contract;
    which of our tools stay directly visible is ours to pin."""
    (tmp_path / "12.x").mkdir()
    server = create_mcp_server("Contract", tmp_path, "12.x", transform_mode="search")
    async with Client(server) as client:
        names = {tool.name for tool in await client.list_tools()}

    assert names == {"search_laravel_docs", "read_laravel_doc_section", "search_tools", "call_tool"}
