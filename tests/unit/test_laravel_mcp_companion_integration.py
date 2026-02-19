"""Integration tests for Laravel MCP Companion using FastMCP Client."""

import pytest
import asyncio
from pathlib import Path
import tempfile

from fastmcp import Client
from laravel_mcp_companion import create_mcp_server


@pytest.fixture
def temp_docs_dir():
    """Create a temporary documentation directory."""
    with tempfile.TemporaryDirectory() as tmpdir:
        docs_path = Path(tmpdir)
        
        # Create some test documentation files
        version_dir = docs_path / "12.x"
        version_dir.mkdir(parents=True)
        
        (version_dir / "blade.md").write_text("# Blade Templates\n\nThis is Blade documentation.")
        (version_dir / "eloquent.md").write_text("# Eloquent ORM\n\nThis is Eloquent documentation.")
        (version_dir / "routing.md").write_text("# Routing\n\nThis is routing documentation.")
        
        # Create metadata file
        metadata_file = version_dir / ".metadata.json"
        metadata_file.write_text("""{
            "version": "12.x",
            "commit_sha": "abc123",
            "commit_date": "2024-01-01",
            "commit_message": "Test commit",
            "sync_time": "2024-01-01T00:00:00Z"
        }""")
        
        yield docs_path


@pytest.fixture
def mcp_server(temp_docs_dir):
    """Create an MCP server instance for testing."""
    server = create_mcp_server("TestLaravelMCP", temp_docs_dir, "12.x")
    return server


class TestMCPIntegration:
    """Test MCP server integration using FastMCP Client."""
    
    @pytest.mark.asyncio
    async def test_list_laravel_docs_tool(self, mcp_server):
        """Test the list_laravel_docs tool through MCP protocol."""
        async with Client(mcp_server) as client:
            # Call the tool
            result = await client.call_tool("list_laravel_docs", {"version": "12.x"})
            
            # Verify result
            assert result is not None
            # FastMCP 2.10+ returns CallToolResult with .content attribute containing list of TextContent
            if hasattr(result, 'content') and isinstance(result.content, list):
                content = result.content[0].text if result.content else ""
            else:
                content = str(result)
            assert "blade.md" in content
            assert "eloquent.md" in content
            assert "routing.md" in content
    
    # Removed test_read_laravel_doc_resource - it was testing FastMCP's URI resolution, not our code.
    # The read_laravel_doc function should be tested directly in unit tests.
    
    @pytest.mark.asyncio
    async def test_search_laravel_docs_tool(self, mcp_server):
        """Test the search_laravel_docs tool through MCP protocol."""
        async with Client(mcp_server) as client:
            # Search for a term
            result = await client.call_tool("search_laravel_docs", {
                "query": "Eloquent",
                "version": "12.x"
            })
            
            # Verify result
            assert result is not None
            # FastMCP 2.10+ returns CallToolResult with .content attribute containing list of TextContent
            if hasattr(result, 'content') and isinstance(result.content, list):
                content = result.content[0].text if result.content else ""
            else:
                content = str(result)
            assert "eloquent.md" in content
    
    @pytest.mark.asyncio
    async def test_laravel_docs_info_tool(self, mcp_server):
        """Test the laravel_docs_info tool through MCP protocol."""
        async with Client(mcp_server) as client:
            # Get documentation info
            result = await client.call_tool("laravel_docs_info", {"version": "12.x"})
            
            # Verify result
            assert result is not None
            # FastMCP 2.10+ returns CallToolResult with .content attribute containing list of TextContent
            if hasattr(result, 'content') and isinstance(result.content, list):
                content = result.content[0].text if result.content else ""
            else:
                content = str(result)
            # TOON format: version and commit_sha fields
            assert "12.x" in content
            assert "abc123" in content
    
    @pytest.mark.asyncio
    async def test_get_laravel_package_recommendations_tool(self, mcp_server):
        """Test the get_laravel_package_recommendations tool through MCP protocol."""
        async with Client(mcp_server) as client:
            # Get package recommendations
            result = await client.call_tool("get_laravel_package_recommendations", {
                "use_case": "authentication"
            })
            
            # Verify result
            assert result is not None
            # FastMCP 2.10+ returns CallToolResult with .content attribute containing list of TextContent
            if hasattr(result, 'content') and isinstance(result.content, list):
                content = result.content[0].text if result.content else ""
            else:
                content = str(result)
            # TOON format: context field contains the use case
            assert "authentication" in content
    
    # Removed test_read_nonexistent_doc - it was testing FastMCP's URI resolution, not our code.
    # Error handling in read_laravel_doc should be tested directly in unit tests.
    
    # Removed test_invalid_tool_parameters - it was testing FastMCP's parameter validation.
    # Our tool parameter validation should be tested in unit tests.
    
    @pytest.mark.asyncio
    async def test_list_all_tools(self, mcp_server):
        """Test listing all available tools."""
        async with Client(mcp_server) as client:
            # Get list of tools
            tools = await client.list_tools()
            
            # Verify some expected tools are present
            tool_names = [tool.name for tool in tools]
            assert "list_laravel_docs" in tool_names
            assert "search_laravel_docs" in tool_names
            assert "update_laravel_docs" in tool_names
            assert "get_laravel_package_recommendations" in tool_names
    
    @pytest.mark.asyncio
    async def test_list_all_resources(self, mcp_server):
        """Test listing all available resource templates."""
        async with Client(mcp_server) as client:
            templates = await client.list_resource_templates()
            assert templates is not None
            template_uris = [str(t.uriTemplate) for t in templates]
            print(f"Registered resource templates: {template_uris}")
            assert any("laravel://" in uri for uri in template_uris)
            assert any("laravel-external://" in uri for uri in template_uris)


