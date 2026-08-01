"""Tests for section chunking, BM25 indexing and retrieval."""

from pathlib import Path

from doc_search import (
    BM25Index,
    DocIndex,
    MAX_RESIDENT_INDEXES,
    Section,
    chunk_markdown,
    clear_indexes,
    extract_snippet,
    get_index,
    resident_index_count,
)


SAMPLE = """# Queues

Intro paragraph before any section.

<a name="dealing-with-failed-jobs"></a>
## Dealing With Failed Jobs

Jobs that exceed max attempts land in failed_jobs.

## Max Job Attempts

Use the tries property.
"""


def test_chunk_splits_on_h2_headings():
    sections = chunk_markdown(SAMPLE, "queues.md", "13.x")
    headings = [s.heading for s in sections]
    assert "Dealing With Failed Jobs" in headings
    assert "Max Job Attempts" in headings


def test_chunk_captures_anchor_when_present():
    sections = chunk_markdown(SAMPLE, "queues.md", "13.x")
    failed = next(s for s in sections if s.heading == "Dealing With Failed Jobs")
    assert failed.anchor == "dealing-with-failed-jobs"


def test_chunk_leaves_anchor_none_when_absent():
    sections = chunk_markdown(SAMPLE, "queues.md", "13.x")
    attempts = next(s for s in sections if s.heading == "Max Job Attempts")
    assert attempts.anchor is None


def test_chunk_keeps_preamble_before_first_heading():
    sections = chunk_markdown(SAMPLE, "queues.md", "13.x")
    assert any("Intro paragraph" in s.text for s in sections)


def test_chunk_file_with_no_h2_returns_one_section():
    sections = chunk_markdown("# Title\n\nBody only.\n", "solo.md", "13.x")
    assert len(sections) == 1
    assert "Body only." in sections[0].text


def test_chunk_records_provenance():
    sections = chunk_markdown(SAMPLE, "queues.md", "13.x")
    assert all(s.filename == "queues.md" for s in sections)
    assert all(s.version == "13.x" for s in sections)
    assert isinstance(sections[0], Section)



CORPUS = [
    "queue jobs are processed by workers and can fail",
    "failed jobs are stored in the failed_jobs table and can be retried",
    "blade templates render views with directives",
]


def test_index_ranks_the_relevant_document_first():
    idx = BM25Index()
    idx.build(CORPUS)
    ranked = idx.query("retry failed jobs", top_k=3)
    assert ranked, "expected at least one hit"
    assert ranked[0][0] == 1


def test_index_returns_scores_in_descending_order():
    idx = BM25Index()
    idx.build(CORPUS)
    scores = [score for _, score in idx.query("jobs", top_k=3)]
    assert scores == sorted(scores, reverse=True)


def test_index_returns_nothing_for_unknown_terms():
    idx = BM25Index()
    idx.build(CORPUS)
    assert idx.query("kubernetes helm chart", top_k=3) == []


def test_index_handles_empty_corpus():
    idx = BM25Index()
    idx.build([])
    assert idx.query("anything", top_k=3) == []


def test_index_respects_top_k():
    idx = BM25Index()
    idx.build(CORPUS)
    assert len(idx.query("jobs", top_k=1)) <= 1


def test_index_releases_token_lists_after_build():
    """Retaining tokenized documents is the bulk of the memory cost."""
    idx = BM25Index()
    idx.build(CORPUS)
    assert not getattr(idx, "_doc_tokens", None)



LONG = (
    "Preamble line that is not relevant at all.\n"
    + ("filler line\n" * 40)
    + "Jobs that exceed their maximum attempts are inserted into the failed_jobs table.\n"
    + ("more filler\n" * 40)
)


def test_snippet_centres_on_the_query_terms():
    snippet = extract_snippet(LONG, "failed_jobs table", max_chars=200)
    assert "failed_jobs" in snippet


def test_snippet_respects_max_chars():
    snippet = extract_snippet(LONG, "failed_jobs", max_chars=200)
    assert len(snippet) <= 260


def test_snippet_falls_back_to_the_start_when_no_term_matches():
    snippet = extract_snippet(LONG, "kubernetes", max_chars=100)
    assert snippet.startswith("Preamble")


def test_snippet_of_short_text_returns_it_whole():
    assert extract_snippet("short body", "body", max_chars=300) == "short body"


def _sections(version, *bodies):
    out = []
    for i, body in enumerate(bodies):
        out.extend(chunk_markdown(f"## Heading {i}\n\n{body}\n", f"f{i}.md", version))
    return out


