"""Structured tool output (MCP 2025-06-18/2025-11-25).

The tabular tools return machine-readable structuredContent alongside their
TOON text, and declare an output schema. TOON stays the text serialization —
structured content is additive, never a replacement.
"""

import pytest

from fastmcp import Client

from laravel_mcp_companion import create_mcp_server

STRUCTURED_TOOLS = (
    "search_laravel_docs",
    "laravel_docs_info",
    "list_laravel_docs",
    "get_laravel_package_recommendations",
    "get_laravel_package_info",
)


@pytest.fixture
def mcp_server(test_docs_dir):
    return create_mcp_server("TestServer", test_docs_dir, "12.x", transform_mode=None)


@pytest.mark.protocol
class TestStructuredOutput:
    async def test_structured_tools_declare_output_schema(self, mcp_server):
        """A real schema, not FastMCP's {"result": "<string>"} auto-wrapper."""
        async with Client(mcp_server) as client:
            tools = {t.name: t for t in await client.list_tools()}
            for name in STRUCTURED_TOOLS:
                schema = tools[name].outputSchema
                assert schema is not None, f"{name} should declare an output schema"
                assert "x-fastmcp-wrap-result" not in schema, (
                    f"{name} still has the auto-wrapped string schema"
                )
                assert schema.get("properties"), f"{name} schema documents no keys"

    async def test_search_returns_structured_content_and_toon_text(self, mcp_server):
        async with Client(mcp_server) as client:
            res = await client.call_tool(
                "search_laravel_docs", {"query": "routing", "include_external": False}
            )
            assert res.structured_content is not None
            assert "query" in res.structured_content or "error" in res.structured_content
            # TOON text is still the text serialization, not JSON
            assert res.content[0].text
            assert not res.content[0].text.lstrip().startswith("{")

    async def test_docs_info_returns_structured_content(self, mcp_server):
        async with Client(mcp_server) as client:
            res = await client.call_tool("laravel_docs_info", {"version": "12.x"})
            assert res.structured_content is not None
            assert res.structured_content.get("version") == "12.x"

    async def test_package_info_returns_structured_content(self, mcp_server):
        async with Client(mcp_server) as client:
            res = await client.call_tool(
                "get_laravel_package_info", {"package_name": "laravel/sanctum"}
            )
            assert res.structured_content is not None
            assert res.structured_content.get("id") == "laravel/sanctum"

    async def test_package_recommendations_return_structured_content(self, mcp_server):
        async with Client(mcp_server) as client:
            res = await client.call_tool(
                "get_laravel_package_recommendations", {"use_case": "authentication"}
            )
            assert res.structured_content is not None
            assert "packages" in res.structured_content or "error" in res.structured_content

    async def test_list_docs_returns_structured_content(self, mcp_server):
        async with Client(mcp_server) as client:
            res = await client.call_tool("list_laravel_docs", {"version": "12.x"})
            assert res.structured_content is not None
            assert (
                "files" in res.structured_content or "error" in res.structured_content
            )

    async def test_error_paths_stay_structured(self, mcp_server):
        async with Client(mcp_server) as client:
            res = await client.call_tool(
                "get_laravel_package_info", {"package_name": "not/a-package"}
            )
            assert res.structured_content is not None
            assert "error" in res.structured_content


@pytest.mark.protocol
class TestSearchTransformProxy:
    """Pin whether the search transform's call_tool proxy forwards structuredContent."""

    async def test_call_tool_proxy_structured_content_behavior(self, test_docs_dir):
        server = create_mcp_server(
            "TestServer", test_docs_dir, "12.x", transform_mode="search"
        )
        async with Client(server) as client:
            res = await client.call_tool(
                "call_tool",
                {"name": "laravel_docs_info", "arguments": {"version": "12.x"}},
            )
            # The proxy forwards structuredContent, so search-mode clients get
            # the same structure as --transform-mode none clients.
            assert res.structured_content is not None
            # The direct pinned tool carries structured content too.
            direct = await client.call_tool(
                "search_laravel_docs", {"query": "routing", "include_external": False}
            )
            assert direct.structured_content is not None
