"""Check the hand-written tables against the documentation actually held.

The need table, learning paths, difficulty map and categories name framework
pages. Laravel renames, removes and adds pages, and nothing told these tables
when it did: by 2026 twenty-three needs and the first learning path pointed at
pages that no longer existed, and thirty-five pages belonged to no category.

`audit` lists every such disagreement for one Laravel version. Two things read
it. The test suite fails on any of them, so a change to the tables cannot
introduce one. The nightly sync report lists them under "Needs attention", so
a change upstream is noticed the night it arrives without holding the
documentation back.
"""

from pathlib import Path
from typing import Dict, List, Optional

from .docs_updater import get_default_version
from .learning_resources import (
    EXPANDED_CATEGORIES,
    LEARNING_PATHS,
    NEED_MAPPINGS,
    TOPIC_DIFFICULTY_MAP,
    categories_of,
    keyword_selects,
)

# Pages about the documentation itself, not about Laravel. They need no
# category, difficulty or need.
NOT_CONTENT = frozenset({"readme", "license", "documentation", "contributions"})

DESCRIPTIONS = {
    "dead_need_targets": "needs pointing at a page that does not exist",
    "dead_path_docs": "learning paths listing a page that does not exist",
    "dead_difficulty_entries": "difficulty entries naming no page",
    "dead_category_keywords": "category keywords selecting no page",
    "uncategorised_pages": "framework pages in no category",
    "pages_without_difficulty": "framework pages with no difficulty",
    "unreached_pages": "framework pages reached by no need or learning path",
}


def audit(docs_path: Path, version: Optional[str] = None) -> Dict[str, List[str]]:
    """Every disagreement between the curated tables and one version's pages.

    Returns a dict with one sorted list per kind of problem (the keys of
    DESCRIPTIONS), each empty when there is nothing wrong. Returns an empty
    dict when the version has no pages on disk: with nothing to compare
    against, nothing can be said.
    """
    version_dir = Path(docs_path) / (version or get_default_version())
    pages = {path.stem for path in version_dir.glob("*.md")} if version_dir.is_dir() else set()
    if not pages:
        return {}
    content = pages - NOT_CONTENT

    reached = {target for targets in NEED_MAPPINGS.values() for target in targets}
    reached |= {doc for path in LEARNING_PATHS.values() for doc in path.get("docs", [])}

    return {
        "dead_need_targets": sorted(
            f"{need} -> {target}" for need, targets in NEED_MAPPINGS.items() for target in targets if target not in pages
        ),
        "dead_path_docs": sorted(
            f"{path_id} -> {doc}" for path_id, path in LEARNING_PATHS.items()
            for doc in path.get("docs", []) if doc not in pages
        ),
        "dead_difficulty_entries": sorted(set(TOPIC_DIFFICULTY_MAP) - pages),
        "dead_category_keywords": sorted(
            f"{category}: {keyword}" for category, keywords in EXPANDED_CATEGORIES.items()
            for keyword in keywords if not any(keyword_selects(keyword, page) for page in pages)
        ),
        "uncategorised_pages": sorted(page for page in content if not categories_of(page)),
        "pages_without_difficulty": sorted(content - set(TOPIC_DIFFICULTY_MAP)),
        "unreached_pages": sorted(content - reached),
    }


def report_lines(docs_path: Path, version: Optional[str] = None) -> List[str]:
    """One line per kind of problem found, for the sync report."""
    return [
        f"{len(items)} {DESCRIPTIONS[kind]} ({', '.join(items[:6])}{', ...' if len(items) > 6 else ''})"
        for kind, items in audit(docs_path, version).items() if items
    ]