class TestMCPExternalDocumentation:
    """Test external documentation tools through MCP protocol."""
    
    @pytest.mark.asyncio
    async def test_list_laravel_services(self, mcp_server):
        """Test listing Laravel services."""
        async with Client(mcp_server) as client:
            # List services
            result = await client.call_tool("list_laravel_services", {})
            
            # Verify result
            assert result is not None
            # FastMCP 2.10+ returns CallToolResult with .content attribute containing list of TextContent
            if hasattr(result, 'content') and isinstance(result.content, list):
                content = result.content[0].text if result.content else ""
            else:
                content = str(result)
            # TOON format: services list with count
            assert "services" in content or "count" in content
    
    @pytest.mark.asyncio
    async def test_search_external_docs_empty_query(self, mcp_server):
        """Test searching external docs with empty query."""
        async with Client(mcp_server) as client:
            # Search with empty query
            result = await client.call_tool("search_external_laravel_docs", {"query": ""})
            
            # Verify error message
            assert result is not None
            # FastMCP 2.10+ returns CallToolResult with .content attribute containing list of TextContent
            if hasattr(result, 'content') and isinstance(result.content, list):
                content = result.content[0].text if result.content else ""
            else:
                content = str(result)
            assert "Search query cannot be empty" in content


class TestMCPPackageTools:
    """Test package-related tools through MCP protocol."""
    
    @pytest.mark.asyncio
    async def test_get_package_info(self, mcp_server):
        """Test getting package information."""
        async with Client(mcp_server) as client:
            # Get package info
            result = await client.call_tool("get_laravel_package_info", {
                "package_name": "laravel/sanctum"
            })
            
            # Verify result
            assert result is not None
            # FastMCP 2.10+ returns CallToolResult with .content attribute containing list of TextContent
            if hasattr(result, 'content') and isinstance(result.content, list):
                content = result.content[0].text if result.content else ""
            else:
                content = str(result)
            assert "Laravel Sanctum" in content
    
    @pytest.mark.asyncio
    async def test_get_package_categories(self, mcp_server):
        """Test getting packages by category."""
        async with Client(mcp_server) as client:
            # Get packages in authentication category
            result = await client.call_tool("get_laravel_package_categories", {
                "category": "authentication"
            })
            
            # Verify result
            assert result is not None
            # FastMCP 2.10+ returns CallToolResult with .content attribute containing list of TextContent
            if hasattr(result, 'content') and isinstance(result.content, list):
                content = result.content[0].text if result.content else ""
            else:
                content = str(result)
            # TOON format: context contains category
            assert "authentication" in content
    
    @pytest.mark.asyncio
    async def test_get_features_for_package(self, mcp_server):
        """Test getting features for a package."""
        async with Client(mcp_server) as client:
            # Get features for Laravel Cashier
            result = await client.call_tool("get_features_for_laravel_package", {
                "package": "laravel/cashier"
            })
            
            # Verify result
            assert result is not None
            # FastMCP 2.10+ returns CallToolResult with .content attribute containing list of TextContent
            if hasattr(result, 'content') and isinstance(result.content, list):
                content = result.content[0].text if result.content else ""
            else:
                content = str(result)
            # TOON format: package name should be present
            assert "laravel/cashier" in content


@pytest.mark.integration
class TestMCPServerLifecycle:
    """Test MCP server lifecycle operations."""
    
    @pytest.mark.asyncio
    async def test_multiple_client_connections(self, mcp_server):
        """Test multiple clients connecting to the same server."""
        # First client
        async with Client(mcp_server) as client1:
            result1 = await client1.call_tool("list_laravel_docs", {"version": "12.x"})
            assert result1 is not None
        
        # Second client (after first closes)
        async with Client(mcp_server) as client2:
            result2 = await client2.call_tool("list_laravel_docs", {"version": "12.x"})
            assert result2 is not None
    
    @pytest.mark.asyncio
    async def test_concurrent_tool_calls(self, mcp_server):
        """Test calling multiple tools concurrently."""
        async with Client(mcp_server) as client:
            # Call multiple tools concurrently
            results = await asyncio.gather(
                client.call_tool("list_laravel_docs", {}),
                client.call_tool("laravel_docs_info", {}),
                client.call_tool("list_laravel_services", {})
            )
            
            # Verify all results
            assert len(results) == 3
            assert all(result is not None for result in results)