# Automated Version Handling Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Eliminate all manual steps when a new Laravel version branch appears on GitHub.

**Architecture:** Replace hardcoded fallback version lists with a `docs/.versions_cache.json` file that is written on every successful GitHub API fetch and read as fallback when the API fails. Remove the pinned Dockerfile `ENV VERSION`. Make README examples version-agnostic.

**Tech Stack:** Python 3.12, pytest, JSON file I/O

---

### File Map

| File | Action | Responsibility |
|------|--------|----------------|
| `docs/.versions_cache.json` | Create | Cached version list, committed to repo |
| `docs_updater.py:129-172` | Modify | Rewrite `get_supported_versions()` to use three-tier resolution |
| `Dockerfile:25` | Modify | Remove `ENV VERSION` line |
| `README.md:93,101,212` | Modify | Make version examples agnostic |
| `tests/unit/test_docs_updater.py:1242-1296` | Modify | Update fallback tests to use cache file |
| `tests/unit/test_runtime_version.py:247-260` | Modify | Update `test_fallback_list_includes_current_latest` to check cache file |
| `tests/unit/test_runtime_version.py` | Modify | Add cache-path tests to `TestNewVersionSimulation` |

---

### Task 1: Create the versions cache file

**Files:**
- Create: `docs/.versions_cache.json`

- [ ] **Step 1: Create the cache file with current versions**

```json
{
  "versions": ["6.x", "7.x", "8.x", "9.x", "10.x", "11.x", "12.x", "13.x"],
  "updated_at": "2026-04-05T00:00:00Z"
}
```

- [ ] **Step 2: Commit**

```bash
git add docs/.versions_cache.json
git commit -m "Add versions cache file for fallback resolution"
```

---

### Task 2: Rewrite `get_supported_versions()` with three-tier resolution

**Files:**
- Modify: `docs_updater.py:129-172`

- [ ] **Step 1: Write failing tests for cache read/write behavior**

Add these tests to `tests/unit/test_docs_updater.py` in the `TestVersionSupport` class. They test the new cache file behavior.

```python
@patch('docs_updater.urllib.request.urlopen')
def test_get_supported_versions_writes_cache_on_success(self, mock_urlopen, tmp_path):
    """Test that successful API fetch writes the cache file."""
    mock_response_data = [
        {"name": "6.x"}, {"name": "12.x"}, {"name": "13.x"},
        {"name": "master"},
    ]
    mock_response = MagicMock()
    mock_response.read.return_value = json.dumps(mock_response_data).encode()
    mock_response.__enter__ = lambda self: self
    mock_response.__exit__ = lambda self, *args: None
    mock_urlopen.return_value = mock_response

    cache_file = tmp_path / ".versions_cache.json"
    versions = get_supported_versions(cache_file=cache_file)

    assert versions == ["6.x", "12.x", "13.x"]
    assert cache_file.exists()
    cached = json.loads(cache_file.read_text())
    assert cached["versions"] == ["6.x", "12.x", "13.x"]
    assert "updated_at" in cached

@patch('docs_updater.urllib.request.urlopen')
def test_get_supported_versions_reads_cache_on_api_failure(self, mock_urlopen, tmp_path):
    """Test that API failure falls back to cache file."""
    cache_file = tmp_path / ".versions_cache.json"
    cache_file.write_text(json.dumps({
        "versions": ["6.x", "11.x", "12.x", "13.x"],
        "updated_at": "2026-04-01T00:00:00Z"
    }))
    mock_urlopen.side_effect = Exception("API down")

    versions = get_supported_versions(cache_file=cache_file)

    assert versions == ["6.x", "11.x", "12.x", "13.x"]

@patch('docs_updater.urllib.request.urlopen')
def test_get_supported_versions_corrupt_cache_uses_last_resort(self, mock_urlopen, tmp_path):
    """Test that corrupt cache file falls through to last resort."""
    cache_file = tmp_path / ".versions_cache.json"
    cache_file.write_text("not valid json{{{")
    mock_urlopen.side_effect = Exception("API down")

    versions = get_supported_versions(cache_file=cache_file)

    assert versions == ["12.x"]

@patch('docs_updater.urllib.request.urlopen')
def test_get_supported_versions_missing_cache_uses_last_resort(self, mock_urlopen, tmp_path):
    """Test that missing cache file falls through to last resort."""
    cache_file = tmp_path / "nonexistent" / ".versions_cache.json"
    mock_urlopen.side_effect = Exception("API down")

    versions = get_supported_versions(cache_file=cache_file)

    assert versions == ["12.x"]
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `.venv/bin/python -m pytest -o "addopts=" tests/unit/test_docs_updater.py::TestVersionSupport::test_get_supported_versions_writes_cache_on_success tests/unit/test_docs_updater.py::TestVersionSupport::test_get_supported_versions_reads_cache_on_api_failure tests/unit/test_docs_updater.py::TestVersionSupport::test_get_supported_versions_corrupt_cache_uses_last_resort tests/unit/test_docs_updater.py::TestVersionSupport::test_get_supported_versions_missing_cache_uses_last_resort -v`

Expected: FAIL — `get_supported_versions()` doesn't accept a `cache_file` parameter yet.

- [ ] **Step 3: Rewrite `get_supported_versions()` in `docs_updater.py`**

Replace the entire function at lines 129-172 with:

```python
# Default cache file path (relative to this script)
VERSIONS_CACHE_FILE = Path(__file__).parent / "docs" / ".versions_cache.json"

