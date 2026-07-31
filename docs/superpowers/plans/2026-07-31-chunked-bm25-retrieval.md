# Chunked BM25 Retrieval Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace substring documentation search with BM25 ranking over heading-level sections, and add a tool to read a single section, so a natural-language question returns a ranked snippet for hundreds of tokens instead of nothing or a whole 34,000-token file.

**Architecture:** A new `doc_search.py` module owns chunking, a ~40-line Okapi BM25 index, and a lazy per-version index registry capped at two resident indexes. `mcp_tools.py` delegates to it; the tool layer in `laravel_mcp_companion.py` keeps the `search_laravel_docs` name with a new result shape, adds `read_laravel_doc_section`, and drops the redundant `search_laravel_docs_with_context`.

**Tech Stack:** Python 3.12, pytest, FastMCP 3.4.5, TOON output via `toon_helpers`.

## Global Constraints

- Python >= 3.12 (`pyproject.toml`); CI installs 3.12 explicitly.
- Chunk on `##` headings only. Finer granularity measured worse (4/4 correct at `##`, 2/4 at `###` and at anchors).
- BM25 parameters: k1=1.5, b=0.75.
- Own the BM25 index. Do not import `fastmcp.server.transforms.search.bm25._BM25Index` — it is a private class and retains token lists after build.
- At most 2 indexes resident, LRU-evicted.
- Index registry must be cleared by the existing `mcp_tools.clear_caches()`.
- All file reads go through `mcp_tools.get_file_content_cached` and enumeration through `mcp_tools.list_contained_markdown`, preserving containment and O_NOFOLLOW behaviour. Do not open files directly.
- Version arguments validate via `mcp_tools.validate_version`; path joins validate via `mcp_tools.resolve_contained_path`.
- Errors from unreadable directories propagate; they are not converted to "no files found".
- Run tests with `.venv/bin/python -m pytest`. Ruff and mypy must stay clean.
- Commit with `git lc` (wrapper handles the repo's commit-time policy), never plain `git commit`.

---

### Task 1: Section chunking

**Files:**
- Create: `doc_search.py`
- Test: `tests/unit/test_doc_search.py`

**Interfaces:**
- Consumes: nothing.
- Produces: `Section` dataclass with fields `version: str`, `filename: str`, `anchor: str | None`, `heading: str`, `text: str`; and `chunk_markdown(text: str, filename: str, version: str) -> list[Section]`.

- [ ] **Step 1: Write the failing test**

```python
# tests/unit/test_doc_search.py
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
```

- [ ] **Step 2: Run test to verify it fails**

Run: `.venv/bin/python -m pytest tests/unit/test_doc_search.py -q --no-cov`
Expected: FAIL with `ModuleNotFoundError: No module named 'doc_search'`

- [ ] **Step 3: Write minimal implementation**

```python
# doc_search.py
"""Section-level chunking, BM25 indexing and retrieval for Laravel documentation.

Kept separate from mcp_tools so that chunking and scoring can be tested without
the MCP tool layer, and so mcp_tools does not grow further.
"""

import re
from dataclasses import dataclass
from typing import Optional

_ANCHOR = re.compile(r'<a\s+name="([^"]+)"\s*>')
_H2_SPLIT = re.compile(r"\n(?=##\s)")


@dataclass(frozen=True)
class Section:
    """One ## section of a documentation file."""

    version: str
    filename: str
    anchor: Optional[str]
    heading: str
    text: str


def chunk_markdown(text: str, filename: str, version: str) -> list[Section]:
    """Split a markdown document into ## sections.

    Chunking at ## was measured as the most robust retrieval unit: finer
    granularity produced sharper hits on some queries but regressed on others,
    because short chunks give BM25 too few terms to discriminate.

    The preamble before the first ## is kept as its own section so that content
    at the top of a file is still reachable.
    """
    sections: list[Section] = []
    for part in _H2_SPLIT.split(text):
        if not part.strip():
            continue

        heading_match = re.match(r"##\s+(.+)", part.lstrip())
        heading = heading_match.group(1).strip() if heading_match else ""
        if not heading:
            title = re.match(r"#\s+(.+)", part.lstrip())
            heading = title.group(1).strip() if title else filename

        anchor_match = _ANCHOR.search(part)
        anchor = anchor_match.group(1) if anchor_match else None

        sections.append(
            Section(
                version=version,
                filename=filename,
                anchor=anchor,
                heading=heading,
                text=part,
            )
        )
    return sections
```

Note: the anchor for a section usually sits on the line *before* its `##`, so after
splitting on `\n(?=##\s)` the anchor lands at the end of the *previous* chunk. Fix
this by scanning for a trailing anchor on the preceding part and attaching it to the
next section. Implement that in Step 3 as follows, replacing the loop body above:

```python
def chunk_markdown(text: str, filename: str, version: str) -> list[Section]:
    parts = [p for p in _H2_SPLIT.split(text) if p.strip()]
    sections: list[Section] = []
    carried_anchor: Optional[str] = None

    for part in parts:
        heading_match = re.match(r"##\s+(.+)", part.lstrip())
        if heading_match:
            heading = heading_match.group(1).strip()
        else:
            title = re.match(r"#\s+(.+)", part.lstrip())
            heading = title.group(1).strip() if title else filename

        own_anchor = _ANCHOR.search(part)
        anchor = carried_anchor or (own_anchor.group(1) if own_anchor else None)

        trailing = list(_ANCHOR.finditer(part))
        carried_anchor = None
        if trailing:
            last = trailing[-1]
            if not part[last.end():].strip():
                carried_anchor = last.group(1)

        sections.append(
            Section(version=version, filename=filename, anchor=anchor,
                    heading=heading, text=part)
        )
    return sections
```

- [ ] **Step 4: Run test to verify it passes**

Run: `.venv/bin/python -m pytest tests/unit/test_doc_search.py -q --no-cov`
Expected: PASS, 6 tests

- [ ] **Step 5: Verify against real documentation**

Run:

```bash
.venv/bin/python -c "
from pathlib import Path
from doc_search import chunk_markdown
t = Path('docs/13.x/queues.md').read_text()
s = chunk_markdown(t, 'queues.md', '13.x')
print(len(s), 'sections')
print([x.heading for x in s][:4])
print('anchored:', sum(1 for x in s if x.anchor), '/', len(s))
"
```

Expected: about 14 sections, headings that read like real headings, and most sections carrying an anchor.

- [ ] **Step 6: Commit**

```bash
git add doc_search.py tests/unit/test_doc_search.py
git lc -m "Add section-level markdown chunking for documentation search"
```

---

### Task 2: BM25 index

**Files:**
- Modify: `doc_search.py`
- Test: `tests/unit/test_doc_search.py`

**Interfaces:**
- Consumes: nothing from Task 1.
- Produces: `BM25Index` with `build(documents: list[str]) -> None` and `query(text: str, top_k: int) -> list[tuple[int, float]]` returning `(document_index, score)` pairs sorted by descending score, excluding zero scores.

- [ ] **Step 1: Write the failing test**

```python
# append to tests/unit/test_doc_search.py
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
    assert not hasattr(idx, "_doc_tokens") or not idx._doc_tokens
```

- [ ] **Step 2: Run test to verify it fails**

Run: `.venv/bin/python -m pytest tests/unit/test_doc_search.py -q --no-cov -k index`
Expected: FAIL with `ImportError: cannot import name 'BM25Index'`

- [ ] **Step 3: Write minimal implementation**

```python
# add to doc_search.py
import math

_TOKEN = re.compile(r"[a-z0-9]+")

BM25_K1 = 1.5
BM25_B = 0.75


def tokenize(text: str) -> list[str]:
    return _TOKEN.findall(text.lower())


class BM25Index:
    """Okapi BM25 over a fixed document set.

    Owned rather than imported. fastmcp ships an equivalent, but it is a private
    class in a fast-moving dependency and retains its tokenized documents after
    building, which is most of the memory cost.
    """

    def __init__(self, k1: float = BM25_K1, b: float = BM25_B) -> None:
        self.k1 = k1
        self.b = b
        self._n = 0
        self._avg_dl = 0.0
        self._lengths: list[int] = []
        self._df: dict[str, int] = {}
        self._tf: list[dict[str, int]] = []

    def build(self, documents: list[str]) -> None:
        self._n = len(documents)
        self._lengths = []
        self._df = {}
        self._tf = []

        for doc in documents:
            tokens = tokenize(doc)
            self._lengths.append(len(tokens))
            tf: dict[str, int] = {}
            for token in tokens:
                tf[token] = tf.get(token, 0) + 1
            self._tf.append(tf)
            for token in tf:
                self._df[token] = self._df.get(token, 0) + 1
            # tokens goes out of scope here; only counts are retained

        self._avg_dl = (sum(self._lengths) / self._n) if self._n else 0.0

    def query(self, text: str, top_k: int) -> list[tuple[int, float]]:
        terms = tokenize(text)
        if not terms or not self._n:
            return []

        scores = [0.0] * self._n
        for term in terms:
            df = self._df.get(term)
            if not df:
                continue
            idf = math.log((self._n - df + 0.5) / (df + 0.5) + 1.0)
            for i, tf_map in enumerate(self._tf):
                tf = tf_map.get(term, 0)
                if not tf:
                    continue
                dl = self._lengths[i]
                denom = tf + self.k1 * (1 - self.b + self.b * dl / self._avg_dl)
                scores[i] += idf * tf * (self.k1 + 1) / denom

        ranked = sorted(range(self._n), key=lambda i: scores[i], reverse=True)
        return [(i, scores[i]) for i in ranked[:top_k] if scores[i] > 0]
```

- [ ] **Step 4: Run test to verify it passes**

Run: `.venv/bin/python -m pytest tests/unit/test_doc_search.py -q --no-cov`
Expected: PASS, 12 tests

- [ ] **Step 5: Commit**

```bash
git add doc_search.py tests/unit/test_doc_search.py
git lc -m "Add owned BM25 index for documentation retrieval"
```

---

### Task 3: Snippet extraction

**Files:**
- Modify: `doc_search.py`
- Test: `tests/unit/test_doc_search.py`

**Interfaces:**
- Consumes: `tokenize` from Task 2.
- Produces: `extract_snippet(text: str, query: str, max_chars: int = 300) -> str`.

- [ ] **Step 1: Write the failing test**

```python
# append to tests/unit/test_doc_search.py
from doc_search import extract_snippet

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
    assert len(snippet) <= 260  # allows for ellipsis markers


def test_snippet_falls_back_to_the_start_when_no_term_matches():
    snippet = extract_snippet(LONG, "kubernetes", max_chars=100)
    assert snippet.startswith("Preamble")


def test_snippet_of_short_text_returns_it_whole():
    assert extract_snippet("short body", "body", max_chars=300) == "short body"
```

- [ ] **Step 2: Run test to verify it fails**

Run: `.venv/bin/python -m pytest tests/unit/test_doc_search.py -q --no-cov -k snippet`
Expected: FAIL with `ImportError: cannot import name 'extract_snippet'`

- [ ] **Step 3: Write minimal implementation**

```python
# add to doc_search.py
def extract_snippet(text: str, query: str, max_chars: int = 300) -> str:
    """Return a readable window of `text` around the best query-term match.

    Aligns to line boundaries so the result reads as prose rather than a
    mid-word slice.
    """
    body = text.strip()
    if len(body) <= max_chars:
        return body

    lowered = body.lower()
    position = -1
    for term in sorted(tokenize(query), key=len, reverse=True):
        position = lowered.find(term)
        if position != -1:
            break

    if position == -1:
        window = body[:max_chars]
        return window.rsplit("\n", 1)[0].strip() or window.strip()

    start = max(0, position - max_chars // 2)
    end = min(len(body), start + max_chars)

    if start > 0:
        newline = body.find("\n", start)
        if newline != -1 and newline < position:
            start = newline + 1
    if end < len(body):
        newline = body.rfind("\n", start, end)
        if newline != -1 and newline > position:
            end = newline

    snippet = body[start:end].strip()
    if start > 0:
        snippet = "..." + snippet
    if end < len(body):
        snippet = snippet + "..."
    return snippet
```

- [ ] **Step 4: Run test to verify it passes**

Run: `.venv/bin/python -m pytest tests/unit/test_doc_search.py -q --no-cov`
Expected: PASS, 16 tests

- [ ] **Step 5: Commit**

```bash
git add doc_search.py tests/unit/test_doc_search.py
git lc -m "Add query-centred snippet extraction"
```

---

### Task 4: Lazy per-version index registry with LRU cap

**Files:**
- Modify: `doc_search.py`
- Test: `tests/unit/test_doc_search.py`

**Interfaces:**
- Consumes: `Section`, `chunk_markdown` (Task 1), `BM25Index` (Task 2).
- Produces:
  - `MAX_RESIDENT_INDEXES: int = 2`
  - `DocIndex` with `sections: list[Section]` and `search(query: str, top_k: int) -> list[tuple[Section, float]]`
  - `get_index(docs_path: Path, key: str, loader) -> DocIndex` where `loader() -> list[Section]`
  - `clear_indexes() -> None`
  - `resident_index_count() -> int`

- [ ] **Step 1: Write the failing test**

```python
# append to tests/unit/test_doc_search.py
from pathlib import Path

from doc_search import (
    DocIndex,
    MAX_RESIDENT_INDEXES,
    clear_indexes,
    get_index,
    resident_index_count,
)


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
```

- [ ] **Step 2: Run test to verify it fails**

Run: `.venv/bin/python -m pytest tests/unit/test_doc_search.py -q --no-cov -k "index or registry"`
Expected: FAIL with `ImportError: cannot import name 'DocIndex'`

- [ ] **Step 3: Write minimal implementation**

```python
# add to doc_search.py
import threading
from collections import OrderedDict
from pathlib import Path
from typing import Callable

MAX_RESIDENT_INDEXES = 2

_registry: "OrderedDict[str, DocIndex]" = OrderedDict()
_registry_lock = threading.Lock()


class DocIndex:
    """A BM25 index over the sections of one version or service."""

    def __init__(self, sections: list[Section]) -> None:
        self.sections = sections
        self._index = BM25Index()
        self._index.build([s.text for s in sections])

    def search(self, query: str, top_k: int) -> list[tuple[Section, float]]:
        return [(self.sections[i], score) for i, score in self._index.query(query, top_k)]

    def substring_search(self, query: str, top_k: int) -> list[tuple[Section, float]]:
        """Literal fallback, preserving exact-symbol lookup such as `mimes:pdf`."""
        needle = query.lower()
        hits = [
            (section, float(section.text.lower().count(needle)))
            for section in self.sections
            if needle in section.text.lower()
        ]
        hits.sort(key=lambda pair: pair[1], reverse=True)
        return hits[:top_k]


def get_index(docs_path: Path, key: str, loader: Callable[[], list[Section]]) -> DocIndex:
    """Return the index for `key`, building it on first use.

    Indexes are ~13 MB each, so only MAX_RESIDENT_INDEXES are kept; the least
    recently used is dropped. Rebuilding costs about 100 ms.
    """
    with _registry_lock:
        existing = _registry.get(key)
        if existing is not None:
            _registry.move_to_end(key)
            return existing

    index = DocIndex(loader())

    with _registry_lock:
        _registry[key] = index
        _registry.move_to_end(key)
        while len(_registry) > MAX_RESIDENT_INDEXES:
            _registry.popitem(last=False)
    return index


def clear_indexes() -> None:
    with _registry_lock:
        _registry.clear()


def resident_index_count() -> int:
    with _registry_lock:
        return len(_registry)
```

- [ ] **Step 4: Run test to verify it passes**

Run: `.venv/bin/python -m pytest tests/unit/test_doc_search.py -q --no-cov`
Expected: PASS, 20 tests

- [ ] **Step 5: Commit**

```bash
git add doc_search.py tests/unit/test_doc_search.py
git lc -m "Add lazy per-version index registry with LRU cap"
```

---

### Task 5: Wire the registry into cache invalidation

**Files:**
- Modify: `mcp_tools.py` (the `clear_caches` function)
- Test: `tests/unit/test_doc_search.py`

**Interfaces:**
- Consumes: `clear_indexes`, `resident_index_count` (Task 4).
- Produces: nothing new; `mcp_tools.clear_caches()` additionally clears the index registry.

- [ ] **Step 1: Write the failing test**

```python
# append to tests/unit/test_doc_search.py
def test_clear_caches_also_clears_indexes():
    """Documentation updates call clear_caches; a stale index must not survive."""
    from mcp_tools import clear_caches

    get_index(Path("/unused"), "13.x", lambda: _sections("13.x", "content"))
    assert resident_index_count() == 1

    clear_caches()
    assert resident_index_count() == 0
```

- [ ] **Step 2: Run test to verify it fails**

Run: `.venv/bin/python -m pytest tests/unit/test_doc_search.py -q --no-cov -k clear_caches`
Expected: FAIL, `assert 1 == 0`

- [ ] **Step 3: Write minimal implementation**

Find `def clear_caches` in `mcp_tools.py` and add the index clearing to it:

```python
def clear_caches() -> None:
    """Clear file, search result, and documentation index caches."""
    from doc_search import clear_indexes

    with _cache_lock:
        _file_content_cache.clear()
        _search_result_cache.clear()
    clear_indexes()
    logger.info("Caches cleared")
```

The import is function-local to avoid a circular import: `doc_search` does not
import `mcp_tools`, but Task 6 makes `mcp_tools` import `doc_search`.

- [ ] **Step 4: Run test to verify it passes**

Run: `.venv/bin/python -m pytest tests/unit/test_doc_search.py -q --no-cov`
Expected: PASS, 21 tests

- [ ] **Step 5: Commit**

```bash
git add mcp_tools.py tests/unit/test_doc_search.py
git lc -m "Clear documentation indexes when caches are cleared"
```

---

### Task 6: Section loading from the documentation tree

**Files:**
- Modify: `mcp_tools.py`
- Test: `tests/unit/test_doc_search.py`

**Interfaces:**
- Consumes: `Section`, `chunk_markdown` (Task 1); existing `list_contained_markdown` and `get_file_content_cached`.
- Produces: `mcp_tools.load_version_sections(docs_path: Path, version: str) -> list[Section]` and `mcp_tools.load_service_sections(external_dir: Path, service: str) -> list[Section]`.

- [ ] **Step 1: Write the failing test**

```python
# append to tests/unit/test_doc_search.py
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
```

- [ ] **Step 2: Run test to verify it fails**

Run: `.venv/bin/python -m pytest tests/unit/test_doc_search.py -q --no-cov -k load_`
Expected: FAIL with `ImportError: cannot import name 'load_version_sections'`

- [ ] **Step 3: Write minimal implementation**

```python
# add to mcp_tools.py, after list_contained_markdown
from doc_search import Section, chunk_markdown


def load_version_sections(docs_path: Path, version: str) -> list[Section]:
    """Chunk every contained markdown file of a version into sections.

    Enumeration goes through list_contained_markdown and reads through
    get_file_content_cached, so containment and the refusal to follow symlinks
    at open time both carry over unchanged.
    """
    version_path = Path(docs_path) / version
    if not version_path.is_dir():
        return []

    sections: list[Section] = []
    for name, path in list_contained_markdown(version_path):
        content = get_file_content_cached(str(path))
        if content.startswith("Error") or content.startswith("File not found"):
            continue
        sections.extend(chunk_markdown(content, name, version))
    return sections


def load_service_sections(external_dir: Path, service: str) -> list[Section]:
    """Chunk an external service's documentation, keyed by service name."""
    service_path = Path(external_dir) / service
    if not service_path.is_dir():
        return []

    sections: list[Section] = []
    for name, path in list_contained_markdown(service_path):
        content = get_file_content_cached(str(path))
        if content.startswith("Error") or content.startswith("File not found"):
            continue
        sections.extend(chunk_markdown(content, name, service))
    return sections
```

- [ ] **Step 4: Run test to verify it passes**

Run: `.venv/bin/python -m pytest tests/unit/test_doc_search.py -q --no-cov`
Expected: PASS, 24 tests

- [ ] **Step 5: Commit**

```bash
git add mcp_tools.py tests/unit/test_doc_search.py
git lc -m "Load documentation sections through the contained enumeration path"
```

---

### Task 7: Replace search_laravel_docs_impl with ranked retrieval

**Files:**
- Modify: `mcp_tools.py` (replace the body of `search_laravel_docs_impl`)
- Test: `tests/unit/test_retrieval_quality.py`

**Interfaces:**
- Consumes: `load_version_sections`, `load_service_sections` (Task 6); `get_index` (Task 4); `extract_snippet` (Task 3); existing `validate_version`, `resolve_search_versions`, `toon_encode`, `format_error`.
- Produces: `search_laravel_docs_impl(docs_path, query, version=None, include_external=True, external_dir=None, runtime_version=None, all_versions=False, limit=5) -> str`.

- [ ] **Step 1: Write the failing test**

```python
# tests/unit/test_retrieval_quality.py
"""The retrieval regression this work exists to fix.

Before: four of these seven questions returned nothing, because search matched
the query as a literal substring.
"""

import pytest

from mcp_tools import SUPPORTED_VERSIONS, search_laravel_docs_impl

VERSION = SUPPORTED_VERSIONS[-1]
DOCS = "docs"

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
    from pathlib import Path

    result = search_laravel_docs_impl(
        Path(DOCS), question, version=VERSION, include_external=False
    )
    assert "No results" not in result, f"{question!r} returned nothing"


def test_ranking_prefers_the_relevant_file():
    """queues.md ranked 13th of 24 for 'queues' under match-count ranking."""
    from pathlib import Path

    result = search_laravel_docs_impl(
        Path(DOCS), "queue jobs and workers", version=VERSION, include_external=False
    )
    assert "queues.md" in result
    first_line = [ln for ln in result.splitlines() if ".md" in ln][0]
    assert "queues.md" in first_line


def test_search_output_stays_within_budget():
    """A search response must not drift back toward whole-file cost."""
    from pathlib import Path

    result = search_laravel_docs_impl(
        Path(DOCS), "retry failed queue job", version=VERSION, include_external=False
    )
    assert len(result) < 4800, f"{len(result)} chars is over the ~1,200 token budget"


def test_exact_symbol_lookup_falls_back_to_substring():
    from pathlib import Path

    result = search_laravel_docs_impl(
        Path(DOCS), "queue:retry", version=VERSION, include_external=False
    )
    assert "No results" not in result
```

- [ ] **Step 2: Run test to verify it fails**

Run: `.venv/bin/python -m pytest tests/unit/test_retrieval_quality.py -q --no-cov`
Expected: FAIL — four of the seven parametrized cases assert "returned nothing", and the budget test fails.

- [ ] **Step 3: Write minimal implementation**

Replace the whole body of `search_laravel_docs_impl` in `mcp_tools.py`:

```python
def search_laravel_docs_impl(
    docs_path: Path,
    query: str,
    version: Optional[str] = None,
    include_external: bool = True,
    external_dir: Optional[Path] = None,
    runtime_version: Optional[str] = None,
    all_versions: bool = False,
    limit: int = 5,
) -> str:
    """Search documentation, returning ranked sections with snippets.

    Ranked by BM25 over ## sections rather than by literal substring count, so a
    multi-word question matches and long files no longer outrank relevant ones.
    """
    from doc_search import extract_snippet, get_index

    version_error = validate_version(version)
    if version_error:
        return version_error

    if not query.strip():
        return format_error("Search query cannot be empty")

    search_versions = resolve_search_versions(version, runtime_version, all_versions)

    cache_key = f"search:{query}:{','.join(search_versions)}:{include_external}:{limit}"
    with _cache_lock:
        if cache_key in _search_result_cache:
            return _search_result_cache[cache_key]

    hits: List[tuple] = []
    for candidate in search_versions:
        index = get_index(
            docs_path, f"version:{candidate}",
            lambda c=candidate: load_version_sections(docs_path, c),
        )
        found = index.search(query, limit) or index.substring_search(query, limit)
        hits.extend(found)

    if include_external and external_dir and Path(external_dir).is_dir():
        for service_dir in sorted(Path(external_dir).iterdir()):
            if not service_dir.is_dir():
                continue
            index = get_index(
                docs_path, f"service:{service_dir.name}",
                lambda s=service_dir.name: load_service_sections(external_dir, s),
            )
            found = index.search(query, limit) or index.substring_search(query, limit)
            hits.extend(found)

    hits.sort(key=lambda pair: pair[1], reverse=True)
    hits = hits[:limit]

    if not hits:
        result = format_error(
            f"No results found for '{query}'",
            {"scope": ", ".join(search_versions)},
        )
    else:
        result = toon_encode({
            "query": query,
            "scope": ", ".join(search_versions),
            "results": [
                {
                    "file": f"{section.version}/{section.filename}",
                    "anchor": section.anchor or "",
                    "heading": section.heading,
                    "score": round(score, 2),
                    "snippet": extract_snippet(section.text, query),
                }
                for section, score in hits
            ],
        })

    with _cache_lock:
        _search_result_cache[cache_key] = result
        if len(_search_result_cache) > _SEARCH_CACHE_MAX_ENTRIES:
            for key in list(_search_result_cache.keys())[:_SEARCH_CACHE_EVICT_COUNT]:
                del _search_result_cache[key]

    return result
```

- [ ] **Step 4: Run test to verify it passes**

Run: `.venv/bin/python -m pytest tests/unit/test_retrieval_quality.py -q --no-cov`
Expected: PASS, 10 tests

- [ ] **Step 5: Run the whole suite and fix fallout**

Run: `.venv/bin/python -m pytest -q --no-cov`

Existing tests assert the old output shape. Update the assertions to the new
shape rather than weakening them; if a test mocked `os.listdir` or
`get_file_content_cached` to control search input, give it real files instead —
enumeration now goes through `list_contained_markdown`.

- [ ] **Step 6: Commit**

```bash
git add mcp_tools.py tests/
git lc -m "Rank documentation search by BM25 over sections"
```

---

### Task 8: read_laravel_doc_section

**Files:**
- Modify: `mcp_tools.py`
- Test: `tests/unit/test_retrieval_quality.py`

**Interfaces:**
- Consumes: `chunk_markdown` (Task 1); existing `validate_version`, `resolve_contained_path`, `get_file_content_cached`.
- Produces: `read_laravel_doc_section_impl(docs_path, filename, section, version=None, runtime_version=None) -> str`.

- [ ] **Step 1: Write the failing test**

```python
# append to tests/unit/test_retrieval_quality.py
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
```

- [ ] **Step 2: Run test to verify it fails**

Run: `.venv/bin/python -m pytest tests/unit/test_retrieval_quality.py -q --no-cov -k read_section`
Expected: FAIL with `ImportError: cannot import name 'read_laravel_doc_section_impl'`

- [ ] **Step 3: Write minimal implementation**

```python
# add to mcp_tools.py
def read_laravel_doc_section_impl(
    docs_path: Path,
    filename: str,
    section: str,
    version: Optional[str] = None,
    runtime_version: Optional[str] = None,
) -> str:
    """Return one ## section of a documentation file.

    `section` matches either the anchor or the heading text, case-insensitively,
    because search output shows both and the caller should not have to guess
    which is canonical.
    """
    version_error = validate_version(version)
    if version_error:
        return version_error

    if not version:
        version = runtime_version if runtime_version else DEFAULT_VERSION

    if not filename.endswith('.md'):
        filename = f"{filename}.md"

    version_path = Path(docs_path) / version
    safe_path = resolve_contained_path(version_path, version_path / filename)
    if safe_path is None:
        logger.warning(f"Access denied: {filename} (attempted directory traversal)")
        return f"Access denied: {filename} (attempted directory traversal)"

    if not safe_path.exists():
        return f"Documentation file not found: {filename} (version: {version})"

    content = get_file_content_cached(str(safe_path))
    if content.startswith("Error") or content.startswith("File not found"):
        return content

    wanted = section.strip().lower().lstrip('#')
    sections = chunk_markdown(content, filename, version)

    for candidate in sections:
        if (candidate.anchor or "").lower() == wanted or candidate.heading.lower() == wanted:
            return candidate.text.strip()

    available = [s.anchor or s.heading for s in sections]
    return format_error(
        f"Section '{section}' not found in {filename}",
        {"available_sections": available},
    )
```

- [ ] **Step 4: Run test to verify it passes**

Run: `.venv/bin/python -m pytest tests/unit/test_retrieval_quality.py -q --no-cov`
Expected: PASS, 15 tests

- [ ] **Step 5: Commit**

```bash
git add mcp_tools.py tests/unit/test_retrieval_quality.py
git lc -m "Add section-level documentation reads"
```

---

### Task 9: Tool layer — expose the section reader, retire with_context

**Files:**
- Modify: `laravel_mcp_companion.py`
- Modify: `mcp_tools.py` (delete `search_laravel_docs_with_context_impl`)
- Test: `tests/unit/test_retrieval_quality.py`

**Interfaces:**
- Consumes: `read_laravel_doc_section_impl` (Task 8), `search_laravel_docs_impl` (Task 7).
- Produces: MCP tools `search_laravel_docs` (new output shape) and `read_laravel_doc_section`; `search_laravel_docs_with_context` no longer registered.

- [ ] **Step 1: Write the failing test**

```python
# append to tests/unit/test_retrieval_quality.py
@pytest.mark.asyncio
async def test_section_reader_is_exposed_as_a_tool(tmp_path):
    from fastmcp import Client

    from laravel_mcp_companion import create_mcp_server

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
```

- [ ] **Step 2: Run test to verify it fails**

Run: `.venv/bin/python -m pytest tests/unit/test_retrieval_quality.py -q --no-cov -k exposed`
Expected: FAIL, `assert 'read_laravel_doc_section' in [...]`

- [ ] **Step 3: Write minimal implementation**

In `laravel_mcp_companion.py`, remove the `search_laravel_docs_with_context` tool
definition and its import, then register the new tool alongside
`read_laravel_doc_content`:

```python
    @mcp.tool(
        description=(
            "Read one section of a Laravel documentation file by its anchor or "
            "heading, as returned by search_laravel_docs. Prefer this over "
            "read_laravel_doc_content: a whole file can exceed 30,000 tokens."
        ),
        annotations={"readOnlyHint": True, "idempotentHint": True},
        tags={"docs", "read"}
    )
    def read_laravel_doc_section(filename: str, section: str, version: Optional[str] = None) -> str:
        """Read a single documentation section.

        Args:
            filename: Documentation file, e.g. 'queues.md'
            section: Anchor or heading, e.g. 'dealing-with-failed-jobs'
            version: Laravel version. Defaults to the configured version.
        """
        return read_laravel_doc_section_impl(
            docs_path, filename, section, version, runtime_version=runtime_version
        )
```

Update the import block to add `read_laravel_doc_section_impl` and drop
`search_laravel_docs_with_context_impl`, then delete
`search_laravel_docs_with_context_impl` from `mcp_tools.py`.

- [ ] **Step 4: Run test to verify it passes**

Run: `.venv/bin/python -m pytest tests/unit/test_retrieval_quality.py -q --no-cov`
Expected: PASS, 16 tests

- [ ] **Step 5: Run the whole suite, ruff and mypy**

```bash
.venv/bin/python -m pytest -q --no-cov
.venv/bin/ruff check .
.venv/bin/mypy --ignore-missing-imports .
```

Remove any test that exercised `search_laravel_docs_with_context`; its coverage is
replaced by the retrieval-quality tests.

- [ ] **Step 6: Commit**

```bash
git add laravel_mcp_companion.py mcp_tools.py tests/
git lc -m "Expose section reads and retire the substring context search"
```

---

### Task 10: Documentation and changelog

**Files:**
- Modify: `README.md`
- Modify: `CHANGELOG.md`

**Interfaces:**
- Consumes: everything above.
- Produces: no code.

- [ ] **Step 1: Update the CHANGELOG**

Add under `## [Unreleased]`:

```markdown
### Breaking
- `search_laravel_docs` returns ranked sections with snippets rather than files
  with match counts, and `search_laravel_docs_with_context` is removed. Both
  matched the query as a literal substring, so four of seven realistic developer
  questions returned nothing; ranking by match count also placed `queues.md`
  13th of 24 for "queues".

### Added
- `read_laravel_doc_section` reads one section by anchor or heading. Answering a
  typical question drops from ~34,000 tokens to under 3,000.
```

- [ ] **Step 2: Update the README**

In the tools section, document `read_laravel_doc_section` and note that
`search_laravel_docs` now returns sections with anchors. Remove any mention of
`search_laravel_docs_with_context`.

- [ ] **Step 3: Verify the version-consistency guard still passes**

Run: `.venv/bin/python -m pytest tests/unit/test_version_consistency.py -q --no-cov`
Expected: PASS

- [ ] **Step 4: Commit**

```bash
git add README.md CHANGELOG.md
git lc -m "Document section reads and the new search output"
```

---

## Self-Review

**Spec coverage.** Chunking at `##` — Task 1. Owned BM25 — Task 2. Snippets — Task 3. Lazy per-version registry with LRU cap of 2 — Task 4. Invalidation through `clear_caches` — Task 5. External service docs keyed by service — Task 6 (`load_service_sections`) and Task 7 (the service loop). Merged ranking across corpora — Task 7 (`hits.sort` then truncate). Substring fallback — Task 4 (`substring_search`), used in Task 7. Tool contract change and `with_context` removal — Task 9. Token budget — Task 7's budget test. Traversal and containment reuse — Tasks 6 and 8.

**Placeholders.** None: every code step carries real code, and every test step carries real assertions.

**Type consistency.** `Section` fields are used identically in Tasks 1, 6, 7 and 8. `BM25Index.query` returns `list[tuple[int, float]]` in Task 2 and is consumed as `(i, score)` in Task 4. `DocIndex.search` returns `list[tuple[Section, float]]` in Task 4 and is consumed as `(section, score)` in Task 7. `get_index(docs_path, key, loader)` is defined in Task 4 and called with that signature in Task 7. `chunk_markdown(text, filename, version)` is defined in Task 1 and called with that signature in Tasks 6 and 8.

**One gap found and closed:** the spec says results are labelled with the service for external hits. Task 7 renders `f"{section.version}/{section.filename}"`, and Task 6 sets `version=service` for service sections, so a Forge hit renders as `forge/introduction.md`. No extra field is needed.
