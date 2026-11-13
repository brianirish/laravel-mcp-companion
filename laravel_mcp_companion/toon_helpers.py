"""TOON encoding for tool results.

TOON (Token-Oriented Object Notation) says the same thing as JSON in fewer
tokens, which is what a tool result is paid for in. Every tool returns its
payload twice: as TOON in the text content, for a model to read, and as the
object itself in the structured content, for a program.
"""

from typing import Any

from toon_format import encode


def toon_encode(data: Any) -> str:
    """Encode data as TOON.

    An encoding failure is raised. It used to fall back to `str(data)`, which
    handed the client a Python repr in a field documented as TOON.
    """
    return encode(data)