LAST_RESORT_VERSIONS = ["12.x"]


def _write_versions_cache(versions: list[str], cache_file: Path) -> None:
    """Write versions to cache file. Errors are logged but not raised."""
    try:
        cache_file.parent.mkdir(parents=True, exist_ok=True)
        cache_file.write_text(json.dumps({
            "versions": versions,
            "updated_at": datetime.now(timezone.utc).isoformat()
        }, indent=2))
    except Exception as e:
        logger.warning(f"Failed to write versions cache: {e}")


def _read_versions_cache(cache_file: Path) -> list[str] | None:
    """Read versions from cache file. Returns None if unavailable or corrupt."""
    try:
        if not cache_file.exists():
            return None
        data = json.loads(cache_file.read_text())
        versions = data.get("versions")
        if isinstance(versions, list) and len(versions) > 0:
            return versions
        return None
    except Exception as e:
        logger.warning(f"Failed to read versions cache: {e}")
        return None


def get_supported_versions(cache_file: Path | None = None) -> list[str]:
    """Get supported Laravel versions with three-tier fallback.

    1. GitHub API (writes cache on success)
    2. Cache file (docs/.versions_cache.json)
    3. Last resort: ["12.x"]

    Args:
        cache_file: Override cache file path (for testing). Defaults to VERSIONS_CACHE_FILE.

    Returns:
        List of supported version branches (e.g., ['6.x', '7.x', '8.x', ...])
    """
    if cache_file is None:
        cache_file = VERSIONS_CACHE_FILE

    logger.debug("Fetching supported Laravel versions from GitHub API")

    url = f"{GITHUB_API_URL}/repos/{LARAVEL_DOCS_REPO}/branches"

    try:
        request = urllib.request.Request(
            url,
            headers={
                "User-Agent": USER_AGENT,
                "Accept": "application/vnd.github.v3+json"
            }
        )

        with urllib.request.urlopen(request) as response:
            branches = json.loads(response.read().decode())

            version_branches = []
            for branch in branches:
                name = branch["name"]
                if re.match(r'^\d+\.x$', name):
                    major_version = int(name.split('.')[0])
                    if major_version >= 6:
                        version_branches.append(name)

            version_branches.sort(key=lambda v: int(v.split('.')[0]))

            if not version_branches:
                logger.warning("No version branches found from API, trying cache")
                cached = _read_versions_cache(cache_file)
                if cached:
                    return cached
                logger.warning("No cache available, using last resort")
                return LAST_RESORT_VERSIONS

            logger.debug(f"Found {len(version_branches)} supported versions: {', '.join(version_branches)}")
            _write_versions_cache(version_branches, cache_file)
            return version_branches

    except Exception as e:
        logger.warning(f"Error fetching versions from GitHub API: {e}, trying cache")
        cached = _read_versions_cache(cache_file)
        if cached:
            return cached
        logger.warning("No cache available, using last resort")
        return LAST_RESORT_VERSIONS
