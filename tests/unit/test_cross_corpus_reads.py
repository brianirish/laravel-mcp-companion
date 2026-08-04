"""The search→read contract across every corpus.

Search returns hits as "<corpus-key>/<path>"; the read tools must resolve
exactly that shape for services, packages (nested included), and learning
sources — the flow was silently broken for service hits since v0.11.0.
"""

from pathlib import Path

import pytest

from mcp_tools import (
    read_laravel_doc_content_impl,
    read_laravel_doc_section_impl,
    search_laravel_docs_data,
)

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
    blog = temp_dir / "learning_resources" / "laravel-blog"
    blog.mkdir(parents=True)
    (blog / "index.md").write_text("# Blog\n\n## Recent\n\nArticle summaries here.\n")
    return temp_dir


class TestCorpusPrefixedReads:
    @pytest.mark.parametrize("filename,expected", [
        ("forge/servers/php.md", "Forge installs PHP"),
        ("spatie/laravel-permission/roles.md", "assignRole"),
        ("laravel-blog/index.md", "Article summaries"),
    ])
    def test_content_reads_resolve_corpus_prefixes(self, corpus, filename, expected):
        content = read_laravel_doc_content_impl(corpus, filename)
        assert expected in content

    @pytest.mark.parametrize("filename,section,expected", [
        ("forge/servers/php.md", "installing-php", "Forge installs PHP"),
        ("spatie/laravel-permission/roles.md", "assigning-roles", "assignRole"),
        ("laravel-blog/index.md", "recent", "Article summaries"),
    ])
    def test_section_reads_resolve_corpus_prefixes(self, corpus, filename, section, expected):
        content = read_laravel_doc_section_impl(corpus, filename, section)
        assert expected in content

    def test_core_paths_unchanged(self, corpus):
        assert "Core routing words" in read_laravel_doc_content_impl(corpus, "12.x/routing.md")
        assert "Core routing words" in read_laravel_doc_section_impl(corpus, "routing.md", "basics", version="12.x")

    def test_version_param_is_irrelevant_for_corpus_paths(self, corpus):
        """A corpus-prefixed read ignores the core version entirely."""
        content = read_laravel_doc_section_impl(
            corpus, "forge/servers/php.md", "installing-php", version="11.x"
        )
        assert "Forge installs PHP" in content

    @pytest.mark.parametrize("filename", [
        "forge/../../12.x/routing.md",
        "spatie/../../../etc/passwd",
    ])
    def test_traversal_from_corpus_roots_denied(self, corpus, filename):
        content = read_laravel_doc_content_impl(corpus, filename)
        assert "Access denied" in content or "not found" in content.lower()
        assert "Core routing words" not in content

    def test_unknown_prefix_falls_through_to_version_logic(self, corpus):
        content = read_laravel_doc_content_impl(corpus, "nonexistent/thing.md", version="12.x")
        assert "not found" in content.lower()


class TestSearchReadFlowContract:
    def test_every_hit_is_readable_back(self, corpus):
        """The contract this whole task exists for, per source type."""
        result = search_laravel_docs_data(
            corpus, "roles php routing article", "12.x",
            external_dir=corpus / "external", limit=10,
        )
        assert len({h["source"].split(":")[0] for h in result["results"]}) >= 3
        for hit in result["results"]:
            section = hit["anchor"] or hit["heading"]
            body = read_laravel_doc_section_impl(corpus, hit["file"], section)
            assert "not found" not in body.lower(), (hit, body)
            assert "Access denied" not in body


class TestPackageResource:
    async def test_package_resource_readable(self, corpus):
        from fastmcp import Client
        from laravel_mcp_companion import create_mcp_server

        server = create_mcp_server("TestServer", corpus, "12.x", transform_mode=None)
        async with Client(server) as client:
            content = await client.read_resource(
                "laravel-package://spatie/laravel-permission/roles.md"
            )
            assert "assignRole" in content[0].text

    async def test_unknown_package_lists_available(self, corpus):
        from fastmcp import Client
        from laravel_mcp_companion import create_mcp_server

        server = create_mcp_server("TestServer", corpus, "12.x", transform_mode=None)
        async with Client(server) as client:
            content = await client.read_resource("laravel-package://nope/intro.md")
            assert "not found" in content[0].text.lower()
            assert "spatie" in content[0].text


@pytest.mark.skipif(not (REPO_DOCS / "external").is_dir(), reason="real corpus absent")
class TestRealCorpusFlow:
    def test_nested_service_hit_reads_back(self):
        result = search_laravel_docs_data(
            REPO_DOCS, "supervisor daemon process", "12.x",
            external_dir=REPO_DOCS / "external", sources=["services"], limit=5,
        )
        assert result.get("results"), result
        top = result["results"][0]
        body = read_laravel_doc_section_impl(
            REPO_DOCS, top["file"], top["anchor"] or top["heading"]
        )
        assert "not found" not in body.lower(), (top, body[:200])
