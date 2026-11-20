# Releasing

How a version gets from `main` to users, and the conditions for tagging 1.0.0.

Builds run in GitHub Actions. The workflows are in `.github/workflows/`:

| Workflow | File | Started by |
|----------|------|------------|
| CI | `ci.yaml` | every pull request and every push to `main` |
| Docs update | `docs-update.yaml` | a schedule, nightly |
| Release image | `release.yaml` | a `vX.Y.Z` or `docs-*` tag |
| Publish to MCP Registry | `publish-mcp.yml` | a `vX.Y.Z` tag |
| Publish to PyPI | `publish-pypi.yml` | a `vX.Y.Z` tag |
| Docs sync watch | `docs-sync-watch.yml` | a schedule, daily |

Each can also be started from the Actions tab, or with `gh workflow run`.
GitHub may start a scheduled workflow late: the sync is scheduled for 00:17
UTC, and its first run began six hours after that.
The nightly sync pushes with the `PAT_FOR_WORKFLOWS` repository secret, a
personal access token. When that token expires the sync fails at its first
step and says so.

## The image, the registry entry and the PyPI package

Publishing a GitHub release creates a `vX.Y.Z` tag on `main`. The tag starts
three things:

- **The Docker image.** The Release image workflow builds
  `ghcr.io/brianirish/laravel-mcp-companion:vX.Y.Z` for amd64 and arm64, and
  fails if the published image is missing either platform. If
  `vX.Y.Z` is the newest stable version, the same image is pushed as
  `:latest`. A release candidate (`v1.0.0-rc1`) or a patch to an older line
  does not move `:latest`.
- **The PyPI package.** `.github/workflows/publish-pypi.yml` builds the wheel,
  checks that it runs from a clean environment, and uploads it. It signs in
  through a trusted publisher on pypi.org that names this repository, that
  workflow file and the `pypi` environment, so no token is stored. PyPI never
  accepts the same file twice, so a published version cannot be replaced. If
  the run fails, start the workflow by hand with the tag
  (`gh workflow run publish-pypi.yml -f tag=vX.Y.Z`). A run started by hand
  uploads whichever of the wheel and the source distribution PyPI does not
  have, so it also finishes an upload that stopped after the first file.
  "Re-run failed jobs" on the tag's own run does not: it fails on the file
  that is already there.
- **The MCP Registry entry.** `.github/workflows/publish-mcp.yml` waits for
  that image and that package, and publishes `server.json`, which lists both.

Between releases, the nightly documentation sync tags `docs-YYYY-MM-DD` on
`main` (a second sync on the same day is tagged `docs-YYYY-MM-DD-HHMM`). The
Release image workflow builds that tag as the newest stable release's code with that
night's `docs/`, and pushes it as `:latest`. So `:latest` is always
released code. Nightly documentation is not published to PyPI: a `pip`
or `uvx` install has the documentation of its release until its user updates
it.

## Steps

1. **Bring the documentation up to date.** Let the nightly sync run, or run
   the Docs update workflow, so the release image does not carry stale docs.
2. **Open a release pull request** that changes:
   - `pyproject.toml`: `version`. This is the one place the version is
     written for the code; `SERVER_VERSION` is read from it.
   - `uv.lock`: run `uv lock`.
   - `server.json`: `version`, the tag in the image `identifier`, and the
     `version` of the PyPI package.
   - `README.md`: the `## Features (vX.Y.Z)` heading.
   - `OPERATIONS.md`: the version tag in the image tag table.
   - `ROADMAP.md`: the `## Current Version: vX.Y.Z` line.
   - `CHANGELOG.md`: rename `Unreleased` to the version and date, add a new
     empty `Unreleased`, and update the compare links at the bottom.
   - `API.md`: run `python scripts/generate_api_reference.py`.

   `tests/unit/test_version_consistency.py` fails if `server.json`, the
   README heading or the ROADMAP line disagrees with `pyproject.toml`, or if
   the version is behind the newest tag or more than one release ahead of it.
   `tests/unit/test_api_reference.py` fails if `API.md` is stale. Nothing
   checks the changelog, the lockfile, or the image tag table in
   `OPERATIONS.md`, which names the version in one row.
3. **Merge it** once CI passes.
4. **Publish the GitHub release** for `vX.Y.Z` targeting `main`, with notes
   taken from the changelog.
5. **Check** that the Release image, PyPI and registry workflows succeeded,
   and that `docker run --rm ghcr.io/brianirish/laravel-mcp-companion:vX.Y.Z --help`
   and `uvx laravel-mcp-companion@X.Y.Z --help` work. The registry lists the
   new version as its latest when this prints it:

   ```bash
   curl -s 'https://registry.modelcontextprotocol.io/v0/servers?search=laravel-mcp-companion&version=latest' \
     | python3 -c 'import json,sys; print(*[s["server"]["version"] for s in json.load(sys.stdin)["servers"]])'
   ```

Both the version build and a nightly docs build push `:latest`, and whichever
finishes last keeps it. Both use the release's code, so the result should be
the same either way. If the two tags were pushed within a few minutes of each
other, check that `:latest` reports the new version (`/healthz` over HTTP, or
the `initialize` response). If it does not, run the Release image workflow by
hand with the version tag.

## Cutting a release candidate

A release candidate goes through the steps above. Only `rcN` is supported;
the version test rejects alpha, beta, dev and post versions. Two things
differ from a final release.

**The version is written in two forms.** PyPI takes `1.0.0rc1`. The git tag,
the image tag and the MCP Registry take the hyphenated form.

