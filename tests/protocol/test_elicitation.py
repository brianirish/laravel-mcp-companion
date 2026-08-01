"""Elicitation for learning path selection (MCP 2025-06-18/2025-11-25).

get_laravel_learning_path called without a path asks the one question the
protocol lets it ask — which path? — instead of dumping the listing. Clients
that decline, cancel, or can't elicit at all get exactly the old behavior.
"""

import pytest

from fastmcp import Client
from fastmcp.client.elicitation import ElicitResult

from laravel_mcp_companion import create_mcp_server
from learning_resources import LEARNING_PATHS


@pytest.fixture
def mcp_server(test_docs_dir):
    return create_mcp_server("TestServer", test_docs_dir, "12.x", transform_mode=None)


@pytest.mark.protocol
class TestLearningPathElicitation:
    async def test_empty_path_name_elicits_and_returns_chosen_path(self, mcp_server):
        seen = {}

        async def handler(message, response_type, params, context):
            seen["message"] = message
            seen["schema"] = params.requestedSchema
            return ElicitResult(action="accept", content={"value": "getting-started"})

        async with Client(mcp_server, elicitation_handler=handler) as client:
            res = await client.call_tool("get_laravel_learning_path", {})
            # The elicitation offered every curated path, with titles
            options = seen["schema"]["properties"]["value"]["oneOf"]
            assert {o["const"] for o in options} == set(LEARNING_PATHS.keys())
            assert all(o.get("title") for o in options)
            # And the answer selected the path
            text = res.content[0].text
            assert "Getting Started" in text
            assert "path_name" in text or "name" in text

    async def test_decline_falls_back_to_listing(self, mcp_server):
        async def handler(message, response_type, params, context):
            return ElicitResult(action="decline")

        async with Client(mcp_server, elicitation_handler=handler) as client:
            res = await client.call_tool("get_laravel_learning_path", {})
            assert "getting-started" in res.content[0].text

    async def test_client_without_elicitation_gets_listing(self, mcp_server):
        async with Client(mcp_server) as client:
            res = await client.call_tool("get_laravel_learning_path", {})
            assert "getting-started" in res.content[0].text

    async def test_explicit_path_name_skips_elicitation(self, mcp_server):
        async def handler(message, response_type, params, context):
            raise AssertionError("must not elicit when a path was given")

        async with Client(mcp_server, elicitation_handler=handler) as client:
            res = await client.call_tool(
                "get_laravel_learning_path", {"path_name": "getting-started"}
            )
            assert "Getting Started" in res.content[0].text
