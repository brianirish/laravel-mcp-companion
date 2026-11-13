#!/usr/bin/env python3
"""
Laravel MCP Companion

This server provides Laravel documentation and package recommendations via the Model Context Protocol (MCP).
It allows AI assistants and other tools to access and search Laravel documentation, as well as
recommend appropriate Laravel packages for specific use cases.
"""

import math
import os
import sys
import logging
import re
import argparse
import json
from pathlib import Path
from typing import Dict, Optional, List, Any, TYPE_CHECKING

if TYPE_CHECKING:
    from fastmcp.server.middleware.rate_limiting import RateLimitingMiddleware
from fastmcp import FastMCP
from fastmcp.server.auth import TokenVerifier
from starlette.requests import Request
from starlette.responses import JSONResponse, Response

import time

from . import __version__, resource_path
from .tools import ToolContext, register_all
from .metrics import MetricsMiddleware, registry as metrics_registry, render_prometheus
from fastmcp.server.transforms.search import BM25SearchTransform
from mcp.types import Icon

# Import documentation updater
from .docs_updater import (
    DocsUpdater, MultiSourceDocsUpdater, get_cached_supported_versions,
    get_default_version, refresh_supported_versions,
)
from .shutdown_handler import GracefulShutdown


# Import standalone MCP tool implementations
from .mcp_tools import (
    resolve_contained_path,
    clear_caches as clear_mcp_tools_caches,
    describe_documentation_date,
    get_documentation_date,
    copy_is_stale,
    get_file_content_cached,
    get_version_from_path
)

# Import learning resources

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("laravel-mcp-companion")

# The server's own version, reported at initialize and stamped into the
# .well-known registry metadata. pyproject.toml is the one place it is written;
# see _read_version in the package __init__ for how it is found.
SERVER_VERSION = __version__

PROJECT_URL = "https://github.com/brianirish/laravel-mcp-companion"

# Get supported versions
SUPPORTED_VERSIONS = get_cached_supported_versions()


def _split_env_list(env_var: str) -> Optional[List[str]]:
    """Parse a comma-separated environment variable into a list of values."""
    raw = os.environ.get(env_var, "")
    values = [item.strip() for item in raw.split(",") if item.strip()]
    return values or None


