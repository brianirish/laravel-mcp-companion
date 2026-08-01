# Documentation Currency Reporting Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Report the date Laravel last changed each documentation set, instead of the date this project last fetched it, so that end-of-life versions stop being reported as stale while identical to upstream.

**Architecture:** Three functions in `mcp_tools.py` read `commit_date` rather than `sync_time`. Per-version staleness is removed outright; the staleness warning inverts to the *newest* change across versions, which is an offline proxy for how old this copy is. `update_laravel_docs` gains the `version` parameter name every other tool uses.

**Tech Stack:** Python 3.12, pytest, FastMCP 3.4.5.

## Global Constraints

- Python >= 3.12. Run tests with `.venv/bin/python -m pytest`; ruff and mypy must stay clean.
- Commit with `git lc`, never plain `git commit`.
- `DOCS_STALE_AFTER_DAYS` keeps its name and value of 30.
- No network calls. Offline operation is a headline feature; currency is reported from metadata already on disk.
- Malformed, missing and future timestamps must keep behaving as they do now: report unknown, never raise, never clamp a future date to "today".
- Do not add a metadata field. Writing one on every cron run would produce a daily commit, tag and image build for metadata-only churn.
- The functions being replaced are consumed by `laravel_mcp_companion.py` at lines 55-58 (imports), 1168, 1567, 1578-1580, 1591 and 1609. Every one must be updated.

---

### Task 1: Read commit_date instead of sync_time

**Files:**
- Modify: `mcp_tools.py:318-395` (the freshness block)
- Test: `tests/unit/test_docs_freshness.py`

**Interfaces:**
- Consumes: existing `get_laravel_docs_metadata`, `SUPPORTED_VERSIONS`.
- Produces:
  - `parse_timestamp(value: object) -> Optional[datetime]` (renamed from `parse_sync_time`)
  - `get_documentation_date(docs_path: Path, version: Optional[str] = None) -> tuple[Optional[str], Optional[int]]` returning `("YYYY-MM-DD", age_days)`; for a specific version its own date, for no version the **newest** across versions
  - `describe_documentation_date(docs_path: Path, version: Optional[str] = None) -> str` returning a bare date or `"unknown"`
  - `copy_is_stale(docs_path: Path) -> bool` — no version argument

- [ ] **Step 1: Write the failing test**