```

Add `from datetime import datetime, timezone` to the imports at the top of the file if not already present. Add `from pathlib import Path` if not already present.

- [ ] **Step 4: Run the new tests to verify they pass**

Run: `.venv/bin/python -m pytest -o "addopts=" tests/unit/test_docs_updater.py::TestVersionSupport -v`

Expected: All `TestVersionSupport` tests PASS.

- [ ] **Step 5: Commit**

```bash
git add docs_updater.py tests/unit/test_docs_updater.py
git commit -m "Replace hardcoded fallback lists with cache-based version resolution"
```

---

### Task 3: Update existing fallback tests

**Files:**
- Modify: `tests/unit/test_docs_updater.py:1242-1296`

The existing tests `test_get_supported_versions_no_versions_found` and `test_get_supported_versions_api_error` still assert against the old hardcoded list behavior. They need to be updated to pass a `cache_file` or use `tmp_path` so they exercise the new fallback logic.

- [ ] **Step 1: Update `test_get_supported_versions_no_versions_found`**

Replace the test at line 1242:

```python
@patch('docs_updater.urllib.request.urlopen')
def test_get_supported_versions_no_versions_found(self, mock_urlopen, tmp_path):
    """Test version fetching when no valid versions found uses cache."""
    mock_response_data = [
        {"name": "master"},
        {"name": "develop"},
        {"name": "feature-branch"},
    ]

    mock_response = MagicMock()
    mock_response.read.return_value = json.dumps(mock_response_data).encode()
    mock_response.__enter__ = lambda self: self
    mock_response.__exit__ = lambda self, *args: None
    mock_urlopen.return_value = mock_response

    # With a cache file present, should use cached versions
    cache_file = tmp_path / ".versions_cache.json"
    cache_file.write_text(json.dumps({
        "versions": ["6.x", "11.x", "12.x", "13.x"],
        "updated_at": "2026-04-01T00:00:00Z"
    }))

    versions = get_supported_versions(cache_file=cache_file)

    assert "12.x" in versions
    assert len(versions) > 0
```

- [ ] **Step 2: Update `test_get_supported_versions_api_error`**

Replace the test at line 1286:

```python
@patch('docs_updater.urllib.request.urlopen')
def test_get_supported_versions_api_error(self, mock_urlopen, tmp_path):
    """Test version fetching with API error falls back to cache."""
    mock_urlopen.side_effect = Exception("API Error")

    cache_file = tmp_path / ".versions_cache.json"
    cache_file.write_text(json.dumps({
        "versions": ["6.x", "11.x", "12.x", "13.x"],
        "updated_at": "2026-04-01T00:00:00Z"
    }))

    versions = get_supported_versions(cache_file=cache_file)

    assert isinstance(versions, list)
    assert len(versions) > 0
    assert "12.x" in versions