def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Laravel Documentation and Package Recommendation MCP Server"
    )
    parser.add_argument(
        "--docs-path",
        type=str,
        default=os.environ.get("DOCS_PATH"),
        help="Path to Laravel documentation directory (default: ./docs, env: DOCS_PATH)"
    )
    parser.add_argument(
        "--server-name",
        type=str,
        default=os.environ.get("SERVER_NAME", "LaravelMCPCompanion"),
        help="Name of the MCP server (default: LaravelMCPCompanion, env: SERVER_NAME)"
    )
    parser.add_argument(
        "--log-level",
        type=str,
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        default=os.environ.get("LOG_LEVEL", "INFO"),
        help="Logging level (default: INFO, env: LOG_LEVEL)"
    )
    parser.add_argument(
        "--host",
        type=str,
        default=os.environ.get("HOST"),
        help="Host to bind to (if using network transport, env: HOST)"
    )
    parser.add_argument(
        "--port",
        type=int,
        default=int(os.environ.get("PORT", "0")) if os.environ.get("PORT") else None,
        help="Port to listen on (if using network transport, env: PORT)"
    )
    parser.add_argument(
        "--transport",
        type=str,
        default=os.environ.get("TRANSPORT", "stdio"),
        choices=["stdio", "http"],
        help="Transport mechanism to use (default: stdio, env: TRANSPORT)"
    )
    parser.add_argument(
        "--version",
        type=str,
        default=os.environ.get("VERSION", get_default_version()),
        help=f"Laravel version branch to use (default: {get_default_version()}, env: VERSION). Supported: {', '.join(SUPPORTED_VERSIONS)}"
    )
    parser.add_argument(
        "--update-docs",
        action="store_true",
        default=os.environ.get("UPDATE_DOCS", "").lower() == "true",
        help="Update documentation before starting server (env: UPDATE_DOCS=true)"
    )
    parser.add_argument(
        "--force-update",
        action="store_true",
        default=os.environ.get("FORCE_UPDATE", "").lower() == "true",
        help="Force update of documentation even if already up to date (env: FORCE_UPDATE=true)"
    )
    # These default to None rather than the env list: argparse's "append" action
    # appends to the default, so a non-empty default would union env values with
    # CLI values instead of letting the CLI replace them. The env fallback is
    # applied below, only when the flag is absent.
    parser.add_argument(
        "--cors-origin",
        action="append",
        default=None,
        metavar="ORIGIN",
        help="Browser origin allowed to call the HTTP transport (repeatable). "
             "Replaces CORS_ORIGINS when given. CORS is disabled unless at least "
             "one origin is set. Wildcards are not accepted (env: CORS_ORIGINS, comma-separated)"
    )
    parser.add_argument(
        "--allowed-host",
        action="append",
        default=None,
        metavar="HOST",
        help="Host header value accepted by the HTTP transport (repeatable). "
             "Replaces ALLOWED_HOSTS when given. Required to serve under a hostname "
             "other than localhost (env: ALLOWED_HOSTS, comma-separated)"
    )
    parser.add_argument(
        "--auth-jwks-uri",
        type=str,
        default=os.environ.get("AUTH_JWKS_URI"),
        metavar="URI",
        help="JWKS endpoint of the OAuth authorization server; enables bearer-token "
             "validation on the HTTP transport (env: AUTH_JWKS_URI)"
    )
    parser.add_argument(
        "--auth-issuer",
        type=str,
        default=os.environ.get("AUTH_ISSUER"),
        metavar="ISSUER",
        help="Required token issuer, matched against the JWT 'iss' claim (env: AUTH_ISSUER)"
    )
    parser.add_argument(
        "--auth-audience",
        type=str,
        default=os.environ.get("AUTH_AUDIENCE"),
        metavar="AUDIENCE",
        help="Required token audience, matched against the JWT 'aud' claim (env: AUTH_AUDIENCE)"
    )
    parser.add_argument(
        "--auth-required-scope",
        action="append",
        default=None,
        metavar="SCOPE",
        help="OAuth scope every token must carry (repeatable). Replaces "
             "AUTH_REQUIRED_SCOPES when given (env: AUTH_REQUIRED_SCOPES, comma-separated)"
    )
    parser.add_argument(
        "--rate-limit",
        type=float,
        default=None,
        metavar="RPS",
        help="MCP requests per second accepted in HTTP mode (operational endpoints "
             "like /healthz are never limited); unset means no limiting (env: RATE_LIMIT_RPS)"
    )
    parser.add_argument(
        "--rate-limit-burst",
        type=int,
        default=None,
        metavar="N",
        help="Token-bucket burst capacity; defaults to max(10, 2*RPS) so the MCP "
             "handshake never self-throttles (env: RATE_LIMIT_BURST)"
    )
    parser.add_argument(
        "--transform-mode",
        type=str,
        default=os.environ.get("TRANSFORM_MODE", "").lower() or None,
        choices=["search", "code", "none"],
        help="Tool exposure mode: 'search' exposes BM25 search_tools/call_tool (default), "
             "'code' enables experimental Code Mode, 'none' exposes all raw tools (env: TRANSFORM_MODE)"
    )
    parser.add_argument(
        "--code-mode",
        action="store_true",
        default=os.environ.get("CODE_MODE", "").lower() == "true",
        help="Deprecated: use --transform-mode code (env: CODE_MODE=true)"
    )

    args = parser.parse_args()

    # argparse does not validate defaults against choices, so check env-provided values
    if args.transform_mode is not None and args.transform_mode not in ("search", "code", "none"):
        parser.error(f"invalid TRANSFORM_MODE: {args.transform_mode!r} (choose from 'search', 'code', 'none')")

    # Fall back to the environment only when the flag was not given, so an
    # explicit allowlist on the command line fully replaces the env value.
    if args.cors_origin is None:
        args.cors_origin = _split_env_list("CORS_ORIGINS") or []
    if args.allowed_host is None:
        args.allowed_host = _split_env_list("ALLOWED_HOSTS") or []
    if args.auth_required_scope is None:
        args.auth_required_scope = _split_env_list("AUTH_REQUIRED_SCOPES") or []

    # argparse type= does not run on defaults, so env fallbacks parse here.
    if args.rate_limit is None and os.environ.get("RATE_LIMIT_RPS"):
        try:
            args.rate_limit = float(os.environ["RATE_LIMIT_RPS"])
        except ValueError:
            parser.error(f"invalid RATE_LIMIT_RPS: {os.environ['RATE_LIMIT_RPS']!r}")
    if args.rate_limit_burst is None and os.environ.get("RATE_LIMIT_BURST"):
        try:
            args.rate_limit_burst = int(os.environ["RATE_LIMIT_BURST"])
        except ValueError:
            parser.error(f"invalid RATE_LIMIT_BURST: {os.environ['RATE_LIMIT_BURST']!r}")

    # Allowed hosts are matched with fnmatch, so a pattern entry would match
    # every Host header and silently disable the guard while still looking like
    # a configured allowlist. Reject them the way wildcard CORS origins are.
    wildcard_hosts = [h for h in args.allowed_host if any(c in h for c in "*?[")]
    if wildcard_hosts:
        parser.error(
            f"wildcard patterns are not accepted in allowed hosts: {', '.join(wildcard_hosts)}. "
            "List each hostname explicitly; a pattern would match every Host header "
            "and disable DNS-rebinding protection."
        )

    return args

