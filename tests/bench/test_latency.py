"""Latency benchmarks over the real documentation corpus.

Run: uv run pytest -m bench --no-cov -s -q

Uses the repo's own docs/ tree (present after any docs sync) through the
in-memory client — no subprocess, no network. Assertions cover setup
correctness only; timing is reported against the v1.0.0 sub-100ms target.
"""

import statistics
import time
from pathlib import Path

import pytest

from fastmcp import Client

from laravel_mcp_companion import create_mcp_server

pytestmark = pytest.mark.bench

REPO_DOCS = Path(__file__).resolve().parents[2] / "docs"
TARGET_MS = 100.0

QUERIES = [
    "routing",
    "queue retry failed jobs",
    "eloquent relationships",
    "middleware",
    "validation rules",
    "cache tags",
    "broadcasting events",
    "sanctum api tokens",
    "blade components",
    "queue:retry",
    # Cross-corpus: exercises the unified fan-out over packages/services too.
    "spatie permission roles",
    "livewire wire:model",
]


@pytest.fixture(scope="module")
def corpus_server():
    if not (REPO_DOCS / "12.x").is_dir():
        pytest.skip("real corpus absent (docs/12.x); run a docs sync first")
    return create_mcp_server("BenchServer", REPO_DOCS, "12.x", transform_mode=None)


def report(operation: str, samples_ms: list) -> None:
    p50 = statistics.median(samples_ms)
    p95 = statistics.quantiles(samples_ms, n=20)[-1] if len(samples_ms) >= 20 else max(samples_ms)
    verdict = "within" if p95 <= TARGET_MS else "OVER"
    print(
        f"\n  {operation:32s} n={len(samples_ms):3d}  "
        f"p50={p50:7.1f}ms  p95={p95:7.1f}ms  max={max(samples_ms):7.1f}ms  "
        f"[{verdict} {TARGET_MS:.0f}ms target]"
    )


class TestSearchLatency:
    async def test_cold_and_warm_search(self, corpus_server):
        async with Client(corpus_server) as client:
            # Cold: first search pays the BM25 index build.
            started = time.perf_counter()
            first = await client.call_tool(
                "search_laravel_docs", {"query": QUERIES[0]}
            )
            cold_ms = (time.perf_counter() - started) * 1000
            assert first.structured_content.get("results"), "cold search returned nothing"
            print(f"\n  {'search (cold, index build)':32s} n=  1  once={cold_ms:7.1f}ms")

            samples = []
            for i in range(30):
                query = QUERIES[i % len(QUERIES)]
                started = time.perf_counter()
                result = await client.call_tool(
                    "search_laravel_docs", {"query": query}
                )
                samples.append((time.perf_counter() - started) * 1000)
                assert result.structured_content is not None
            report("search (warm)", samples)


class TestReadLatency:
    async def test_section_read(self, corpus_server):
        async with Client(corpus_server) as client:
            hit = (await client.call_tool(
                "search_laravel_docs", {"query": "queue retry failed jobs"}
            )).structured_content["results"][0]
            filename = hit["file"].split("/", 1)[1]
            section = hit["anchor"] or hit["heading"]

            samples = []
            for _ in range(30):
                started = time.perf_counter()
                result = await client.call_tool(
                    "read_laravel_doc_section", {"filename": filename, "section": section}
                )
                samples.append((time.perf_counter() - started) * 1000)
                assert not result.is_error
            report("read_laravel_doc_section", samples)


class TestInfoLatency:
    async def test_docs_info(self, corpus_server):
        async with Client(corpus_server) as client:
            samples = []
            for _ in range(30):
                started = time.perf_counter()
                result = await client.call_tool("laravel_docs_info", {"version": "12.x"})
                samples.append((time.perf_counter() - started) * 1000)
                assert result.structured_content.get("version") == "12.x"
            report("laravel_docs_info", samples)
