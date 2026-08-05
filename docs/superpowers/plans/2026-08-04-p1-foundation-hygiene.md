# Plan 1: Foundation Hygiene Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Non-breaking cleanup that later v1.0 work builds on: one path-security module, one file cache (the O_NOFOLLOW one everywhere), one version parser, no dead server-side code, no import-time network I/O, no module-global server config, and a coverage gate that measures every product file.

**Architecture:** Extract the duplicated security primitives into a new `path_security.py` leaf module both `mcp_tools.py` and `docs_updater.py` import. Delete `laravel_mcp_companion.py`'s duplicate utility layer and re-export the `mcp_tools` versions so existing importers (including tests) keep working. Version discovery becomes cache-only at import with an explicit network refresh at startup.

**Tech Stack:** Python 3.12, pytest (markers per `pytest.ini`; default run deselects `e2e`/`bench`), coverage.py with `--cov-fail-under=80`.

## Global Constraints

- No breaking changes to the MCP tool surface in this plan — tool names, arguments, and output text stay byte-identical. (The breaking consolidation is Plan 2.)
- Full test suite must pass after every task: `pytest` (uses `pytest.ini` defaults).
- Lint/type gates: `ruff check .` and `mypy --ignore-missing-imports .` clean after every task.
- Personal repo commit-timestamp rule applies: during Toronto weekday business hours commit with `git lc`; otherwise plain `git commit`. Never `git add -A` (the versions cache and docs corpus dirty easily — stage explicit paths).
- Python's stdlib only; no new dependencies.

---

### Task 1: Close the ignore-file gaps

**Files:**
- Modify: `.gitignore`
- Modify: `.dockerignore`

**Interfaces:**
- Consumes: nothing
- Produces: nothing other tasks rely on; pure hygiene

- [ ] **Step 1: Read both ignore files**

Read `.gitignore` and `.dockerignore` fully so additions land in sensible groupings and nothing is duplicated.

- [ ] **Step 2: Add the missing gitignore entries**

Append to `.gitignore` (near the existing test-artifact entries):

```
# Scratch fixture dirs used by some local test runs; never ship or track
test_data/
test_docs/
```

- [ ] **Step 3: Add the missing dockerignore entries**

Append to `.dockerignore` (skip any line already present — check first):

```
test_data/
test_docs/
.channels_cache_v2.json
.users_cache.json
uv.lock
CHANGELOG.md
ROADMAP.md
CONTRIBUTING.md
test_docker_args.sh
CLAUDE.md
htmlcov/
coverage.xml
.coverage
```

- [ ] **Step 4: Verify**

Run: `git check-ignore test_data test_docs && git status --porcelain`
Expected: both paths print (ignored); status shows only the two modified ignore files.

- [ ] **Step 5: Commit**

```bash
git add .gitignore .dockerignore
git commit -m "Ignore scratch test dirs and stop baking repo metadata into the image"
```

---

### Task 2: Delete dead server-side code

**Files:**
- Modify: `toon_helpers.py` (delete `format_search_results`, `format_learning_resource_search`)
- Modify: `mcp_tools.py` (delete `search_laravel_docs_impl`, ~line 914)
- Modify: `laravel_mcp_companion.py` (delete the `update_laravel_docs` / `laravel_docs_info` stubs at ~lines 1221–1230 that return `"This function requires server context to execute"`)
- Modify: `tests/unit/test_toon_helpers.py` (delete the tests for the two dead formatters, ~lines 62–103 plus any `format_learning_resource_search` tests)
- Modify: `tests/unit/test_containment_consistency.py` (retarget from `search_laravel_docs_impl` to `search_laravel_docs_data`)
- Modify: any other test that imports the deleted names (found by grep in Step 1)

**Interfaces:**
- Consumes: `mcp_tools.search_laravel_docs_data(query, version=None, sources=None, limit=...) -> dict` — the live search entry point that replaces the stale `_impl` wrapper. Its return is a dict with keys `query`, `scope`, `results` (list of dicts with `file`, `anchor`, `heading`, `score`, `snippet`, `source`) — or `error`/`context` keys on failure.
- Produces: nothing new; removals only. After this task the names `format_search_results`, `format_learning_resource_search`, `search_laravel_docs_impl`, and the two stubs no longer exist anywhere.