def setup_docs_path(user_path: Optional[str] = None) -> Path:
    """Set up and validate the docs directory path."""
    if user_path:
        docs_path = Path(user_path).resolve()
    else:
        # The corpus that ships with the project: inside the package in an
        # installed wheel, at the repository root in a checkout.
        docs_path = resource_path("docs").resolve()
    
    # Create directory if it doesn't exist
    docs_path.mkdir(parents=True, exist_ok=True)
    
    return docs_path

def clear_file_cache():
    """Clear every documentation cache, in this module and in mcp_tools."""
    clear_mcp_tools_caches()

def update_documentation(docs_path: Path, version: str, force: bool = False) -> bool:
    """Update the documentation if needed or forced."""
    try:
        updater = DocsUpdater(docs_path, version)
        updated = updater.update(force=force)
        return updated
    except Exception as e:
        logger.error(f"Failed to update documentation: {str(e)}")
        return False

def build_server_instructions(
    docs_path: Path,
    runtime_version: str,
    transform_mode: Optional[str] = "search",
) -> str:
    """Compose the instructions an MCP client injects into the model's context.

    This is where the assistant learns what date the bundled documentation
    describes. Without it, the model answers questions about features newer than
    the corpus without knowing the corpus could not contain them, and the user
    has no reason to suspect it.

    The date reported is that of `runtime_version`, the version this server
    actually answers from. Reporting the newest version present would describe a
    corpus the user is not reading -- an older pinned version can be a year
    behind while another sits at today's date.

    The described workflow follows `transform_mode`, because the search and code
    transforms replace the individual tools with a small synthetic surface. In
    search mode the tools behind that surface are named anyway, with how to
    reach them: a tool the model has never heard of is one it never looks for.
    """
    documentation_date = describe_documentation_date(docs_path, runtime_version)

    answering = """To answer a Laravel question: call search_laravel_docs, then \
read_laravel_doc_section with the `file` and `section` of the result you want. That \
reads one section, a small fraction of a page. Read a whole page with \
read_laravel_doc_content only when the whole page is the point."""

    if transform_mode == "search":
        workflow = f"""{answering}

Those two tools are listed directly. The others are reached through a search \
interface: call search_tools with a description of what you need, then call_tool with \
the tool's name and arguments. They are list_laravel_docs, laravel_docs_info, \
read_laravel_doc_content, compare_laravel_versions and update_laravel_docs for the \
documentation itself; get_laravel_package and recommend_laravel_packages for the \
curated package catalog; get_laravel_service_info for the first-party services; and \
get_laravel_learning_path and browse_docs_by_category for reading orders and topic \
browsing."""
        info_tool = 'call_tool with "laravel_docs_info"'
    elif transform_mode == "code":
        workflow = f"""Tools are exposed through Code Mode. Use tags and search to \
discover them, get_schema for their parameters, and execute to run Python that calls \
them.

{answering}"""
        info_tool = "the laravel_docs_info tool"
    else:
        workflow = f"""{answering}

compare_laravel_versions shows what changed between two releases, \
laravel_docs_info and list_laravel_docs describe what this server holds, and \
update_laravel_docs fetches newer documentation. recommend_laravel_packages suggests packages for a described need and \
get_laravel_package gives the details of one; get_laravel_service_info describes a \
first-party service. get_laravel_learning_path and browse_docs_by_category offer \
reading orders and a topic index."""
        info_tool = "laravel_docs_info"

    return f"""Laravel's documentation, held locally: the framework docs for Laravel \
{', '.join(SUPPORTED_VERSIONS)}, the first-party services (Forge, Vapor, Envoyer, Nova, \
Cloud, Nightwatch, Herd) and widely used packages (Livewire, Filament, Inertia, Spatie).

{workflow}

Documentation answers default to Laravel {runtime_version}; pass `version` to target \
another, or `all_versions` to search every one.

This copy reflects Laravel's documentation as of {documentation_date}. If you are \
asked about a feature that may have been added after that date, say so rather than \
answering as if the documentation covered it. {info_tool} reports this date, and the \
state of every other source, at any time."""


def setup_server_environment(args: argparse.Namespace) -> Path:
    """Setup the server environment based on command line arguments.

    Args:
        args: Parsed command line arguments

    Returns:
        Validated docs_path
    """
    # Set logging level
    logger.setLevel(getattr(logging, args.log_level))

    # Setup docs path
    docs_path = setup_docs_path(args.docs_path)
    logger.info(f"Using docs path: {docs_path}")

    if args.version not in SUPPORTED_VERSIONS:
        logger.error(f"Unsupported version: {args.version}. Supported versions: {', '.join(SUPPORTED_VERSIONS)}")
        sys.exit(1)

    return docs_path


