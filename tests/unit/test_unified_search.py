"""search_laravel_docs: one ranked search over every corpus.

Fixture-tree tests pin the mechanics (sources, labels, limits, how a page of
results is shared out). The real-corpus tests pin retrieval quality for
queries that have gone wrong before.
"""

from pathlib import Path

import pytest

from laravel_mcp_companion.doc_search import Section
from laravel_mcp_companion.tools import ToolFailure
from laravel_mcp_companion.tools.docs import read_section
from laravel_mcp_companion.tools.search import (
    MAX_LIMIT, keep_need_page, matched_needs, rank_hits, search, spread_across_sources,
)

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
    (core / "filesystem.md").write_text(
        "# File Storage\n\n<a name=\"file-uploads\"></a>\n## File Uploads\n\nStore an uploaded "
        "file on a disk with the store method of the uploaded file instance.\n"
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
    learning = temp_dir / "learning_resources" / "laracasts-index"
    learning.mkdir(parents=True)
    (learning / "index.md").write_text(
        "# Laracasts Topics\n\n## Laracon Announcements\n\n"
        "Everything announced at the conference including managed queues.\n"
    )
    return temp_dir


def find(corpus, query, **kwargs):
    kwargs.setdefault("version", "12.x")
    kwargs.setdefault("limit", 10)
    return search(corpus, corpus / "external", query, **kwargs)


def files_of(result):
    return [hit["file"] for hit in result["results"]]


def sources_of(result):
    return {hit["source"] for hit in result["results"]}


class TestSourcesFanOut:
    def test_default_reaches_all_four_sources(self, corpus):
        result = find(corpus, "queue")

        assert {"core", "service:forge", "package:spatie", "learning:laracasts-index"} <= sources_of(result)
        assert result["sources"] == ["core", "services", "packages", "learning"]

    def test_sources_filter_narrows(self, corpus):
        result = find(corpus, "roles permission", sources=["packages"])

        assert sources_of(result) == {"package:spatie"}
        assert set(files_of(result)) == {"spatie/laravel-permission-roles.md"}

    def test_an_unknown_source_is_refused_and_the_valid_ones_named(self, corpus):
        with pytest.raises(ToolFailure) as raised:
            find(corpus, "queue", sources=["core", "reddit"])

        assert raised.value.code == "invalid_argument"
        assert raised.value.details["valid_sources"] == ["core", "services", "packages", "learning"]

    def test_version_scopes_core_only(self, corpus):
        """Package hits are identical whichever core version is searched."""
        a = find(corpus, "roles permission", version="12.x", sources=["packages"])
        b = find(corpus, "roles permission", version="11.x", sources=["packages"])

        assert files_of(a) == files_of(b) != []

    def test_a_hit_names_its_file_section_and_source(self, corpus):
        top = find(corpus, "supervisor daemon", limit=5)["results"][0]

        assert set(top) == {"file", "section", "heading", "score", "snippet", "source"}
        assert top["file"].startswith("forge/")


class TestNothingFoundIsNotAnError:
    def test_no_match_is_a_result_with_count_zero(self, corpus):
        result = find(corpus, "zzzzunfindableqqqq")

        assert (result["count"], result["results"]) == (0, [])
        assert "error" not in result

    def test_an_empty_query_is_an_error(self, corpus):
        with pytest.raises(ToolFailure) as raised:
            find(corpus, "   ")

        assert raised.value.code == "invalid_argument"


class TestLimit:
    def test_the_limit_caps_the_results(self, corpus):
        assert find(corpus, "queue", limit=2)["count"] == 2

    def test_count_matches_the_results(self, corpus):
        result = find(corpus, "queue", limit=3)

        assert result["count"] == len(result["results"])

    @pytest.mark.parametrize("bad", [0, -1, MAX_LIMIT + 1])
    def test_a_limit_out_of_range_is_refused(self, corpus, bad):
        with pytest.raises(ToolFailure) as raised:
            find(corpus, "queue", limit=bad)

        assert raised.value.code == "invalid_argument"


class TestEverySearchResultCanBeRead:
    """Service and package pages have no anchors, so the old `anchor` field was
    empty for them and a result could not be handed to the section reader."""

    def test_a_result_without_an_anchor_still_carries_a_section(self, corpus):
        hit = find(corpus, "supervisor daemon")["results"][0]

        assert hit["section"] == "supervisor-daemons"

    def test_an_explicit_anchor_is_preferred(self, corpus):
        hit = find(corpus, "store an uploaded file on a disk", sources=["core"])["results"][0]

        assert hit["section"] == "file-uploads"

    def test_every_result_round_trips_through_the_section_reader(self, corpus):
        for hit in find(corpus, "queue")["results"]:
            reply = read_section(corpus, hit["file"], hit["section"], runtime_version="12.x")

            assert reply.data["heading"] == hit["heading"]


def hit(source, score, name="x.md"):
    family, _, key = source.partition(":")
    return (Section(version=key or "12.x", filename=name, anchor=None, heading=name, text=""), score, family)


def labels(hits):
    return ["core" if family == "core" else f"{family}:{section.version}" for section, _score, family in hits]


class TestOneSourceCannotTakeTheWholePage:
    """"assign roles" used to return five Spatie pages out of five, and the
    framework's own authorization docs never appeared."""

    def test_a_dominant_source_leaves_room_for_the_others(self):
        ranked = [hit("package:spatie", 20 - i) for i in range(6)] + [hit("core", 9), hit("core", 8)]

        page = labels(spread_across_sources(ranked, 5))

        assert page.count("package:spatie") == 3
        assert page.count("core") == 2

    def test_the_page_keeps_rank_order(self):
        ranked = [hit("package:spatie", 20), hit("package:spatie", 19), hit("core", 18),
                  hit("package:spatie", 17), hit("package:spatie", 16), hit("core", 15)]

        scores = [score for _s, score, _f in spread_across_sources(ranked, 5)]

        assert scores == sorted(scores, reverse=True)

    def test_a_lone_source_fills_the_page(self):
        ranked = [hit("package:spatie", 20 - i) for i in range(6)]

        assert len(spread_across_sources(ranked, 5)) == 5

    def test_room_left_over_goes_back_to_the_best_remaining_hits(self):
        ranked = [hit("package:spatie", 20 - i) for i in range(6)] + [hit("core", 9)]

        page = labels(spread_across_sources(ranked, 5))

        assert (page.count("package:spatie"), page.count("core")) == (4, 1)

    def test_two_packages_are_separate_sources(self):
        ranked = [hit("package:spatie", 20 - i) for i in range(4)] + [hit("package:livewire", 10 - i) for i in range(4)]

        page = labels(spread_across_sources(ranked, 5))

        assert page.count("package:spatie") == 3 and page.count("package:livewire") == 2


class TestCorePreferredOnNearTies:
    """Scores from separate indexes are only roughly comparable, since each
    corpus has its own IDF. When Filament's docs grew from 62 pages to 164, a
    page about import jobs outscored the framework's own "Dealing With Failed
    Jobs" by 30.04 to 29.52 for "how do I retry a failed queue job". A lead
    that small is noise; the framework's docs win it."""

    def _order(self, hits):
        return [family for _section, _score, family in rank_hits(hits)]

    def test_core_wins_a_near_tie_against_a_package(self):
        assert self._order([("a", 30.04, "package"), ("b", 29.52, "core")]) == ["core", "package"]

    def test_a_clear_lead_is_not_overturned(self):
        assert self._order([("a", 36.0, "package"), ("b", 29.52, "core")]) == ["package", "core"]

    def test_non_core_sources_are_ordered_by_score_among_themselves(self):
        assert self._order([("a", 20.0, "service"), ("b", 25.0, "package"), ("c", 22.0, "learning")]) == [
            "package", "learning", "service",
        ]

    def test_reported_scores_are_left_as_computed(self):
        assert [score for _s, score, _f in rank_hits([("a", 30.04, "package"), ("b", 29.52, "core")])] == [29.52, 30.04]


class TestCommonTasksPointAtTheirPages:
    """The need table ("upload files" -> filesystem, validation, requests) used
    to power a separate, weaker finder that saw only the framework docs. It now
    informs the one search."""

    def test_a_task_named_in_the_query_is_recognised(self):
        assert "upload files" in matched_needs("how do I upload files from a form?")

    def test_a_task_is_matched_as_whole_words(self):
        assert "upload files" not in matched_needs("reupload filesystems")

    def test_word_order_and_number_do_not_matter(self):
        assert "upload files" in matched_needs("file upload")

    def test_every_word_of_the_task_has_to_be_there(self):
        assert "upload files" not in matched_needs("upload an avatar")

    def test_a_query_naming_no_task_matches_nothing(self):
        assert matched_needs("eloquent accessor casting") == {}

    def test_the_search_reports_the_tasks_it_recognised(self, corpus):
        assert find(corpus, "upload files")["matched_needs"] == ["upload files"]

    def test_a_page_the_task_points_at_outranks_a_slightly_better_scoring_page(self):
        ranked = rank_hits(
            [hit("core", 10.0, "routing.md"), hit("core", 9.0, "filesystem.md")], need_pages={"filesystem.md"}
        )

        assert [section.filename for section, _s, _f in ranked] == ["filesystem.md", "routing.md"]

    def test_the_pointed_at_page_is_found_even_when_it_ranks_below_the_page(self, corpus):
        result = find(corpus, "upload files", limit=1, sources=["core"])

        assert files_of(result) == ["12.x/filesystem.md"]

    def test_no_field_is_added_when_nothing_was_recognised(self, corpus):
        assert "matched_needs" not in find(corpus, "supervisor daemon")


@pytest.mark.skipif(not (REPO_DOCS / "packages").is_dir(), reason="real corpus absent")
class TestRealCorpusQuality:
    def _find(self, query, **kwargs):
        return search(REPO_DOCS, REPO_DOCS / "external", query, version="12.x", **kwargs)

    def test_spatie_query_surfaces_the_spatie_docs(self):
        result = self._find("spatie permission roles")

        assert any(h["source"] == "package:spatie" for h in result["results"][:3]), result["results"][:3]

    def test_livewire_query_surfaces_livewire_docs(self):
        result = self._find("livewire wire:model binding")

        assert any(h["source"] == "package:livewire" for h in result["results"]), result["results"]

    def test_core_query_still_prefers_core(self):
        top = self._find("how do I retry a failed queue job")["results"][0]

        assert top["source"] == "core"
        assert "queues.md" in top["file"]

    def test_a_package_heavy_query_still_shows_the_framework(self):
        result = self._find("assign roles to a user")

        assert "core" in sources_of(result)
        assert any(source.startswith("package:") for source in sources_of(result))

    def test_every_real_result_round_trips_through_the_section_reader(self):
        """Across all four kinds of source, on the real corpus."""
        for query in ("queue worker", "deploy a site", "assign roles", "file upload", "nightwatch sampling"):
            for found in self._find(query, limit=10)["results"]:
                reply = read_section(REPO_DOCS, found["file"], found["section"], runtime_version="12.x")
                assert reply.data["content"], (query, found)


class TestARecognisedTaskKeepsAPlace:
    """With Laravel Cloud in the corpus, "assign roles to a user" filled its
    page with Spatie and Cloud pages, and the framework page the need table
    names for roles was ranked sixth. A curated pointer that never shows is
    no pointer."""

    def test_the_best_page_a_task_points_at_is_on_the_page(self):
        ranked = [hit("package:spatie", 20 - i) for i in range(4)] + [hit("service:cloud", 15), hit("service:cloud", 14)]
        ranked.append(hit("core", 9.0, "authorization.md"))

        page = keep_need_page(spread_across_sources(ranked, 5), ranked, {"authorization.md"})

        assert "authorization.md" in [section.filename for section, _s, _f in page]
        assert len(page) == 5

    def test_it_takes_the_place_of_the_weakest_result(self):
        ranked = [hit("package:spatie", 20 - i, f"p{i}.md") for i in range(5)] + [hit("core", 9.0, "authorization.md")]

        page = keep_need_page(ranked[:5], ranked, {"authorization.md"})

        assert [section.filename for section, _s, _f in page] == ["p0.md", "p1.md", "p2.md", "p3.md", "authorization.md"]

    def test_a_page_already_holding_one_is_left_alone(self):
        ranked = [hit("core", 20, "authorization.md")] + [hit("package:spatie", 19 - i, f"p{i}.md") for i in range(5)]

        assert keep_need_page(ranked[:5], ranked, {"authorization.md"}) == ranked[:5]

    def test_nothing_changes_when_no_task_was_recognised(self):
        ranked = [hit("package:spatie", 20 - i, f"p{i}.md") for i in range(6)]

        assert keep_need_page(ranked[:5], ranked, set()) == ranked[:5]

    def test_nothing_changes_when_the_pointed_at_page_is_not_a_candidate(self):
        ranked = [hit("package:spatie", 20 - i, f"p{i}.md") for i in range(6)]

        assert keep_need_page(ranked[:5], ranked, {"authorization.md"}) == ranked[:5]
