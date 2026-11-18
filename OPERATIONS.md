# Configuration and operations

Everything about running Laravel MCP Companion beyond the quick start in the
[README](README.md): every option, how tools are listed, keeping the documentation current,
running over HTTP, and the output format.

- [Options](#options)
- [Tool listing modes](#tool-listing-modes)
- [Keeping the documentation current](#keeping-the-documentation-current)
- [Running over HTTP](#running-over-http)
- [Output format](#output-format)

## Options

Options go after the image name in the Docker command, or after `laravel-mcp-companion`:

```bash
# Answer from Laravel 11.x unless a question names another version
docker run --rm -i ghcr.io/brianirish/laravel-mcp-companion:latest --version 11.x
```

Every version stays available whatever `--version` says; it sets the default.

| Option | Description | Default |
|--------|-------------|---------|
| `--version VERSION` | Laravel version answered from by default, e.g. `11.x` (env: `VERSION`) | The newest |
| `--docs-path PATH` | Read and update the documentation in this directory (env: `DOCS_PATH`) | The copy that ships with the image or package; see [Fetching without a new image](#fetching-without-a-new-image) |
| `--update-docs` | On startup, fetch the framework docs for the default version if Laravel has changed them | false |
| `--force-update` | On startup, fetch them whether or not they have changed | false |
| `--transform-mode MODE` | How tools are listed: `search`, `code`, or `none`; see [Tool listing modes](#tool-listing-modes) (env: `TRANSFORM_MODE`) | `search` |
| `--log-level LEVEL` | DEBUG, INFO, WARNING, ERROR, CRITICAL (env: `LOG_LEVEL`) | INFO |
| `--server-name NAME` | Name the server reports to clients (env: `SERVER_NAME`) | `LaravelMCPCompanion` |
| `--transport TRANSPORT` | `stdio`, or `http`; see [Running over HTTP](#running-over-http) (env: `TRANSPORT`) | `stdio` |
| `--host HOST` | Interface to bind in HTTP mode (env: `HOST`) | `127.0.0.1` (`0.0.0.0` in Docker) |
| `--port PORT` | Port for the HTTP transport (env: `PORT`) | `8081` |
| `--cors-origin ORIGIN` | Browser origin allowed to call the HTTP transport, repeatable (env: `CORS_ORIGINS`) | none (CORS off) |
| `--allowed-host HOST` | Additional `Host` header accepted in HTTP mode, repeatable (env: `ALLOWED_HOSTS`) | `localhost`, `127.0.0.1`, `::1` |
| `--auth-jwks-uri URI` | JWKS endpoint enabling bearer-token auth in HTTP mode (env: `AUTH_JWKS_URI`) | none (auth off) |
| `--auth-issuer ISSUER` | Required token issuer, with `--auth-jwks-uri` (env: `AUTH_ISSUER`) | none |
| `--auth-audience AUD` | Required token audience, with `--auth-jwks-uri` (env: `AUTH_AUDIENCE`) | none |
| `--auth-required-scope SCOPE` | Scope every token must carry, repeatable (env: `AUTH_REQUIRED_SCOPES`) | none |
| `--rate-limit RPS` | MCP requests/second accepted in HTTP mode (env: `RATE_LIMIT_RPS`) | none (no limiting) |
| `--rate-limit-burst N` | Token-bucket burst capacity (env: `RATE_LIMIT_BURST`) | `max(10, 2×RPS)` |

Two settings are environment variables only: `AUTH_STATIC_TOKENS`, described under
[Authentication](#authentication), and `LARAVEL_MCP_COMPANION_HOME`, described under
[Fetching without a new image](#fetching-without-a-new-image).

## Tool listing modes

An MCP client receives the description of every tool a server lists and keeps them in the model's
context, where each one costs tokens on every request. The server is built on [FastMCP](https://gofastmcp.com), which can list a small search
interface in place of the full set. `--transform-mode` chooses:

- **`search`** (default). Lists four tools: `search_laravel_docs` and `read_laravel_doc_section`,
  which answer almost every question, plus `search_tools`, which finds a tool from a description
  of what you need, and `call_tool`, which runs any tool by name.
- **`none`**. Lists all twelve tools directly. Use this if your client does not handle
  `search_tools` and `call_tool` well, or if you call tools from a program.
- **`code`** (experimental). Lists FastMCP's Code Mode tools (`tags`, `search`, `get_schema`,
  `execute`), which let the client find tools and combine them with sandboxed Python. Do not expose
  this over HTTP: `execute` runs code.

```bash
docker run --rm -i ghcr.io/brianirish/laravel-mcp-companion:latest --transform-mode none
```

## Keeping the documentation current

A GitHub Actions workflow in this repository runs every night. It refetches every source, and when
the content has changed it publishes a new Docker image with that night's documentation. You get
it by pulling the image, or by asking the server to fetch for itself.

The server tells your assistant how old its documentation is, so when you ask about something
newer the assistant can say so and offer to refresh.

### Docker: pull a newer image

`docker run` keeps using the image you already have until you pull again:

```bash
docker pull ghcr.io/brianirish/laravel-mcp-companion:latest
```

Or add `--pull=always` to your MCP config so every start checks for a newer image. It costs a
moment at startup and needs a connection:

```jsonc
"args": ["run", "--rm", "-i", "--pull=always",
         "ghcr.io/brianirish/laravel-mcp-companion:latest"]
```

Which documentation an image holds depends on its tag:

| Tag | Code | Documentation |
|-----|------|---------------|
| `:latest` | the newest stable release | refreshed nightly |
| `:v1.0.0-rc1` and other version tags | that release | as it was on the release date |
| `:docs-YYYY-MM-DD` | the newest stable release as of that date | that night's sync |

### Fetching without a new image

- **While the server runs,** your assistant can call the `update_laravel_docs` tool. Its `scope`
  selects the framework docs, the services, the packages or all of them.
- **At startup,** `--update-docs` fetches the framework docs for the default Laravel version. It
  does not fetch services or packages.

Where the fetched documentation is kept depends on how you run the server.

**Docker.** With `--rm` the download is discarded when the container exits. A named volume keeps
it:

```bash
docker run --rm -i -v laravel-mcp-docs:/app/docs \
  ghcr.io/brianirish/laravel-mcp-companion:latest --update-docs
```

> **A volume replaces the image's documentation.** Docker fills a new volume from the image the
> first time it is used. From then on the server reads the volume, pulling a newer image no longer
> changes what it reads, and updating becomes your job. Use a volume when
> you want to control updates yourself; otherwise leave it out and pull the image.

**`uvx` or `pip`.** An install made this way keeps its documentation in a per-user directory,
created from the bundled copy the first time the server starts. Updates go there, where a
reinstall or an upgrade does not touch them:

| System | Directory |
|--------|-----------|
| macOS | `~/Library/Application Support/laravel-mcp-companion/docs` |
| Linux | `~/.local/share/laravel-mcp-companion/docs` (or under `$XDG_DATA_HOME`) |
| Windows | `%LOCALAPPDATA%\laravel-mcp-companion\docs` |

To keep it elsewhere, set `LARAVEL_MCP_COMPANION_HOME` to a directory; the documentation goes in
`docs` inside it. When you install a version of the package whose bundled documentation is newer
than that copy, the copy is replaced from it at the next start, so a newer install is never hidden
behind an older fetch. If the directory cannot be written, the server reads the bundled copy and
says so in its log. A `--docs-path` you give overrides all of this: that one directory is read and
updated.

### What the nightly sync does

This part is for the curious and for contributors.

- **The framework docs** come from the `laravel/docs` repository, one branch per version.
- **Services** are read from the `llms.txt` index each site publishes, as markdown.
- **Learning material** is read from laravel.com/learn and the Laracasts topic list.
- **Package docs** are read from the same kind of index where one exists (Filament, Inertia) and
  from the site's own navigation where it does not (Livewire, Spatie). When a package releases a
  new major version, the sync follows it.
- **A page that a site has dropped is removed** only when the rest of that source was fetched
  completely. A partial fetch removes nothing.

When content has changed, the workflow opens a pull request that merges once the tests pass, tags
the merge `docs-YYYY-MM-DD`, and builds the image from the newest stable release's code with that night's
documentation. `:latest` is therefore always released code. Each pull request carries a report of
every source: how many pages were fetched, of how many, and when. A source that fetched far fewer
pages than it should have is flagged in that report and in an issue.

## Running over HTTP

By default the server speaks MCP over stdio: the client starts it and owns the process. To run it
as a service, start it with `--transport http`:

```bash
docker run --rm -p 127.0.0.1:8081:8081 ghcr.io/brianirish/laravel-mcp-companion:latest --transport http
```

Clients connect to `http://127.0.0.1:8081/mcp/`. The examples below start the server with the
`laravel-mcp-companion` command from the Python package; the same options work after the image
name.

### Authentication

**Authentication is off by default.** Anyone who can reach the port can call every tool,
including the one that makes the server fetch documentation. Turn on bearer-token validation
before exposing it beyond your own machine:

```bash
# Validate tokens issued by an OAuth 2.1 authorization server
laravel-mcp-companion --transport http \
  --auth-jwks-uri https://auth.example/.well-known/jwks.json \
  --auth-issuer https://auth.example \
  --auth-audience laravel-mcp-companion

# For development: fixed tokens from the environment, written as
# "token:client-id" pairs separated by commas. There is no command-line flag
# for this, so that secrets stay out of process listings.
AUTH_STATIC_TOKENS="my-token:my-client" laravel-mcp-companion --transport http
```

The server validates tokens and never issues them. `--auth-issuer` and `--auth-audience` are
required with `--auth-jwks-uri`, so that a token from another issuer, or one issued for another
service, is refused. A request without a valid token gets `401` with a `WWW-Authenticate` header
(RFC 9728). A wrong configuration fails at startup, and if the JWKS endpoint cannot be reached,
requests are refused. Authentication applies to HTTP only; over stdio, whoever can start the
process can use it.

An authenticating reverse proxy in front of the server does the same job, if you already run one.

### Network defaults

- **It binds `127.0.0.1`** outside Docker. Inside the container it binds `0.0.0.0`, and what you
  publish with `-p` decides who can reach it.
- **`Host` and `Origin` headers are checked**, which blocks DNS-rebinding and requests made from a
  web page in the user's browser.
- **CORS is off** unless you pass `--cors-origin`. Wildcard origins are rejected.

Only `localhost`, `127.0.0.1` and `::1` are accepted as `Host` values, which is what a client on
the same machine sends, including to the Docker command above. **If clients reach the server by
another name, add it**:

```bash
laravel-mcp-companion --transport http \
  --host 0.0.0.0 \
  --allowed-host mcp.internal.example \
  --cors-origin https://app.example
```

A request with an unrecognised `Host` gets `421`, and one from an unlisted `Origin` gets `403`.
`--allowed-host` and `--cors-origin` on the command line replace the corresponding environment
variable; they do not add to it.

### Rate limiting

Off by default. `--rate-limit 20` caps MCP requests at 20 a second. It is one limit for the whole
server, not one per client. A throttled request receives an MCP error and is not
queued; the client has to send it again. The endpoints in the next section are never limited, so a load balancer's health checks
are not throttled.

The initialize handshake counts toward the limit. The burst capacity defaults to
`max(10, 2×RPS)`; if you lower it with `--rate-limit-burst`, leave room for several clients
connecting at once.

### Health, metrics and discovery

- **`GET /healthz`** returns JSON and needs no token. Its `status` is `ok` or `degraded`, both
  with HTTP 200. `degraded` means the documentation is more than 30 days old and should be refreshed. 503 means
  no documentation is readable.
- **`GET /metrics`** returns Prometheus text: per-tool call counters, a latency histogram, request
  counts, uptime and the age of the documentation. It requires a token whenever authentication is
  on.
- **`GET /.well-known/mcp/server.json`** returns the server's MCP Registry entry.

The Docker image declares a `HEALTHCHECK` and runs as an unprivileged user.

## Output format

The text of a result is [TOON](https://toonformat.dev) (Token-Oriented Object Notation), which
says what JSON says in fewer characters. A search for "retry a failed job", limited to two results:

```
query: retry a failed job
scope: 13.x
sources[4]: core,services,packages,learning
count: 2
results[2]{file,section,heading,score,snippet,source}:
  13.x/queues.md,dealing-with-failed-jobs,Dealing With Failed Jobs,22.53,"## Dealing With Failed Jobs ...",core
  cloud/metrics/queues.md,job-volume,Job volume,21.55,"... A job failed permanently because ...","service:cloud"
```

A search result is 16 to 20% smaller than the same data as JSON, measured in characters. The two
read tools return the page's markdown as their text. Every tool also returns the same data as a
JSON object in `structuredContent`, which is what a program should read.