def handle_documentation_update(docs_path: Path, version: str, update_docs: bool, force_update: bool) -> bool:
    """Handle documentation update if requested.
    
    Args:
        docs_path: Path to documentation directory
        version: Laravel version
        update_docs: Whether to update docs
        force_update: Whether to force update
        
    Returns:
        True if update was performed, False otherwise
    """
    if update_docs or force_update:
        logger.info(f"Updating documentation (version: {version}, force: {force_update})")
        updated = update_documentation(docs_path, version, force_update)
        if updated:
            logger.info("Documentation updated successfully")
        else:
            logger.info("Documentation update not performed or not needed")
        return updated
    return False


def build_rate_limiter(args) -> Optional["RateLimitingMiddleware"]:
    """Build the opt-in token-bucket limiter from CLI/env configuration.

    One global bucket for the whole server — a total-throughput cap, not
    per-client fairness; without auth there is no reliable client identity
    to key on. The limiter counts every MCP request including the initialize
    handshake, so the burst default stays comfortably above handshake size.

    Returns None when unset, or when the transport is stdio, where a single
    local client throttling itself serves nobody.
    """
    if args.rate_limit is None:
        return None

    if args.transport != "http":
        logger.warning(
            "A rate limit is configured but the transport is stdio; ignoring it. "
            "Rate limiting only applies to the HTTP transport."
        )
        return None

    # nan/inf pass a <=0 comparison and float() parses both from env, so a
    # finiteness check is what stands between a config typo and either an
    # uncontrolled math.ceil traceback or a bucket with infinite capacity.
    if not math.isfinite(args.rate_limit) or args.rate_limit <= 0:
        logger.error(f"--rate-limit must be a positive finite number, got {args.rate_limit}")
        sys.exit(1)

    burst = args.rate_limit_burst
    if burst is None:
        burst = max(10, math.ceil(2 * args.rate_limit))
    elif burst < 1:
        logger.error(f"--rate-limit-burst must be at least 1, got {burst}")
        sys.exit(1)

    from fastmcp.server.middleware.rate_limiting import RateLimitingMiddleware
    logger.info(f"Rate limiting enabled: {args.rate_limit} req/s, burst {burst}")
    return RateLimitingMiddleware(
        max_requests_per_second=args.rate_limit,
        burst_capacity=burst,
    )


def harden_verifier(verifier: "TokenVerifier") -> "TokenVerifier":
    """Make verify_token fail closed instead of raising.

    FastMCP's auth middleware eagerly verifies any request that carries an
    Authorization header — on every route, custom ones included — and an
    exception from the verifier (a JWKS fetch failing, say) becomes an
    app-wide 500, taking /healthz and /.well-known down with it. Catching
    here turns an outage into 401s for token-bearing requests while every
    public route keeps answering.
    """
    inner = verifier.verify_token

    async def resilient(token: str):
        try:
            return await inner(token)
        except Exception as e:
            logger.error(f"Token verification failed closed: {e}")
            return None

    verifier.verify_token = resilient  # type: ignore[method-assign]
    return verifier


def build_auth_provider(args) -> Optional["TokenVerifier"]:
    """Build the OAuth 2.1 token verifier from CLI/env configuration.

    The server is a resource server only: it validates bearer tokens issued
    elsewhere and never issues its own. Two mutually exclusive modes:

    - JWKS (production): --auth-jwks-uri + --auth-issuer + --auth-audience.
      Issuer and audience are mandatory -- accepting any issuer's tokens, or
      tokens minted for a different service, is authentication theater.
    - Static tokens (dev/internal, env only): AUTH_STATIC_TOKENS as
      "token:client_id[,token:client_id...]". Deliberately not a CLI flag so
      secrets stay out of process listings.

    Returns None when no auth is configured, or when the transport is stdio,
    where the process boundary is the access control.
    """
    static_tokens = os.environ.get("AUTH_STATIC_TOKENS", "").strip()
    jwks_configured = bool(args.auth_jwks_uri)

    if not static_tokens and not jwks_configured:
        return None

    if args.transport != "http":
        logger.warning(
            "Auth is configured but the transport is stdio; ignoring it. "
            "Bearer-token auth only applies to the HTTP transport."
        )
        return None

    if static_tokens and jwks_configured:
        logger.error("AUTH_STATIC_TOKENS and --auth-jwks-uri are mutually exclusive")
        sys.exit(1)

    if jwks_configured:
        if not args.auth_issuer or not args.auth_audience:
            logger.error(
                "--auth-jwks-uri requires --auth-issuer and --auth-audience: "
                "without them any issuer's tokens, or tokens minted for another "
                "service, would be accepted"
            )
            sys.exit(1)
        from fastmcp.server.auth.providers.jwt import JWTVerifier
        logger.info(f"Bearer-token auth enabled (JWKS: {args.auth_jwks_uri})")
        return harden_verifier(JWTVerifier(
            jwks_uri=args.auth_jwks_uri,
            issuer=args.auth_issuer,
            audience=args.auth_audience,
            required_scopes=args.auth_required_scope or None,
        ))

    tokens: Dict[str, Dict[str, Any]] = {}
    for entry in static_tokens.split(","):
        token, sep, client_id = entry.strip().partition(":")
        if not sep or not token or not client_id:
            logger.error(
                "AUTH_STATIC_TOKENS must be 'token:client_id[,token:client_id...]'"
            )
            sys.exit(1)
        tokens[token] = {"client_id": client_id, "scopes": args.auth_required_scope or []}
    from fastmcp.server.auth.providers.jwt import StaticTokenVerifier
    logger.warning(
        "Static-token auth enabled; fine for development, use --auth-jwks-uri "
        "with a real authorization server in production"
    )
    return harden_verifier(StaticTokenVerifier(tokens=tokens, required_scopes=args.auth_required_scope or None))


