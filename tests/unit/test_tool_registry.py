"""How a tool's return value, or its failure, becomes what the client receives."""

import asyncio

import pytest

from laravel_mcp_companion.tools import ERROR_CODES, ERROR_SCHEMA, REGISTRY, STABLE_TOOLS, Reply, ToolFailure
from laravel_mcp_companion.tools.registry import _reporting_failures, failure, success


class TestSuccess:
    def test_a_payload_is_sent_as_toon_text_and_as_the_object(self):
        result = success({"count": 2, "files": ["a.md", "b.md"]})

        assert result.structured_content == {"count": 2, "files": ["a.md", "b.md"]}
        assert result.content[0].text == "count: 2\nfiles[2]: a.md,b.md"
        assert result.is_error is False

    def test_a_reply_supplies_its_own_text(self):
        result = success(Reply(data={"file": "a.md", "content": "# A\n\nBody."}, text="# A\n\nBody."))

        assert result.content[0].text == "# A\n\nBody."
        assert result.structured_content["file"] == "a.md"


class TestFailure:
    def test_a_failure_is_marked_as_an_error(self):
        assert failure(ToolFailure("not_found", "No such page")).is_error is True

    def test_the_error_object_is_in_the_structured_content_and_the_text(self):
        result = failure(ToolFailure("unknown_version", "No 99.x", {"supported_versions": ["12.x"]}))

        assert result.structured_content == {"error": {
            "code": "unknown_version", "message": "No 99.x", "details": {"supported_versions": ["12.x"]},
        }}
        assert "code: unknown_version" in result.content[0].text

    def test_details_are_left_out_when_there_are_none(self):
        assert failure(ToolFailure("not_found", "gone")).structured_content == {
            "error": {"code": "not_found", "message": "gone"},
        }

    def test_an_error_object_matches_the_published_error_schema(self):
        payload = ToolFailure("invalid_argument", "bad", {"limit": 0}).payload()
        schema = ERROR_SCHEMA["properties"]["error"]

        assert set(schema["required"]) <= set(payload["error"])
        assert payload["error"]["code"] in schema["properties"]["code"]["enum"]

    def test_a_code_outside_the_published_set_cannot_be_raised(self):
        with pytest.raises(ValueError):
            ToolFailure("teapot", "no")

    def test_the_published_codes_are_the_ones_the_schema_allows(self):
        assert tuple(ERROR_SCHEMA["properties"]["error"]["properties"]["code"]["enum"]) == ERROR_CODES


class TestToolsNeverRaise:
    def test_a_tool_failure_becomes_an_error_result(self):
        def tool():
            raise ToolFailure("not_found", "gone")

        result = _reporting_failures("example", tool)()

        assert (result.is_error, result.structured_content["error"]["code"]) == (True, "not_found")

    def test_an_unexpected_exception_becomes_an_internal_error(self):
        def tool():
            raise KeyError("oops")

        result = _reporting_failures("example", tool)()

        assert result.structured_content["error"]["code"] == "internal"
        assert "example" in result.structured_content["error"]["message"]

    def test_an_async_tool_is_wrapped_the_same_way(self):
        async def tool():
            raise ToolFailure("update_failed", "offline")

        result = asyncio.run(_reporting_failures("example", tool)())

        assert result.structured_content["error"]["code"] == "update_failed"

    def test_a_successful_async_tool_returns_its_payload(self):
        async def tool():
            return {"scope": "core"}

        assert asyncio.run(_reporting_failures("example", tool)()).structured_content == {"scope": "core"}


