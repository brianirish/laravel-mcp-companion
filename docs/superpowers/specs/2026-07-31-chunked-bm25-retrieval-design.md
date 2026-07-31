# Chunked BM25 Retrieval — Design

**Date:** 2026-07-31
**Status:** Approved, not yet implemented

## Problem

The project's purpose is to make it as easy as possible to have the latest Laravel
documentation at the ready when using LLMs. Acquisition works: all eight versions
match `laravel/docs` branch HEAD exactly. Retrieval does not.

`search_laravel_docs` compiles the query with `re.escape` and ranks by raw match
count. Measured against `docs/13.x`:

| query | result today |
|---|---|
| `how do I validate a file upload` | 0 results |
| `retry failed queue job` | 0 results |
| `send email with attachment` | 0 results |
| `rate limiting api routes` | 0 results |
| `database transactions` | ok |
| `eloquent relationships` | ok |
| `queue` | ok |

**Four of seven realistic questions return nothing**, because a multi-word question
is rarely a verbatim substring. Ranking is also anti-correlated with relevance: raw
term frequency rewards long files, so `queues.md` (54 matches) ranks 13th of 24 for
"queues", behind `images.md` (1 match). There is no IDF and no length normalization.

When search fails the only fallback is `read_laravel_doc_content`, which returns
whole files. `queues.md` is ~34,048 tokens; 25% of 13.x files exceed 10,000. The
sections that answer a typical question are roughly 28% of that.

The root cause is structural: **there is no retrieval unit between a filename and a
whole file.**

## Goals

1. Multi-word natural-language questions return relevant results.
2. Results are ranked by relevance, not by file length.
3. Answering a typical question costs hundreds of tokens, not tens of thousands.
4. Results cite a section that can be fetched directly.

## Non-goals

Stemming, synonym expansion, embeddings or semantic search, a persisted index,
and cross-encoder reranking. Also out of scope, each its own change: the freshness
metric reporting fetch-age instead of content-age, `read_laravel_doc_content` not
being pinned in the search transform, and the unused `TOOL_DESCRIPTIONS` entries.

## Architecture

A new module, `doc_search.py`. `mcp_tools.py` is already ~1,300 lines of tool
implementations; chunking, indexing and scoring are a separate concern with a clean
interface and are far easier to test standalone.

```
Section            dataclass: version, filename, anchor, heading, text
chunk_markdown()   split on ## ; capture <a name="..."> anchor for citation
BM25Index          build(docs) / query(text, k) -> [(index, score)]
DocIndex           per-version lazy index, snippet extraction, LRU registry
```

`BM25Index` is roughly 40 lines of Okapi BM25 (k1=1.5, b=0.75), owned rather than
imported. fastmcp ships `_BM25Index`, which is generic enough to reuse, but it is a
private underscore-prefixed class in a fast-moving dependency, and it retains its
token lists after `build()` — most of the measured 26.5 MB per version. Owning it
drops those and roughly halves the footprint. This project was broken twice in one
week by upstream changes it did not control (MCP Inspector 2.0's CLI, ruff 0.15's
default rule set); a private class is the same bet a third time.

### Chunk granularity

Chunk on `##`. Measured on `docs/13.x`:

| granularity | chunks | avg tokens | correct top-1 of 4 |
|---|---|---|---|
| `##` | 838 | ~1,013 | **4** |
| `##` + `###` | 2,167 | ~391 | 2 |
| `<a name>` anchors | 4,117 | ~206 | 2 |

Finer chunks are sharper when they hit — `### Retrying Failed Jobs` beats
`## Dealing With Failed Jobs` — but regress elsewhere. "validate a file upload"
drifts to `filesystem.md#temporary-upload-urls`, and "rate limiting api routes"
collapses onto the file-header chunk, because short chunks give BM25 too few terms
to discriminate. Anchors are better as citation and drill-down targets than as
index units.

### Index lifecycle

A module-level `{version: DocIndex}` registry, built on first query for a version
and cleared by the existing `clear_caches()`, which already runs on documentation
update — invalidation needs no new machinery.

Measured: 6 ms to chunk, 103 ms to build, 0.4 ms per query for one version (838
sections). Precomputing an index at sync time and shipping it was considered and
rejected: it adds a build step, image weight, and a staleness failure mode to save
a tenth of a second.

Memory is the binding constraint at ~13 MB per version after dropping token lists.
**At most two indexes stay resident, LRU-evicted.** Search already defaults to a
single version, so `all_versions=true` is the rare path; it sweeps versions and
rebuilds at ~100 ms each, trading speed on an uncommon call for a bounded footprint.

