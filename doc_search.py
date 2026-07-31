#!/usr/bin/env python3
"""Section-level chunking, BM25 indexing and retrieval for Laravel documentation.

Kept separate from mcp_tools so chunking and scoring can be tested without the
MCP tool layer, and so mcp_tools does not grow further.
"""

import math
import re
import threading
from collections import OrderedDict
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Optional

# Consumes the closing </a> so that "is anything after this anchor?" is answered
# about the document, not about the tag's own second half.
_ANCHOR = re.compile(r'<a\s+name="([^"]+)"\s*>\s*(?:</a>)?')
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

    Chunking at ## was measured as the most robust retrieval unit. Finer
    granularity produced sharper hits on some queries but regressed on others,
    because short chunks give BM25 too few terms to discriminate.

    The preamble before the first ## is kept as its own section so content at
    the top of a file stays reachable.

    Anchors in Laravel's documentation sit on the line *before* their heading,
    so after splitting they land at the end of the preceding chunk and are
    carried forward to the section they actually label.
    """
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

        anchors = list(_ANCHOR.finditer(part))

        # An anchor with nothing after it labels the *next* section, so it is
        # carried forward and must not be claimed as this section's own.
        trailing: Optional[str] = None
        if anchors and not part[anchors[-1].end():].strip():
            trailing = anchors[-1].group(1)
            anchors = anchors[:-1]

        anchor = carried_anchor or (anchors[0].group(1) if anchors else None)
        carried_anchor = trailing

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


_TOKEN = re.compile(r"[a-z0-9]+")

BM25_K1 = 1.5
BM25_B = 0.75


def tokenize(text: str) -> list[str]:
    """Lowercase alphanumeric tokens."""
    return _TOKEN.findall(text.lower())


class BM25Index:
    """Okapi BM25 over a fixed document set.

    Owned rather than imported. fastmcp ships an equivalent, but it is a private
    underscore-prefixed class in a fast-moving dependency, and it retains its
    tokenized documents after building -- which is most of the memory cost. Only
    term counts are kept here; the token lists go out of scope during build.
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
            # `tokens` is released here; only counts are retained.

        self._avg_dl = (sum(self._lengths) / self._n) if self._n else 0.0

    def query(self, text: str, top_k: int) -> list[tuple[int, float]]:
        """Return (document_index, score) pairs, best first, omitting zero scores."""
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


def extract_snippet(text: str, query: str, max_chars: int = 300) -> str:
    """Return a readable window of `text` around the best query-term match.

    Aligns to line boundaries so the result reads as prose rather than a
    mid-word slice. Falls back to the start of the section when no query term
    appears, which happens when a section matched on terms that the snippet
    window did not reach.
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
        return (window.rsplit("\n", 1)[0].strip() or window.strip()) + "..."

    start = max(0, position - max_chars // 2)
    end = min(len(body), start + max_chars)

    # Trim to line boundaries, but only when doing so leaves a usable snippet.
    # Laravel formats paragraphs as single long lines, so the nearest newline is
    # often the one just after the heading -- snapping to it would return the
    # heading alone and tell the reader nothing.
    minimum = max_chars // 2

    if start > 0:
        newline = body.find("\n", start)
        if newline != -1 and newline < position and end - (newline + 1) >= minimum:
            start = newline + 1
    if end < len(body):
        newline = body.rfind("\n", start, end)
        if newline != -1 and newline > position and newline - start >= minimum:
            end = newline

    snippet = body[start:end].strip()
    if start > 0:
        snippet = "..." + snippet
    if end < len(body):
        snippet = snippet + "..."
    return snippet


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
        return [
            (self.sections[i], score) for i, score in self._index.query(query, top_k)
        ]

    def substring_search(self, query: str, top_k: int) -> list[tuple[Section, float]]:
        """Literal fallback, preserving exact-symbol lookup such as `queue:retry`.

        BM25 tokenizes on alphanumerics, so a punctuated symbol is split into
        parts that may rank poorly. This is the one thing the previous substring
        implementation did well, and it would otherwise be lost.
        """
        needle = query.lower()
        hits = [
            (section, float(section.text.lower().count(needle)))
            for section in self.sections
            if needle in section.text.lower()
        ]
        hits.sort(key=lambda pair: pair[1], reverse=True)
        return hits[:top_k]


def get_index(
    docs_path: Path, key: str, loader: Callable[[], list[Section]]
) -> DocIndex:
    """Return the index for `key`, building it on first use.

    Indexes cost roughly 13 MB each, so only MAX_RESIDENT_INDEXES are kept and
    the least recently used is dropped. Rebuilding costs about 100 ms, which is
    the right trade for a bounded footprint given search defaults to a single
    version.
    """
    with _registry_lock:
        existing = _registry.get(key)
        if existing is not None:
            _registry.move_to_end(key)
            return existing

    # Built outside the lock: loading and indexing is slow and must not block
    # other lookups.
    index = DocIndex(loader())

    with _registry_lock:
        _registry[key] = index
        _registry.move_to_end(key)
        while len(_registry) > MAX_RESIDENT_INDEXES:
            _registry.popitem(last=False)
    return index


def clear_indexes() -> None:
    """Drop every resident index. Called when documentation is updated."""
    with _registry_lock:
        _registry.clear()


def resident_index_count() -> int:
    with _registry_lock:
        return len(_registry)
