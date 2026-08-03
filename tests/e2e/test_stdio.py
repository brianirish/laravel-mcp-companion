"""End-to-end over stdio: the transport Docker's ENTRYPOINT serves."""

import pytest

from fastmcp import Client
from fastmcp.client.transports import PythonStdioTransport

import laravel_mcp_companion
from .conftest import SERVER_SCRIPT, server_args

pytestmark = [pytest.mark.e2e, pytest.mark.timeout(60)]


def stdio_client(docs, *extra: str) -> Client:
    args = server_args(docs, "--transport", "stdio", *extra)[1:]  # drop script path
    return Client(PythonStdioTransport(str(SERVER_SCRIPT), args=args, cwd=str(SERVER_SCRIPT.parent)))


class TestStdioRawSurface:
    async def test_initialize_flow_and_section_read(self, e2e_docs):
        async with stdio_client(e2e_docs, "--transform-mode", "none") as client:
            info = client.initialize_result.serverInfo
            assert info.version == laravel_mcp_companion.SERVER_VERSION
            caps = client.initialize_result.capabilities.model_dump(exclude_none=True)
            assert "tasks" in caps

            tools = {t.name for t in await client.list_tools()}
            assert {"search_laravel_docs", "read_laravel_doc_section",
                    "update_laravel_docs"} <= tools

            search = await client.call_tool(
                "search_laravel_docs",
                {"query": "route parameters", "include_external": False},
            )
            assert search.structured_content is not None
            results = search.structured_content.get("results", [])
            assert results, f"no hits: {search.structured_content}"
            top = results[0]
            assert top["file"] == "12.x/routing.md"

            section = await client.call_tool(
                "read_laravel_doc_section",
                {"filename": "routing.md", "section": top["anchor"] or top["heading"]},
            )
            assert "Route" in section.content[0].text

    async def test_structured_content_and_resource_read(self, e2e_docs):
        async with stdio_client(e2e_docs, "--transform-mode", "none") as client:
            info = await client.call_tool("laravel_docs_info", {"version": "12.x"})
            assert info.structured_content.get("version") == "12.x"
            assert info.structured_content.get("commit_sha") == "e2efixture"

            resource = await client.read_resource("laravel://12.x/installation.md")
            assert "# Installation" in resource[0].text


class TestStdioDefaultSurface:
    async def test_search_transform_is_the_default(self, e2e_docs):
        async with stdio_client(e2e_docs) as client:
            tools = {t.name for t in await client.list_tools()}
            assert "search_tools" in tools
            assert "call_tool" in tools
            assert "search_laravel_docs" in tools  # pinned
            assert "update_laravel_docs" not in tools  # behind the proxy

            proxied = await client.call_tool(
                "call_tool",
                {"name": "laravel_docs_info", "arguments": {"version": "12.x"}},
            )
            assert proxied.structured_content.get("version") == "12.x"
