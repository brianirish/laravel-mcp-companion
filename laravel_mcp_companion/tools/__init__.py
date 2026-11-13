"""The server's tools.

Importing this package declares every tool: each module below registers its
tools with `registry.REGISTRY` as it is imported. `register_all` then attaches
them to a server.

STABLE_TOOLS is the surface the versioning policy covers. The tools in
EXPERIMENTAL_TOOLS are shipped and tested, and may change in a minor release.
"""

from . import catalog, docs, learning, search  # noqa: F401  (imported for their registrations)
from .errors import ERROR_CODES, ERROR_MEANINGS, ERROR_SCHEMA, ToolFailure
from .registry import REGISTRY, Reply, ToolContext, ToolSpec, register_all

STABLE_TOOLS = tuple(name for name, spec in REGISTRY.items() if spec.stable)
EXPERIMENTAL_TOOLS = tuple(name for name, spec in REGISTRY.items() if not spec.stable)

__all__ = [
    "ERROR_CODES", "ERROR_MEANINGS", "ERROR_SCHEMA", "EXPERIMENTAL_TOOLS", "REGISTRY", "Reply", "STABLE_TOOLS",
    "ToolContext", "ToolFailure", "ToolSpec", "register_all",
]