- [ ] **Step 1: Map every reference**

Run: `grep -rn "format_search_results\|format_learning_resource_search\|search_laravel_docs_impl\|requires server context" --include="*.py" .`
Expected: definitions in `toon_helpers.py` / `mcp_tools.py` / `laravel_mcp_companion.py`, references only in test files. If any *production* file references one of these names, stop and re-check — the audit found none.

- [ ] **Step 2: Retarget the containment-consistency test**

`tests/unit/test_containment_consistency.py` exercises search containment through `search_laravel_docs_impl` — a path clients cannot reach. Point it at the live function. The test's structure (build a docs tree with an out-of-tree symlink, search, assert the escaped content never appears) stays; only the call changes:

```python
from mcp_tools import search_laravel_docs_data

def test_search_never_reads_outside_docs_root(tmp_path_docs_with_symlink_escape):
    docs_path, secret_text = tmp_path_docs_with_symlink_escape
    result = search_laravel_docs_data(str(docs_path), "SECRET", version="12.x")
    serialized = str(result)
    assert secret_text not in serialized
```

Match the real signature: open `mcp_tools.py` at `search_laravel_docs_data` (~line 789) first and mirror its actual parameter order — do not guess. Keep every existing assertion scenario in the file, converted the same way (dict result instead of TOON string; assert on `str(result)` or on `result["results"]`).

- [ ] **Step 3: Delete the dead code and dead tests**

Remove the four definitions listed under Files and the tests that exercised the two formatters. Do not leave commented-out remnants.

- [ ] **Step 4: Run the suite**

