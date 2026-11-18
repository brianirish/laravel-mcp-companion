# Laravel MCP Companion

[![GitHub release (latest by date)](https://img.shields.io/github/v/release/brianirish/laravel-mcp-companion)](https://github.com/brianirish/laravel-mcp-companion/releases)
[![Python Version](https://img.shields.io/badge/python-3.12%2B-blue)](https://www.python.org/downloads/)
[![License](https://img.shields.io/github/license/brianirish/laravel-mcp-companion)](https://github.com/brianirish/laravel-mcp-companion/blob/main/LICENSE)
[![PyPI](https://img.shields.io/pypi/v/laravel-mcp-companion)](https://pypi.org/project/laravel-mcp-companion/)
[![Docker Image](https://img.shields.io/badge/docker-ghcr.io-blue)](https://github.com/brianirish/laravel-mcp-companion/pkgs/container/laravel-mcp-companion)
[![GitHub Stars](https://img.shields.io/github/stars/brianirish/laravel-mcp-companion?style=social)](https://github.com/brianirish/laravel-mcp-companion)

**Every Laravel version, the whole ecosystem, fully local.**

Laravel MCP Companion is an [MCP](https://modelcontextprotocol.io) server that keeps Laravel's
documentation on your machine and lets an AI assistant search and read it. It holds the framework
docs for every version from 6.x to the newest, the first-party services, and widely used packages.
No documentation is fetched while you work, so it answers without a network connection.

> **Status:** pre-1.0. The tools listed below, with their arguments and results, are the ones 1.0
> will promise not to break. Upgrading from 0.14 or earlier? See [MIGRATING.md](MIGRATING.md).

## What it is for

- **Every version, side by side.** Laravel 6.x through 13.x are all held. Ask about the version an
  older application runs on, or compare two versions to see what an upgrade brings.
- **Fully local.** The documentation ships inside the Docker image and the Python package. Your
  questions go nowhere but your assistant, and no documentation service is called, so it works
  offline and behind an air gap. Documentation is fetched only when you ask for an update. The
  one other request is at startup: if its list of Laravel versions is more than a day old, the
  server asks GitHub for it, and carries on with the list it has when there is no answer.
- **It needs no project.** It works in a chat client with no code open.

[Laravel Boost](https://github.com/laravel/boost) is the first-party tool for writing code inside a
Laravel project: it is installed into the application and knows what the application uses. Use Boost
while building. Use Companion to look something up in any Laravel version, in a client with no
project open, or where the documentation has to stay on the machine.

## Documentation held

- **The framework documentation** for Laravel 6.x through 13.x.
- **First-party services:** Forge, Vapor, Envoyer, Nova, Cloud, Nightwatch and Herd.
- **Package documentation:** Livewire, Filament, Inertia, and Spatie's Permission, Media Library
  and Backup, each for the package's current major version, and the smaller docs of Debugbar and
  IDE Helper.
- **Learning material:** the courses at laravel.com/learn and an index of Laracasts topics.
- **A package catalog.** Separate from the documentation above: a hand-written list of
  42 curated packages, saying what each is for, how to install it, what goes with it, and which
  ones have been superseded.

The project refetches the documentation every night and publishes it;
[Keeping the documentation current](#keeping-the-documentation-current) says how it reaches you.
The catalog is revised by hand. Ask your assistant how current its documentation is, or call
`laravel_docs_info`, to see the date and page count of every source.

## Installation

Run it with [`uvx`](https://docs.astral.sh/uv/) or with
[Docker](https://docs.docker.com/get-docker/), whichever you already have. Both carry the
documentation with them. The server is on [PyPI](https://pypi.org/project/laravel-mcp-companion/)
and in the
[official MCP Registry](https://registry.modelcontextprotocol.io/?search=laravel-mcp-companion)
as `io.github.brianirish/laravel-mcp-companion`.

**Claude Code:**

```bash
# with uv
claude mcp add laravel-mcp-companion -- uvx laravel-mcp-companion

# with Docker
claude mcp add laravel-mcp-companion -- docker run --rm -i ghcr.io/brianirish/laravel-mcp-companion:latest
```

**Claude Desktop, and most other MCP clients:** add one of these to the client's MCP
configuration (Settings → Developer → Edit Config in Claude Desktop), then restart it.

With uv:

```json
{
  "mcpServers": {
    "laravel-mcp-companion": {
      "command": "uvx",
      "args": ["laravel-mcp-companion"]
    }
  }
}
```

With Docker:

```json
{
  "mcpServers": {
    "laravel-mcp-companion": {
      "command": "docker",
      "args": ["run", "--rm", "-i", "ghcr.io/brianirish/laravel-mcp-companion:latest"]
    }
  }
}
```

`pip install laravel-mcp-companion` works too, on Python 3.12 or newer, and installs a
`laravel-mcp-companion` command.

Then ask your assistant *"how current are your Laravel docs?"*. It should answer with a date and a
list of sources.

## Features (v0.15.1)

Twelve tools. [API.md](API.md) documents every argument and result field.

| Tool | What it does |
|------|--------------|
| `search_laravel_docs` | Ranked search over everything held; returns sections, each with a snippet |
| `read_laravel_doc_section` | Reads one section of a page |
| `read_laravel_doc_content` | Reads a whole page, or lists its headings |
| `list_laravel_docs` | Lists what is held, or the files of one collection |
| `laravel_docs_info` | Reports how current every source is |
| `compare_laravel_versions` | Lists the pages one Laravel version has and another lacks |
| `update_laravel_docs` | Fetches newer documentation |
| `get_laravel_package` | Looks up a package, or a category, in the catalog |
| `recommend_laravel_packages` | Suggests packages for a described need |
| `get_laravel_service_info` | Describes a first-party service and what is held for it |
| `get_laravel_learning_path` | Returns a reading order for a goal *(experimental)* |
| `browse_docs_by_category` | Lists pages by topic and difficulty *(experimental)* |

- **Ranked sections, not files.** Ask in plain language ("how do I retry a failed queue job") and
  get the sections that answer it. A section is usually a few hundred tokens where the whole page
  is tens of thousands.
- **Unified search** - One search covers the core framework docs, the services, the package docs
  and the learning resources, and labels each result with its source. `sources` narrows it.
- **Results a program can use.** Every tool returns a JSON object matching a declared schema, as
  well as text for the model. A failure is an error with a `code` to branch on.
- **A stable surface.** The tools are recorded in a contract file that a test enforces.
  [VERSIONING.md](VERSIONING.md) says what 1.0 will promise; the two tools marked *experimental*
  are outside it.

By default a client is shown four tools, not twelve: the first two above, and two helpers that
find and run the rest. That keeps tool descriptions out of the model's context.
`--transform-mode none` lists all twelve; see
[Tool listing modes](OPERATIONS.md#tool-listing-modes).

## Keeping the documentation current

The project refetches every source each night and publishes a new image. To get it:

```bash
docker pull ghcr.io/brianirish/laravel-mcp-companion:latest
```

Or ask your assistant to update its Laravel docs, and it will fetch them itself.
[OPERATIONS.md](OPERATIONS.md#keeping-the-documentation-current) covers image tags, keeping
fetched documentation in a Docker volume, and where a `pip` or `uvx` install stores it.

## More

| | |
|---|---|
| [OPERATIONS.md](OPERATIONS.md) | Every option, tool listing modes, running over HTTP with authentication and rate limiting, health and metrics, the output format |
| [API.md](API.md) | Every tool, argument, result field and error code |
| [MIGRATING.md](MIGRATING.md) | Upgrading from 0.14 or earlier |
| [VERSIONING.md](VERSIONING.md) | What a version number promises |
| [ROADMAP.md](ROADMAP.md) | What is left before 1.0 |
| [CONTRIBUTING.md](CONTRIBUTING.md) | Development setup and tests |
| [SECURITY.md](SECURITY.md) | Reporting a vulnerability |

## License

MIT. See [LICENSE](LICENSE).

## Acknowledgements

- Laravel for their excellent documentation
- Laravel package authors for their contributions to the ecosystem

<!-- mcp-name: io.github.brianirish/laravel-mcp-companion -->