def test_docindex_returns_sections_ranked():
    index = DocIndex(_sections("13.x", "failed jobs are retried", "blade templates"))
    hits = index.search("retry failed jobs", top_k=2)
    assert hits
    assert "failed jobs" in hits[0][0].text


def test_docindex_substring_search_finds_exact_symbols():
    index = DocIndex(_sections("13.x", "run queue:retry to requeue", "unrelated"))
    hits = index.substring_search("queue:retry", top_k=2)
    assert hits
    assert "queue:retry" in hits[0][0].text


def test_get_index_builds_once_per_key():
    clear_indexes()
    calls = []

    def loader():
        calls.append(1)
        return _sections("13.x", "queue workers")

    get_index(Path("/unused"), "13.x", loader)
    get_index(Path("/unused"), "13.x", loader)
    assert len(calls) == 1


def test_registry_evicts_beyond_the_cap():
    clear_indexes()
    for n in range(MAX_RESIDENT_INDEXES + 2):
        get_index(Path("/unused"), f"v{n}", lambda: _sections("x", "content"))
    assert resident_index_count() == MAX_RESIDENT_INDEXES


def test_clear_indexes_empties_the_registry():
    get_index(Path("/unused"), "13.x", lambda: _sections("13.x", "content"))
    clear_indexes()
    assert resident_index_count() == 0


def test_clear_caches_also_clears_indexes():
    """Documentation updates call clear_caches; a stale index must not survive."""
    from mcp_tools import clear_caches

    clear_indexes()
    get_index(Path("/unused"), "13.x", lambda: _sections("13.x", "content"))
    assert resident_index_count() == 1

    clear_caches()
    assert resident_index_count() == 0


def test_load_version_sections_reads_real_files(tmp_path):
    from mcp_tools import SUPPORTED_VERSIONS, load_version_sections

    version = SUPPORTED_VERSIONS[-1]
    docs = tmp_path / "docs"
    (docs / version).mkdir(parents=True)
    (docs / version / "queues.md").write_text(
        "# Queues\n\n## Failed Jobs\n\nRetry them with queue:retry.\n"
    )

    sections = load_version_sections(docs, version)

    assert any(s.heading == "Failed Jobs" for s in sections)
    assert all(s.filename == "queues.md" for s in sections)


def test_load_version_sections_skips_escaping_symlinks(tmp_path):
    """Containment behaviour must match the read path."""
    import os

    from mcp_tools import SUPPORTED_VERSIONS, load_version_sections

    version = SUPPORTED_VERSIONS[-1]
    docs = tmp_path / "docs"
    (docs / version).mkdir(parents=True)
    (docs / version / "real.md").write_text("## Real\n\ncontent\n")
    outside = tmp_path / "outside.md"
    outside.write_text("## Secret\n\nCANARY-9021\n")
    os.symlink(outside, docs / version / "escape.md")

    sections = load_version_sections(docs, version)

    assert not any("CANARY-9021" in s.text for s in sections)


def test_load_version_sections_of_missing_version_is_empty(tmp_path):
    from mcp_tools import SUPPORTED_VERSIONS, load_version_sections

    assert load_version_sections(tmp_path, SUPPORTED_VERSIONS[-1]) == []


def test_load_service_sections_keys_by_service(tmp_path):
    from mcp_tools import load_service_sections

    external = tmp_path / "external"
    (external / "forge").mkdir(parents=True)
    (external / "forge" / "intro.md").write_text("## Provisioning\n\nServer setup.\n")

    sections = load_service_sections(external, "forge")

    assert sections
    assert all(s.version == "forge" for s in sections)


def test_snippet_returns_body_text_not_just_the_heading():
    """A snippet that stops at the heading tells the model nothing.

    The line-boundary trim must not collapse the window when the matched term
    sits in the heading itself.
    """
    # A single long paragraph, as Laravel's documentation actually formats them:
    # the only newline before the window ends is the one after the heading.
    section = (
        "## Dealing With Failed Jobs\n\n"
        "Sometimes your queued jobs will fail. Jobs that exceed their configured "
        "attempts are inserted into the failed_jobs table. Retry them with the "
        "queue:retry Artisan command, which pushes the job back onto its original "
        "queue so a worker may attempt it again at the next opportunity.\n"
    )
    snippet = extract_snippet(section, "retry failed queue job", max_chars=300)
    assert "failed_jobs" in snippet or "queue:retry" in snippet, (
        f"snippet carried no body: {snippet!r}"
    )
