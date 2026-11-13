"""search_laravel_docs: one ranked search over every corpus the server holds."""

import math
from pathlib import Path
from typing import Annotated, Any, Dict, List, Optional, Tuple

from fastmcp import Context
from pydantic import Field

from .. import mcp_tools
from ..doc_search import Section, extract_snippet, get_index, tokenize
from ..learning_resources import NEED_MAPPINGS
from .common import require_version, slugify
from .errors import ToolFailure
from .registry import companion, tool

SOURCES = ("core", "services", "packages", "learning")
DEFAULT_LIMIT = 5
MAX_LIMIT = 20

# How much of a result page one source may take when others have hits too.
SOURCE_SHARE = 0.6
# Applied to the rank of a core page that a matched need points at.
NEED_BOOST = 1.25

SCHEMA: Dict[str, Any] = {
    "type": "object",
    "required": ["query", "scope", "sources", "count", "results"],
    "properties": {
        "query": {"type": "string"},
        "scope": {"type": "string", "description": "The Laravel versions searched, comma-separated"},
        "sources": {"type": "array", "items": {"type": "string", "enum": list(SOURCES)}},
        "count": {"type": "integer", "description": "How many results follow; 0 when nothing matched"},
        "matched_needs": {
            "type": "array",
            "items": {"type": "string"},
            "description": "Common tasks recognised in the query, whose usual documentation pages were favoured",
        },
        "results": {
            "type": "array",
            "items": {
                "type": "object",
                "required": ["file", "section", "heading", "score", "snippet", "source"],
                "properties": {
                    "file": {"type": "string", "description": "Pass to read_laravel_doc_section or read_laravel_doc_content"},
                    "section": {"type": "string", "description": "Pass to read_laravel_doc_section with `file`"},
                    "heading": {"type": "string"},
                    "score": {"type": "number"},
                    "snippet": {"type": "string"},
                    "source": {
                        "type": "string",
                        "description": "core, service:<name>, package:<name> or learning:<name>",
                    },
                },
            },
        },
    },
}

DESCRIPTION = """Search Laravel's documentation and get back the sections that answer the question.

Covers every corpus on this server at once: the framework docs for the selected Laravel version, the first-party services (Forge, Vapor, Envoyer, Nova, Cloud, Nightwatch, Herd), fetched package docs (Livewire, Filament, Inertia, Spatie and others) and learning resources. Each result names a file and a section; pass both to read_laravel_doc_section to read just that section.

Use it first for any Laravel question. Narrow with `sources` when you know the corpus, and set `version` for an older Laravel release. Results are ranked across corpora, and no single source takes the whole page when others match. Nothing found is a normal result with count 0."""


def section_id(section: Section) -> str:
    """What to ask read_laravel_doc_section for to get this section back."""
    return section.anchor or slugify(section.heading) or section.heading


def matched_needs(query: str) -> Dict[str, List[str]]:
    """Common tasks named in the query, with the core pages each points at.

    `NEED_MAPPINGS` is a hand-kept table from a task as people phrase it
    ("upload files") to the framework pages that cover it. A task counts as
    named when every word of its phrase is in the query, in any order and in
    either number, so "file upload" and "uploading a file" both name it.
    """
    asked = set(tokenize(query))
    return {need: pages for need, pages in NEED_MAPPINGS.items() if set(tokenize(need)) <= asked}


def rank_hits(hits: List[Tuple[Section, float, str]], need_pages: Any = frozenset()) -> List[Tuple[Section, float, str]]:
    """Order (section, score, family) hits from every corpus into one ranking.

    Raw score is close enough to rank on, with two adjustments to the order
    only; the scores reported to the caller are the ones computed. A framework
    page is ranked as if it scored CORE_NEAR_TIE_MARGIN higher, which settles
    near-ties with package pages in the framework's favour. A framework page
    that a recognised need points at is ranked NEED_BOOST higher again.
    """
    def rank_score(hit: Tuple[Section, float, str]) -> float:
        section, score, family = hit
        if family != "core":
            return score
        boosted = score * (1 + mcp_tools.CORE_NEAR_TIE_MARGIN)
        return boosted * NEED_BOOST if getattr(section, "filename", None) in need_pages else boosted

    return sorted(hits, key=rank_score, reverse=True)


