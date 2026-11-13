"""The search→read contract across every corpus.

Search returns hits as "<corpus-key>/<path>"; the read tools must resolve
exactly that shape for services, packages (nested included), and learning
sources — the flow was silently broken for service hits since v0.11.0.
"""

from pathlib import Path

import pytest

from laravel_mcp_companion.tools import ToolFailure
from laravel_mcp_companion.tools.docs import read_content, read_section
from laravel_mcp_companion.tools.search import search

REPO_DOCS = Path(__file__).resolve().parents[2] / "docs"


@pytest.fixture
def corpus(temp_dir):
    core = temp_dir / "12.x"
    core.mkdir()
    (core / "routing.md").write_text("# Routing\n\n## Basics\n\nCore routing words.\n")
    forge = temp_dir / "external" / "forge"
    (forge / "servers").mkdir(parents=True)
    (forge / "servers" / "php.md").write_text(
        "# PHP\n\n## Installing PHP\n\nForge installs PHP versions per server.\n"
    )
    spatie = temp_dir / "packages" / "spatie" / "laravel-permission"
    spatie.mkdir(parents=True)
    (spatie / "roles.md").write_text(
        "# Roles\n\n## Assigning Roles\n\nAssign roles with assignRole.\n"
    )
    blog = temp_dir / "learning_resources" / "laracasts-index"
    blog.mkdir(parents=True)
    (blog / "index.md").write_text("# Blog\n\n## Recent\n\nArticle summaries here.\n")
    return temp_dir


class TestCorpusPrefixedReads:
    @pytest.mark.parametrize("filename,expected", [
        ("forge/servers/php.md", "Forge installs PHP"),
        ("spatie/laravel-permission/roles.md", "assignRole"),
        ("laracasts-index/index.md", "Article summaries"),
    ])
    def test_content_reads_resolve_corpus_prefixes(self, corpus, filename, expected):
        reply = read_content(corpus, filename)

        assert expected in reply.text
        assert reply.data["file"] == filename
        assert reply.data["corpus"] == filename.split("/")[0]

    @pytest.mark.parametrize("filename,section,expected", [
        ("forge/servers/php.md", "installing-php", "Forge installs PHP"),
        ("spatie/laravel-permission/roles.md", "assigning-roles", "assignRole"),
        ("laracasts-index/index.md", "recent", "Article summaries"),
    ])
    def test_section_reads_resolve_corpus_prefixes(self, corpus, filename, section, expected):
        assert expected in read_section(corpus, filename, section).text

    def test_core_paths_unchanged(self, corpus):
        assert "Core routing words" in read_content(corpus, "12.x/routing.md").text
        assert "Core routing words" in read_section(corpus, "routing.md", "basics", version="12.x").text

    def test_a_core_read_reports_its_version_and_no_corpus(self, corpus):
        data = read_content(corpus, "12.x/routing.md").data

        assert (data["file"], data["version"]) == ("routing.md", "12.x")
        assert "corpus" not in data

    def test_version_param_is_irrelevant_for_corpus_paths(self, corpus):
        """A corpus-prefixed read ignores the core version entirely."""
        reply = read_section(corpus, "forge/servers/php.md", "installing-php", version="11.x")

        assert "Forge installs PHP" in reply.text

    @pytest.mark.parametrize("filename", [
        "forge/../../12.x/routing.md",
        "spatie/../../../etc/passwd",
        # ".." as the corpus key would make external/.. (= the docs root) a
        # readable corpus — the regression the traversal suite caught.
        "../12.x/routing.md",
        "../12.x-backup/leak.md",
        "./forge/servers/php.md",
        ".metadata/sync_info.json.md",
    ])
    def test_traversal_from_corpus_roots_denied(self, corpus, filename):
        # Read as Laravel 11.x, a version this corpus has no directory for, so
        # a path that climbs into 12.x is climbing out of its own root.
        with pytest.raises(ToolFailure) as raised:
            read_content(corpus, filename, version="11.x")

        assert raised.value.code in ("access_denied", "not_found")
        assert "Core routing words" not in str(raised.value.payload())

    def test_unknown_prefix_falls_through_to_version_logic(self, corpus):
        with pytest.raises(ToolFailure) as raised:
            read_content(corpus, "nonexistent/thing.md", version="12.x")

        assert raised.value.code == "not_found"


