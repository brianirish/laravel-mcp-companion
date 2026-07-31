"""The retrieval regression this work exists to fix.

Before this change four of these seven questions returned nothing, because the
query was matched as a literal substring. Ranking by raw match count also placed
queues.md 13th of 24 for "queues", behind a file with a single match.
"""

from pathlib import Path

import pytest

from mcp_tools import SUPPORTED_VERSIONS, search_laravel_docs_impl

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
    result = search_laravel_docs_impl(
        DOCS, question, version=VERSION, include_external=False
    )
    assert "No results" not in result, f"{question!r} returned nothing"


def test_ranking_prefers_the_relevant_file():
    result = search_laravel_docs_impl(
        DOCS, "queue jobs and workers", version=VERSION, include_external=False
    )
    assert "queues.md" in result
    first = [ln for ln in result.splitlines() if ".md" in ln][0]
    assert "queues.md" in first, f"top hit was {first!r}"


def test_search_output_stays_within_budget():
    """A search response must not drift back toward whole-file cost."""
    result = search_laravel_docs_impl(
        DOCS, "retry failed queue job", version=VERSION, include_external=False
    )
    assert len(result) < 4800, f"{len(result)} chars exceeds the ~1,200 token budget"


def test_results_carry_an_anchor_for_drill_down():
    result = search_laravel_docs_impl(
        DOCS, "retry failed queue job", version=VERSION, include_external=False
    )
    assert "anchor" in result


def test_exact_symbol_lookup_falls_back_to_substring():
    result = search_laravel_docs_impl(
        DOCS, "queue:retry", version=VERSION, include_external=False
    )
    assert "No results" not in result


def test_empty_query_is_rejected():
    assert "cannot be empty" in search_laravel_docs_impl(DOCS, "   ", version=VERSION)


def test_invalid_version_is_rejected():
    assert "Invalid version" in search_laravel_docs_impl(DOCS, "queue", version="..")


def test_read_section_by_anchor(tmp_path):
    from mcp_tools import read_laravel_doc_section_impl

    docs = tmp_path / "docs"
    (docs / VERSION).mkdir(parents=True)
    (docs / VERSION / "queues.md").write_text(
        '# Queues\n\n<a name="failed-jobs"></a>\n## Failed Jobs\n\n'
        "Retry with queue:retry.\n\n## Other\n\nUnrelated.\n"
    )

    result = read_laravel_doc_section_impl(docs, "queues.md", "failed-jobs", VERSION)

    assert "queue:retry" in result
    assert "Unrelated" not in result


def test_read_section_by_heading_case_insensitively(tmp_path):
    from mcp_tools import read_laravel_doc_section_impl

    docs = tmp_path / "docs"
    (docs / VERSION).mkdir(parents=True)
    (docs / VERSION / "queues.md").write_text("## Failed Jobs\n\nRetry it.\n")

    result = read_laravel_doc_section_impl(docs, "queues.md", "failed jobs", VERSION)

    assert "Retry it." in result


def test_unknown_section_lists_available_ones(tmp_path):
    from mcp_tools import read_laravel_doc_section_impl

    docs = tmp_path / "docs"
    (docs / VERSION).mkdir(parents=True)
    (docs / VERSION / "queues.md").write_text(
        '<a name="failed-jobs"></a>\n## Failed Jobs\n\nBody.\n'
    )

    result = read_laravel_doc_section_impl(docs, "queues.md", "nope", VERSION)

    assert "failed-jobs" in result


def test_read_section_rejects_traversal(tmp_path):
    from mcp_tools import read_laravel_doc_section_impl

    docs = tmp_path / "docs"
    (docs / VERSION).mkdir(parents=True)
    (tmp_path / "secret.md").write_text("## Secret\n\nCANARY-5150\n")

    result = read_laravel_doc_section_impl(docs, "../../secret.md", "secret", VERSION)

    assert "CANARY-5150" not in result


def test_read_section_rejects_invalid_version(tmp_path):
    from mcp_tools import read_laravel_doc_section_impl

    result = read_laravel_doc_section_impl(tmp_path, "queues.md", "failed-jobs", "..")

    assert "Invalid version" in result


def test_read_section_costs_far_less_than_the_whole_file():
    """The point of the exercise: a section instead of 34,000 tokens."""
    from mcp_tools import read_laravel_doc_content_impl, read_laravel_doc_section_impl

    whole = read_laravel_doc_content_impl(DOCS, "queues.md", VERSION)
    section = read_laravel_doc_section_impl(
        DOCS, "queues.md", "dealing-with-failed-jobs", VERSION
    )

    assert "Access denied" not in section
    assert len(section) < len(whole) / 5, (
        f"section {len(section)} vs whole {len(whole)} chars"
    )