```python
# replace the body of tests/unit/test_docs_freshness.py
"""Currency reporting reflects when Laravel changed its documentation.

The previous implementation measured when this project last fetched a change.
For a branch that no longer changes that recedes forever, so five of eight
shipped versions were reported stale while byte-identical to upstream.
"""

import json
import time

import pytest

from mcp_tools import (
    DOCS_STALE_AFTER_DAYS,
    copy_is_stale,
    describe_documentation_date,
    get_documentation_date,
    parse_timestamp,
)


def write_metadata(docs_path, version, changed_days_ago, fetched_days_ago=None):
    """Write metadata for a version, separating change date from fetch date."""
    if fetched_days_ago is None:
        fetched_days_ago = changed_days_ago
    metadata_dir = docs_path / version / ".metadata"
    metadata_dir.mkdir(parents=True, exist_ok=True)
    fmt = "%Y-%m-%dT%H:%M:%SZ"
    (metadata_dir / "sync_info.json").write_text(json.dumps({
        "version": version,
        "sync_time": time.strftime(fmt, time.gmtime(time.time() - fetched_days_ago * 86400)),
        "commit_date": time.strftime(fmt, time.gmtime(time.time() - changed_days_ago * 86400)),
        "commit_sha": "abc1234",
    }))


class TestDocumentationDate:
    def test_reports_when_the_documentation_changed_not_when_it_was_fetched(self, tmp_path):
        """The distinction the whole change rests on."""
        write_metadata(tmp_path, "13.x", changed_days_ago=400, fetched_days_ago=1)

        _, age = get_documentation_date(tmp_path, "13.x")

        assert age == 400

    @pytest.mark.parametrize("days", [0, 1, 30, 425])
    def test_reports_age_in_days(self, tmp_path, days):
        write_metadata(tmp_path, "13.x", changed_days_ago=days)
        _, age = get_documentation_date(tmp_path, days and "13.x" or "13.x")
        assert age == days

    def test_across_versions_reports_the_newest(self, tmp_path):
        """The newest change is a proxy for how old this copy is."""
        write_metadata(tmp_path, "8.x", changed_days_ago=425)
        write_metadata(tmp_path, "13.x", changed_days_ago=1)

        _, age = get_documentation_date(tmp_path)

        assert age == 1, "must report the newest, not the oldest"

    def test_missing_metadata_is_not_an_error(self, tmp_path):
        assert get_documentation_date(tmp_path) == (None, None)

    @pytest.mark.parametrize("bad", ["garbage", "", None, 1753900000, {"a": 1}, ["x"]])
    def test_malformed_commit_date_is_never_fatal(self, tmp_path, bad):
        metadata_dir = tmp_path / "13.x" / ".metadata"
        metadata_dir.mkdir(parents=True, exist_ok=True)
        (metadata_dir / "sync_info.json").write_text(json.dumps({"commit_date": bad}))
        assert get_documentation_date(tmp_path) == (None, None)

    def test_future_dates_report_unknown(self, tmp_path):
        """Clock skew must not be presented as freshness."""
        write_metadata(tmp_path, "13.x", changed_days_ago=-5)
        assert get_documentation_date(tmp_path) == (None, None)


class TestStaleness:
    def test_end_of_life_version_is_not_stale(self, tmp_path):
        """The regression this change exists to fix.

        8.x last changed 425 days ago and is byte-identical to upstream. It is
        not stale; upstream simply stopped.
        """
        write_metadata(tmp_path, "8.x", changed_days_ago=425)
        write_metadata(tmp_path, "13.x", changed_days_ago=1)

        assert copy_is_stale(tmp_path) is False

    def test_stale_when_every_version_is_old(self, tmp_path):
        """A months-old image: even the active version stopped changing."""
        write_metadata(tmp_path, "8.x", changed_days_ago=425)
        write_metadata(tmp_path, "13.x", changed_days_ago=DOCS_STALE_AFTER_DAYS + 1)

        assert copy_is_stale(tmp_path) is True

    def test_not_stale_at_the_threshold(self, tmp_path):
        write_metadata(tmp_path, "13.x", changed_days_ago=DOCS_STALE_AFTER_DAYS)
        assert copy_is_stale(tmp_path) is False

    def test_unknown_age_is_not_stale(self, tmp_path):
        assert copy_is_stale(tmp_path) is False


class TestDescription:
    def test_returns_a_bare_date(self, tmp_path):
        """No age phrasing: '425 days ago' reintroduces the alarm being removed."""
        write_metadata(tmp_path, "8.x", changed_days_ago=425)

        described = describe_documentation_date(tmp_path, "8.x")

        assert "days ago" not in described
        assert "today" not in described
        assert described.count("-") == 2, f"expected a bare date, got {described!r}"

    def test_unknown_when_no_metadata(self, tmp_path):
        assert "unknown" in describe_documentation_date(tmp_path, "13.x")


class TestParseTimestamp:
    @pytest.mark.parametrize("value", [None, "", "unknown", "not-a-date", 17539, {}, []])
    def test_unparseable_values_return_none(self, value):
        assert parse_timestamp(value) is None

    def test_zulu_suffix_is_understood(self):
        parsed = parse_timestamp("2026-07-30T12:00:00Z")
        assert parsed is not None and parsed.year == 2026
```

- [ ] **Step 2: Run test to verify it fails**

Run: `.venv/bin/python -m pytest tests/unit/test_docs_freshness.py -q --no-cov -p no:cacheprovider`
Expected: FAIL, `ImportError: cannot import name 'copy_is_stale'`

- [ ] **Step 3: Write minimal implementation**

Replace `mcp_tools.py` lines 318-395 (from `def parse_sync_time` through the end of `docs_are_stale`) with:

