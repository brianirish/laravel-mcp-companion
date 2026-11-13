"""Integration tests for Laravel MCP Companion using FastMCP Client."""

import pytest
import asyncio
from pathlib import Path
import tempfile

from fastmcp import Client
from laravel_mcp_companion.server import create_mcp_server


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
    """Create an MCP server instance for testing (no transforms for raw tool access)."""
    server = create_mcp_server("TestLaravelMCP", temp_docs_dir, "12.x", transform_mode=None)
    return server


# Every tool, called through the protocol with arguments that succeed on the
# small tree above, and one key its structured result must carry.
CALLS = [
    ("search_laravel_docs", {"query": "Eloquent", "version": "12.x"}, "results"),
    ("read_laravel_doc_section", {"filename": "blade.md", "section": "blade-templates"}, "content"),
    ("read_laravel_doc_content", {"filename": "blade.md"}, "content"),
    ("read_laravel_doc_content", {"filename": "blade.md", "mode": "outline"}, "headings"),
    ("list_laravel_docs", {}, "collections"),
    ("list_laravel_docs", {"name": "12.x"}, "collections"),
    ("laravel_docs_info", {}, "versions"),
    ("laravel_docs_info", {"version": "12.x"}, "versions"),
    ("get_laravel_package", {"name": "laravel/sanctum"}, "packages"),
    ("get_laravel_package", {"category": "authentication"}, "packages"),
    ("recommend_laravel_packages", {"use_case": "authentication"}, "packages"),
    ("get_laravel_service_info", {"service": "forge"}, "status"),
    ("get_laravel_learning_path", {"path_name": "getting-started"}, "paths"),
    ("browse_docs_by_category", {}, "categories"),
    ("browse_docs_by_category", {"category": "frontend"}, "docs"),
]


class TestMCPIntegration:
    """Each tool, reached the way a client reaches it."""

    @pytest.mark.asyncio
    @pytest.mark.parametrize("name,arguments,key", CALLS, ids=[f"{n}:{','.join(a) or 'no-args'}" for n, a, _ in CALLS])
    async def test_a_tool_answers_with_text_and_structured_content(self, mcp_server, name, arguments, key):
        async with Client(mcp_server) as client:
            result = await client.call_tool(name, arguments)

        assert result.is_error is False
        assert key in result.structured_content
        assert result.content[0].text

    @pytest.mark.asyncio
    async def test_compare_needs_two_versions_on_disk(self, mcp_server, temp_docs_dir):
        (temp_docs_dir / "11.x").mkdir()
        (temp_docs_dir / "11.x" / "blade.md").write_text("# Blade\n")

        async with Client(mcp_server) as client:
            result = await client.call_tool("compare_laravel_versions", {"from_version": "11.x", "to_version": "12.x"})

        assert result.structured_content["added_files"] == ["eloquent.md", "routing.md"]

    @pytest.mark.asyncio
    async def test_a_listing_names_the_files_of_a_version(self, mcp_server):
        async with Client(mcp_server) as client:
            result = await client.call_tool("list_laravel_docs", {"name": "12.x"})

        assert result.structured_content["collections"][0]["files"] == [
            "12.x/blade.md", "12.x/eloquent.md", "12.x/routing.md",
        ]

    @pytest.mark.asyncio
    async def test_a_documentation_page_is_returned_as_markdown_text(self, mcp_server):
        """A page reads better as the markdown it is than as an encoded object."""
        async with Client(mcp_server) as client:
            result = await client.call_tool("read_laravel_doc_content", {"filename": "blade.md"})

        assert result.content[0].text == "# Blade Templates\n\nThis is Blade documentation."
        assert result.structured_content["content"] == result.content[0].text

    @pytest.mark.asyncio
    async def test_a_failure_is_an_error_result_with_a_code(self, mcp_server):
        async with Client(mcp_server) as client:
            result = await client.call_tool("read_laravel_doc_content", {"filename": "missing.md"}, raise_on_error=False)

        assert result.is_error is True
        assert result.structured_content["error"]["code"] == "not_found"

    @pytest.mark.asyncio
    async def test_a_search_that_finds_nothing_is_not_an_error(self, mcp_server):
        async with Client(mcp_server) as client:
            result = await client.call_tool("search_laravel_docs", {"query": "zzzqqqxxx", "sources": ["core"]})

        assert result.is_error is False
        assert result.structured_content["count"] == 0

    @pytest.mark.asyncio
    async def test_the_removed_tools_are_gone(self, mcp_server):
        async with Client(mcp_server) as client:
            names = {tool.name for tool in await client.list_tools()}

        assert not names & {
            "verify_laravel_feature", "find_laravel_docs_for_need", "search_external_laravel_docs",
            "search_laravel_learning_resources", "get_doc_structure", "list_laravel_services",
            "update_external_laravel_docs", "get_laravel_package_info", "get_laravel_package_recommendations",
        }

    @pytest.mark.asyncio
    async def test_there_are_no_prompts(self, mcp_server):
        async with Client(mcp_server) as client:
            assert await client.list_prompts() == []


class TestMCPServerLifecycle:
    """Test MCP server lifecycle operations."""
    
    @pytest.mark.asyncio
    async def test_multiple_client_connections(self, mcp_server):
        """Test multiple clients connecting to the same server."""
        # First client
        async with Client(mcp_server) as client1:
            result1 = await client1.call_tool("list_laravel_docs", {"name": "12.x"})
            assert result1 is not None
        
        # Second client (after first closes)
        async with Client(mcp_server) as client2:
            result2 = await client2.call_tool("list_laravel_docs", {"name": "12.x"})
            assert result2 is not None
    
    @pytest.mark.asyncio
    async def test_concurrent_tool_calls(self, mcp_server):
        """Test calling multiple tools concurrently."""
        async with Client(mcp_server) as client:
            # Call multiple tools concurrently
            results = await asyncio.gather(
                client.call_tool("list_laravel_docs", {}),
                client.call_tool("laravel_docs_info", {}),
                client.call_tool("get_laravel_service_info", {"service": "forge"})
            )
            
            # Verify all results
            assert len(results) == 3
            assert all(result is not None for result in results)


