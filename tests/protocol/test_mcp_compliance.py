"""MCP Protocol Compliance Tests.

These tests verify that the Laravel MCP Companion server correctly implements
the Model Context Protocol specification.
"""

import pytest
import re

from laravel_mcp_companion import create_mcp_server


@pytest.fixture
def mcp_server(temp_dir):
    """Create an MCP server instance for testing."""
    return create_mcp_server("TestServer", temp_dir, "12.x")


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

    async def test_server_has_prompts(self, mcp_server):
        """Server should advertise available prompts."""
        prompts = await mcp_server.list_prompts()
        assert len(prompts) > 0, "Server should have at least one prompt"


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
            "read_laravel_doc_content",
            "get_laravel_package_recommendations",
            "verify_laravel_feature",
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
                assert len(params) > 0, f"Template has braces but no params"


@pytest.mark.protocol
class TestErrorResponses:
    """Test that error responses follow MCP spec format."""

    def test_invalid_package_returns_error(self, mcp_server):
        """Requesting invalid package should return proper error."""
        from laravel_mcp_companion import get_laravel_package_info
        result = get_laravel_package_info("nonexistent/package")
        # Should return TOON-encoded error
        assert "error" in result.lower() or "not found" in result.lower()

    def test_empty_search_query_handled(self, mcp_server, temp_dir):
        """Empty search queries should be handled gracefully."""
        from mcp_tools import search_laravel_docs_impl
        result = search_laravel_docs_impl(temp_dir, "", None, False, None, runtime_version="12.x")
        # Should return error or empty results, not crash
        assert result is not None


@pytest.mark.protocol
class TestToolInvocationStructure:
    """Test that tool invocations return correct content structure."""

    def test_package_recommendations_return_structured_data(self, mcp_server):
        """Package recommendations should return structured TOON data."""
        from laravel_mcp_companion import get_laravel_package_recommendations
        result = get_laravel_package_recommendations("authentication")
        # Should contain package data in TOON format
        assert result is not None
        assert len(result) > 0
        # TOON format indicators
        assert ":" in result or "packages" in result.lower()

    def test_package_info_return_structure(self, mcp_server):
        """Package info should return expected fields."""
        from laravel_mcp_companion import get_laravel_package_info
        result = get_laravel_package_info("laravel/sanctum")
        assert result is not None
        # Should contain key fields in TOON format
        assert "sanctum" in result.lower()

    def test_feature_map_returns_structured_data(self, mcp_server):
        """Feature lookup should return structured data."""
        from laravel_mcp_companion import get_features_for_laravel_package
        result = get_features_for_laravel_package("laravel/sanctum")
        assert result is not None
        assert "features" in result.lower() or ":" in result


@pytest.mark.protocol
class TestPromptStructure:
    """Test that prompts follow MCP specification."""

    async def test_prompts_have_names(self, mcp_server):
        """All prompts should have names."""
        prompts = await mcp_server.list_prompts()
        for prompt in prompts:
            assert prompt.name, "Prompt must have a name"
            assert len(prompt.name) > 0, "Prompt name cannot be empty"

    async def test_prompts_return_strings(self, mcp_server):
        """Prompt functions should return strings."""
        prompts = await mcp_server.list_prompts()
        for prompt in prompts:
            if hasattr(prompt, 'fn') and prompt.fn:
                result = prompt.fn()
                assert isinstance(result, str), f"Prompt '{prompt.name}' should return string"
                assert len(result) > 0, f"Prompt '{prompt.name}' returned empty string"


@pytest.mark.protocol
class TestToolAnnotations:
    """Test that tools have correct MCP annotations."""

    async def test_readonly_tools_are_marked(self, mcp_server):
        """Read-only tools should have readOnlyHint annotation."""
        tools = await mcp_server.list_tools()
        readonly_tool_names = {
            "list_laravel_docs",
            "search_laravel_docs",
            "read_laravel_doc_content",
            "get_laravel_package_recommendations",
            "verify_laravel_feature",
        }
        for tool in tools:
            if tool.name in readonly_tool_names:
                if hasattr(tool, 'annotations') and tool.annotations:
                    assert tool.annotations.readOnlyHint is True, \
                        f"Tool '{tool.name}' should be marked read-only"

    async def test_update_tools_not_marked_readonly(self, mcp_server):
        """Update tools should not be marked as read-only."""
        tools = await mcp_server.list_tools()
        update_tool_names = {"update_laravel_docs", "update_external_laravel_docs"}
        for tool in tools:
            if tool.name in update_tool_names:
                if hasattr(tool, 'annotations') and tool.annotations:
                    assert tool.annotations.readOnlyHint is False, \
                        f"Tool '{tool.name}' should not be marked read-only"