```python
def parse_timestamp(value: object) -> Optional[datetime]:
    """Parse a metadata timestamp into an aware UTC datetime, or None.

    Total by design. Metadata lives in a mutable, network-populated directory
    that users can mount over, and this runs during server construction -- a
    malformed value must degrade to "unknown", never raise.
    """
    if not isinstance(value, str) or not value or value == "unknown":
        return None
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except (TypeError, ValueError):
        return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed


def get_documentation_date(
    docs_path: Path, version: Optional[str] = None
) -> tuple[Optional[str], Optional[int]]:
    """Return (date, age_in_days) for when Laravel last changed the documentation.

    Reads `commit_date`, not `sync_time`. `sync_time` records when this project
    last fetched a change, which for a branch that no longer changes recedes
    forever -- reporting an end-of-life version as increasingly stale while it
    is byte-identical to upstream.

    For a specific version, that version's date. Across versions, the *newest*:
    13.x changes near-daily, so the most recent change is a proxy for how old
    this copy is, which is the only part a user can act on.

    Returns (None, None) when no metadata is readable, or when the date is in
    the future -- clock skew we cannot interpret and must not present as fresh.
    """
    base = Path(docs_path)
    versions = [version] if version is not None else SUPPORTED_VERSIONS
    newest: Optional[datetime] = None

    for candidate in versions:
        metadata = get_laravel_docs_metadata(base, candidate)
        if not isinstance(metadata, dict):
            continue
        changed = parse_timestamp(metadata.get("commit_date"))
        if changed and (newest is None or changed > newest):
            newest = changed

    if newest is None:
        return None, None

    age = (datetime.now(timezone.utc) - newest).days
    if age < 0:
        logger.warning(f"Documentation commit_date is in the future: {newest.isoformat()}")
        return None, None

    return newest.strftime("%Y-%m-%d"), age


def describe_documentation_date(docs_path: Path, version: Optional[str] = None) -> str:
    """A bare date for the server instructions, or "unknown".

    Deliberately carries no age phrasing. Rendering "425 days ago" would
    reintroduce exactly the alarm this reporting exists to remove, even though
    the number is factual.
    """
    date, _ = get_documentation_date(docs_path, version)
    return date or "unknown (no documentation synced yet)"


def copy_is_stale(docs_path: Path) -> bool:
    """Whether this copy of the documentation is behind, judged offline.

    Takes no version argument: a single version's date being old means upstream
    stopped changing, which is neither a problem nor actionable. What is
    actionable is a stale *image*, which shows up as every version being old --
    including the one that normally changes daily.
    """
    _, age = get_documentation_date(docs_path)
    return age is not None and age > DOCS_STALE_AFTER_DAYS
```

- [ ] **Step 4: Run test to verify it passes**

Run: `.venv/bin/python -m pytest tests/unit/test_docs_freshness.py -q --no-cov -p no:cacheprovider`
Expected: PASS

- [ ] **Step 5: Verify against the real documentation tree**

Run:

```bash
.venv/bin/python -c "
from pathlib import Path
from mcp_tools import get_documentation_date, copy_is_stale, SUPPORTED_VERSIONS
for v in SUPPORTED_VERSIONS:
    print(f'  {v:6} {get_documentation_date(Path(\"docs\"), v)}')
print('  copy stale?', copy_is_stale(Path('docs')))
"
```

Expected: each version reports its own upstream change date; 8.x and 9.x show 2025 dates with large ages; `copy stale? False`, because 13.x changed within the last day.

- [ ] **Step 6: Commit**

```bash
git add mcp_tools.py tests/unit/test_docs_freshness.py
git lc -m "Report when documentation changed, not when it was fetched"
```

---

### Task 2: Update the server instructions

**Files:**
- Modify: `laravel_mcp_companion.py:55-58` (imports) and `:1168` and the instruction text below it
- Test: `tests/unit/test_docs_freshness.py`

**Interfaces:**
- Consumes: `describe_documentation_date` (Task 1).
- Produces: no new API; `build_server_instructions` wording changes.

- [ ] **Step 1: Write the failing test**

```python
# append to tests/unit/test_docs_freshness.py
class TestServerInstructions:
    def test_instructions_state_the_documentation_date(self, tmp_path):
        from laravel_mcp_companion import build_server_instructions

        write_metadata(tmp_path, "13.x", changed_days_ago=2)
        instructions = build_server_instructions(tmp_path, "13.x")

        assert "reflects Laravel's documentation as of" in instructions

    def test_instructions_do_not_call_an_eol_version_stale(self, tmp_path):
        """8.x is byte-identical to upstream; the model must not be told to refresh."""
        from laravel_mcp_companion import build_server_instructions

        write_metadata(tmp_path, "8.x", changed_days_ago=425)
        instructions = build_server_instructions(tmp_path, "8.x")

        assert "425 days ago" not in instructions
        assert "stale" not in instructions.lower()

    def test_instructions_report_the_served_version(self, tmp_path):
        from laravel_mcp_companion import build_server_instructions

        write_metadata(tmp_path, "8.x", changed_days_ago=425)
        write_metadata(tmp_path, "13.x", changed_days_ago=0)

        instructions = build_server_instructions(tmp_path, "8.x")
        eight, _ = get_documentation_date(tmp_path, "8.x")

        assert eight in instructions

    def test_instructions_survive_missing_metadata(self, tmp_path):
        from laravel_mcp_companion import build_server_instructions

        assert "unknown" in build_server_instructions(tmp_path, "13.x")
```

