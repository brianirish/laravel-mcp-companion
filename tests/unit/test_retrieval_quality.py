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
