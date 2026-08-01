"""MCP tasks (SEP-1686, experimental in 2025-11-25).

The two update tools are the only calls that legitimately take minutes, so
they are the task-capable surface: task-aware clients poll instead of holding
the connection open, and everyone else keeps the synchronous behavior.
"""

import asyncio

import pytest

from fastmcp import Client

import laravel_mcp_companion
from laravel_mcp_companion import create_mcp_server


class FakeDocsUpdater:
    """Stands in for DocsUpdater so no test touches the network."""

    def __init__(self, docs_path, version):
        self.docs_path = docs_path
        self.version = version

    def update(self, force=False):
        return False  # "already up to date"


@pytest.fixture
def mcp_server(test_docs_dir, monkeypatch):
    monkeypatch.setattr(laravel_mcp_companion, "DocsUpdater", FakeDocsUpdater)
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
            assert "up to date" in str(result)

    async def test_update_docs_still_works_synchronously(self, mcp_server):
        async with Client(mcp_server) as client:
            res = await client.call_tool("update_laravel_docs", {"version": "12.x"})
            assert "up to date" in res.content[0].text

    async def test_both_update_tools_declare_task_support(self, mcp_server):
        """Both long-running tools advertise execution.taskSupport = optional.

        "optional" is the non-breaking mode: task-aware clients poll, sync
        clients run the tool exactly as before.
        """
        async with Client(mcp_server) as client:
            tools = {t.name: t for t in await client.list_tools()}
            for name in ("update_laravel_docs", "update_external_laravel_docs"):
                execution = getattr(tools[name], "execution", None)
                assert execution is not None, f"{name} should declare task execution"
                assert execution.taskSupport == "optional"

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
            assert "Invalid version" in res.content[0].text
