"""Tests for section chunking, BM25 indexing and retrieval."""

from doc_search import Section, chunk_markdown

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


from doc_search import BM25Index

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
