"""MCP Protocol Compliance Tests.

These tests verify that the Laravel MCP Companion server correctly implements
the Model Context Protocol specification.
"""

import pytest
import re

from fastmcp import Client

from laravel_mcp_companion import server as companion_server
from laravel_mcp_companion.server import create_mcp_server


@pytest.fixture
def mcp_server(temp_dir):
    """Create an MCP server instance for testing."""
    return create_mcp_server("TestServer", temp_dir, "12.x", transform_mode=None)


@pytest.mark.protocol
class TestServerIdentity:
    """The server must identify itself at initialize (registry prerequisite)."""

    async def test_initialize_reports_server_version(self, mcp_server):
        async with Client(mcp_server) as client:
            info = client.initialize_result.serverInfo
            assert info.version == companion_server.SERVER_VERSION

    async def test_server_declares_an_icon(self, mcp_server):
        icons = mcp_server.icons
        assert icons, "Server should declare an icon (SEP-973)"
        assert str(icons[0].src).startswith("data:image/svg+xml;base64,"), (
            "Icon must be a self-contained data URI, not a network fetch"
        )


@pytest.mark.protocol
class TestServerCapabilities:
    """Test that server capabilities are correctly advertised."""

    async def test_server_has_tools(self, mcp_server):
        """Server should advertise available tools."""
        tools = await mcp_server.list_tools()
        assert len(tools) > 0, "Server should have at least one tool"

    async def test_server_has_resources(self, mcp_server):
        """Server should advertise available resources."""
        templates = await mcp_server.list_resource_templates()
        assert len(templates) > 0, "Server should have resource templates"

    async def test_server_advertises_no_prompts(self, mcp_server):
        """The three prompts the server once had were fixed strings naming
        tools that did not exist. There are none now."""
        assert await mcp_server.list_prompts() == []


@pytest.mark.protocol
class TestToolSchemas:
    """Test that all tools have valid JSON schemas."""

    async def test_all_tools_have_descriptions(self, mcp_server):
        """Every tool should have a description."""
        tools = await mcp_server.list_tools()
        for tool in tools:
            assert tool.description, f"Tool '{tool.name}' missing description"

    async def test_tool_parameters_are_valid(self, mcp_server):
        """Tool parameters should be valid JSON Schema."""
        tools = await mcp_server.list_tools()
        for tool in tools:
            if hasattr(tool, 'parameters') and tool.parameters:
                schema = tool.parameters
                assert isinstance(schema, dict), f"Tool '{tool.name}' parameters not a dict"

    async def test_required_tools_exist(self, mcp_server):
        """Required documentation tools should exist."""
        tools = await mcp_server.list_tools()
        tool_names = {t.name for t in tools}
        required_tools = [
            "list_laravel_docs",
            "search_laravel_docs",
            "read_laravel_doc_section",
            "read_laravel_doc_content",
            "recommend_laravel_packages",
        ]
        for tool_name in required_tools:
            assert tool_name in tool_names, f"Required tool '{tool_name}' missing"


@pytest.mark.protocol
class TestResourceTemplates:
    """Test that resource templates are valid URI templates."""

    async def test_laravel_resource_template(self, mcp_server):
        """Laravel resource template should be valid."""
        templates = await mcp_server.list_resource_templates()
        template_uris = [str(t.uri_template) for t in templates]
        assert any("laravel://" in uri for uri in template_uris), \
            "Missing laravel:// resource template"

    async def test_external_resource_template(self, mcp_server):
        """External Laravel services resource template should be valid."""
        templates = await mcp_server.list_resource_templates()
        template_uris = [str(t.uri_template) for t in templates]
        assert any("laravel-external://" in uri for uri in template_uris), \
            "Missing laravel-external:// resource template"

    async def test_resource_templates_have_parameters(self, mcp_server):
        """Resource templates should define their parameters."""
        templates = await mcp_server.list_resource_templates()
        for template in templates:
            uri = str(template.uri_template)
            # URI templates use {param} or {param*} syntax
            if "{" in uri:
                params = re.findall(r'\{(\w+)\*?\}', uri)
                assert len(params) > 0, "Template has braces but no params"


@pytest.mark.protocol
class TestToolAnnotations:
    """Test that tools have correct MCP annotations."""

    async def test_readonly_tools_are_marked(self, mcp_server):
        """Read-only tools should have readOnlyHint annotation."""
        tools = await mcp_server.list_tools()
        for tool in tools:
            if tool.name != "update_laravel_docs":
                assert tool.annotations is not None and tool.annotations.readOnlyHint is True, \
                    f"Tool '{tool.name}' should be marked read-only"

    async def test_update_tools_not_marked_readonly(self, mcp_server):
        """Update tools should not be marked as read-only."""
        tools = await mcp_server.list_tools()
        update = next(tool for tool in tools if tool.name == "update_laravel_docs")

        assert update.annotations.readOnlyHint is False
        assert update.annotations.openWorldHint is True, "it reaches out to the network"
        assert update.annotations.destructiveHint is False
