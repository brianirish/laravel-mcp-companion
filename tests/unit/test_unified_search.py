"""Unified search: packages and learning resources join the flagship search.

Fixture-tree tests pin the mechanics (sources filter, labels, precedence);
the real-corpus tests pin retrieval quality for the queries that returned
noise before this existed.
"""

from pathlib import Path

import pytest

from mcp_tools import search_laravel_docs_data

REPO_DOCS = Path(__file__).resolve().parents[2] / "docs"


@pytest.fixture
def corpus(temp_dir):
    """A miniature four-source corpus with distinctive vocabulary per source."""
    core = temp_dir / "12.x"
    core.mkdir()
    (core / "queues.md").write_text(
        "# Queues\n\n## Retrying Failed Jobs\n\nUse queue:retry to retry failed "
        "jobs from the failed_jobs table after fixing the underlying exception.\n"
    )
    forge = temp_dir / "external" / "forge"
    forge.mkdir(parents=True)
    (forge / "daemons.md").write_text(
        "# Daemons\n\n## Supervisor Daemons\n\nForge manages supervisor daemon "
        "processes that keep queue workers running on your server.\n"
    )
    spatie = temp_dir / "packages" / "spatie"
    spatie.mkdir(parents=True)
    (spatie / "laravel-permission-roles.md").write_text(
        "# Roles and Permissions\n\n## Assigning Roles\n\nThe spatie permission "
        "package assigns roles to users with assignRole and syncRoles methods, "
        "including for queue worker contexts.\n"
    )
    blog = temp_dir / "learning_resources" / "laravel-blog"
    blog.mkdir(parents=True)
    (blog / "index.md").write_text(
        "# Laravel Blog - Recent Articles\n\n## Laracon Announcements\n\n"
        "Everything announced at the conference including managed queues.\n"
    )
    return temp_dir


def files_of(result):
    return [hit["file"] for hit in result.get("results", [])]


def sources_of(result):
    return {hit["source"] for hit in result.get("results", [])}


class TestSourcesFanOut:
    def test_default_reaches_all_four_sources(self, corpus):
        result = search_laravel_docs_data(
            corpus, "queue", "12.x", external_dir=corpus / "external", limit=10
        )
        assert "error" not in result
        assert {"core", "service:forge", "package:spatie", "learning:laravel-blog"} <= sources_of(result)

    def test_sources_filter_narrows(self, corpus):
        result = search_laravel_docs_data(
            corpus, "roles permission", "12.x",
            external_dir=corpus / "external", sources=["packages"], limit=10,
        )
        assert sources_of(result) == {"package:spatie"}
        assert set(files_of(result)) == {"spatie/laravel-permission-roles.md"}

    def test_sources_core_equals_include_external_false(self, corpus):
        via_sources = search_laravel_docs_data(
            corpus, "queue", "12.x", external_dir=corpus / "external",
            sources=["core"], limit=10,
        )
        via_flag = search_laravel_docs_data(
            corpus, "queue", "12.x", include_external=False,
            external_dir=None, limit=10,
        )
        assert files_of(via_sources) == files_of(via_flag)
        assert sources_of(via_sources) == {"core"}

    def test_explicit_sources_beats_include_external(self, corpus):
        result = search_laravel_docs_data(
            corpus, "roles permission", "12.x", include_external=False,
            external_dir=corpus / "external", sources=["packages"], limit=10,
        )
        assert sources_of(result) == {"package:spatie"}

    def test_invalid_source_names_the_valid_set(self, corpus):
        result = search_laravel_docs_data(
            corpus, "queue", "12.x", external_dir=corpus / "external",
            sources=["core", "reddit"], limit=10,
        )
        assert "error" in result
        for valid in ("core", "services", "packages", "learning"):
            assert valid in str(result)

    def test_version_scopes_core_only(self, corpus):
        """Package hits are identical whichever core version is searched."""
        a = search_laravel_docs_data(
            corpus, "roles permission", "12.x",
            external_dir=corpus / "external", sources=["packages"], limit=10,
        )
        b = search_laravel_docs_data(
            corpus, "roles permission", "11.x",
            external_dir=corpus / "external", sources=["packages"], limit=10,
        )
        assert files_of(a) == files_of(b) != []

    def test_hits_remain_readable_shape(self, corpus):
        result = search_laravel_docs_data(
            corpus, "supervisor daemon", "12.x",
            external_dir=corpus / "external", limit=5,
        )
        top = result["results"][0]
        assert set(top) >= {"file", "anchor", "heading", "score", "snippet", "source"}
        assert top["file"].startswith("forge/")


@pytest.mark.skipif(not (REPO_DOCS / "packages").is_dir(), reason="real corpus absent")
class TestRealCorpusQuality:
    def test_spatie_query_surfaces_the_spatie_docs(self):
        result = search_laravel_docs_data(
            REPO_DOCS, "spatie permission roles", "12.x",
            external_dir=REPO_DOCS / "external", limit=5,
        )
        top3_sources = [h["source"] for h in result["results"][:3]]
        assert any(s == "package:spatie" for s in top3_sources), result["results"][:3]

    def test_livewire_query_surfaces_livewire_docs(self):
        result = search_laravel_docs_data(
            REPO_DOCS, "livewire wire:model binding", "12.x",
            external_dir=REPO_DOCS / "external", limit=5,
        )
        assert any(h["source"] == "package:livewire" for h in result["results"]), \
            result["results"]

    def test_core_query_still_prefers_core(self):
        result = search_laravel_docs_data(
            REPO_DOCS, "how do I retry a failed queue job", "12.x",
            external_dir=REPO_DOCS / "external", limit=5,
        )
        assert result["results"][0]["source"] == "core"
        assert "queues.md" in result["results"][0]["file"]
