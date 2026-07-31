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

from laravel_mcp_companion import TOOL_DESCRIPTIONS, create_mcp_server

REPO_ROOT = Path(__file__).resolve().parents[2]

PRODUCT_MODULES = ["laravel_mcp_companion.py", "mcp_tools.py", "docs_updater.py"]


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


class TestToolDescriptions:
    @pytest.mark.asyncio
    async def test_every_description_belongs_to_a_real_tool(self, tool_names):
        """`search_laravel_docs_with_context` was removed in v0.11.0; its
        description outlived it."""
        orphaned = set(TOOL_DESCRIPTIONS) - tool_names
        assert not orphaned, f"TOOL_DESCRIPTIONS describes tools that no longer exist: {sorted(orphaned)}"

    @pytest.mark.asyncio
    async def test_tools_use_the_description_written_for_them(self, tmp_path):
        """Three tools were registered with one-line summaries while their real
        descriptions sat unused. That is not cosmetic: BM25SearchTransform
        indexes descriptions, so an unwired tool is harder to discover in the
        default mode.
        """
        server = create_mcp_server("Test", tmp_path, "13.x", transform_mode=None)
        async with Client(server) as client:
            registered = {tool.name: (tool.description or "") for tool in await client.list_tools()}

        mismatched = [
            name for name, expected in TOOL_DESCRIPTIONS.items()
            if name in registered and registered[name].strip() != expected.strip()
        ]
        assert not mismatched, (
            f"these tools have a description in TOOL_DESCRIPTIONS but do not use it: {sorted(mismatched)}"
        )

    def test_no_description_claims_to_be_the_primary_read_path(self):
        """`read_laravel_doc_content` called itself "the primary tool for
        accessing actual documentation content". Since v0.11.0 that is
        `read_laravel_doc_section`; whole-file reads cost roughly ten times as
        much and are the fallback.
        """
        content = TOOL_DESCRIPTIONS.get("read_laravel_doc_content", "")
        assert "primary tool" not in content.lower(), (
            "read_laravel_doc_content is no longer the primary read path"
        )