def _registry_metadata() -> Dict[str, Any]:
    """The repo's server.json with the running server's version stamped in.

    The checked-in file carries the last released version; a deployment built
    from a later commit should describe itself, not the file's snapshot.
    """
    data = json.loads(resource_path("server.json").read_text(encoding="utf-8"))
    data["version"] = SERVER_VERSION
    for package in data.get("packages", []):
        identifier = package.get("identifier", "")
        if ":" in identifier:
            # OCI packages have no separate version field (the registry
            # rejects one); the tag keeps its leading v because Harness tags
            # images with the git tag verbatim.
            package["identifier"] = f"{identifier.rsplit(':', 1)[0]}:v{SERVER_VERSION}"
    return data


def _server_icon() -> "Icon":
    """The repo icon as a self-contained data URI (SEP-973).

    Embedded rather than linked so clients need no network fetch and stdio
    servers have an icon at all.
    """
    import base64

    svg = (Path(__file__).parent / "icon.svg").read_bytes()
    encoded = base64.b64encode(svg).decode("ascii")
    return Icon(src=f"data:image/svg+xml;base64,{encoded}", mimeType="image/svg+xml")


def create_mcp_server(server_name: str, docs_path: Path, runtime_version: str, transform_mode: Optional[str] = "search", auth: Optional["TokenVerifier"] = None, rate_limiter: Optional["RateLimitingMiddleware"] = None) -> FastMCP:
    """Create and configure the MCP server with all tools and resources.

    Args:
        server_name: Name for the MCP server
        docs_path: Path to documentation directory
        runtime_version: Runtime default Laravel version (from --version flag)
        transform_mode: "search" for BM25SearchTransform (default),
                       "code" for CodeMode transform,
                       None for no transforms
        auth: Optional token verifier for the HTTP transport (see
              build_auth_provider); None leaves the server unauthenticated

    Returns:
        Configured FastMCP server instance
    """
    # Create the MCP server
    mcp: FastMCP = FastMCP(
        server_name,
        version=SERVER_VERSION,
        website_url=PROJECT_URL,
        icons=[_server_icon()],
        auth=auth,
        instructions=build_server_instructions(docs_path, runtime_version, transform_mode)
    )
    
    # Registry discovery endpoint (HTTP mode only; stdio never builds the app).
    # Public by design even when the MCP endpoint requires auth: it is the
    # same metadata the MCP Registry republishes to everyone.
    @mcp.custom_route("/.well-known/mcp/server.json", methods=["GET"])
    async def well_known_server_json(request: "Request") -> "JSONResponse":
        return JSONResponse(_registry_metadata())

    # Metrics collection is always on (negligible overhead: one lock and a
    # clock read per call) so the HTTP endpoints never lie about "since when".
    # Registered before the rate limiter so throttled requests still count —
    # the ordering contract is pinned by test, not assumed from upstream docs.
    mcp.add_middleware(MetricsMiddleware())
    if rate_limiter is not None:
        mcp.add_middleware(rate_limiter)
    start_time = time.monotonic()
    metrics_registry.set_info(SERVER_VERSION)
    metrics_registry.set_gauge_callable(
        "laravel_mcp_uptime_seconds",
        lambda: round(time.monotonic() - start_time, 3),
    )

    def _docs_age_days() -> Optional[float]:
        _, age = get_documentation_date(docs_path)
        return float(age) if age is not None else None

    metrics_registry.set_gauge_callable("laravel_mcp_docs_copy_age_days", _docs_age_days)

    def _health_payload() -> tuple[Dict[str, Any], int]:
        versions_available = sum(
            1 for v in SUPPORTED_VERSIONS if (docs_path / v).is_dir() and any((docs_path / v).glob("*.md"))
        )
        current_to, age = get_documentation_date(docs_path)
        stale = copy_is_stale(docs_path)
        if versions_available == 0:
            status, code = "unhealthy", 503
        elif stale:
            status, code = "degraded", 200
        else:
            status, code = "ok", 200
        return {
            "status": status,
            "version": SERVER_VERSION,
            "uptime_seconds": round(time.monotonic() - start_time, 3),
            "docs": {
                "versions_available": versions_available,
                "documentation_current_to": current_to or "unknown",
                # Numeric or null, never a string: monitors parse this field.
                "copy_age_days": age,
                "stale": stale,
            },
        }, code

    # Always public: load balancers cannot do OAuth. "degraded" (stale corpus)
    # still serves traffic; 503 is reserved for "no documentation readable".
    @mcp.custom_route("/healthz", methods=["GET"])
    async def healthz(request: "Request") -> "JSONResponse":
        payload, code = _health_payload()
        return JSONResponse(payload, status_code=code)

    # Custom routes bypass FastMCP's auth middleware (the .well-known route
    # relies on that), so this route enforces its own check with the same
    # TokenVerifier the MCP endpoint uses — token semantics cannot drift.
    @mcp.custom_route("/metrics", methods=["GET"])
    async def metrics_endpoint(request: "Request") -> "Response":
        if auth is not None:
            header = request.headers.get("authorization", "")
            token = header[7:] if header.lower().startswith("bearer ") else ""
            # verify_token is hardened at construction (see harden_verifier):
            # a verifier-side outage returns None rather than raising, so it
            # reads as 401 here — same as FastMCP's own middleware, which
            # verifies first on any request carrying an Authorization header.
            if not token or await auth.verify_token(token) is None:
                return Response(
                    "unauthorized\n", status_code=401,
                    headers={"WWW-Authenticate": "Bearer"},
                    media_type="text/plain",
                )
        return Response(
            render_prometheus(metrics_registry),
            media_type="text/plain; version=0.0.4; charset=utf-8",
        )

    # Initialize multi-source documentation updater
    multi_updater = MultiSourceDocsUpdater(docs_path, runtime_version)
    
    # Define resource handler functions
    def read_laravel_doc(path: str) -> str:
        """Read a specific Laravel documentation file."""
        logger.debug(f"read_laravel_doc function called with path: {path}")

        # Extract version and relative path, using runtime version as default
        version_inner, relative_path = get_version_from_path(path, runtime_version)

        # Make sure the path ends with .md
        if not relative_path.endswith('.md'):
            relative_path = f"{relative_path}.md"

        file_path = Path(docs_path) / version_inner / relative_path

        # Security check - read the resolved path this returns, not file_path,
        # so the file that was checked is the file that gets opened.
        version_path = Path(docs_path) / version_inner
        safe_path = resolve_contained_path(version_path, file_path)
        if safe_path is None:
            logger.warning(f"Access denied: {path} (attempted directory traversal)")
            return f"Access denied: {path} (attempted directory traversal)"

        if not safe_path.exists():
            logger.warning(f"Documentation file not found: {safe_path}")
            return f"Documentation file not found: {path} (version: {version_inner})"

        try:
            content = get_file_content_cached(str(safe_path))
            if not content.startswith("Error") and not content.startswith("File not found"):
                logger.debug(f"Successfully read file: {safe_path} ({len(content)} bytes)")
            return content
        except Exception as e:
            logger.error(f"Error reading file {safe_path}: {str(e)}")
            return f"Error reading file: {str(e)}"
    
    def read_external_laravel_doc(service: str, path: str) -> str:
        """Read a specific external Laravel service documentation file."""
        logger.debug(f"Reading external Laravel doc: {service}/{path}")
        
        try:
            # Validate service
            if service not in multi_updater.external_fetcher.list_available_services():
                available_services = multi_updater.external_fetcher.list_available_services()
                return f"Service '{service}' not found. Available: {', '.join(available_services)}"
            
            # Get service directory
            service_dir = multi_updater.external_fetcher.get_service_cache_path(service)
            
            # Make sure the path ends with .md
            if not path.endswith('.md'):
                path = f"{path}.md"
            
            file_path = service_dir / path
            
            # Security check - open the resolved path this returns, not
            # file_path, so the check and the open see the same file.
            safe_path = resolve_contained_path(service_dir, file_path)
            if safe_path is None:
                return f"Access denied: {service}/{path} (path traversal attempted)"

            if not safe_path.exists():
                # List available files to help user
                available_files = []
                try:
                    available_files = [f.name for f in service_dir.glob("*.md")][:10]
                except Exception:
                    pass
                
                if available_files:
                    return f"File not found: {service}/{path}. Available files: {', '.join(available_files)}"
                else:
                    return f"File not found: {service}/{path}. No documentation cached for {service}. Use update_external_laravel_docs(['{service}']) to fetch documentation."
            
            content = get_file_content_cached(str(safe_path))
            logger.debug(f"Successfully read external file: {safe_path} ({len(content)} bytes)")
            return content
        except Exception as e:
            logger.error(f"Error reading external file {service}/{path}: {str(e)}")
            return f"Error reading file: {str(e)}"
    
    def read_package_doc(package: str, path: str) -> str:
        """Read a fetched community-package documentation file."""
        packages_dir = Path(docs_path) / "packages"
        # The package key becomes the containment root: ".." here would make
        # packages/.. (the docs root) the root and serve core files through
        # this scheme — the same rule resolve_corpus_file enforces.
        if (
            not re.fullmatch(r"[A-Za-z0-9_-][A-Za-z0-9._-]*", package)
            or package in (".", "..")
            or resolve_contained_path(packages_dir, packages_dir / package) is None
        ):
            return f"Package '{package}' not found."
        package_dir = packages_dir / package
        if not package_dir.is_dir():
            available = sorted(
                p.name for p in packages_dir.iterdir() if p.is_dir()
            ) if packages_dir.is_dir() else []
            return f"Package '{package}' not found. Available: {', '.join(available) or 'none fetched'}"

        if not path.endswith('.md'):
            path = f"{path}.md"

        safe_path = resolve_contained_path(package_dir, package_dir / path)
        if safe_path is None:
            return f"Access denied: {package}/{path} (path traversal attempted)"
        if not safe_path.exists():
            return f"File not found: {package}/{path}"
        return get_file_content_cached(str(safe_path))

    # Register resources using functional approach (decorator as function)
    mcp.resource("laravel://{path*}")(read_laravel_doc)
    mcp.resource("laravel-external://{service}/{path*}")(read_external_laravel_doc)
    mcp.resource("laravel-package://{package}/{path*}")(read_package_doc)
    logger.debug("Registered resource template: laravel://{path*}")
    logger.debug("Registered resource template: laravel-external://{service}/{path*}")
    logger.debug("Registered resource template: laravel-package://{package}/{path*}")
    
    
    # Configure all tools
    configure_mcp_server(mcp, docs_path, runtime_version, multi_updater)

    # Apply transforms
    apply_transforms(mcp, transform_mode)

    return mcp


