"""Cheaply-testable README claims, guarded so they cannot rot.

Born from the 2026-08 claims audit (docs/superpowers/specs/
2026-08-03-claims-audit-notes.md): "50+ curated packages" had drifted from a
22-entry catalog, and the search description advertised a contract two
releases dead.
"""

import json
import re
import shlex
import statistics
import tomllib
from pathlib import Path

import pytest

from laravel_mcp_companion import docs_updater, mcp_tools
from laravel_mcp_companion.catalog import PACKAGE_CATALOG
from laravel_mcp_companion.tools import EXPERIMENTAL_TOOLS, REGISTRY

REPO_ROOT = Path(__file__).resolve().parents[2]


def readme() -> str:
    return (REPO_ROOT / "README.md").read_text(encoding="utf-8")


def test_curated_package_count_matches_catalog():
    matches = re.findall(r"(\d+)\+? curated packages", readme())
    assert matches, "README no longer states the curated-package count"
    for figure in matches:
        assert int(figure) == len(PACKAGE_CATALOG), (
            f"README claims {figure} curated packages; the catalog has "
            f"{len(PACKAGE_CATALOG)}"
        )


def test_search_description_matches_the_actual_contract():
    description = REGISTRY["search_laravel_docs"].description
    assert "match counts" not in description  # the pre-v0.11 contract
    assert "ranked" in description.lower()
    assert "sources" in description


def test_readme_search_copy_matches_the_actual_contract():
    """The README's search claims regress independently of the tool
    description — both surfaces are guarded."""
    text = readme()
    assert "match counts" not in text
    assert "source label" in text or "`sources`" in text, (
        "README no longer documents the unified-search source labeling/filter"
    )
    unified = re.search(r"\*\*Unified search\*\*[^*]*", text)
    assert unified, "README lost its Unified search bullet"
    for corpus in ("core", "services", "package", "learning"):
        assert corpus in unified.group(0).lower(), (
            f"Unified search bullet no longer names the {corpus} corpus"
        )


@pytest.mark.skipif(
    not (REPO_ROOT / "docs" / "packages").is_dir(), reason="shipped corpus absent"
)
def test_named_package_ecosystems_are_fetched():
    fetched = {p.name for p in (REPO_ROOT / "docs" / "packages").iterdir() if p.is_dir()}
    for name in ("spatie", "livewire", "inertia", "filament"):
        assert name in fetched, f"README names {name} but it is not fetched"


def descriptions() -> dict[str, str]:
    """Every place that states the range of Laravel versions held."""
    pyproject = tomllib.loads((REPO_ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    server = json.loads((REPO_ROOT / "server.json").read_text(encoding="utf-8"))
    return {
        "README.md": readme(),
        "pyproject.toml": pyproject["project"]["description"],
        "server.json": server["description"],
    }


def test_every_stated_version_range_starts_at_the_oldest_held_and_ends_at_one_held():
    # A range that stops short of a newly added version is incomplete, not
    # false, so it does not fail here: the nightly sync adds versions on its own.
    held = list(docs_updater.SUPPORTED_VERSIONS)
    for where, text in descriptions().items():
        ranges = re.findall(r"(\d+\.x) (?:through|to) (\d+\.x)", text)
        ranges += [(first, held[-1]) for first in re.findall(r"since (\d+\.x)", text)]
        assert ranges or where == "README.md", f"{where} no longer states a version range"
        for first, last in ranges:
            assert first == held[0], f"{where} says {first}; the oldest version held is {held[0]}"
            assert last in held, f"{where} says {last}, which is not held ({held})"
    assert re.search(r"\d+\.x (?:through|to) \d+\.x", readme())


def readme_tool_table() -> dict[str, str]:
    rows = re.findall(r"^\| `([a-z_]+)` \| (.+) \|$", readme(), re.MULTILINE)
    assert rows, "README lost its tool table"
    return dict(rows)


def test_the_tool_table_lists_every_tool_and_nothing_else():
    assert set(readme_tool_table()) == set(REGISTRY)


def test_the_tools_marked_experimental_are_the_experimental_ones():
    marked = {name for name, text in readme_tool_table().items() if "*(experimental)*" in text}
    assert marked == set(EXPERIMENTAL_TOOLS)


def install_commands() -> list[list[str]]:
    """The command and arguments of every way the README tells a client to start the server."""
    commands = []
    for block in re.findall(r"```json\n(.*?)```", readme(), re.DOTALL):
        for entry in json.loads(block)["mcpServers"].values():
            commands.append([entry["command"], *entry["args"]])
    for line in re.findall(r"^claude mcp add .*$", readme(), re.MULTILINE):
        words = shlex.split(line)
        commands.append(words[words.index("--") + 1:])
    return commands


def test_every_install_command_starts_the_published_server():
    pyproject = tomllib.loads((REPO_ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    package = pyproject["project"]["name"]
    assert package in pyproject["project"]["scripts"], "the package name is not its command"
    server = json.loads((REPO_ROOT / "server.json").read_text(encoding="utf-8"))
    oci = next(p for p in server["packages"] if p["registryType"] == "oci")
    image = oci["identifier"].rsplit(":", 1)[0] + ":latest"

    commands = install_commands()
    assert len(commands) == 4, commands
    for command in commands:
        assert command in (["uvx", package], ["docker", "run", "--rm", "-i", image]), command
    assert ["uvx", package] in commands and ["docker", "run", "--rm", "-i", image] in commands


def test_operations_lists_every_option_and_environment_variable():
    source = (REPO_ROOT / "laravel_mcp_companion" / "server.py").read_text(encoding="utf-8")
    parser = source[source.index("def parse_arguments"):source.index("args = parser.parse_args()")]
    options = set(re.findall(r'^\s+"(--[a-z-]+)",', parser, re.MULTILINE))
    variables = set(re.findall(r'(?:os\.environ\.get\(|os\.environ\[|_split_env_list\()"([A-Z_]+)"', source))
    assert len(options) >= 19 and variables, (options, variables)

    operations = (REPO_ROOT / "OPERATIONS.md").read_text(encoding="utf-8")
    for name in sorted(options):
        assert f"| `{name}" in operations, f"OPERATIONS.md has no row for {name}"
    for name in sorted(variables):
        assert f"`{name}" in operations, f"OPERATIONS.md does not mention {name}"


def tokens(text: str) -> float:
    # About four characters to a token in English prose and markdown.
    return len(text) / 4


@pytest.mark.corpus
def test_section_and_page_sizes_are_as_the_readme_says():
    """README: a section is usually under a thousand tokens; a whole page is
    usually several thousand, and the longest run past 30,000."""
    version = docs_updater.get_default_version()
    sections = mcp_tools.load_version_sections(REPO_ROOT / "docs", version)
    pages = [tokens(p.read_text(encoding="utf-8")) for p in (REPO_ROOT / "docs" / version).glob("*.md")]
    assert sections and pages

    assert statistics.median(tokens(s.text) for s in sections) < 1000
    assert 2000 <= statistics.median(pages) < 10000
    assert max(pages) > 30000