- [ ] **Step 2: Run test to verify it fails**

Run: `.venv/bin/python -m pytest tests/unit/test_docs_freshness.py -q --no-cov -p no:cacheprovider -k Instructions`
Expected: FAIL, the phrase "reflects Laravel's documentation as of" is absent.

- [ ] **Step 3: Write minimal implementation**

In `laravel_mcp_companion.py`, change the import block at lines 55-58 from
`describe_docs_freshness, get_docs_snapshot_age, docs_are_stale, DOCS_STALE_AFTER_DAYS`
to `describe_documentation_date, get_documentation_date, copy_is_stale, DOCS_STALE_AFTER_DAYS`.

Change line 1168 from `freshness = describe_docs_freshness(...)` to:

```python
    documentation_date = describe_documentation_date(docs_path, runtime_version)
```

Replace the final paragraph of the instructions string with:

```python
    return f"""Laravel documentation for the whole ecosystem: core Laravel \
{', '.join(SUPPORTED_VERSIONS)}, the first-party services (Forge, Vapor, Nova, \
Envoyer), and community packages (Spatie, Livewire, Filament, Inertia).

{workflow}

Documentation answers default to Laravel {runtime_version}; pass `version` to target \
another, or `all_versions` to search every one.

This copy reflects Laravel's documentation as of {documentation_date}. If you are \
asked about a feature that may have been added after that date, say so rather than \
answering as if the documentation covered it. {info_tool} reports this date at any \
time."""
```

Delete the `refresh` local variable and its three branch assignments: the
instructions no longer tell the assistant to refresh, because refreshing cannot
change a date set by upstream.

- [ ] **Step 4: Run test to verify it passes**

Run: `.venv/bin/python -m pytest tests/unit/test_docs_freshness.py -q --no-cov -p no:cacheprovider`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add laravel_mcp_companion.py tests/unit/test_docs_freshness.py
git lc -m "Tell the assistant the documentation's date, not a refresh instruction"
```

---

### Task 3: Update laravel_docs_info

**Files:**
- Modify: `laravel_mcp_companion.py:1567-1615` (the `laravel_docs_info` tool body)
- Test: `tests/unit/test_docs_freshness.py`

**Interfaces:**
- Consumes: `get_documentation_date`, `copy_is_stale` (Task 1).
- Produces: no new API; output fields change.

- [ ] **Step 1: Write the failing test**

```python
# append to tests/unit/test_docs_freshness.py
class TestDocsInfoTool:
    @pytest.mark.asyncio
    async def test_summary_does_not_warn_when_the_copy_is_current(self, tmp_path):
        """The permanent-warning bug: 6.x can never get fresher."""
        from fastmcp import Client

        from laravel_mcp_companion import create_mcp_server

        write_metadata(tmp_path, "6.x", changed_days_ago=425)
        write_metadata(tmp_path, "13.x", changed_days_ago=1)

        server = create_mcp_server("T", tmp_path, "13.x", transform_mode=None)
        async with Client(server) as client:
            result = await client.call_tool("laravel_docs_info", {})
            text = result.content[0].text

        assert "note" not in text, f"warned about a current copy: {text}"
        assert "documentation_current_to" in text

    @pytest.mark.asyncio
    async def test_summary_warns_when_the_whole_copy_is_old(self, tmp_path):
        from fastmcp import Client

        from laravel_mcp_companion import create_mcp_server

        write_metadata(tmp_path, "6.x", changed_days_ago=425)
        write_metadata(tmp_path, "13.x", changed_days_ago=DOCS_STALE_AFTER_DAYS + 5)

        server = create_mcp_server("T", tmp_path, "13.x", transform_mode=None)
        async with Client(server) as client:
            result = await client.call_tool("laravel_docs_info", {})
            text = result.content[0].text

        assert "note" in text
        assert "pull" in text.lower(), "should advise pulling a newer image"
        assert "update_laravel_docs" not in text, "that tool cannot fix a stale image"

    @pytest.mark.asyncio
    async def test_per_version_reports_a_date_and_never_warns(self, tmp_path):
        from fastmcp import Client

        from laravel_mcp_companion import create_mcp_server

        write_metadata(tmp_path, "8.x", changed_days_ago=425)

        server = create_mcp_server("T", tmp_path, "8.x", transform_mode=None)
        async with Client(server) as client:
            result = await client.call_tool("laravel_docs_info", {"version": "8.x"})
            text = result.content[0].text

        assert "documentation_date" in text
        assert "note" not in text, "a version whose upstream stopped is not a problem"