def configure_mcp_server(mcp: FastMCP, docs_path: Path, runtime_version: str, multi_updater: MultiSourceDocsUpdater) -> None:
    """Register the tools. They are declared in the `tools` package; this
    gives them the server they run in."""
    register_all(mcp, ToolContext(docs_path=Path(docs_path), runtime_version=runtime_version, updater=multi_updater))


def apply_transforms(mcp: FastMCP, transform_mode: Optional[str] = "search") -> None:
    """Apply search or code mode transforms to the MCP server.

    Args:
        mcp: FastMCP server instance
        transform_mode: "search" for BM25SearchTransform (default),
                       "code" for CodeMode transform,
                       None for no transforms
    """
    if transform_mode is None:
        logger.info("No transforms applied (raw tool mode)")
        return

    if transform_mode == "code":
        try:
            from fastmcp.experimental.transforms.code_mode import (
                CodeMode,
                GetTags,
                Search,
                GetSchemas,
            )
        except ImportError as e:
            raise RuntimeError(
                "Code Mode requires the code-mode extra. "
                "Install with: pip install 'fastmcp[code-mode]'"
            ) from e

        code_mode = CodeMode(
            discovery_tools=[GetTags(), Search(), GetSchemas()],
        )
        mcp.add_transform(code_mode)
        logger.info("Code Mode transform applied (experimental)")
    elif transform_mode == "search":
        mcp.add_transform(BM25SearchTransform(
            max_results=10,
            # Search returns section anchors; reading one is the other half of
            # the same move. Leaving the reader behind a search_tools lookup put
            # a round trip in the middle of the most common path.
            always_visible=["search_laravel_docs", "read_laravel_doc_section"],
        ))
        logger.info(
            "BM25 Search transform applied (max_results=10; search_laravel_docs "
            "and read_laravel_doc_section pinned)"
        )
    else:
        raise ValueError(f"Unknown transform_mode: {transform_mode!r}. Use 'search', 'code', or None.")


