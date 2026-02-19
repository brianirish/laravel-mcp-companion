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

    def test_server_has_tools(self, mcp_server):
        """Server should advertise available tools."""
        # FastMCP stores tools internally
        assert hasattr(mcp_server, '_tool_manager')
        tools = mcp_server._tool_manager._tools
        assert len(tools) > 0, "Server should have at least one tool"

    def test_server_has_resources(self, mcp_server):
        """Server should advertise available resources."""
        assert hasattr(mcp_server, '_resource_manager')
        # Check that resource templates are registered
        templates = mcp_server._resource_manager._templates
        assert len(templates) > 0, "Server should have resource templates"

    def test_server_has_prompts(self, mcp_server):
        """Server should advertise available prompts."""
        assert hasattr(mcp_server, '_prompt_manager')
        prompts = mcp_server._prompt_manager._prompts
        assert len(prompts) > 0, "Server should have at least one prompt"


@pytest.mark.protocol
class TestToolSchemas:
    """Test that all tools have valid JSON schemas."""

    def test_all_tools_have_descriptions(self, mcp_server):
        """Every tool should have a description."""
        tools = mcp_server._tool_manager._tools
        for name, tool in tools.items():
            assert tool.description, f"Tool '{name}' missing description"

    def test_tool_parameters_are_valid(self, mcp_server):
        """Tool parameters should be valid JSON Schema."""
        tools = mcp_server._tool_manager._tools
        for name, tool in tools.items():
            # FastMCP tools have parameters defined via function signatures
            # The schema is generated automatically
            if hasattr(tool, 'parameters') and tool.parameters:
                schema = tool.parameters
                # Basic JSON Schema validation
                assert isinstance(schema, dict), f"Tool '{name}' parameters not a dict"

    def test_required_tools_exist(self, mcp_server):
        """Required documentation tools should exist."""
        tools = mcp_server._tool_manager._tools
        required_tools = [
            "list_laravel_docs",
            "search_laravel_docs",
            "read_laravel_doc_content",
            "get_laravel_package_recommendations",
            "verify_laravel_feature",
        ]
        for tool_name in required_tools:
            assert tool_name in tools, f"Required tool '{tool_name}' missing"


@pytest.mark.protocol
class TestResourceTemplates:
    """Test that resource templates are valid URI templates."""

    def test_laravel_resource_template(self, mcp_server):
        """Laravel resource template should be valid."""
        templates = mcp_server._resource_manager._templates
        # Check that we have a laravel:// resource template
        template_uris = [str(t.uri_template) for t in templates.values()]
        assert any("laravel://" in uri for uri in template_uris), \
            "Missing laravel:// resource template"

    def test_external_resource_template(self, mcp_server):
        """External Laravel services resource template should be valid."""
        templates = mcp_server._resource_manager._templates
        template_uris = [str(t.uri_template) for t in templates.values()]
        assert any("laravel-external://" in uri for uri in template_uris), \
            "Missing laravel-external:// resource template"

    def test_resource_templates_have_parameters(self, mcp_server):
        """Resource templates should define their parameters."""
        templates = mcp_server._resource_manager._templates
        for name, template in templates.items():
            uri = str(template.uri_template)
            # URI templates use {param} syntax
            if "{" in uri:
                # Should have at least one parameter
                params = re.findall(r'\{(\w+)\}', uri)
                assert len(params) > 0, f"Template '{name}' has braces but no params"


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

    def test_prompts_have_names(self, mcp_server):
        """All prompts should have names."""
        prompts = mcp_server._prompt_manager._prompts
        for name, prompt in prompts.items():
            assert name, "Prompt must have a name"
            assert len(name) > 0, "Prompt name cannot be empty"

    def test_prompts_return_strings(self, mcp_server):
        """Prompt functions should return strings."""
        prompts = mcp_server._prompt_manager._prompts
        for name, prompt in prompts.items():
            # FastMCP prompts have a fn attribute
            if hasattr(prompt, 'fn') and prompt.fn:
                result = prompt.fn()
                assert isinstance(result, str), f"Prompt '{name}' should return string"
                assert len(result) > 0, f"Prompt '{name}' returned empty string"


@pytest.mark.protocol
class TestToolAnnotations:
    """Test that tools have correct MCP annotations."""

    def test_readonly_tools_are_marked(self, mcp_server):
        """Read-only tools should have readOnlyHint annotation."""
        tools = mcp_server._tool_manager._tools
        readonly_tools = [
            "list_laravel_docs",
            "search_laravel_docs",
            "read_laravel_doc_content",
            "get_laravel_package_recommendations",
            "verify_laravel_feature",
        ]
        for tool_name in readonly_tools:
            if tool_name in tools:
                tool = tools[tool_name]
                # Check annotations if present (Pydantic model with attributes)
                if hasattr(tool, 'annotations') and tool.annotations:
                    assert tool.annotations.readOnlyHint is True, \
                        f"Tool '{tool_name}' should be marked read-only"

    def test_update_tools_not_marked_readonly(self, mcp_server):
        """Update tools should not be marked as read-only."""
        tools = mcp_server._tool_manager._tools
        update_tools = ["update_laravel_docs", "update_external_laravel_docs"]
        for tool_name in update_tools:
            if tool_name in tools:
                tool = tools[tool_name]
                if hasattr(tool, 'annotations') and tool.annotations:
                    # readOnlyHint should be False for update tools
                    assert tool.annotations.readOnlyHint is False, \
                        f"Tool '{tool_name}' should not be marked read-only"