Run: `pytest tests/unit/test_toon_helpers.py tests/unit/test_containment_consistency.py -v && pytest -q`
Expected: all pass; no `ImportError` anywhere (a failure here means Step 1's grep missed a reference).

- [ ] **Step 5: Commit**

```bash
git add toon_helpers.py mcp_tools.py laravel_mcp_companion.py tests/unit/test_toon_helpers.py tests/unit/test_containment_consistency.py
git commit -m "Delete dead formatters, stale search wrapper, and server-context stubs"
```

---

### Task 3: One path-security module

**Files:**
- Create: `path_security.py`
- Modify: `mcp_tools.py` (move `_no_follow_opener`, `resolve_contained_path`, `is_safe_path` out; re-import)
- Modify: `docs_updater.py` (delete `is_within_directory` body, ~line 165; re-import)
- Test: `tests/unit/test_path_security.py`

**Interfaces:**
- Consumes: nothing from other tasks.
- Produces: module `path_security` with exactly these:
  - `no_follow_opener(path, flags) -> int` — `open()` opener OR-ing `O_NOFOLLOW` (renamed from `_no_follow_opener`; it is now a cross-module API, not a private helper)
  - `resolve_contained_path(base_path: Path, target_path: Path) -> Optional[Path]` — moved verbatim from `mcp_tools.py:142`
  - `is_safe_path(base_path: Path, target_path: Path) -> bool` — moved verbatim
  - `is_within_directory(base_dir: Path, target: Path) -> bool` — kept as an alias: `return is_safe_path(base_dir, target)` (semantics are already identical: resolve both, `is_relative_to`, fail closed)
  - `mcp_tools` re-exports `resolve_contained_path` and `is_safe_path` (plain `from path_security import ...`) so `laravel_mcp_companion.py:70` and all existing tests keep importing from `mcp_tools` unchanged.

- [ ] **Step 1: Write the failing identity + behavior test**

```python
# tests/unit/test_path_security.py
from pathlib import Path

import path_security
import mcp_tools
import docs_updater


def test_single_containment_primitive():
    """Every module's containment check is literally the same function."""
    assert mcp_tools.resolve_contained_path is path_security.resolve_contained_path
    assert mcp_tools.is_safe_path is path_security.is_safe_path
    assert docs_updater.is_within_directory is path_security.is_within_directory


def test_containment_rejects_prefix_sibling(tmp_path):
    base = tmp_path / "docs" / "12.x"
    base.mkdir(parents=True)
    sibling = tmp_path / "docs" / "12.x-backup" / "secret.md"
    sibling.parent.mkdir()
    sibling.write_text("secret")
    assert path_security.resolve_contained_path(base, sibling) is None
    assert path_security.is_within_directory(base, sibling) is False


def test_containment_accepts_inside(tmp_path):
    base = tmp_path / "docs"
    inside = base / "12.x" / "blade.md"
    inside.parent.mkdir(parents=True)
    inside.write_text("x")
    assert path_security.resolve_contained_path(base, inside) == inside.resolve()


def test_no_follow_opener_refuses_symlink(tmp_path):
    target = tmp_path / "real.md"
    target.write_text("content")
    link = tmp_path / "link.md"
    link.symlink_to(target)
    import pytest
    with pytest.raises(OSError):
        open(link, "r", opener=path_security.no_follow_opener)
```

- [ ] **Step 2: Run to verify failure**

Run: `pytest tests/unit/test_path_security.py -v`
Expected: FAIL with `ModuleNotFoundError: No module named 'path_security'`

- [ ] **Step 3: Create the module and rewire imports**

Create `path_security.py` with a module docstring ("Single source of truth for path containment and symlink-refusing opens; both the server and the updater import from here so the rules cannot drift") and the four functions moved verbatim (docstrings included). In `mcp_tools.py`: delete the three moved definitions, add `from path_security import no_follow_opener, resolve_contained_path, is_safe_path`, and update the one internal caller (`get_file_content_cached` passes `opener=no_follow_opener`). Keep a module-level alias `_no_follow_opener = no_follow_opener` only if grep shows tests referencing the old name — otherwise don't. In `docs_updater.py`: delete `is_within_directory`'s body and replace with `from path_security import is_within_directory` (note: `docs_updater` must not import `mcp_tools` — `mcp_tools` imports `docs_updater`, and `path_security` existing as a leaf is what avoids the cycle).

- [ ] **Step 4: Run the full suite**

Run: `pytest tests/unit/test_path_security.py -v && pytest -q && ruff check . && mypy --ignore-missing-imports .`
Expected: all pass. The security suites (`test_security.py`, `test_path_traversal_security.py`, `test_cross_corpus_reads.py`) are the real regression net here — every one must stay green.

- [ ] **Step 5: Commit**

```bash
git add path_security.py mcp_tools.py docs_updater.py tests/unit/test_path_security.py
git commit -m "Extract path containment and O_NOFOLLOW open into one shared module"
```

---

### Task 4: One file cache, one version parser, one validator, one metadata reader

**Files:**
- Modify: `laravel_mcp_companion.py` — delete the duplicate `get_file_content_cached` (~line 881), the module caches `_file_content_cache`/`_search_result_cache`/`_cache_lock` (~lines 103–105), `get_version_from_path` (~line 949), `validate_version` (~line 1289), `get_laravel_docs_metadata` (~line 971); import all four from `mcp_tools`; switch `read_external_laravel_doc`'s direct `open()` (~line 1753) to the cached read
- Test: `tests/unit/test_single_primitives.py` (new)
- Modify: any tests pinning the deleted mtime-keyed cache behavior (found by grep)

**Interfaces:**
- Consumes: from `mcp_tools`: `get_file_content_cached(file_path: str) -> str` (O_NOFOLLOW, path-keyed, 512-entry), `get_version_from_path(path: str, runtime_version: Optional[str] = None) -> tuple[str, str]`, `validate_version(version: str) -> bool`, `get_laravel_docs_metadata(docs_path, version=None) -> dict` (~`mcp_tools.py:512` — confirm its exact signature before wiring), `clear_caches`.
- Produces: `laravel_mcp_companion` re-exports these same names (via `from mcp_tools import ...`), so every existing importer and test keeps working. `clear_file_cache()` survives but its body is exactly one call: `clear_mcp_tools_caches()`. **Security effect later tasks rely on:** the `laravel://` and `laravel-package://` resource handlers now read through the O_NOFOLLOW cache.

- [ ] **Step 1: Map usages of the doomed duplicates**

Run: `grep -rn "get_file_content_cached\|get_version_from_path\|get_laravel_docs_metadata\|validate_version" --include="*.py" laravel_mcp_companion.py tests/ | grep -v mcp_tools`
Expected: calls inside `laravel_mcp_companion.py` (resource handlers, tool bodies, `laravel_docs_info` paths) and test imports. Note which tests import these names *from `laravel_mcp_companion`* — the re-export keeps them working, but any test asserting **mtime-keyed** cache behavior (e.g. rewriting a file and expecting the fresh content without a cache clear) pins the deleted implementation and must be updated to call `clear_file_cache()` between writes.

- [ ] **Step 2: Write the failing test**

```python
# tests/unit/test_single_primitives.py
import laravel_mcp_companion
import mcp_tools


def test_one_file_cache_implementation():
    assert laravel_mcp_companion.get_file_content_cached is mcp_tools.get_file_content_cached


def test_one_version_parser():
    assert laravel_mcp_companion.get_version_from_path is mcp_tools.get_version_from_path


def test_one_metadata_reader():
    assert laravel_mcp_companion.get_laravel_docs_metadata is mcp_tools.get_laravel_docs_metadata


def test_cached_read_refuses_symlink_swap(tmp_path):
    """The TOCTOU regression: a symlink in the final component is refused."""
    secret = tmp_path / "outside.md"
    secret.write_text("SECRET")
    docs = tmp_path / "docs"
    docs.mkdir()
    link = docs / "blade.md"
    link.symlink_to(secret)
    content = laravel_mcp_companion.get_file_content_cached(str(link))
    assert "SECRET" not in content
```

- [ ] **Step 3: Run to verify failure**

Run: `pytest tests/unit/test_single_primitives.py -v`
Expected: the three identity tests FAIL (different function objects); the symlink test FAILS (the current mtime-keyed cache uses a plain `open()` and serves the secret).

- [ ] **Step 4: Delete duplicates, rewire, fix pinned tests**

In `laravel_mcp_companion.py`: extend the existing `from mcp_tools import (...)` block with `get_file_content_cached`, `get_version_from_path`, `get_laravel_docs_metadata`; delete the four local definitions and the module cache dicts; the local `validate_version` is deleted outright (the import block at ~line 71 already brings in `validate_version as validate_version_arg` — grep for bare `validate_version(` calls and point them at `validate_version_arg`). If Step 1's grep shows tests importing `validate_version` *from `laravel_mcp_companion`*, keep the name alive as an identity alias — `validate_version = validate_version_arg` — so those imports resolve to the single `mcp_tools` implementation. `clear_file_cache()` keeps its name and docstring, body becomes the single delegate call. In `read_external_laravel_doc`, replace the `with open(safe_path...)` block with `content = get_file_content_cached(str(safe_path))` followed by the same return. Update any mtime-pinning tests found in Step 1 to clear the cache explicitly.

- [ ] **Step 5: Run the full suite**

Run: `pytest tests/unit/test_single_primitives.py -v && pytest -q && ruff check . && mypy --ignore-missing-imports .`
Expected: all pass. Pay attention to update-flow tests (docs update → read fresh content): they pass because the update tools call `clear_file_cache()`; if one fails, the fix is a missing cache clear in the *test*, not a revert to mtime keying.

- [ ] **Step 6: Commit**

```bash
git add laravel_mcp_companion.py tests/unit/test_single_primitives.py
git commit -m "Collapse duplicate cache, version, and metadata helpers onto mcp_tools; close the resource-path TOCTOU"
```

---

### Task 5: Kill the `_server_config` module global

**Files:**
- Modify: `laravel_mcp_companion.py` — `create_mcp_server` (~line 1561): delete the `global _server_config` assignment (~lines 1577–1582) and the module-level `_server_config: Dict[str, Any] = {}` (~line 1808); `read_laravel_doc` (~line 1680) uses the closure's `docs_path`/`runtime_version` directly
- Test: `tests/unit/test_multi_instance.py` (new)

**Interfaces:**
- Consumes: `create_mcp_server(server_name, docs_path, runtime_version, transform_mode=..., auth=None, rate_limiter=None) -> FastMCP` — unchanged signature.
- Produces: no `_server_config` symbol anywhere. Two servers created in one process serve their own docs paths. Plan 2's `tools/` split relies on handlers taking configuration from arguments, not globals.

- [ ] **Step 1: Write the failing test**

```python
# tests/unit/test_multi_instance.py
import asyncio
import pytest
from fastmcp import Client

from laravel_mcp_companion import create_mcp_server


def _make_docs(tmp_path, name, marker):
    docs = tmp_path / name
    (docs / "12.x").mkdir(parents=True)
    (docs / "12.x" / "blade.md").write_text(f"# Blade\n\n{marker}\n")
    return docs


@pytest.mark.asyncio
async def test_two_servers_serve_their_own_docs(tmp_path):
    docs_a = _make_docs(tmp_path, "a", "MARKER-ALPHA")
    docs_b = _make_docs(tmp_path, "b", "MARKER-BETA")
    server_a = create_mcp_server("a", docs_a, "12.x", transform_mode=None)
    server_b = create_mcp_server("b", docs_b, "12.x", transform_mode=None)

    async with Client(server_a) as client_a:
        content_a = await client_a.read_resource("laravel://12.x/blade.md")
    async with Client(server_b) as client_b:
        content_b = await client_b.read_resource("laravel://12.x/blade.md")

    assert "MARKER-ALPHA" in content_a[0].text  # fails today: A serves B's docs
    assert "MARKER-BETA" in content_b[0].text
```

Check `pytest.ini` / existing protocol tests for the async plugin in use (`pytest-asyncio` vs `anyio`) and match the existing convention — copy the decorator style from `tests/protocol/test_mcp_compliance.py` rather than assuming.

- [ ] **Step 2: Run to verify failure**

Run: `pytest tests/unit/test_multi_instance.py -v`
Expected: first assertion FAILS — creating server B repointed the shared `_server_config`, so server A serves MARKER-BETA.

- [ ] **Step 3: Delete the global**

In `create_mcp_server`, remove the `global _server_config` block. In `read_laravel_doc`, replace `config = _server_config`, `config.get('version')`, and `Path(config['docs_path'])` with the closure variables `runtime_version` and `docs_path`. Delete the module-level declaration at ~line 1808. Run `grep -n "_server_config" laravel_mcp_companion.py tests/ -r` — zero hits remain (update any test that pokes it).

- [ ] **Step 4: Run the full suite**

Run: `pytest tests/unit/test_multi_instance.py -v && pytest -q`
Expected: all pass.

- [ ] **Step 5: Commit**

```bash
git add laravel_mcp_companion.py tests/unit/test_multi_instance.py
git commit -m "Drop the module-global server config; resource handlers use their closure"
```

---

### Task 6: No network I/O at import time

**Files:**
- Modify: `docs_updater.py` — module scope ~lines 306–318 and `get_supported_versions` (~line 235)
- Modify: `mcp_tools.py` — `get_version_from_path`'s default-version lookup (~line 138), module `SUPPORTED_VERSIONS` (~line 54)
- Modify: `laravel_mcp_companion.py` — call the new refresh at startup in `setup_server_environment` (~line 1301) or `main`; migrate any `DEFAULT_VERSION` uses
- Test: `tests/unit/test_import_time.py` (new)

**Interfaces:**
- Consumes: `_read_versions_cache(cache_file, max_age_seconds=None) -> list[str] | None` and `get_supported_versions(cache_file=None) -> list[str]` — both already exist in `docs_updater.py`.
- Produces (all in `docs_updater`):
  - Import-time `SUPPORTED_VERSIONS` is now resolved **cache-only**: `_read_versions_cache(VERSIONS_CACHE_FILE)` (no TTL — stale is fine at import) falling back to `LAST_RESORT_VERSIONS`. No `urlopen`, no cache write, at import. It stays a plain `list[str]` and — critically — **the same list object forever**: refresh mutates it in place, so `mcp_tools.SUPPORTED_VERSIONS` and `laravel_mcp_companion.SUPPORTED_VERSIONS` (bindings to the same object) see updates.
  - `refresh_supported_versions() -> list[str]` — the explicit, network-allowed resolution: calls `get_supported_versions()`, then `SUPPORTED_VERSIONS[:] = result`, returns it. Called once at server startup.
  - `get_default_version() -> str` — `return SUPPORTED_VERSIONS[-1]`. Replaces reads of the `DEFAULT_VERSION` constant (which is frozen at import and goes stale after refresh). Keep `DEFAULT_VERSION = SUPPORTED_VERSIONS[-1]` as a module attribute for back-compat, but migrate `mcp_tools.get_version_from_path` and every use in `laravel_mcp_companion.py` (grep) to `get_default_version()`.

- [ ] **Step 1: Write the failing tests**

```python
# tests/unit/test_import_time.py
import subprocess
import sys

import docs_updater


def test_import_performs_no_network_io():
    """Importing the server must not open sockets or write the versions cache."""
    code = (
        "import socket\n"
        "class Boom(Exception): pass\n"
        "def _no(*a, **k): raise Boom('socket at import')\n"
        "socket.socket = _no\n"
        "socket.create_connection = _no\n"
        "import laravel_mcp_companion\n"
        "print('CLEAN-IMPORT')\n"
    )
    result = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True, timeout=60)
    assert "CLEAN-IMPORT" in result.stdout, result.stderr


def test_refresh_mutates_shared_list_in_place(monkeypatch):
    before = docs_updater.SUPPORTED_VERSIONS
    monkeypatch.setattr(docs_updater, "get_supported_versions", lambda cache_file=None: ["6.x", "12.x", "99.x"])
    result = docs_updater.refresh_supported_versions()
    assert result == ["6.x", "12.x", "99.x"]
    assert docs_updater.SUPPORTED_VERSIONS is before          # same object
    assert docs_updater.get_default_version() == "99.x"


def test_default_version_tracks_refresh(monkeypatch):
    monkeypatch.setattr(docs_updater, "get_supported_versions", lambda cache_file=None: ["12.x", "13.x"])
    docs_updater.refresh_supported_versions()
    import mcp_tools
    version, rel = mcp_tools.get_version_from_path("blade.md")
    assert version == "13.x"
```

Note: `refresh_supported_versions` mutating module state leaks across tests — add a `conftest`-level fixture or in-test `finally` restoring the original list contents (`SUPPORTED_VERSIONS[:] = saved`) so test order doesn't matter.

- [ ] **Step 2: Run to verify failure**

Run: `pytest tests/unit/test_import_time.py -v`
Expected: the subprocess test FAILS whenever the checked-in `docs/.versions_cache.json` is past its 24h TTL (today's import path goes to the network on TTL lapse); the other two FAIL with `AttributeError: refresh_supported_versions`. If the cache happens to be fresh the first test passes by luck — the implementation change is still required; rely on the other two failures.

- [ ] **Step 3: Implement**

In `docs_updater.py`, replace lines ~306–318 with:

```python
_SUPPORTED_VERSIONS_CACHE = None

def get_cached_supported_versions() -> list[str]:
    """Cache-only at first call (import time); refresh_supported_versions() adds network."""
    global _SUPPORTED_VERSIONS_CACHE
    if _SUPPORTED_VERSIONS_CACHE is None:
        _SUPPORTED_VERSIONS_CACHE = (
            _read_versions_cache(VERSIONS_CACHE_FILE) or list(LAST_RESORT_VERSIONS)
        )
    return _SUPPORTED_VERSIONS_CACHE

SUPPORTED_VERSIONS = get_cached_supported_versions()
DEFAULT_VERSION = SUPPORTED_VERSIONS[-1]

def get_default_version() -> str:
    return SUPPORTED_VERSIONS[-1]

def refresh_supported_versions() -> list[str]:
    """Resolve versions with network allowed and update every module's view in place."""
    resolved = get_supported_versions()
    SUPPORTED_VERSIONS[:] = resolved
    return SUPPORTED_VERSIONS
```

In `mcp_tools.py` `get_version_from_path`, replace the `DEFAULT_VERSION` read with `docs_updater.get_default_version()` (add `import docs_updater`; the existing `from docs_updater import ...` names can stay). Grep `laravel_mcp_companion.py` for `DEFAULT_VERSION` and migrate the same way. In `setup_server_environment` (or `main`, whichever runs unconditionally before `create_mcp_server`), add:

```python
from docs_updater import refresh_supported_versions
refresh_supported_versions()
```

wrapped in `try/except Exception` with a `logger.warning` — startup must not die because GitHub is down; the cache/last-resort list already loaded at import.

- [ ] **Step 4: Run the suite and the worktree check**

Run: `pytest tests/unit/test_import_time.py -v && pytest -q && python -c "import laravel_mcp_companion" && git status --porcelain docs/.versions_cache.json`
Expected: tests pass; the final status line prints **nothing** — importing no longer rewrites the versions cache (this has been dirtying worktrees on every TTL lapse).

- [ ] **Step 5: Commit**

```bash
git add docs_updater.py mcp_tools.py laravel_mcp_companion.py tests/unit/test_import_time.py
git commit -m "Resolve versions cache-only at import; network refresh happens explicitly at startup"
```

---

### Task 7: Coverage gate measures every product file

**Files:**
- Modify: `pyproject.toml` (`[tool.coverage.run] source` gains `doc_search`, `metrics`, `tool_schemas`)
- Modify: `tests/conftest.py` (delete the redundant marker re-registration at ~lines 16–22 — `pytest.ini` owns markers and `--strict-markers` enforces them)
- Test: `tests/unit/test_doc_search.py` (create or extend)
- Test: `tests/unit/test_metrics_registry.py` (create or extend — check for an existing metrics test file first and extend it instead of duplicating)

**Interfaces:**
- Consumes: `doc_search`: `chunk_markdown(text, filename, version) -> list[Section]`, `Section(version, filename, anchor, heading, text)`, `BM25Index().build(docs)/.query(text, top_k)`, `extract_snippet(text, query, max_chars=300)`, `get_index(docs_path, key, loader)`, `clear_indexes()`, `resident_index_count()`, `MAX_RESIDENT_INDEXES = 8`. `metrics`: `MetricsRegistry`, `render_prometheus(reg)`, `BUCKETS`.
- Produces: a coverage figure that includes the retrieval engine, making the README's "product coverage" claim true. The gate stays `--cov-fail-under=80`.

- [ ] **Step 1: Include the files and measure the real number**

In `pyproject.toml`, add `"doc_search", "metrics", "tool_schemas"` to `[tool.coverage.run] source`. Run: `pytest -q 2>&1 | tail -20`
Expected: suite passes; note the per-file coverage for the three new entries. Existing tests exercise them transitively, so the gap is likely small — the next steps close whatever remains. If total is already ≥80 and per-file coverage of `doc_search.py` is ≥80, write only the tests below that cover *uncovered* lines (check `pytest --cov --cov-report=term-missing -q | grep -A2 doc_search`).

- [ ] **Step 2: Write direct doc_search tests (failing only if behavior is broken — these are gap-fillers, TDD against the coverage report)**

```python
# tests/unit/test_doc_search.py
from pathlib import Path

from doc_search import (
    BM25Index, chunk_markdown, clear_indexes, extract_snippet,
    get_index, resident_index_count, MAX_RESIDENT_INDEXES, Section,
)

DOC = """# Blade

Intro paragraph before any section.

<a name="displaying-data"></a>
## Displaying Data

You may display data passed to your Blade views.

<a name="raw-echos"></a>
## Raw Echos

Use double curly braces.
"""


def test_chunk_preamble_kept_and_anchors_attached():
    sections = chunk_markdown(DOC, "blade.md", "12.x")
    assert sections[0].heading == "Blade"            # preamble stays reachable
    assert sections[1].heading == "Displaying Data"
    assert sections[1].anchor == "displaying-data"   # anchor carried from previous chunk
    assert sections[2].anchor == "raw-echos"


def test_bm25_ranks_matching_doc_first_and_omits_zero_scores():
    index = BM25Index()
    index.build(["queues and failed jobs retry", "blade templates", "eloquent models"])
    hits = index.query("retry failed queue job", top_k=3)
    assert hits[0][0] == 0
    assert all(score > 0 for _, score in hits)


def test_bm25_empty_query_and_empty_index():
    index = BM25Index()
    index.build([])
    assert index.query("anything", top_k=5) == []
    index.build(["some document"])
    assert index.query("", top_k=5) == []


def test_snippet_short_text_returned_whole():
    assert extract_snippet("short body", "query") == "short body"


def test_snippet_no_match_falls_back_to_start():
    body = ("line one of the document\n" * 40).strip()
    snippet = extract_snippet(body, "zzzunfindable")
    assert snippet.endswith("...")
    assert snippet.startswith("line one")


def test_snippet_windows_around_match():
    body = "padding " * 100 + "NEEDLE in context" + " trailing" * 100
    snippet = extract_snippet(body, "needle")
    assert "NEEDLE" in snippet


def test_index_registry_lru_eviction(tmp_path):
    clear_indexes()
    loader = lambda: [Section("12.x", "a.md", None, "A", "text body")]
    for i in range(MAX_RESIDENT_INDEXES + 2):
        get_index(tmp_path, f"key-{i}", loader)
    assert resident_index_count() == MAX_RESIDENT_INDEXES
    clear_indexes()
    assert resident_index_count() == 0
```

- [ ] **Step 3: Write direct metrics tests**

```python
# tests/unit/test_metrics_registry.py
from metrics import BUCKETS, MetricsRegistry, render_prometheus


def test_tool_call_lands_in_correct_bucket_and_renders():
    reg = MetricsRegistry()
    reg.record_tool_call("search_laravel_docs", 0.010, ok=True)   # second bucket (0.025)
    reg.record_tool_call("search_laravel_docs", 99.0, ok=False)   # overflow bucket
    reg.record_request("tools/call")
    reg.set_info("0.13.0")
    out = render_prometheus(reg)
    assert 'laravel_mcp_tool_calls_total{status="ok",tool="search_laravel_docs"} 1' in out
    assert 'laravel_mcp_tool_calls_total{status="error",tool="search_laravel_docs"} 1' in out
    assert 'laravel_mcp_tool_call_seconds_bucket{le="+Inf"} 2' in out
    assert 'laravel_mcp_requests_total{method="tools/call"} 1' in out
    assert 'laravel_mcp_info{version="0.13.0"} 1' in out


def test_gauge_none_and_raising_gauges_are_omitted():
    reg = MetricsRegistry()
    reg.set_gauge_callable("gone", lambda: None)
    def boom():
        raise RuntimeError("scrape-time failure")
    reg.set_gauge_callable("broken", boom)
    reg.set_gauge_callable("present", lambda: 4.5)
    out = render_prometheus(reg)
    assert "gone" not in out
    assert "broken" not in out
    assert "present 4.5" in out


def test_reset_clears_everything():
    reg = MetricsRegistry()
    reg.record_tool_call("x", 0.001, ok=True)
    reg.reset()
    snap = reg.snapshot()
    assert snap["tool_calls"] == {} and snap["duration_count"] == 0
```

- [ ] **Step 4: Run with coverage and confirm the gate**

Run: `pytest -q && pytest --cov --cov-report=term-missing -q 2>&1 | tail -15`
Expected: suite green, total ≥80 with the three files included. If `doc_search.py` still shows uncovered branches (e.g. the trailing-anchor carry at `doc_search.py:63-69` or snippet boundary trimming at `:186-195`), add one targeted test per missing branch — the term-missing output names the lines.

- [ ] **Step 5: Fix the conftest marker duplication**

Delete the marker re-registration block in `tests/conftest.py` (~lines 16–22). Run: `pytest -q` — `--strict-markers` passing proves `pytest.ini` alone covers every marker in use.

- [ ] **Step 6: Commit**

```bash
git add pyproject.toml tests/conftest.py tests/unit/test_doc_search.py tests/unit/test_metrics_registry.py
git commit -m "Measure doc_search, metrics, and tool_schemas in the coverage gate"
```

---

## Verification (end of plan)

- `pytest -q` green; `pytest -m e2e` green (transport smoke tests still work).
- `ruff check .` and `mypy --ignore-missing-imports .` clean.
- `grep -rn "_server_config\|search_laravel_docs_impl\|format_search_results" --include="*.py" .` → no hits.
- `python -c "import laravel_mcp_companion"` leaves `git status --porcelain` empty.
- Coverage report includes `doc_search.py`, `metrics.py`, `tool_schemas.py`; total ≥80%.