def build_http_app(args, mcp: FastMCP):
    """Assemble the HTTP app: host/origin guard, CORS, bind address.

    Extracted from main() so the assembled result is testable in-process;
    binding the socket stays in main(). Returns (app, host, port).
    """
    from starlette.middleware.cors import CORSMiddleware

    # Use PORT from environment or args, default to 8081. An explicit
    # --port 0 stays 0 (ephemeral bind); only an omitted port defaults.
    # Bind loopback by default: this server ships no authentication unless
    # auth flags are configured, so every tool is exposed to anyone who can
    # reach the socket.
    port = args.port if args.port is not None else 8081
    host = args.host or "127.0.0.1"
    is_loopback = host in ("127.0.0.1", "::1", "localhost")

    # FastMCP's origin guard matches allowed_origins with fnmatch, the same
    # way it matches allowed hosts: "https://*.example.com" in this list lets
    # any matching Origin through the DNS-rebinding protection while
    # presenting as a scoped allowlist. Reject every pattern entry loudly,
    # exactly like the ALLOWED_HOSTS check in parse_arguments.
    cors_origins = args.cors_origin or []
    pattern_origins = [o for o in cors_origins if any(c in o for c in "*?[")]
    if pattern_origins:
        logger.error(
            f"wildcard patterns are not accepted in CORS origins: {', '.join(pattern_origins)}. "
            "Pass explicit origins."
        )
        sys.exit(1)

    if not is_loopback:
        logger.warning(
            f"Binding {host} exposes the MCP server to the network. "
            "Restrict access at the network layer and set --allowed-host."
        )

    # Enable FastMCP's Host/Origin guard (off by default upstream). Strict
    # mode is required off-loopback, where the 'auto' heuristic disengages.
    app = mcp.http_app(
        host_origin_protection="auto" if is_loopback else True,
        allowed_hosts=args.allowed_host or None,
        allowed_origins=cors_origins or None,
    )

    # Browser clients need CORS; everything else does not. Only add the
    # middleware when explicit origins are configured, and never reflect
    # arbitrary origins with credentials attached.
    if cors_origins:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=cors_origins,
            allow_credentials=False,
            allow_methods=["GET", "POST", "OPTIONS"],
            allow_headers=["content-type", "mcp-session-id", "mcp-protocol-version", "authorization"],
            expose_headers=["mcp-session-id", "mcp-protocol-version"],
            max_age=86400,
        )
        logger.info(f"CORS enabled for: {', '.join(cors_origins)}")

    return app, host, port


