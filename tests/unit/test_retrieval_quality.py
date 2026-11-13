"""The retrieval regression this work exists to fix.

Before this change four of these seven questions returned nothing, because the
query was matched as a literal substring. Ranking by raw match count also placed
queues.md 13th of 24 for "queues", behind a file with a single match.
"""

from pathlib import Path

import pytest

from laravel_mcp_companion.mcp_tools import SUPPORTED_VERSIONS
from laravel_mcp_companion.tools import ToolFailure
from laravel_mcp_companion.tools.docs import read_content, read_section
from laravel_mcp_companion.tools.search import search
from laravel_mcp_companion.toon_helpers import toon_encode

VERSION = SUPPORTED_VERSIONS[-1]
DOCS = Path("docs")

QUESTIONS = [
    "how do I validate a file upload",
    "retry failed queue job",
    "send email with attachment",
    "database transactions",
    "rate limiting api routes",
    "eloquent relationships",
    "queue",
]


@pytest.mark.parametrize("question", QUESTIONS)
def test_realistic_questions_return_results(question):
    result = search(DOCS, None, question, version=VERSION, sources=["core"])
    assert result["count"] > 0, f"{question!r} returned nothing"


def test_ranking_prefers_the_relevant_file():
    result = search(DOCS, None, "queue jobs and workers", version=VERSION, sources=["core"])
    assert any("queues.md" in r["file"] for r in result["results"])
    first = result["results"][0]
    assert "queues.md" in first["file"], f"top hit was {first!r}"


def test_search_output_stays_within_budget():
    """A search response must not drift back toward whole-file cost."""
    result = search(DOCS, None, "retry failed queue job", version=VERSION, sources=["core"])
    encoded = toon_encode(result)
    assert len(encoded) < 4800, f"{len(encoded)} chars exceeds the ~1,200 token budget"


def test_results_carry_a_section_for_drill_down():
    result = search(DOCS, None, "retry failed queue job", version=VERSION, sources=["core"])
    assert all(r["section"] for r in result["results"])


def test_exact_symbol_lookup_falls_back_to_substring():
    result = search(DOCS, None, "queue:retry", version=VERSION, sources=["core"])
    assert result["count"] > 0


def test_empty_query_is_rejected():
    with pytest.raises(ToolFailure) as raised:
        search(DOCS, None, "   ", version=VERSION)
    assert raised.value.code == "invalid_argument"


def test_invalid_version_is_rejected():
    with pytest.raises(ToolFailure) as raised:
        search(DOCS, None, "queue", version="..")
    assert raised.value.code == "unknown_version"


def test_read_section_by_anchor(tmp_path):
    docs = tmp_path / "docs"
    (docs / VERSION).mkdir(parents=True)
    (docs / VERSION / "queues.md").write_text(
        '# Queues\n\n<a name="failed-jobs"></a>\n## Failed Jobs\n\n'
        "Retry with queue:retry.\n\n## Other\n\nUnrelated.\n"
    )

    result = read_section(docs, "queues.md", "failed-jobs", VERSION).text

    assert "queue:retry" in result
    assert "Unrelated" not in result


def test_read_section_by_heading_case_insensitively(tmp_path):
    docs = tmp_path / "docs"
    (docs / VERSION).mkdir(parents=True)
    (docs / VERSION / "queues.md").write_text("## Failed Jobs\n\nRetry it.\n")

    result = read_section(docs, "queues.md", "failed jobs", VERSION).text

    assert "Retry it." in result


def test_unknown_section_lists_available_ones(tmp_path):
    docs = tmp_path / "docs"
    (docs / VERSION).mkdir(parents=True)
    (docs / VERSION / "queues.md").write_text(
        '<a name="failed-jobs"></a>\n## Failed Jobs\n\nBody.\n'
    )

    with pytest.raises(ToolFailure) as raised:
        read_section(docs, "queues.md", "nope", VERSION)

    assert raised.value.code == "not_found"
    assert "failed-jobs" in raised.value.details["available_sections"]


def test_read_section_rejects_traversal(tmp_path):
    docs = tmp_path / "docs"
    (docs / VERSION).mkdir(parents=True)
    (tmp_path / "secret.md").write_text("## Secret\n\nCANARY-5150\n")

    with pytest.raises(ToolFailure) as raised:
        read_section(docs, "../../secret.md", "secret", VERSION)

    assert raised.value.code == "access_denied"
    assert "CANARY-5150" not in str(raised.value.payload())


def test_read_section_rejects_invalid_version(tmp_path):
    with pytest.raises(ToolFailure) as raised:
        read_section(tmp_path, "queues.md", "failed-jobs", "..")

    assert raised.value.code == "unknown_version"


def test_read_section_costs_far_less_than_the_whole_file():
    """The point of the exercise: a section instead of 34,000 tokens."""

    whole = read_content(DOCS, "queues.md", VERSION).text
    section = read_section(DOCS, "queues.md", "dealing-with-failed-jobs", VERSION).text

    assert len(section) < len(whole) / 5, (
        f"section {len(section)} vs whole {len(whole)} chars"
    )


@pytest.mark.asyncio
async def test_section_reader_is_exposed_and_context_search_retired(tmp_path):
    from fastmcp import Client

    from laravel_mcp_companion.server import create_mcp_server

    docs = tmp_path / "docs"
    (docs / VERSION).mkdir(parents=True)
    (docs / VERSION / "queues.md").write_text(
        '<a name="failed-jobs"></a>\n## Failed Jobs\n\nRetry with queue:retry.\n'
    )

    server = create_mcp_server("T", docs, VERSION, transform_mode=None)
    async with Client(server) as client:
        names = [t.name for t in await client.list_tools()]
        assert "read_laravel_doc_section" in names
        assert "search_laravel_docs_with_context" not in names

        result = await client.call_tool(
            "read_laravel_doc_section",
            {"filename": "queues.md", "section": "failed-jobs", "version": VERSION},
        )
        assert "queue:retry" in result.content[0].text