```

- [ ] **Step 2: Run test to verify it fails**

Run: `.venv/bin/python -m pytest tests/unit/test_docs_freshness.py -q --no-cov -p no:cacheprovider -k DocsInfo`
Expected: FAIL, `documentation_current_to` absent and a note present.

- [ ] **Step 3: Write minimal implementation**

In the specific-version branch, replace the snapshot lines with:

```python
            documentation_date, _ = get_documentation_date(docs_path, version)
            info: Dict[str, Any] = {
                "version": version,
                "documentation_date": documentation_date or "unknown",
                "last_updated": metadata.get('sync_time', 'unknown'),
                "commit_sha": metadata.get('commit_sha', 'unknown'),
                "commit_date": metadata.get('commit_date', 'unknown'),
                "commit_message": metadata.get('commit_message', 'unknown'),
                "github_url": metadata.get('commit_url', 'unknown')
            }
            return toon_encode(info)
```

Delete the per-version staleness note entirely.

In the all-versions branch, replace the per-row age lookup with a date, and the
summary with:

```python
                if "version" in metadata:
                    v_date, _ = get_documentation_date(docs_path, v)
                    versions_data.append({
                        "version": v,
                        "documentation_date": v_date or "unknown",
                        "last_updated": metadata.get('sync_time', 'unknown'),
                        "commit": metadata.get('commit_sha', 'unknown')[:7] if metadata.get('commit_sha') else 'unknown',
                        "available": True
                    })
```

```python
            current_to, copy_age = get_documentation_date(docs_path)
            summary: Dict[str, Any] = {
                "documentation_current_to": current_to or "unknown",
                "copy_age_days": copy_age if copy_age is not None else "unknown",
                "default_version": runtime_version,
                "versions": versions_data
            }
            if copy_is_stale(docs_path):
                summary["note"] = (
                    f"No version has changed in over {DOCS_STALE_AFTER_DAYS} days, which "
                    "suggests this copy is behind. Pull a newer image to get current "
                    "documentation."
                )
            return toon_encode(summary)
```

- [ ] **Step 4: Run test to verify it passes**

Run: `.venv/bin/python -m pytest tests/unit/test_docs_freshness.py -q --no-cov -p no:cacheprovider`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add laravel_mcp_companion.py tests/unit/test_docs_freshness.py
git lc -m "Report documentation dates and warn only on a stale copy"
```

---

### Task 4: Rename version_param to version

**Files:**
- Modify: `laravel_mcp_companion.py:1495-1510`
- Test: `tests/unit/test_docs_freshness.py`

**Interfaces:**
- Consumes: nothing new.
- Produces: `update_laravel_docs(version: Optional[str] = None, force: bool = False)`.

- [ ] **Step 1: Write the failing test**

```python
# append to tests/unit/test_docs_freshness.py
class TestUpdateToolParameterName:
    @pytest.mark.asyncio
    async def test_accepts_the_parameter_name_every_other_tool_uses(self, tmp_path):
        """An assistant told to refresh guesses `version`; it used to hard-error."""
        from fastmcp import Client

        from laravel_mcp_companion import create_mcp_server

        write_metadata(tmp_path, "13.x", changed_days_ago=1)
        server = create_mcp_server("T", tmp_path, "13.x", transform_mode=None)

        async with Client(server) as client:
            tools = {t.name: t for t in await client.list_tools()}
            schema = tools["update_laravel_docs"].inputSchema

        assert "version" in schema["properties"]
        assert "version_param" not in schema["properties"]
```

- [ ] **Step 2: Run test to verify it fails**

