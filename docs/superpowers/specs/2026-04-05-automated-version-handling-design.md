# Automated Version Handling

**Date:** 2026-04-05
**Status:** Approved
**Goal:** Eliminate all manual steps when a new Laravel version (e.g., 14.x) is released.

## Problem

When Laravel releases a new version branch, several hardcoded values break:
- Fallback version lists in `docs_updater.py` (lines 165, 172)
- `Dockerfile` `ENV VERSION` pinned to a specific version
- README examples referencing specific versions

The runtime code already resolves versions dynamically from the GitHub API, but the fallback path and Docker/docs are manual.

## Design

### Cache-based Fallback (`docs/.versions_cache.json`)

Replace the two hardcoded fallback lists in `get_supported_versions()` with a file-based cache that is maintained by both CI and runtime.

**File format:**
```json
{
  "versions": ["6.x", "7.x", "8.x", "9.x", "10.x", "11.x", "12.x", "13.x"],
  "updated_at": "2026-04-05T00:00:00Z"
}
```

**Three-tier resolution in `get_supported_versions()`:**
1. GitHub API succeeds -> write result to `docs/.versions_cache.json`, return it
2. API fails -> read `docs/.versions_cache.json`, return cached versions
3. Cache file also missing/corrupt -> return `["12.x"]` as absolute last resort

The last resort is intentionally a single old-but-stable version, not a maintained list. It's the "something is very wrong but don't crash" path.

### CI Integration

The daily `docs-update` workflow already runs `docs_updater.py` which calls `get_supported_versions()`. On success, this writes `docs/.versions_cache.json`. The workflow already does `git add docs/`, so the cache file is committed alongside doc changes automatically. No new workflow or cron job needed.

### Dockerfile

Remove `ENV VERSION="13.x"`. The runtime code resolves `DEFAULT_VERSION` dynamically from the API (or cache). The env var was redundant — it only took effect if the entrypoint read `$VERSION`, but the Python code already handles version resolution independently.

### README

Change version examples from specific current versions to `11.x` — an intentionally older version that demonstrates "here's how to pin to a non-default version." The default is already documented as "Latest" in the options table.

## Error Handling

- **API returns empty version list:** Log warning, fall through to cache file.
- **Cache file has bad JSON:** Log warning, treat as missing, fall through to `["12.x"]` last resort.
- **Cache file write fails (permissions):** Log warning, don't crash. Runtime still works from API result in memory.

## Testing

- Test cache write on successful API fetch
- Test cache read on API failure
- Test corrupt/missing cache falls through to last resort
- Test that committed cache file contains current `DEFAULT_VERSION` (canary for staleness)
- Update `TestNewVersionSimulation` to cover the cache path
- Remove tests for the old hardcoded fallback lists

## Migration

1. Create `docs/.versions_cache.json` with current versions
2. Rewrite `get_supported_versions()` to use three-tier resolution
3. Remove both hardcoded fallback lists from `docs_updater.py`
4. Remove `ENV VERSION` from Dockerfile
5. Update README examples to use `11.x`
6. Update/add tests
