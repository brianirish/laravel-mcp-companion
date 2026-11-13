# Releasing

How a version gets from `main` to users, and the conditions for tagging 1.0.0.

## The image, the registry entry and the PyPI package

Publishing a GitHub release creates a `vX.Y.Z` tag on `main`. The tag starts
two things:

- **The Docker image.** The Harness `release` pipeline builds
  `ghcr.io/brianirish/laravel-mcp-companion:vX.Y.Z` for amd64 and arm64. If
  `vX.Y.Z` is the newest stable version, the same image is pushed as
  `:latest`. A release candidate (`v1.0.0-rc1`) or a patch to an older line
  does not move `:latest`.
- **The MCP Registry entry.** `.github/workflows/publish-mcp.yml` waits for
  that image and publishes `server.json`.

The PyPI package is published separately, by running
`.github/workflows/publish-pypi.yml` by hand with the tag. It needs a trusted
publisher configured on PyPI first; the workflow file says how.

Between releases, the nightly documentation sync tags `docs-YYYY-MM-DD` on
`main`. The same pipeline builds that tag as the newest release's code with
that night's `docs/`, and pushes it as `:latest`. So `:latest` is always
released code.

## Steps

1. **Bring the documentation up to date.** Let the nightly sync run, or run
   the `docs_update` pipeline, so the release image does not carry stale docs.
2. **Open a release pull request** that changes:
   - `pyproject.toml`: `version`. This is the one place the version is
     written for the code; `SERVER_VERSION` is read from it.
   - `uv.lock`: run `uv lock`.
   - `server.json`: `version`, and the tag in the image `identifier`.
   - `README.md`: the `## Features (vX.Y.Z)` heading.
   - `ROADMAP.md`: the `## Current Version: vX.Y.Z` line.
   - `CHANGELOG.md`: rename `Unreleased` to the version and date, add a new
     empty `Unreleased`, and update the compare links at the bottom.
   - `API.md`: run `python scripts/generate_api_reference.py`.

   `tests/unit/test_version_consistency.py` fails if these disagree, or if
   the version is more than one bump ahead of the newest tag.
3. **Merge it** once CI passes.
4. **Publish the GitHub release** for `vX.Y.Z` targeting `main`, with notes
   taken from the changelog.
5. **Check** that the release pipeline succeeded, that
   `docker run --rm ghcr.io/brianirish/laravel-mcp-companion:vX.Y.Z --help`
   works, and that the registry workflow succeeded.
6. **Publish to PyPI** by running the PyPI workflow with the tag.

If the documentation tag and the version tag are pushed within a few minutes
of each other, check afterwards that `:latest` and `:vX.Y.Z` are the same
image. Both builds use the release's code, so they should be.

## Conditions for tagging 1.0.0

1.0.0 is tagged when all of these hold. None of them is a date.

- [ ] 0.15 has been released and used, and nothing in
      `tests/protocol/contract.json` needs to change. A change after this
      point is a 2.0.
- [ ] The nightly sync has run green for 14 consecutive nights: every source
      `ok` in the sync report, and nothing under "Needs attention".
- [ ] `pytest`, `pytest -m e2e --no-cov` and `pytest -m bench --no-cov` pass
      on `main`. The plain `pytest` run includes the tests marked `corpus`.
- [ ] `docker run` works on amd64 and arm64 from the published image, over
      stdio and over HTTP.
- [ ] `pip install laravel-mcp-companion` and `uvx laravel-mcp-companion` work
      from PyPI, offline once installed.
- [ ] The failure email has been seen to arrive from a failed Harness run, and
      the stale-sync issue has been seen to open from the GitHub workflow.
- [ ] The support window in [VERSIONING.md](VERSIONING.md) is confirmed.
- [ ] The README makes no claim a test or a command in this file does not
      back.

A release candidate, `v1.0.0-rc1`, is the way to let people try the frozen
surface while the fourteen nights run. It gets its own image tag and does not
move `:latest`.
