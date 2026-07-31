# Documentation Currency Reporting — Design

**Date:** 2026-07-31
**Status:** Approved, not yet implemented

## Problem

The freshness reporting added in v0.10.0 measures the wrong thing, and the
result is worse than reporting nothing.

`sync_time` records when this project last *fetched* a change, not when the
documentation last *changed*. `DocsUpdater.update()` returns early when the
upstream commit SHA matches (`docs_updater.py:1704`) and therefore never
rewrites the metadata, so `sync_time` is frozen at the last content change. For
a branch that no longer changes, it recedes indefinitely.

Every one of the eight shipped versions matches `laravel/docs` branch HEAD
exactly. Verified against the GitHub API — for example 9.x, local
`177c095cc802` against upstream `177c095cc802`. Despite that:

- **Five of eight versions are reported as stale.** The server tells the
  assistant that 6.x, 8.x, 9.x, 10.x and 11.x are "more than 30 days old" and
  should be refreshed, while they are byte-identical to upstream.
- **The warning cannot be cleared.** Calling `update_laravel_docs` returns
  "Documentation is already up to date" and leaves `sync_time` untouched, so the
  warning persists. An assistant that follows the server's own instruction loops.
- **The recommended tool rejects the obvious argument.** Every other tool takes
  `version`; this one exposes `version_param`, a leaked internal name. Passing
  `version='9.x'` raises `ToolError: Unexpected keyword argument`.
- **`laravel_docs_info()` warns permanently.** With no version argument it
  reports the *oldest* version's age — 425 days — and fires the staleness note
  regardless of which version the user actually reads. Because 6.x can never get
  fresher, that warning can never clear.

The net effect is that the assistant hedges on correct documentation, is told to
run a tool that cannot help, and guesses a parameter name the tool refuses.

## Goals

1. Report something true about every version, including end-of-life ones.
2. Give the assistant what it actually needs: whether the documentation could
   predate the feature being asked about.
3. Warn only about a problem the user can act on.
4. Preserve offline operation.

## Non-goals

Verifying against upstream at runtime, and any change to the Dockerfile layer
ordering or `--pull=always` economics. Also out of scope: pinning
`read_laravel_doc_content` in the search transform.

## Design

### Report the documentation's own date

Use `commit_date`, already present in every version's metadata. It is the date
Laravel last changed that documentation upstream.

> The Laravel 8.x documentation reflects Laravel's documentation as of
> 2025-04-01.

That is true, needs no network, adds no metadata field, and reads correctly for
an end-of-life branch. It also answers the question the assistant actually has:
anything Laravel added after that date is not in this corpus, so the model can
decide for itself whether to caveat an answer.

Real values:

| version | upstream last changed | fetched |
|---|---|---|
| 13.x | 2026-07-30 | 2026-07-31 |
| 12.x | 2026-07-27 | 2026-07-28 |
| 11.x | 2026-04-20 | 2026-04-21 |
| 8.x | 2025-04-01 | 2025-06-01 |

### Warn on the newest change, not the oldest

The one thing `commit_date` alone cannot tell you is whether *this copy* is
behind — a user running a six-month-old image sees dates that are accurate for
what they have while newer documentation exists.

That is detectable offline. 13.x changes near-daily, so the **newest**
`commit_date` across all versions is a proxy for when this copy was built. If
the most recently changed version last changed months ago, the copy is months
old.

So the warning inverts: it fires when the newest change across all versions is
older than `DOCS_STALE_AFTER_DAYS` (30), meaning "this copy is behind, pull a newer
image." It no longer fires because an end-of-life branch stopped changing.

Measured today: newest change across all versions is 2026-07-30, zero days ago.

### Rename `version_param` to `version`

`update_laravel_docs(version_param=...)` is the only tool not taking `version`.
An assistant told to refresh documentation guesses `version` and receives a hard
`ToolError`. This is a breaking change to a tool signature, accepted because the
current name is a leaked internal and the tool is unusable as named.

## Data flow

Internals keep their shape so callers change minimally:

```
get_documentation_date(docs_path, version) -> (date_str | None, age_days | None)
  reads commit_date; replaces get_docs_snapshot_age

describe_documentation_date(docs_path, version) -> str
  "2026-07-30", or "unknown" -- a bare date, no age phrasing

copy_is_stale(docs_path) -> bool
  newest commit_date across versions older than DOCS_STALE_AFTER_DAYS
  takes no version: per-version staleness is not a meaningful question
```

**No per-version staleness.** A version's `commit_date` being old means upstream
stopped changing, which is not a problem and not actionable. `docs_are_stale` is
replaced by `copy_is_stale`, which takes no version argument, so there is no way
to ask the meaningless question.

**No age phrasing in the served-version report.** `describe_documentation_date`
returns the bare date. Rendering "425 days ago" would reintroduce exactly the
alarm this change removes, even though the number is factual.
`DOCS_STALE_AFTER_DAYS` keeps its name and value of 30.

`laravel_docs_info` field changes:

- per version: `age_days` becomes `documentation_date`. No per-version age
  number, for the reason above.
- summary: `oldest_snapshot_date` / `oldest_snapshot_age_days` become
  `documentation_current_to` (newest `commit_date`) and `copy_age_days`
- the per-version branch emits no staleness note at all
- the summary note fires on copy age and says to pull a newer image, not to run
  `update_laravel_docs`, which cannot help

## Error handling

Unchanged from the existing implementation, which already handles these and
applies equally to `commit_date`: malformed or non-string timestamps report
unknown rather than raising, a future timestamp reports unknown and logs a
warning rather than being clamped to "today", and a missing metadata file is not
an error.

## Testing

Written failing-first.

- **The regression that matters:** a version whose `commit_date` is old but which
  matches upstream is *not* reported as stale. Uses 9.x-shaped metadata — old
  `commit_date`, old `sync_time` — and asserts no staleness warning.
- `laravel_docs_info()` with no version does not warn when the newest version is
  current, even while older versions have old dates. This is the permanent-warning
  bug and it must be pinned.
- The warning *does* fire when every version's `commit_date` is old, which is the
  stale-image case it now exists to catch.
- Instructions quote the served version's documentation date, not another
  version's.
- `update_laravel_docs` accepts `version=`; the old `version_param=` is gone.
- Malformed, missing and future `commit_date` values behave as the existing
  freshness tests already require.

## Risks

**A stale image is only inferred, not measured.** The proxy assumes 13.x keeps
changing. If Laravel froze all branches simultaneously the warning would go
quiet — an acceptable failure mode, since in that case there would be nothing to
pull.

**Another breaking change to a tool signature.** Mitigated: the argument being
renamed cannot currently be passed successfully by name, so the surface being
broken is one that does not work.
