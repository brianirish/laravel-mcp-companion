"""The tool surface must describe itself honestly.

Every defect here is the same shape: the server tells the assistant something
about its own tools that is not true. That cost a release already -- v0.10.0
advertised `update_laravel_docs(version_param=...)`, an argument no caller could
successfully pass, and an assistant following the advice hard-errored.
"""

import re
from pathlib import Path

import pytest
from fastmcp import Client

from laravel_mcp_companion.server import build_server_instructions, create_mcp_server
from laravel_mcp_companion.tools import REGISTRY

REPO_ROOT = Path(__file__).resolve().parents[2]

PRODUCT_MODULES = sorted(
    str(path.relative_to(Path(__file__).resolve().parents[2]))
    for path in (Path(__file__).resolve().parents[2] / "laravel_mcp_companion").rglob("*.py")
)


@pytest.fixture
async def tool_names(tmp_path):
    server = create_mcp_server("Test", tmp_path, "13.x", transform_mode=None)
    async with Client(server) as client:
        return {tool.name for tool in await client.list_tools()}


class TestNoPhantomTools:
    @pytest.mark.asyncio
    async def test_error_messages_only_name_tools_that_exist(self, tool_names):
        """Two error paths advised calling `update_learning_docs()`, which is not
        a tool -- it is a DocsUpdater method reachable only through
        `update_all_docs()`, which nothing exposes. A user hitting that error had
        no way to act on the advice.
        """
        advised = set()
        for module in PRODUCT_MODULES:
            text = (REPO_ROOT / module).read_text(encoding="utf-8")
            advised |= set(re.findall(r"Use (\w+)\(\) to", text))

        phantom = advised - tool_names
        assert not phantom, (
            f"error messages tell the assistant to call {sorted(phantom)}, "
            f"which are not registered tools"
        )


class TestPinnedTools:
    @pytest.mark.asyncio
    async def test_reading_a_section_is_reachable_without_a_lookup(self, tmp_path):
        """Search returns section anchors; reading one is the other half.

        With only `search_laravel_docs` pinned, the single most common path --
        search, then read the section it just pointed at -- costs a `search_tools`
        round trip in between.
        """
        server = create_mcp_server("Test", tmp_path, "13.x", transform_mode="search")
        async with Client(server) as client:
            visible = {tool.name for tool in await client.list_tools()}

        assert "search_laravel_docs" in visible
        assert "read_laravel_doc_section" in visible, (
            f"search results are unreadable without a lookup; visible: {sorted(visible)}"
        )

    @pytest.mark.asyncio
    async def test_the_pinned_surface_stays_small(self, tmp_path):
        """Pinning everything would defeat the transform's purpose."""
        server = create_mcp_server("Test", tmp_path, "13.x", transform_mode="search")
        async with Client(server) as client:
            visible = {tool.name for tool in await client.list_tools()}

        assert len(visible) <= 5, f"too many tools pinned: {sorted(visible)}"


TOOL_NAME = re.compile(r"\b(?:[a-z]+_)*(?:laravel|docs)_[a-z_]+\b|\b(?:search|read|list|get|browse|compare|update|recommend|verify|find)_[a-z_]*laravel[a-z_]*\b")


class TestToolDescriptions:
    @pytest.mark.asyncio
    async def test_the_served_description_is_the_declared_one(self, tmp_path):
        """BM25SearchTransform indexes descriptions, so a tool served with some
        other text is harder to find in the default mode."""
        server = create_mcp_server("Test", tmp_path, "13.x", transform_mode=None)
        async with Client(server) as client:
            served = {tool.name: (tool.description or "") for tool in await client.list_tools()}

        assert {name: text.strip() for name, text in served.items()} == {
            name: spec.description.strip() for name, spec in REGISTRY.items()
        }

    @pytest.mark.parametrize("name", sorted(REGISTRY))
    def test_a_description_only_names_tools_that_exist(self, name):
        """A description that sends the model to a tool that was renamed or
        removed gets a failed call every time it is followed."""
        mentioned = {match.group(0) for match in TOOL_NAME.finditer(REGISTRY[name].description)}

        assert mentioned <= set(REGISTRY) | {"search_tools", "call_tool"}, mentioned - set(REGISTRY)

    def test_the_whole_page_reader_points_at_the_cheaper_path(self):
        """Whole-file reads cost roughly ten times a section read and are the
        fallback; the description has to say so."""
        description = REGISTRY["read_laravel_doc_content"].description

        assert "primary tool" not in description.lower()
        assert "read_laravel_doc_section" in description


class TestInstructionsNameTheTools:
    """In search mode only two tools are listed. The instructions are the one
    place the model learns the other ten exist."""

    @pytest.mark.parametrize("mode", ["search", None])
    def test_every_tool_is_named(self, tmp_path, mode):
        instructions = build_server_instructions(tmp_path, "13.x", mode)

        assert [name for name in REGISTRY if name not in instructions] == []

    @pytest.mark.parametrize("mode", ["search", "code", None])
    def test_no_tool_that_does_not_exist_is_named(self, tmp_path, mode):
        instructions = build_server_instructions(tmp_path, "13.x", mode)
        mentioned = {match.group(0) for match in TOOL_NAME.finditer(instructions)}

        assert mentioned <= set(REGISTRY) | {"search_tools", "call_tool", "get_schema"}, mentioned - set(REGISTRY)

    @pytest.mark.parametrize("mode", ["search", "code", None])
    def test_the_section_reader_is_the_recommended_way_to_read(self, tmp_path, mode):
        """The instructions used to send the model to the whole-file reader,
        against the advice of that tool's own description."""
        instructions = build_server_instructions(tmp_path, "13.x", mode)

        assert instructions.index("read_laravel_doc_section") < instructions.index("read_laravel_doc_content")
