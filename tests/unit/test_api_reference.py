"""API.md is generated from the running server and must match it.

A hand-written reference described a contract two releases dead by the time
anyone checked. This one is produced by scripts/generate_api_reference.py from
the tools a live server serves, and this test fails when the committed file
is not what the generator produces now.
"""

import importlib.util
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]


def generator():
    spec = importlib.util.spec_from_file_location("generate_api_reference", REPO_ROOT / "scripts" / "generate_api_reference.py")
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_the_committed_reference_is_what_the_generator_produces():
    committed = (REPO_ROOT / "API.md").read_text(encoding="utf-8")

    assert committed == generator().render(), "API.md is out of date. Run: python scripts/generate_api_reference.py"


def test_the_reference_documents_every_tool_and_error_code():
    from laravel_mcp_companion.tools import ERROR_CODES, REGISTRY

    reference = (REPO_ROOT / "API.md").read_text(encoding="utf-8")

    assert [name for name in REGISTRY if f"### `{name}`" not in reference] == []
    assert [code for code in ERROR_CODES if f"| `{code}` |" not in reference] == []


def test_experimental_tools_are_marked_as_such():
    reference = (REPO_ROOT / "API.md").read_text(encoding="utf-8")
    section = reference.split("### `get_laravel_learning_path`", 1)[1].split("###", 1)[0]

    assert "Experimental" in section
