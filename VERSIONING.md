# Versioning and compatibility

This page says what a version number promises. It is a draft until 1.0.0 is
released; the promise starts there.

## Covered by the compatibility promise

From 1.0.0, a release that breaks any of the following increases the major
version:

- **The stable tools.** The ten tools not marked experimental: their names,
  their arguments, and their output schemas. An argument is not removed or
  renamed, a required argument is not added, and a field marked *always* in
  [API.md](API.md) is not removed or retyped.
- **The error object.** Its shape, and the meaning of each error code, as
  given under [Errors in API.md](API.md#errors).
- **The resource templates.** `laravel://`, `laravel-external://` and
  `laravel-package://`, and the kinds of path each accepts.
- **The command line.** The flags and environment variables in the README's
  configuration table.
- **The image tags.** What `:latest`, a version tag and a `docs-` tag mean.

`tests/protocol/contract.json` is the machine-readable record of the first
three. A test fails when the served surface differs from it, so a change
cannot ship unnoticed.

A minor release may add a tool, an optional argument, an optional output
field, an error code or an allowed value. Write clients to ignore fields and
codes they do not know.

## Not covered

- **Experimental tools.** `get_laravel_learning_path` and
  `browse_docs_by_category`. Each carries the tag `experimental` in the tool
  list a client receives, a note in [API.md](API.md), and `"stable": false`
  in the contract file. They answer from the curated tables described below,
  and their shape may change in a minor release.
- **The meta-tools.** The server is built on the FastMCP framework. In the
  default `search` mode, and in `code` mode, most of the tools a client lists
  are FastMCP's own (`search_tools`, `call_tool` and the Code Mode set). Their schemas are FastMCP's to change.
  `search_laravel_docs` and `read_laravel_doc_section` are listed directly in
  search mode, and that is covered.
- **Wording.** Tool descriptions, server instructions, error messages and the
  text content of results. Branch on structured content and error codes.
- **Ranking.** Which results a search returns for a query, and in what order.
- **The documentation itself.** Pages are other people's work, fetched
  nightly. A page upstream renames or removes changes here too, including in a
  patch release or with no release at all.
- **The curated tables.** The package catalog, the categories, the difficulty
  levels, the learning paths and the table of common tasks are written by
  hand, and are revised as the ecosystem changes.
- **Python import paths.** The package is an application. Its modules may be
  renamed or reorganised in any release.

## Before 1.0

While the version is `0.x`, a minor release may break anything, and the
changelog says so under a "Breaking" heading. 0.15 is intended to be the last
such release.

## Which versions get fixes

Proposed, and the maintainer's to confirm before 1.0.0:

- The newest release gets bug fixes and documentation updates.
- When a new major is released, the previous major gets security fixes for
  six months.
- A `docs-` image is built nightly for the newest release only.

## Deprecation

A stable tool, argument or field that is going away is marked deprecated in
its description and in [API.md](API.md) for at least one minor release before
the major release that removes it, and keeps working until then.