def spread_across_sources(ranked: List[Tuple[Section, float, str]], limit: int) -> List[Tuple[Section, float, str]]:
    """Take `limit` hits in rank order without letting one source fill the page.

    A source is a corpus as labelled in the results: `core`, `package:spatie`,
    `service:forge`. Each may take at most SOURCE_SHARE of the page while hits
    from other sources are waiting. Whatever room is left once every source
    has had its turn goes to the best remaining hits, whatever their source.
    """
    def label(hit: Tuple[Section, float, str]) -> str:
        section, _score, family = hit
        return "core" if family == "core" else f"{family}:{section.version}"

    if len({label(hit) for hit in ranked}) < 2:
        return ranked[:limit]

    share = max(1, math.ceil(limit * SOURCE_SHARE))
    taken: Dict[str, int] = {}
    chosen: List[Tuple[Section, float, str]] = []
    held_back: List[Tuple[Section, float, str]] = []
    for hit in ranked:
        if len(chosen) == limit:
            break
        if taken.get(label(hit), 0) < share:
            chosen.append(hit)
            taken[label(hit)] = taken.get(label(hit), 0) + 1
        else:
            held_back.append(hit)
    chosen.extend(held_back[: limit - len(chosen)])
    order = {id(hit): position for position, hit in enumerate(ranked)}
    return sorted(chosen, key=lambda hit: order[id(hit)])