class TestArgumentsAreBounded:
    """A string argument is matched against headings and scored against every
    section. Over HTTP it can be megabytes long, and one such request held the
    whole process for seconds. No real filename, section or question is close
    to the limit."""

    def test_a_string_argument_over_the_limit_is_refused_before_the_tool_runs(self):
        from laravel_mcp_companion.tools.registry import MAX_ARGUMENT_LENGTH
        ran = []
        wrapped = _reporting_failures("example", lambda **kwargs: ran.append(kwargs) or {})

        result = wrapped(section="[" * (MAX_ARGUMENT_LENGTH + 1))

        assert result.is_error
        error = result.structured_content["error"]
        assert error["code"] == "invalid_argument"
        assert "section" in error["message"]
        assert not ran

    def test_an_argument_at_the_limit_is_passed_through(self):
        from laravel_mcp_companion.tools.registry import MAX_ARGUMENT_LENGTH
        wrapped = _reporting_failures("example", lambda **kwargs: {"length": len(kwargs["query"])})

        assert wrapped(query="a" * MAX_ARGUMENT_LENGTH).structured_content == {"length": MAX_ARGUMENT_LENGTH}

    def test_a_string_inside_a_list_is_bounded_too(self):
        from laravel_mcp_companion.tools.registry import MAX_ARGUMENT_LENGTH
        wrapped = _reporting_failures("example", lambda **kwargs: {})

        assert wrapped(names=["forge", "x" * (MAX_ARGUMENT_LENGTH + 1)]).is_error

    def test_a_list_with_too_many_items_is_refused(self):
        from laravel_mcp_companion.tools.registry import MAX_LIST_ITEMS
        wrapped = _reporting_failures("example", lambda **kwargs: {})

        assert wrapped(names=["a"] * (MAX_LIST_ITEMS + 1)).is_error
        assert not wrapped(names=["a"] * MAX_LIST_ITEMS).is_error

    def test_an_async_tool_is_bounded_the_same_way(self):
        from laravel_mcp_companion.tools.registry import MAX_ARGUMENT_LENGTH

        async def tool(**kwargs):
            return {}

        result = asyncio.run(_reporting_failures("example", tool)(query="a" * (MAX_ARGUMENT_LENGTH + 1)))

        assert result.structured_content["error"]["code"] == "invalid_argument"

    async def test_a_real_tool_refuses_an_overlong_section_over_the_protocol(self, tmp_path):
        from fastmcp import Client
        from laravel_mcp_companion.server import create_mcp_server
        from laravel_mcp_companion.tools.registry import MAX_ARGUMENT_LENGTH

        server = create_mcp_server("t", tmp_path, "12.x", transform_mode=None)
        async with Client(server) as client:
            result = await client.call_tool(
                "read_laravel_doc_section",
                {"filename": "queues.md", "section": "[" * (MAX_ARGUMENT_LENGTH + 1)},
                raise_on_error=False,
            )

        assert result.is_error
        assert result.structured_content["error"]["code"] == "invalid_argument"


class TestWhatIsDeclared:
    def test_there_are_twelve_tools(self):
        assert len(REGISTRY) == 12

    def test_ten_of_them_are_covered_by_the_versioning_guarantee(self):
        assert len(STABLE_TOOLS) == 10

    @pytest.mark.parametrize("name", sorted(REGISTRY))
    def test_every_tool_declares_an_object_schema_with_required_fields(self, name):
        schema = REGISTRY[name].output_schema

        assert schema["type"] == "object"
        assert schema["required"], f"{name} names no required output field"
        assert set(schema["required"]) <= set(schema["properties"])

    @pytest.mark.parametrize("name", sorted(REGISTRY))
    def test_no_success_schema_has_an_error_field(self, name):
        """Success and failure used to share one shape, which is why nothing
        could be required."""
        assert "error" not in REGISTRY[name].output_schema["properties"]

    @pytest.mark.parametrize("name", sorted(REGISTRY))
    def test_every_tool_has_a_description_that_says_when_to_use_it(self, name):
        assert len(REGISTRY[name].description) > 120

    def test_only_the_update_tool_writes(self):
        assert [name for name, spec in REGISTRY.items() if not spec.read_only] == ["update_laravel_docs"]
