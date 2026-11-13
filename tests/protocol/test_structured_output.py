"""Structured tool output (MCP 2025-06-18/2025-11-25).

Every tool returns machine-readable structuredContent that satisfies the
output schema it declares, alongside text for a model to read. Before v0.15
five of twenty-six tools did; the rest returned undocumented strings.
"""

import pytest

from fastmcp import Client

from laravel_mcp_companion.server import create_mcp_server
from laravel_mcp_companion.tools import ERROR_SCHEMA, REGISTRY

# One call per tool that succeeds on the shared fixture tree (11.x and 12.x).
SUCCESSFUL_CALLS = {
    "search_laravel_docs": {"query": "routing", "sources": ["core"]},
    "read_laravel_doc_section": {"filename": "routing.md", "section": "routing"},
    "read_laravel_doc_content": {"filename": "routing.md", "mode": "outline"},
    "list_laravel_docs": {"name": "12.x"},
    "laravel_docs_info": {},
    "compare_laravel_versions": {"from_version": "11.x", "to_version": "12.x"},
    "get_laravel_package": {"name": "laravel/sanctum"},
    "recommend_laravel_packages": {"use_case": "authentication"},
    "get_laravel_service_info": {"service": "forge"},
    "get_laravel_learning_path": {"path_name": "getting-started"},
    "browse_docs_by_category": {"category": "database"},
}

# One call per tool that fails, and the code it must fail with.
FAILING_CALLS = {
    "search_laravel_docs": ({"query": " "}, "invalid_argument"),
    "read_laravel_doc_section": ({"filename": "routing.md", "section": "no-such-section"}, "not_found"),
    "read_laravel_doc_content": ({"filename": "../../etc/passwd"}, "access_denied"),
    "list_laravel_docs": ({"name": "no-such-collection"}, "not_found"),
    "laravel_docs_info": ({"version": "99.x"}, "unknown_version"),
    "compare_laravel_versions": ({"from_version": "12.x", "to_version": "12.x"}, "invalid_argument"),
    "get_laravel_package": ({"name": "not/a-package"}, "not_found"),
    "recommend_laravel_packages": ({"use_case": ""}, "invalid_argument"),
    "get_laravel_service_info": ({"service": "horizon"}, "not_found"),
    "get_laravel_learning_path": ({"path_name": "no-such-path"}, "not_found"),
    "browse_docs_by_category": ({"difficulty": "expert"}, "invalid_argument"),
    "update_laravel_docs": ({"scope": "everything"}, "invalid_argument"),
}


def satisfies(value, schema, path="$"):
    """Problems found checking `value` against the subset of JSON Schema the
    tool schemas use: type, required, properties, items and enum."""
    problems = []
    expected = schema.get("type")
    types = {"object": dict, "array": list, "string": str, "boolean": bool, "integer": int, "number": (int, float)}
    if expected and (not isinstance(value, types[expected]) or (expected in ("integer", "number") and isinstance(value, bool))):
        return [f"{path}: expected {expected}, got {type(value).__name__}"]
    if "enum" in schema and value not in schema["enum"]:
        problems.append(f"{path}: {value!r} is not one of {schema['enum']}")
    if isinstance(value, dict):
        problems += [f"{path}: missing required {key!r}" for key in schema.get("required", []) if key not in value]
        for key, sub in schema.get("properties", {}).items():
            if key in value:
                problems += satisfies(value[key], sub, f"{path}.{key}")
    if isinstance(value, list) and "items" in schema:
        for index, item in enumerate(value):
            problems += satisfies(item, schema["items"], f"{path}[{index}]")
    return problems


@pytest.fixture
def mcp_server(test_docs_dir):
    return create_mcp_server("TestServer", test_docs_dir, "12.x", transform_mode=None)


def test_every_tool_has_a_successful_call_here_or_a_reason_not_to():
    # update_laravel_docs needs the network to succeed; test_tasks.py covers it with a stubbed updater.
    assert set(REGISTRY) - set(SUCCESSFUL_CALLS) == {"update_laravel_docs"}


def test_every_tool_has_a_failing_call_here():
    assert set(FAILING_CALLS) == set(REGISTRY)


@pytest.mark.protocol
class TestStructuredOutput:
    async def test_every_tool_declares_a_real_output_schema(self, mcp_server):
        """Not FastMCP's {"result": "<string>"} auto-wrapper."""
        async with Client(mcp_server) as client:
            tools = {t.name: t for t in await client.list_tools()}

        for name, tool in tools.items():
            assert tool.outputSchema is not None, f"{name} declares no output schema"
            assert "x-fastmcp-wrap-result" not in tool.outputSchema, f"{name} has the auto-wrapped string schema"
            assert tool.outputSchema.get("required"), f"{name} requires nothing of its own output"

    @pytest.mark.parametrize("name", sorted(SUCCESSFUL_CALLS))
    async def test_a_successful_result_satisfies_the_declared_schema(self, mcp_server, name):
        async with Client(mcp_server) as client:
            result = await client.call_tool(name, SUCCESSFUL_CALLS[name])

        assert result.is_error is False
        assert satisfies(result.structured_content, REGISTRY[name].output_schema) == []

    @pytest.mark.parametrize("name", sorted(SUCCESSFUL_CALLS))
    async def test_the_text_is_for_reading_and_is_not_json(self, mcp_server, name):
        async with Client(mcp_server) as client:
            result = await client.call_tool(name, SUCCESSFUL_CALLS[name])

        assert result.content[0].text
        assert not result.content[0].text.lstrip().startswith("{")

    @pytest.mark.parametrize("name", sorted(FAILING_CALLS))
    async def test_a_failure_is_an_error_result_matching_the_error_schema(self, mcp_server, name):
        arguments, code = FAILING_CALLS[name]
        async with Client(mcp_server) as client:
            result = await client.call_tool(name, arguments, raise_on_error=False)

        assert result.is_error is True
        assert satisfies(result.structured_content, ERROR_SCHEMA) == []
        assert result.structured_content["error"]["code"] == code

    async def test_a_section_read_returns_the_markdown_as_its_text(self, mcp_server):
        async with Client(mcp_server) as client:
            result = await client.call_tool("read_laravel_doc_section", {"filename": "routing.md", "section": "routing"})

        assert result.content[0].text == result.structured_content["content"]
        assert result.content[0].text.startswith("# Routing")


@pytest.mark.protocol
class TestSearchTransformProxy:
    """Search-mode clients get the same structure as --transform-mode none clients."""

    async def test_the_call_tool_proxy_forwards_structured_content(self, test_docs_dir):
        server = create_mcp_server("TestServer", test_docs_dir, "12.x", transform_mode="search")
        async with Client(server) as client:
            proxied = await client.call_tool("call_tool", {"name": "laravel_docs_info", "arguments": {"version": "12.x"}})
            direct = await client.call_tool("search_laravel_docs", {"query": "routing", "sources": ["core"]})

        assert proxied.structured_content["versions"][0]["version"] == "12.x"
        assert direct.structured_content["count"] >= 1

    async def test_a_failure_through_the_proxy_is_still_an_error_with_a_code(self, test_docs_dir):
        server = create_mcp_server("TestServer", test_docs_dir, "12.x", transform_mode="search")
        async with Client(server) as client:
            result = await client.call_tool(
                "call_tool", {"name": "laravel_docs_info", "arguments": {"version": "99.x"}}, raise_on_error=False,
            )

        assert result.is_error is True
        assert "unknown_version" in result.content[0].text
