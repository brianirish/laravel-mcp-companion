"""get_laravel_package, recommend_laravel_packages and get_laravel_service_info.

The first replaces four tools that were four views of one 22-row table: a
package's details, its features, its relatives, and the packages in a category.
"""

import json
import time
from types import SimpleNamespace

import pytest

from laravel_mcp_companion import catalog
from laravel_mcp_companion.docs_updater import MultiSourceDocsUpdater
from laravel_mcp_companion.learning_resources import RELATED_PACKAGES
from laravel_mcp_companion.tools import ToolFailure
from laravel_mcp_companion.tools.catalog import RECOMMEND_LIMIT, get_package, recommend_packages, service_info


class TestOnePackage:
    def test_everything_about_a_package_comes_back_in_one_record(self):
        package = get_package("laravel/cashier")["packages"][0]

        assert set(package) >= {
            "id", "name", "description", "categories", "use_cases", "installation",
            "features", "related", "documentation_link",
        }
        assert package["id"] == "laravel/cashier"
        assert package["installation"].startswith("composer require")

    def test_features_come_from_the_feature_map(self):
        assert get_package("laravel/cashier")["packages"][0]["features"] == catalog.FEATURE_MAP["laravel/cashier"]

    def test_related_packages_come_from_the_relations_table(self):
        assert get_package("laravel/cashier")["packages"][0]["related"] == RELATED_PACKAGES["laravel/cashier"]

    def test_a_single_result_has_count_one(self):
        assert get_package("laravel/sanctum")["count"] == 1

    def test_a_short_name_finds_the_package(self):
        assert get_package("sanctum")["packages"][0]["id"] == "laravel/sanctum"

    def test_a_short_name_means_the_package_of_exactly_that_name(self):
        """"cashier" is laravel/cashier, though laravel/cashier-paddle contains it too."""
        assert get_package("cashier")["packages"][0]["id"] == "laravel/cashier"

    def test_the_name_is_matched_whatever_its_case(self):
        assert get_package("  Laravel/Sanctum ")["packages"][0]["id"] == "laravel/sanctum"

    def test_an_unknown_package_is_not_found_and_the_catalog_is_listed(self):
        with pytest.raises(ToolFailure) as raised:
            get_package("acme/widgets")

        assert raised.value.code == "not_found"
        assert "laravel/cashier" in raised.value.details["available"]

    def test_an_ambiguous_fragment_is_not_guessed_at(self):
        with pytest.raises(ToolFailure):
            get_package("laravel")


class TestACategory:
    def test_every_package_in_the_category_is_listed(self):
        result = get_package(category="payment")

        assert {p["id"] for p in result["packages"]} == set(catalog.packages_in_category("payment"))
        assert result["count"] == len(result["packages"]) > 0
        assert result["category"] == "payment"

    def test_a_listed_package_is_a_summary(self):
        package = get_package(category="payment")["packages"][0]

        assert "features" not in package and "installation" in package

    def test_an_unknown_category_is_not_found_and_the_real_ones_are_listed(self):
        with pytest.raises(ToolFailure) as raised:
            get_package(category="blockchain")

        assert raised.value.code == "not_found"
        assert raised.value.details["available_categories"] == catalog.all_categories()

    def test_name_and_category_together_are_refused(self):
        with pytest.raises(ToolFailure) as raised:
            get_package("cashier", "payment")

        assert raised.value.code == "invalid_argument"


class TestTheWholeCatalog:
    def test_with_no_arguments_every_package_and_category_is_listed(self):
        result = get_package()

        assert result["count"] == len(catalog.PACKAGE_CATALOG)
        assert result["categories"] == catalog.all_categories()


class TestRecommendations:
    def test_a_described_need_finds_the_package_for_it(self):
        ids = [p["id"] for p in recommend_packages("accept subscription payments")["packages"]]

        assert ids[0] in ("laravel/cashier", "laravel/cashier-paddle")

    def test_recommendations_are_full_records(self):
        package = recommend_packages("role based permissions")["packages"][0]

        assert package["id"] == "spatie/laravel-permission"
        assert package["installation"] and "features" in package

    def test_the_list_is_capped(self):
        assert recommend_packages("laravel")["count"] <= RECOMMEND_LIMIT

    def test_nothing_fitting_is_count_zero_not_an_error(self):
        assert recommend_packages("xyzzy plugh") == {"use_case": "xyzzy plugh", "count": 0, "packages": []}

    def test_an_empty_description_is_refused(self):
        with pytest.raises(ToolFailure) as raised:
            recommend_packages("  ")

        assert raised.value.code == "invalid_argument"


class TestCatalogIsWellFormed:
    @pytest.mark.parametrize("package_id", sorted(catalog.PACKAGE_CATALOG))
    def test_every_entry_has_the_fields_the_tools_return(self, package_id):
        entry = catalog.PACKAGE_CATALOG[package_id]

        assert entry["name"] and entry["description"]
        assert isinstance(entry["categories"], list) and entry["categories"]
        assert isinstance(entry["use_cases"], list) and entry["use_cases"]

    @pytest.mark.parametrize("package_id", sorted(catalog.FEATURE_MAP))
    def test_every_feature_list_belongs_to_a_catalogued_package(self, package_id):
        assert package_id in catalog.PACKAGE_CATALOG
        assert all(isinstance(feature, str) and feature for feature in catalog.FEATURE_MAP[package_id])


@pytest.fixture
def server(temp_dir):
    docs = temp_dir / "docs"
    forge = docs / "external" / "forge"
    forge.mkdir(parents=True)
    (forge / ".cache_metadata.json").write_text(json.dumps({
        "fetched_sections": ["a", "b", "c"], "total_sections": 3, "success_rate": 1.0, "cached_at": time.time(),
    }))
    nova = docs / "external" / "nova"
    nova.mkdir()
    (nova / ".cache_metadata.json").write_text(json.dumps({
        "fetched_sections": ["a"], "total_sections": 5, "success_rate": 0.2, "version": "v5", "cached_at": time.time(),
    }))
    return SimpleNamespace(docs_path=docs, runtime_version="12.x", updater=MultiSourceDocsUpdater(docs, "12.x"))


class TestServiceInfo:
    def test_a_service_reports_where_its_docs_live_and_what_is_held(self, server):
        info = service_info(server, "forge")

        assert (info["id"], info["name"], info["status"], info["pages"], info["pages_expected"]) == (
            "forge", "Laravel Forge", "ok", 3, 3,
        )
        assert info["documentation_url"] == "https://laravel.com/forge/docs"
        assert info["last_synced"]

    def test_a_partly_fetched_service_is_partial_and_names_its_major(self, server):
        info = service_info(server, "nova")

        assert (info["status"], info["pages"], info["pages_expected"], info["version"]) == ("partial", 1, 5, "v5")

    def test_a_service_with_no_copy_is_missing(self, server):
        assert service_info(server, "herd")["status"] == "missing"

    def test_the_name_is_matched_whatever_its_case(self, server):
        assert service_info(server, " Forge ")["id"] == "forge"

    def test_an_unknown_service_is_not_found_and_the_real_ones_are_listed(self, server):
        with pytest.raises(ToolFailure) as raised:
            service_info(server, "horizon")

        assert raised.value.code == "not_found"
        assert set(raised.value.details["available_services"]) == {
            "forge", "vapor", "envoyer", "nova", "cloud", "nightwatch", "herd",
        }