def search(
    docs_path: Path,
    external_dir: Optional[Path],
    query: str,
    version: Optional[str] = None,
    runtime_version: Optional[str] = None,
    all_versions: bool = False,
    sources: Optional[List[str]] = None,
    limit: int = DEFAULT_LIMIT,
) -> Dict[str, Any]:
    """Ranked sections from every selected corpus, as data.

    Ranked by BM25 over `##` sections, so a multi-word question matches and a
    long file does not outrank a relevant one. A literal substring search is
    the fallback, which keeps exact symbols such as `queue:retry` findable.
    """
    require_version(version)
    if not query.strip():
        raise ToolFailure("invalid_argument", "query is empty")
    if not 1 <= limit <= MAX_LIMIT:
        raise ToolFailure("invalid_argument", f"limit must be between 1 and {MAX_LIMIT}", {"limit": limit})
    if sources is not None:
        invalid = [source for source in sources if source not in SOURCES]
        if invalid:
            raise ToolFailure(
                "invalid_argument", f"Unknown sources: {', '.join(invalid)}", {"valid_sources": list(SOURCES)}
            )
    chosen_sources = list(dict.fromkeys(sources)) if sources else list(SOURCES)
    versions = mcp_tools.resolve_search_versions(version, runtime_version, all_versions)

    # The docs path is part of the key: two servers in one process, each with
    # its own tree, must not be handed each other's results.
    cache_key = f"search:{docs_path}:{query}:{','.join(versions)}:{','.join(chosen_sources)}:{limit}"
    with mcp_tools._cache_lock:
        cached = mcp_tools._search_result_cache.get(cache_key)
    if cached is not None:
        return cached

    needs = matched_needs(query) if "core" in chosen_sources else {}
    need_pages = {f"{page}.md" for pages in needs.values() for page in pages}

    hits: List[Tuple[Section, float, str]] = []

    def add_need_pages(index: Any, found: List[Tuple[Section, float]], version_key: str) -> None:
        # A page a recognised task points at is a candidate whether or not
        # its words match: BM25 does not stem, so "upload files" misses a
        # page that says "uploaded file". Its best-matching section is used,
        # or failing any match its opening section, scored just under the
        # weakest real hit so it informs the page without leading it.
        present = {section.filename for section, _ in found if section.version == version_key}
        deeper = [(section, score) for section, score in index.search(query, 100) if section.version == version_key]
        floor = min((score for _, score in found), default=1.0) * 0.9
        for page in sorted(need_pages - present):
            match = next(((section, score) for section, score in deeper if section.filename == page), None)
            if match is None:
                opening = next(
                    (section for section in index.sections if section.version == version_key and section.filename == page),
                    None,
                )
                match = (opening, floor) if opening is not None else None
            if match is not None:
                hits.append((match[0], match[1], "core"))

    def collect(index_key: str, loader: Any, family: str) -> None:
        index = get_index(docs_path, f"{docs_path}:{index_key}", loader)
        found = index.search(query, limit) or index.substring_search(query, limit)
        hits.extend((section, score, family) for section, score in found)
        if family == "core" and need_pages:
            add_need_pages(index, found, index_key.split(":", 1)[1])

    packages_dir = Path(docs_path) / "packages"
    learning_dir = Path(docs_path) / "learning_resources"
    services = mcp_tools.contained_subdirectories(Path(external_dir)) if external_dir else []

    if len(chosen_sources) > 1 and len(versions) == 1:
        # Several corpora, one Laravel version: the ordinary search. Ranked
        # from a single index over everything, because a score only means
        # something relative to the corpus it was computed in. With an index
        # per corpus, a word that is everywhere in the framework docs and
        # rare in a package's ("cache", "authentication") scored low in the
        # first and high in the second, and the framework's own page on the
        # subject did not make the list at all.
        candidate = versions[0]
        family_of = {name: "learning" for name in mcp_tools.contained_subdirectories(learning_dir)}
        family_of.update({name: "package" for name in mcp_tools.contained_subdirectories(packages_dir)})
        family_of.update({name: "service" for name in services})
        wanted = {"core": "core", "service": "services", "package": "packages", "learning": "learning"}

        def load_everything() -> List[Section]:
            sections = list(mcp_tools.load_version_sections(docs_path, candidate))
            for name in services:
                sections += mcp_tools.load_service_sections(external_dir, name)  # type: ignore[arg-type]
            sections += mcp_tools.load_package_sections(packages_dir)
            sections += mcp_tools.load_learning_sections(learning_dir)
            return sections

        index = get_index(docs_path, f"{docs_path}:everything:{candidate}", load_everything)
        depth = max(60, limit * 12)
        pool = index.search(query, depth) or index.substring_search(query, depth)
        found = []
        for section, score in pool:
            family = "core" if section.version == candidate else family_of.get(section.version)
            if family and wanted[family] in chosen_sources:
                hits.append((section, score, family))
                found.append((section, score))
        if need_pages:
            add_need_pages(index, found, candidate)
    else:
        # One corpus, or every Laravel version at once: an index per corpus.
        # A single corpus needs no cross-corpus comparison, and one combined
        # index per version would hold the same package pages eight times.
        if "core" in chosen_sources:
            for candidate in versions:
                collect(f"version:{candidate}", lambda c=candidate: mcp_tools.load_version_sections(docs_path, c), "core")
        if "services" in chosen_sources:
            for name in services:
                collect(f"service:{name}", lambda n=name: mcp_tools.load_service_sections(external_dir, n), "service")  # type: ignore[arg-type]
        if "packages" in chosen_sources and packages_dir.is_dir():
            collect("packages", lambda: mcp_tools.load_package_sections(packages_dir), "package")
        if "learning" in chosen_sources and learning_dir.is_dir():
            collect("learning", lambda: mcp_tools.load_learning_sections(learning_dir), "learning")

    page = spread_across_sources(rank_hits(hits, need_pages), limit)

    result: Dict[str, Any] = {
        "query": query,
        "scope": ", ".join(versions),
        "sources": chosen_sources,
        "count": len(page),
        "results": [
            {
                "file": f"{section.version}/{section.filename}",
                "section": section_id(section),
                "heading": section.heading,
                "score": round(score, 2),
                "snippet": extract_snippet(section.text, query),
                "source": "core" if family == "core" else f"{family}:{section.version}",
            }
            for section, score, family in page
        ],
    }
    if needs:
        result["matched_needs"] = sorted(needs)

    with mcp_tools._cache_lock:
        cache = mcp_tools._search_result_cache
        cache[cache_key] = result
        if len(cache) > mcp_tools._SEARCH_CACHE_MAX_ENTRIES:
            for key in list(cache.keys())[: mcp_tools._SEARCH_CACHE_EVICT_COUNT]:
                del cache[key]
    return result


@tool("search_laravel_docs", description=DESCRIPTION, output_schema=SCHEMA, tags=frozenset({"docs", "read"}))
def search_laravel_docs(
    query: str,
    version: Optional[str] = None,
    all_versions: bool = False,
    sources: Annotated[Optional[List[str]], Field(json_schema_extra={"items": {"type": "string", "enum": list(SOURCES)}})] = None,
    limit: Annotated[int, Field(json_schema_extra={"minimum": 1, "maximum": MAX_LIMIT})] = DEFAULT_LIMIT,
    ctx: Context = None,  # type: ignore[assignment]
) -> Dict[str, Any]:
    """Search all aggregated documentation.

    Args:
        query: What to look for, as a question or as keywords
        version: Laravel version for the framework docs (e.g. "12.x"). Defaults to the server's configured version. Services, packages and learning resources are not Laravel-versioned.
        all_versions: Search every Laravel version instead of one
        sources: Restrict the search to any of "core", "services", "packages", "learning". Default: all four
        limit: How many results to return, 1 to 20. Default 5
    """
    tc = companion(ctx)
    return search(tc.docs_path, tc.external_dir, query, version, tc.runtime_version, all_versions, sources, limit)
