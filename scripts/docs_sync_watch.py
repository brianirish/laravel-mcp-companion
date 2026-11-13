#!/usr/bin/env python3
"""Has the nightly documentation sync published recently?

    git ls-remote --tags origin 'docs-*' | python scripts/docs_sync_watch.py

Reads tag names (or `git ls-remote` lines) on standard input. Prints one line
saying when the sync last published and exits 0, or exits 1 when the newest
`docs-YYYY-MM-DD` tag is older than MAX_AGE_DAYS.

The sync tags only when documentation changed, so a quiet night leaves no tag
and a short gap is normal. The allowance is set to catch an outage within days
without firing over a long weekend.
"""

import re
import sys
from datetime import date, datetime, timezone
from typing import Iterable, Optional

MAX_AGE_DAYS = 4

_DOCS_TAG = re.compile(r"(?:^|/)docs-(\d{4})-(\d{2})-(\d{2})(?:-\d{4})?$")


def newest_sync(tags: Iterable[str]) -> Optional[date]:
    """The most recent date named by a docs tag, or None when there is none."""
    dates = []
    for tag in tags:
        match = _DOCS_TAG.search(tag.strip())
        if not match:
            continue
        try:
            dates.append(date(*map(int, match.groups())))
        except ValueError:
            continue
    return max(dates) if dates else None


def verdict(tags: Iterable[str], today: date) -> tuple[bool, str]:
    """(stale, one-line explanation)."""
    newest = newest_sync(tags)
    if newest is None:
        return True, "No docs tag exists, so the documentation sync has never published."
    age = (today - newest).days
    days = f"{age} day{'' if age == 1 else 's'}"
    if age > MAX_AGE_DAYS:
        return True, (
            f"The documentation sync last published on {newest.isoformat()}, {days} ago. "
            f"The allowance is {MAX_AGE_DAYS} days."
        )
    return False, f"The documentation sync last published on {newest.isoformat()}, {days} ago."


if __name__ == "__main__":
    # `git ls-remote` prints "<sha>\trefs/tags/<name>"; a bare name works too.
    names = [line.split()[-1] for line in sys.stdin if line.strip()]
    # Tags are named for the UTC date of the sync.
    is_stale, text = verdict(names, datetime.now(timezone.utc).date())
    print(text)
    sys.exit(1 if is_stale else 0)