class TestTransformConfiguration:
    """Test transform configuration via CLI and server setup."""

    def test_parse_arguments_code_mode_flag(self, monkeypatch):
        """Test that --code-mode flag is parsed correctly."""
        import sys
        from laravel_mcp_companion.server import parse_arguments

        # Test default (no flag)
        monkeypatch.delenv("CODE_MODE", raising=False)
        monkeypatch.setattr(sys, "argv", ["prog"])
        args = parse_arguments()
        assert args.code_mode is False

        # Test with flag
        monkeypatch.delenv("CODE_MODE", raising=False)
        monkeypatch.setattr(sys, "argv", ["prog", "--code-mode"])
        args = parse_arguments()
        assert args.code_mode is True

    def test_parse_arguments_transform_mode(self, monkeypatch):
        """Test that --transform-mode flag and TRANSFORM_MODE env are parsed correctly."""
        import sys
        from laravel_mcp_companion.server import parse_arguments

        monkeypatch.delenv("TRANSFORM_MODE", raising=False)
        monkeypatch.delenv("CODE_MODE", raising=False)

        # Default: unset (main() resolves this to "search")
        monkeypatch.setattr(sys, "argv", ["prog"])
        assert parse_arguments().transform_mode is None

        # Explicit CLI values
        for mode in ("search", "code", "none"):
            monkeypatch.setattr(sys, "argv", ["prog", "--transform-mode", mode])
            assert parse_arguments().transform_mode == mode

        # Env var
        monkeypatch.setenv("TRANSFORM_MODE", "code")
        monkeypatch.setattr(sys, "argv", ["prog"])
        assert parse_arguments().transform_mode == "code"

        # Invalid env var is rejected (argparse doesn't validate defaults)
        monkeypatch.setenv("TRANSFORM_MODE", "garbage")
        monkeypatch.setattr(sys, "argv", ["prog"])
        with pytest.raises(SystemExit):
            parse_arguments()

    @pytest.mark.asyncio
    async def test_search_transform_applied_by_default(self, temp_docs_dir):
        """Test that BM25SearchTransform is applied when code_mode=False."""
        from laravel_mcp_companion.server import create_mcp_server

        server = create_mcp_server("TestMCP", temp_docs_dir, "12.x", transform_mode="search")
        async with Client(server) as client:
            tools = await client.list_tools()
            tool_names = [t.name for t in tools]
            # Should have synthetic search tools, not raw tools
            assert "search_tools" in tool_names
            assert "call_tool" in tool_names
            # search_laravel_docs is pinned via always_visible (CI smoke test relies on this)
            assert "search_laravel_docs" in tool_names
            # Other raw tools should NOT be listed
            assert "list_laravel_docs" not in tool_names

    @pytest.mark.asyncio
    async def test_code_mode_transform_applied(self, temp_docs_dir):
        """Test that CodeMode is applied when code_mode=True."""
        from laravel_mcp_companion.server import create_mcp_server

        server = create_mcp_server("TestMCP", temp_docs_dir, "12.x", transform_mode="code")
        async with Client(server) as client:
            tools = await client.list_tools()
            tool_names = [t.name for t in tools]
            # Should have Code Mode meta-tools
            assert "search" in tool_names
            assert "execute" in tool_names
            # Raw tools should NOT be listed
            assert "list_laravel_docs" not in tool_names

    @pytest.mark.asyncio
    async def test_no_transforms_mode(self, temp_docs_dir):
        """Test that transform_mode=None applies no transforms (for backward compat)."""
        from laravel_mcp_companion.server import create_mcp_server

        server = create_mcp_server("TestMCP", temp_docs_dir, "12.x", transform_mode=None)
        async with Client(server) as client:
            tools = await client.list_tools()
            tool_names = [t.name for t in tools]
            # Should have raw tools, not transform tools
            assert "list_laravel_docs" in tool_names
            assert "search_laravel_docs" in tool_names
            assert "search_tools" not in tool_names
            assert "call_tool" not in tool_names

    @pytest.mark.asyncio
    async def test_search_tools_finds_relevant_tools(self, temp_docs_dir):
        """Test that search_tools returns relevant results for a query."""
        from laravel_mcp_companion.server import create_mcp_server

        server = create_mcp_server("TestMCP", temp_docs_dir, "12.x", transform_mode="search")
        async with Client(server) as client:
            result = await client.call_tool("search_tools", {"query": "documentation list search"})
            if hasattr(result, 'content') and isinstance(result.content, list):
                content = result.content[0].text if result.content else ""
            else:
                content = str(result)
            # Should find doc-related tools
            assert "list_laravel_docs" in content or "search_laravel_docs" in content

    @pytest.mark.asyncio
    async def test_call_tool_proxy_works(self, temp_docs_dir):
        """Test that call_tool proxy can invoke underlying tools."""
        from laravel_mcp_companion.server import create_mcp_server

        server = create_mcp_server("TestMCP", temp_docs_dir, "12.x", transform_mode="search")
        async with Client(server) as client:
            # Use the call_tool proxy to invoke a real tool
            result = await client.call_tool("call_tool", {
                "name": "list_laravel_docs",
                "arguments": {"name": "12.x"}
            })
            if hasattr(result, 'content') and isinstance(result.content, list):
                content = result.content[0].text if result.content else ""
            else:
                content = str(result)
            assert "blade.md" in content