### External service documentation

`include_external=True` is the existing default and must keep working.
`docs/external/<service>/*.md` is markdown with the same heading structure, so it
is chunked and indexed identically, keyed by service name rather than version, in
the same registry and under the same LRU cap. A `Section` from external docs
carries the service in place of the version, and results label it as such.

### Ranking across multiple corpora

When more than one version or service is searched, each is queried against its own
index and the hits are merged by score, then truncated to `limit`.

BM25 scores from separate corpora are not formally comparable, since IDF is
computed per index. In practice these corpora are near-identical in size,
vocabulary and structure — they are the same documentation at different versions —
so the scores are close enough to rank against each other. This is an
approximation, and it is the reason the default remains a single version rather
than a merged sweep.

## Tool contract

Breaking, by decision. `search_laravel_docs` keeps its name and gains a new output
shape; leaving the broken implementation as the default would undercut the fix.
`search_laravel_docs_with_context` is removed as redundant — it is substring-based
and returns nothing for the same queries.

```
search_laravel_docs(query, version=None, include_external=True,
                    all_versions=False, limit=5)
```

```
query: retry failed queue job
scope: 13.x
results[3]{file,anchor,heading,score,snippet}:
  queues.md,dealing-with-failed-jobs,Dealing With Failed Jobs,8.4,
    "...jobs exceeding max attempts are inserted into the
     failed_jobs table. Retry with php artisan queue:retry..."
```

Snippets are a ~300-character window on line boundaries around the highest-scoring
term, so they read as prose rather than a mid-word slice.

```
read_laravel_doc_section(filename, section, version=None)
```

`section` accepts either the anchor (`dealing-with-failed-jobs`) or the heading
text, case-insensitively. The model sees both in search output and should not have
to guess which is canonical. An unknown section returns the available anchors,
making the error a discovery path rather than a dead end.

### Substring fallback

If BM25 returns no results, fall back to literal substring matching over the same
sections. This preserves the one thing the current implementation does well —
exact symbol lookup such as `mimes:pdf` or `Rule::contains` — for about five lines.
Without it this change would be a straight upgrade that quietly loses a capability.

## Data flow

```
search_laravel_docs(query, ...)
  -> validate_version / resolve_search_versions       (existing)
  -> get_or_build_index(version)                      (lazy, LRU)
  -> BM25 query -> top-k (Section, score)
  -> substring fallback if empty
  -> extract_snippet per hit
  -> TOON encode

read_laravel_doc_section(filename, section, version)
  -> validate_version                                 (existing)
  -> resolve_contained_path                           (existing)
  -> chunk file, match anchor or heading
  -> return section text, or available anchors
```

Chunking reads through `list_contained_markdown`, and section reads validate via
`validate_version` and `resolve_contained_path`, so the containment and TOCTOU
hardening carries over unchanged rather than being reimplemented.

## Error handling

Empty query and invalid version reuse the existing validators. No results reports
the versions actually searched. Unreadable directories propagate rather than
reporting "no files found", matching the decision already made in
`list_contained_markdown`. An unknown section lists the available anchors.

## Testing

Written failing-first, per the test-driven-development skill.

- `chunk_markdown`: anchor and heading capture; a file with no `##`; preamble
  before the first heading; a heading with no anchor
- `BM25Index`: known-answer scoring; empty corpus; a query whose terms appear
  nowhere; verification that token lists are released after `build()`
- **Retrieval regression:** the seven realistic queries above, currently 3/7, must
  reach 7/7. Asserted as a test rather than claimed in a commit message.
- **Ranking:** `queues.md` outranks `images.md` for "queues" (13th of 24 today)
- **Token budget:** a `limit=5` search response stays under 1,200 tokens
  (~4,800 characters), so output cannot silently balloon back toward whole-file
  cost. Measured against today's 34,048-token path for the same question.
- Substring fallback returns results for an exact symbol that BM25 misses
- `read_laravel_doc_section`: by anchor; by heading; case-insensitive; unknown
  section lists anchors; traversal still blocked
- LRU eviction holds at two resident indexes
- End-to-end through a real `fastmcp.Client`

## Risks

**A fifth breaking change since v0.10.0.** Mitigated by keeping the tool name and
arguments stable — only the result shape changes — and by the fact that the tool
being replaced returns nothing for most real queries.

**BM25 quality is not guaranteed to generalize** beyond the queries measured here.
The regression test pins seven; more should be added as real failures surface.

**Snippets may cut mid-sentence** despite line-boundary alignment. Acceptable: the
anchor is always returned, so full text is one call away.