def main():
    """Main entry point for the Laravel MCP Companion."""
    # The one place the server asks GitHub which Laravel versions exist.
    # Importing the module does not, so this runs before the arguments are
    # parsed: --version is validated against the refreshed list.
    refresh_supported_versions()
    args = parse_arguments()
    
    # Setup server environment
    docs_path = setup_server_environment(args)
    
    # Update documentation if requested
    handle_documentation_update(docs_path, args.version, args.update_docs, args.force_update)
    
    # Create temporary file paths if needed
    temp_files = []
    
    # Function to clean up temporary files
    def cleanup_temp_files():
        for file_path in temp_files:
            try:
                if os.path.exists(file_path):
                    logger.debug(f"Removing temporary file: {file_path}")
                    os.remove(file_path)
            except Exception as e:
                logger.warning(f"Failed to remove temporary file {file_path}: {str(e)}")
    
    # Resolve transform mode (--code-mode is a deprecated alias for --transform-mode code)
    if args.transform_mode is not None:
        mode = args.transform_mode
        if args.code_mode and mode != "code":
            logger.warning(f"--code-mode ignored because --transform-mode={mode} was given")
    elif args.code_mode:
        logger.warning("--code-mode is deprecated; use --transform-mode code")
        mode = "code"
    else:
        mode = "search"

    if mode == "code" and args.transport == "http":
        logger.warning(
            "Code Mode over HTTP exposes an execution endpoint. "
            "Do not expose this publicly unless you have reviewed sandbox and network risk."
        )

    # Create and configure the MCP server
    mcp = create_mcp_server(
        args.server_name, docs_path, args.version,
        transform_mode=None if mode == "none" else mode,
        auth=build_auth_provider(args),
        rate_limiter=build_rate_limiter(args)
    )

    # Log server startup
    logger.info(f"Starting Laravel MCP Companion ({args.server_name})")
    logger.info(f"Transport: {args.transport}")
    logger.info(f"Transform mode: {mode}")
    logger.info(f"Supported Laravel versions: {', '.join(SUPPORTED_VERSIONS)}")
    
    # Setup graceful shutdown handler
    shutdown_handler = GracefulShutdown(logger)
    
    # Define cleanup function
    def cleanup():
        logger.info("Performing cleanup before shutdown")
        
        # Clean up any temporary files
        cleanup_temp_files()
        
        # Save any pending state if needed
        try:
            # Example: save server stats or state
            logger.debug("Saving server state")
        except Exception as e:
            logger.error(f"Error saving server state: {str(e)}")
        
        logger.info("Cleanup complete")
    
    # Register cleanup with shutdown handler only (not with atexit)
    shutdown_handler.register(cleanup)
    
    # Run the server
    try:
        if args.transport == "http":
            # HTTP mode for web-based deployments
            logger.info("Starting in HTTP mode...")
            import uvicorn

            app, host, port = build_http_app(args, mcp)
            logger.info(f"Listening on {host}:{port}")

            uvicorn.run(app, host=host, port=port, log_level="info")
        else:
            logger.info("Server ready. Press Ctrl+C to stop.")
            mcp.run()
    except Exception as e:
        logger.critical(f"Server error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