class TestOutline:
    def test_an_outline_lists_headings_without_the_text(self, corpus):
        data = read_content(corpus, "forge/servers/php.md", mode="outline")

        assert data["headings"] == [
            {"level": 1, "text": "PHP", "section": ""},
            {"level": 2, "text": "Installing PHP", "section": "installing-php"},
        ]
        assert "content" not in data

    def test_a_hash_inside_a_code_block_is_not_a_heading(self, temp_dir):
        (temp_dir / "12.x").mkdir()
        (temp_dir / "12.x" / "artisan.md").write_text(
            "# Artisan\n\n## Usage\n\n```shell\n# install the thing\nphp artisan install\n```\n\n## Next\n\nMore.\n"
        )

        headings = [h["text"] for h in read_content(temp_dir, "artisan.md", version="12.x", mode="outline")["headings"]]

        assert headings == ["Artisan", "Usage", "Next"]

    def test_a_section_named_in_an_outline_can_be_read(self, corpus):
        outline = read_content(corpus, "spatie/laravel-permission/roles.md", mode="outline")
        section = next(h["section"] for h in outline["headings"] if h["level"] == 2)

        assert "assignRole" in read_section(corpus, "spatie/laravel-permission/roles.md", section).text

    def test_an_unknown_mode_is_refused(self, corpus):
        with pytest.raises(ToolFailure) as raised:
            read_content(corpus, "12.x/routing.md", mode="summary")

        assert raised.value.code == "invalid_argument"


class TestSearchReadFlowContract:
    def test_every_hit_is_readable_back(self, corpus):
        """The contract this whole task exists for, per source type."""
        result = search(corpus, corpus / "external", "roles php routing article", version="12.x", limit=10)

        assert len({h["source"].split(":")[0] for h in result["results"]}) >= 3
        for hit in result["results"]:
            assert read_section(corpus, hit["file"], hit["section"], runtime_version="12.x").data["content"]


class TestPackageResource:
    async def test_package_key_traversal_denied(self, corpus):
        """'..' as the package key made packages/.. (the docs root) the
        containment root — the same hole resolve_corpus_file closes, left
        open in the resource handler. laravel-package://../12.x/routing.md
        must not serve core files through the package scheme."""
        from fastmcp import Client
        from laravel_mcp_companion.server import create_mcp_server

        server = create_mcp_server("TestServer", corpus, "12.x", transform_mode=None)
        async with Client(server) as client:
            content = await client.read_resource("laravel-package://../12.x/routing.md")
            text = content[0].text
            assert "Core routing words" not in text
            assert "not found" in text.lower() or "denied" in text.lower()

    async def test_symlinked_ecosystem_not_indexed_or_served(self, corpus, temp_dir):
        """A symlinked ecosystem dir must be invisible to BOTH search and
        read — indexing what reading refuses is the search-as-oracle
        asymmetry the v0.11 containment work eliminated."""
        import os

        outside = temp_dir.parent / "outside-tree"
        outside.mkdir(exist_ok=True)
        (outside / "secret.md").write_text(
            "# Secret\n\n## Planted\n\nOUTSIDE-CONTENT that must never index.\n"
        )
        os.symlink(outside, corpus / "packages" / "linked")

        from laravel_mcp_companion.mcp_tools import load_package_sections

        sections = load_package_sections(corpus / "packages")
        assert all(s.version != "linked" for s in sections)
        assert all("OUTSIDE-CONTENT" not in s.text for s in sections)
    async def test_package_resource_readable(self, corpus):
        from fastmcp import Client
        from laravel_mcp_companion.server import create_mcp_server

        server = create_mcp_server("TestServer", corpus, "12.x", transform_mode=None)
        async with Client(server) as client:
            content = await client.read_resource(
                "laravel-package://spatie/laravel-permission/roles.md"
            )
            assert "assignRole" in content[0].text

    async def test_unknown_package_lists_available(self, corpus):
        from fastmcp import Client
        from laravel_mcp_companion.server import create_mcp_server

        server = create_mcp_server("TestServer", corpus, "12.x", transform_mode=None)
        async with Client(server) as client:
            content = await client.read_resource("laravel-package://nope/intro.md")
            assert "not found" in content[0].text.lower()
            assert "spatie" in content[0].text


@pytest.mark.skipif(not (REPO_DOCS / "external").is_dir(), reason="real corpus absent")
class TestRealCorpusFlow:
    def test_nested_service_hit_reads_back(self):
        result = search(REPO_DOCS, REPO_DOCS / "external", "supervisor daemon process", version="12.x", sources=["services"])

        assert result["count"], result
        top = result["results"][0]
        assert read_section(REPO_DOCS, top["file"], top["section"]).data["content"]
