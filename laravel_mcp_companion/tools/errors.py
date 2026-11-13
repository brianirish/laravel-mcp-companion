"""How a tool reports failure.

A tool that cannot do what it was asked raises `ToolFailure`. The registry
turns that into a result marked `isError`, carrying one object in both its
text and its structured content:

    {"error": {"code": "unknown_version", "message": "...", "details": {...}}}

`code` is one of ERROR_CODES and is what a client should branch on; `message`
is for a person or a model to read. Success payloads never contain an `error`
key, so the two shapes cannot be confused and each success schema can name
its required fields.

Finding nothing is not a failure. A search with no hits, or a category with
no documents, succeeds with `count: 0`.
"""

from typing import Any, Dict, Optional

# What went wrong, for a client to branch on, and what each code means.
ERROR_MEANINGS: Dict[str, str] = {
    "invalid_argument": "An argument was missing, empty or not one of the allowed values.",
    "unknown_version": "A Laravel version this server does not carry.",
    "not_found": "The named file, section, package, service, category or path does not exist.",
    "access_denied": "A path that resolves outside the documentation tree.",
    "update_failed": "A documentation update could not be completed.",
    "internal": "Anything unexpected. The message says which tool failed.",
}
ERROR_CODES = tuple(ERROR_MEANINGS)

ERROR_SCHEMA: Dict[str, Any] = {
    "type": "object",
    "required": ["error"],
    "properties": {
        "error": {
            "type": "object",
            "required": ["code", "message"],
            "properties": {
                "code": {"type": "string", "enum": list(ERROR_CODES)},
                "message": {"type": "string"},
                "details": {
                    "type": "object",
                    "description": "Whatever helps the caller recover: the supported versions, the sections a file does have.",
                },
            },
        }
    },
}


class ToolFailure(Exception):
    """A tool could not do what it was asked."""

    def __init__(self, code: str, message: str, details: Optional[Dict[str, Any]] = None):
        if code not in ERROR_CODES:
            raise ValueError(f"unknown error code: {code!r}")
        super().__init__(message)
        self.code = code
        self.message = message
        self.details = details or {}

    def payload(self) -> Dict[str, Any]:
        error: Dict[str, Any] = {"code": self.code, "message": self.message}
        if self.details:
            error["details"] = self.details
        return {"error": error}
