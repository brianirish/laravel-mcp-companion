"""MCP tasks (SEP-1686, experimental in 2025-11-25).

update_laravel_docs is the only call that legitimately takes minutes, so it
is the task-capable surface: task-aware clients poll instead of holding the
connection open, and everyone else keeps the synchronous behavior.
"""

import asyncio

import pytest

from fastmcp import Client

from laravel_mcp_companion.server import create_mcp_server
from laravel_mcp_companion.tools import docs as docs_tools


class FakeDocsUpdater:
    """Stands in for DocsUpdater so no test touches the network."""

    def __init__(self, docs_path, version):
        self.docs_path = docs_path
        self.version = version

    def update(self, force=False):
        return False  # "already up to date"


@pytest.fixture
def mcp_server(test_docs_dir, monkeypatch):
    monkeypatch.setattr(docs_tools, "DocsUpdater", FakeDocsUpdater)
    return create_mcp_server("TestServer", test_docs_dir, "12.x", transform_mode=None)


@pytest.mark.protocol
class TestTasks:
    async def test_tasks_capability_advertised(self, mcp_server):
        async with Client(mcp_server) as client:
            caps = client.initialize_result.capabilities.model_dump(exclude_none=True)
            assert "tasks" in caps, "Server should negotiate the tasks capability"

    async def test_update_docs_runs_as_task(self, mcp_server):
        async with Client(mcp_server) as client:
            task = await client.call_tool(
                "update_laravel_docs", {"version": "12.x"}, task=True
            )
            for _ in range(100):
                status = await client.get_task_status(task.task_id)
                if status.status in ("completed", "failed", "cancelled"):
                    break
                await asyncio.sleep(0.05)
            assert status.status == "completed"
            result = await client.get_task_result(task.task_id)
            assert "unchanged" in str(result)

    async def test_update_docs_still_works_synchronously(self, mcp_server):
        async with Client(mcp_server) as client:
            res = await client.call_tool("update_laravel_docs", {"version": "12.x"})
            assert res.structured_content["results"] == [
                {"source": "core", "name": "12.x", "outcome": "unchanged", "commit": "abc123x"},
            ]

    async def test_the_update_tool_declares_task_support(self, mcp_server):
        """It advertises execution.taskSupport = optional.

        "optional" is the non-breaking mode: task-aware clients poll, sync
        clients run the tool exactly as before.
        """
        async with Client(mcp_server) as client:
            tools = {t.name: t for t in await client.list_tools()}
            execution = getattr(tools["update_laravel_docs"], "execution", None)
            assert execution is not None, "update_laravel_docs should declare task execution"
            assert execution.taskSupport == "optional"

    async def test_no_other_tool_declares_task_support(self, mcp_server):
        async with Client(mcp_server) as client:
            tools = await client.list_tools()

        task_capable = [
            t.name for t in tools
            if getattr(getattr(t, "execution", None), "taskSupport", None) not in (None, "forbidden")
        ]
        assert task_capable == ["update_laravel_docs"]

    async def test_short_tools_do_not_declare_task_support(self, mcp_server):
        """Fast tools stay plain; a task handle for a 5ms read is overhead."""
        async with Client(mcp_server) as client:
            tools = {t.name: t for t in await client.list_tools()}
            execution = getattr(tools["list_laravel_docs"], "execution", None)
            assert execution is None or getattr(execution, "taskSupport", "forbidden") in (
                None, "forbidden"
            )

    async def test_invalid_version_still_rejected(self, mcp_server):
        async with Client(mcp_server) as client:
            res = await client.call_tool(
                "update_laravel_docs", {"version": "../../etc"},
                raise_on_error=False,
            )
            assert res.is_error is True
            assert res.structured_content["error"]["code"] == "unknown_version"
