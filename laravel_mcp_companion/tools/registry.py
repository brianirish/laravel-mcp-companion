"""The tool surface, declared in one place.

Every tool is a module-level function decorated with `@tool`. The decorator
records a `ToolSpec` in `REGISTRY`, and `register_all` hands each spec to the
server. Nothing else registers a tool, so `REGISTRY` is the whole surface: the
snapshot test that pins the v1 contract reads it through a live server and
fails when a name, an input schema or an output schema changes.

A tool function returns its success payload as a dict, or a `Reply` when the
text a client should read is not the payload's TOON encoding (a documentation
page reads better as the markdown it is). It raises `ToolFailure` when it
cannot do what was asked; see errors.py for what the client receives.
"""

import functools
import inspect
import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, Dict, FrozenSet, Optional

from fastmcp import Context, FastMCP
from fastmcp.tools.tool import ToolResult
from mcp.types import TextContent

from ..docs_updater import MultiSourceDocsUpdater
from ..toon_helpers import toon_encode
from .errors import ToolFailure

logger = logging.getLogger("laravel-mcp-companion")


@dataclass(frozen=True)
class ToolContext:
    """What a tool needs from the server it is running in."""

    docs_path: Path
    runtime_version: str
    updater: MultiSourceDocsUpdater

    @property
    def external_dir(self) -> Path:
        return self.updater.external_fetcher.external_dir


@dataclass(frozen=True)
class Reply:
    """A success payload whose text form is given, not derived."""

    data: Dict[str, Any]
    text: str


@dataclass(frozen=True)
class ToolSpec:
    name: str
    handler: Callable[..., Any]
    description: str
    output_schema: Dict[str, Any]
    tags: FrozenSet[str]
    # Covered by the semantic-versioning guarantee. A tool with stable=False
    # is shipped and tested but may change in a minor release.
    stable: bool = True
    read_only: bool = True
    open_world: bool = False
    task: bool = False
    timeout: Optional[float] = None


REGISTRY: Dict[str, ToolSpec] = {}

_CONTEXT_ATTRIBUTE = "_laravel_companion_context"


def companion(ctx: Context) -> ToolContext:
    """The ToolContext of the server this call arrived at."""
    return getattr(ctx.fastmcp, _CONTEXT_ATTRIBUTE)


def success(result: Any) -> ToolResult:
    if isinstance(result, Reply):
        return ToolResult(content=[TextContent(type="text", text=result.text)], structured_content=result.data)
    return ToolResult(content=[TextContent(type="text", text=toon_encode(result))], structured_content=result)


def failure(error: ToolFailure) -> ToolResult:
    payload = error.payload()
    return ToolResult(
        content=[TextContent(type="text", text=toon_encode(payload))],
        structured_content=payload,
        is_error=True,
    )


def _reporting_failures(name: str, fn: Callable[..., Any]) -> Callable[..., Any]:
    """Wrap a tool so a ToolFailure, or anything unexpected, becomes an error
    result instead of an exception the framework would render as prose."""

    def unexpected(exc: Exception) -> ToolResult:
        logger.exception(f"{name} failed unexpectedly")
        return failure(ToolFailure("internal", f"{name} failed: {exc}"))

    if inspect.iscoroutinefunction(fn):
        @functools.wraps(fn)
        async def async_wrapper(*args: Any, **kwargs: Any) -> ToolResult:
            try:
                return success(await fn(*args, **kwargs))
            except ToolFailure as error:
                return failure(error)
            except Exception as exc:
                return unexpected(exc)

        return async_wrapper

    @functools.wraps(fn)
    def wrapper(*args: Any, **kwargs: Any) -> ToolResult:
        try:
            return success(fn(*args, **kwargs))
        except ToolFailure as error:
            return failure(error)
        except Exception as exc:
            return unexpected(exc)

    return wrapper


def tool(
    name: str,
    *,
    description: str,
    output_schema: Dict[str, Any],
    tags: FrozenSet[str] = frozenset(),
    stable: bool = True,
    read_only: bool = True,
    open_world: bool = False,
    task: bool = False,
    timeout: Optional[float] = None,
) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    def decorate(fn: Callable[..., Any]) -> Callable[..., Any]:
        if name in REGISTRY:
            raise ValueError(f"tool {name!r} is declared twice")
        handler = _reporting_failures(name, fn)
        # The framework builds the input schema from the signature; the
        # wrapper's return annotation would otherwise be read as the output.
        handler.__annotations__ = {**getattr(fn, "__annotations__", {}), "return": ToolResult}
        REGISTRY[name] = ToolSpec(
            name=name, handler=handler, description=description, output_schema=output_schema,
            tags=frozenset(tags), stable=stable, read_only=read_only, open_world=open_world,
            task=task, timeout=timeout,
        )
        return fn

    return decorate


def register_all(mcp: FastMCP, context: ToolContext) -> None:
    """Attach the context to the server and register every declared tool."""
    setattr(mcp, _CONTEXT_ATTRIBUTE, context)
    for spec in REGISTRY.values():
        annotations: Dict[str, Any] = {"readOnlyHint": spec.read_only, "idempotentHint": True}
        if not spec.read_only:
            annotations["destructiveHint"] = False
        if spec.open_world:
            annotations["openWorldHint"] = True
        options: Dict[str, Any] = {
            "name": spec.name,
            "description": spec.description,
            "annotations": annotations,
            "tags": set(spec.tags) | ({"experimental"} if not spec.stable else set()),
            "output_schema": spec.output_schema,
        }
        if spec.task:
            options["task"] = True
        if spec.timeout is not None:
            options["timeout"] = spec.timeout
        mcp.tool(**options)(spec.handler)