| Where | What it holds for 1.0.0 rc1 |
|-------|-----------------------------|
| `pyproject.toml` `version` (and so `uv.lock`, `SERVER_VERSION`, `/healthz`, the `initialize` response) | `1.0.0rc1` |
| `server.json` `version` | `1.0.0-rc1` |
| `server.json` image `identifier` | `ghcr.io/brianirish/laravel-mcp-companion:v1.0.0-rc1` |
| `server.json` PyPI package `version` | `1.0.0rc1` |
| `README.md` heading | `## Features (v1.0.0-rc1)` |
| `ROADMAP.md` line | `## Current Version: v1.0.0-rc1` |
| `OPERATIONS.md` image tag table | `:v1.0.0-rc1` |
| `CHANGELOG.md` heading | `## [1.0.0-rc1] - YYYY-MM-DD` |
| The git tag and the GitHub release | `v1.0.0-rc1` |

`tests/unit/test_version_consistency.py` checks the `pyproject.toml`,
`server.json`, README and ROADMAP rows. From a final release it accepts the
first candidate of the next patch, minor or major version (`0.15.1` to
`0.15.2rc1`, `0.16.0rc1` or `1.0.0rc1`). From a candidate it accepts the next
candidate or the final version (`1.0.0rc1` to `1.0.0rc2` or `1.0.0`). It
fails on a skipped candidate, and on a `v*` tag that is neither `vX.Y.Z` nor
`vX.Y.Z-rcN`.

The PyPI workflow compares the tag with `pyproject.toml` after removing the
hyphen, and the registry workflow writes each form into `server.json` from
the tag, so both accept `v1.0.0-rc1` as it is.

**Tick "Set as a pre-release" when publishing the GitHub release.** No
workflow reads that box. It keeps GitHub's "Latest" label on the last final
release.

What a candidate does not change:

- `:latest` stays on the newest final release. The candidate's image is
  pushed as `:v1.0.0-rc1` only, and the nightly `docs-` builds keep using the
  newest final release's code (`scripts/release_tree.sh`, tested in
  `tests/unit/test_release_tree.py`).
- `pip install laravel-mcp-companion` and `uvx laravel-mcp-companion` keep
  installing the newest final release. pip and uv leave a pre-release out
  unless it is asked for: `uvx laravel-mcp-companion@1.0.0rc1`, or
  `pip install laravel-mcp-companion==1.0.0rc1`.

The MCP Registry is the exception. It has no notion of a pre-release and
marks the candidate as the server's latest version, so anything that reads
the latest registry entry gets the `:v1.0.0-rc1` image and the `1.0.0rc1`
PyPI package until the final release is published. A version cannot be
published to the registry twice, so the only way past a candidate with a
broken entry is the next candidate.

In step 5, check `docker run --rm ghcr.io/brianirish/laravel-mcp-companion:v1.0.0-rc1 --help`
and `uvx laravel-mcp-companion@1.0.0rc1 --help`, and that `:latest` still
reports the last final version.

The final release after a candidate is an ordinary release: `1.0.0` in
`pyproject.toml`, `v1.0.0` as the tag.

## Conditions for tagging 1.0.0

1.0.0 is tagged when all of these hold. None of them is a date.

- [ ] 0.15 has been released and used, and nothing in
      `tests/protocol/contract.json` needs to change. A change after this
      point is a 2.0.
- [x] The nightly sync has run green for seven consecutive nights: every
      source `ok` in the sync report, and nothing under "Needs attention".
      The report is in the body of each night's documentation pull request,
      and `python -m laravel_mcp_companion.docs_updater --sync-report` prints
      it. Seen for the scheduled runs of 14 to 20 November 2026. This was 14
      nights until 2026-11-20, when both alarms had been seen to work: a sync
      that breaks after the release is now reported within a day.
- [x] `pytest`, `pytest -m e2e --no-cov` and `pytest -m bench --no-cov` pass
      on `main`. The plain `pytest` run includes the tests marked `corpus`,
      which compare the curated tables with the documentation in `docs/`.
      CI runs all three on every push to `main`, and the release pull
      request runs them again.
- [x] `docker run` works on amd64 and arm64 from the published image, over
      stdio and over HTTP. Checked on 2026-11-20 with `:v1.0.0-rc1`: on each
      platform the container reported its architecture, and over stdio and
      over HTTP (`--transport http`, with `/healthz` answering) it listed its
      tools, answered a search and returned a section.
- [x] `pip install laravel-mcp-companion` and `uvx laravel-mcp-companion` work
      from PyPI, offline once installed. Checked on 2026-11-20 with
      `1.0.0rc1` through pip and `uvx laravel-mcp-companion@1.0.0rc1`, and
      with `0.15.1` through plain `uvx`. Each was installed while online,
      then started under
      `sandbox-exec -p '(version 1)(allow default)(deny network*)'` (macOS),
      where it listed its 12 tools, answered a search and returned
      `queues.md`.
- [x] Both alarms have been seen to work: the email GitHub sends when a
      Docs update or Release image run fails, and the issue
      `.github/workflows/docs-sync-watch.yml` opens when no `docs-` tag has
      appeared for four days. Both were seen on 2026-11-20. A Release image
      run given a tag that does not exist failed, and the email arrived. A
      watch run fed an old tag opened #539, and the next run on `main` closed
      it.
- [x] The support window in [VERSIONING.md](VERSIONING.md) is confirmed.
      Confirmed on 2026-11-18.
- [x] The README makes no claim a test or a command in this file does not
      back. Checked on 2026-11-20 (#540, #541): claims that were wrong were
      corrected, claims about other clients were cut, and the rest are
      tested, most of them in `tests/unit/test_readme_claims.py`. Check
      again if the README changes.

A release candidate, `v1.0.0-rc1`, is the way to let people try the frozen
surface while the conditions above are met. It gets its own image tag and does not
move `:latest`.