Run: `.venv/bin/python -m pytest tests/unit/test_docs_freshness.py -q --no-cov -p no:cacheprovider -k ParameterName`
Expected: FAIL, `assert 'version' in {...'version_param'...}`

- [ ] **Step 3: Write minimal implementation**

In `laravel_mcp_companion.py`, rename the parameter and its three uses:

```python
    def update_laravel_docs(version: Optional[str] = None, force: bool = False) -> str:
        """Update Laravel documentation from the official repository.

        Args:
            version: Laravel version branch (e.g., "12.x")
            force: Force update even if already up to date
        """
        logger.debug(f"update_laravel_docs called (version: {version}, force: {force})")

        doc_version = version or runtime_version

        version_error = validate_version_arg(version)
        if version_error:
            return version_error
```

- [ ] **Step 4: Run test to verify it passes**

Run: `.venv/bin/python -m pytest tests/unit/test_docs_freshness.py -q --no-cov -p no:cacheprovider`
Expected: PASS

- [ ] **Step 5: Run the whole suite, ruff and mypy**

```bash
.venv/bin/python -m pytest -q --no-cov -p no:cacheprovider
.venv/bin/ruff check .
.venv/bin/mypy --ignore-missing-imports .
```

Existing tests referencing `version_param`, `docs_are_stale`,
`get_docs_snapshot_age`, `describe_docs_freshness` or `parse_sync_time` must be
updated to the new names. Update assertions to the new behaviour rather than
weakening them — in particular, a test asserting that an old version is stale is
now asserting the bug and should be inverted.

- [ ] **Step 6: Commit**

```bash
git add laravel_mcp_companion.py tests/
git lc -m "Accept `version` on update_laravel_docs"
```

---

### Task 5: Documentation and changelog

**Files:**
- Modify: `CHANGELOG.md`

- [ ] **Step 1: Update the CHANGELOG**

Add under `## [Unreleased]`, in the existing `### Breaking` and `### Fixed` sections:

```markdown
- `update_laravel_docs` takes `version` rather than `version_param`. Every other
  tool takes `version`, so an assistant following the server's own advice
  guessed it and received a hard error.
- `laravel_docs_info` reports `documentation_date` per version and
  `documentation_current_to` / `copy_age_days` in the summary, replacing the
  snapshot-age fields.
```

```markdown
- Documentation currency is reported from the date Laravel last changed each
  version, not the date this project last fetched it. The two diverge for a
  branch that no longer changes, so five of eight shipped versions were being
  reported as stale while byte-identical to upstream, with a warning that no
  tool could clear. The staleness warning now fires only when no version has
  changed recently, which indicates a stale image rather than an end-of-life
  branch.
```

- [ ] **Step 2: Verify the version guard still passes**

Run: `.venv/bin/python -m pytest tests/unit/test_version_consistency.py -q --no-cov -p no:cacheprovider`
Expected: PASS

- [ ] **Step 3: Commit**

```bash
git add CHANGELOG.md
git lc -m "Record the documentation currency change"
```

---

## Self-Review

**Spec coverage.** `commit_date` as the signal — Task 1 (`get_documentation_date`). Bare date, no age phrasing — Task 1 (`describe_documentation_date`) and its test. Warning inverted to the newest change — Task 1 (`copy_is_stale`) and Task 3's summary. No per-version staleness — Task 1 removes the parameter, Task 3 deletes the note, and both are asserted. `version_param` rename — Task 4. Offline preserved — no task adds a network call. Malformed, missing and future timestamps — Task 1's parametrized tests. Field renames — Task 3. Constant name and value unchanged — Global Constraints.

**Placeholders.** None; every code step carries real code and every test step real assertions.

**Type consistency.** `get_documentation_date` returns `tuple[Optional[str], Optional[int]]` in Task 1 and is unpacked as `(date, age)` in Tasks 1, 2 and 3. `copy_is_stale(docs_path) -> bool` is defined in Task 1 with no version argument and called that way in Task 3. `describe_documentation_date` returns `str` and is interpolated into a string in Task 2. `parse_timestamp` is defined in Task 1 and referenced only by its own tests.

**One gap found and closed:** Task 1's step 3 replaces a specific line range, so it must delete `docs_are_stale`'s `age_days` parameter, which Task 3's old call site passed. Task 3 now rewrites that call as `copy_is_stale(docs_path)` with no arguments, and the Global Constraints list every consumer line so none is missed.