```

- [ ] **Step 3: Run updated tests**

Run: `.venv/bin/python -m pytest -o "addopts=" tests/unit/test_docs_updater.py::TestVersionSupport -v`

Expected: All PASS.

- [ ] **Step 4: Commit**

```bash
git add tests/unit/test_docs_updater.py
git commit -m "Update fallback tests to use cache-based version resolution"
```

---

### Task 4: Update `TestNewVersionSimulation` with cache tests

**Files:**
- Modify: `tests/unit/test_runtime_version.py:247-260`

- [ ] **Step 1: Replace `test_fallback_list_includes_current_latest` and add cache test**

Replace the existing `test_fallback_list_includes_current_latest` method in `TestNewVersionSimulation` with these two tests:

```python
def test_cache_file_contains_current_default(self):
    """Committed cache file includes the current DEFAULT_VERSION."""
    from docs_updater import DEFAULT_VERSION, VERSIONS_CACHE_FILE
    import json
    assert VERSIONS_CACHE_FILE.exists(), f"Cache file missing: {VERSIONS_CACHE_FILE}"
    data = json.loads(VERSIONS_CACHE_FILE.read_text())
    assert DEFAULT_VERSION in data["versions"], (
        f"Cache file is stale: missing {DEFAULT_VERSION}"
    )

def test_api_failure_with_cache_returns_cached_versions(self, tmp_path):
    """When API fails, the cache file provides the fallback."""
    import json
    from docs_updater import get_supported_versions
    cache_file = tmp_path / ".versions_cache.json"
    cache_file.write_text(json.dumps({
        "versions": self.FUTURE_VERSIONS,
        "updated_at": "2026-04-05T00:00:00Z"
    }))

    with patch('docs_updater.urllib.request.urlopen') as mock_urlopen:
        mock_urlopen.side_effect = Exception("API down")
        versions = get_supported_versions(cache_file=cache_file)

    assert versions == self.FUTURE_VERSIONS
    assert self.FUTURE_VERSION in versions
```

- [ ] **Step 2: Run tests**

Run: `.venv/bin/python -m pytest -o "addopts=" tests/unit/test_runtime_version.py::TestNewVersionSimulation -v`

Expected: All PASS.

- [ ] **Step 3: Commit**

```bash
git add tests/unit/test_runtime_version.py
git commit -m "Add cache-based fallback tests to version simulation suite"
```

---

### Task 5: Remove `ENV VERSION` from Dockerfile

**Files:**
- Modify: `Dockerfile:25`

- [ ] **Step 1: Remove the VERSION env line**

Delete this line from `Dockerfile`:
```dockerfile
ENV VERSION="13.x"
```

- [ ] **Step 2: Verify Docker builds**

Run: `docker build -t laravel-mcp-test . 2>&1 | tail -5`

Expected: Build succeeds.

- [ ] **Step 3: Commit**

```bash
git add Dockerfile
git commit -m "Remove pinned VERSION env from Dockerfile"
```

---

### Task 6: Make README examples version-agnostic

**Files:**
- Modify: `README.md:93,101,212`

- [ ] **Step 1: Update version references**

Line 93 — change the Docker example:
```bash
# Pin to a specific older Laravel version
docker run --rm -i ghcr.io/brianirish/laravel-mcp-companion:latest --version 11.x
```

Line 101 — update the options table:
```
| `--version VERSION` | Laravel version (e.g., "11.x", "12.x") | Latest |
```

Line 212 — update the Inspector example:
```bash
npx @modelcontextprotocol/inspector python laravel_mcp_companion.py --version 11.x
```

- [ ] **Step 2: Commit**

```bash
git add README.md
git commit -m "Make README version examples agnostic"
```

---

### Task 7: Run full test suite and verify

**Files:** None (verification only)

- [ ] **Step 1: Run the full test suite**

Run: `.venv/bin/python -m pytest -o "addopts=" tests/ -v`

Expected: All tests PASS (442+ tests).

- [ ] **Step 2: Verify no hardcoded fallback lists remain**

Run: `grep -n '"6.x", "7.x", "8.x"' docs_updater.py`

Expected: No matches.

- [ ] **Step 3: Verify no pinned VERSION in Dockerfile**

Run: `grep 'ENV VERSION' Dockerfile`

Expected: No matches.
