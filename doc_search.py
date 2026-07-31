#!/usr/bin/env python3
"""Section-level chunking, BM25 indexing and retrieval for Laravel documentation.

Kept separate from mcp_tools so chunking and scoring can be tested without the
MCP tool layer, and so mcp_tools does not grow further.
"""

import re
from dataclasses import dataclass
from typing import Optional

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
