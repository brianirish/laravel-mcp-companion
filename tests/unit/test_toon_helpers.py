"""Unit tests for TOON format helper functions."""

from unittest.mock import patch, MagicMock

import toon_helpers


class TestToonEncode:
    """Test the toon_encode function."""

    def test_toon_encode_basic_dict(self):
        """Test encoding a basic dictionary."""
        data = {"key": "value", "count": 42}
        result = toon_helpers.toon_encode(data)
        assert "key" in result
        assert "value" in result
        assert "42" in result

    def test_toon_encode_list(self):
        """Test encoding a list."""
        data = [{"name": "item1"}, {"name": "item2"}]
        result = toon_helpers.toon_encode(data)
        assert "item1" in result
        assert "item2" in result

    def test_toon_encode_exception_fallback(self):
        """Test that encoding failures fall back to string representation."""
        # Create an object that will fail TOON encoding
        class UnserializableObject:
            def __repr__(self):
                return "UnserializableObject()"

        # Mock toon_format.encode to raise an exception
        with patch('toon_helpers.encode') as mock_encode:
            mock_encode.side_effect = Exception("Encoding failed")

            obj = UnserializableObject()
            result = toon_helpers.toon_encode(obj)

            # Should fall back to str representation
            assert result == "UnserializableObject()"


class TestFormatVersionList:
    """Test the format_version_list function."""

    def test_format_version_list_basic(self):
        """Test formatting a version list."""
        versions = [
            {"version": "12.x", "files": ["installation.md", "routing.md"]},
            {"version": "11.x", "files": ["installation.md"]}
        ]
        result = toon_helpers.format_version_list(versions)
        assert "12.x" in result
        assert "11.x" in result
        assert "installation.md" in result


class TestFormatSearchResults:
    """Test the format_search_results function."""

    def test_format_search_results_core_only(self):
        """Test formatting search results with core results only."""
        query = "authentication"
        core_results = [
            {"file": "12.x/authentication.md", "matches": 5},
            {"file": "12.x/sanctum.md", "matches": 3}
        ]

        result = toon_helpers.format_search_results(query, core_results)

        assert "authentication" in result
        assert "sanctum.md" in result
        assert "5" in result or "matches" in result

    def test_format_search_results_with_external(self):
        """Test formatting search results including external results."""
        query = "deployment"
        core_results = [
            {"file": "12.x/deployment.md", "matches": 2}
        ]
        external_results = [
            {"service": "forge", "file": "deployment.md", "matches": 8},
            {"service": "vapor", "file": "environments.md", "matches": 3}
        ]

        result = toon_helpers.format_search_results(query, core_results, external_results)

        # Should include all data
        assert "deployment" in result
        assert "forge" in result
        assert "vapor" in result
        # Should include external count info
        assert "external" in result.lower() or "2" in result  # external count = 2

    def test_format_search_results_empty_external(self):
        """Test that empty external results list is treated as None."""
        query = "test"
        core_results = [{"file": "test.md", "matches": 1}]

        # When external_results is None, the external data shouldn't be included
        result_without = toon_helpers.format_search_results(query, core_results, None)
        result_with_empty = toon_helpers.format_search_results(query, core_results, [])

        # Empty list should behave similarly to None (external_results is falsy)
        assert "test.md" in result_without
        assert "test.md" in result_with_empty


class TestFormatPackageList:
    """Test the format_package_list function."""

    def test_format_package_list_basic(self):
        """Test formatting a package list."""
        packages = [
            {"name": "laravel/sanctum", "description": "API auth"},
            {"name": "laravel/cashier", "description": "Payments"}
        ]
        result = toon_helpers.format_package_list(packages, "authentication")

        assert "sanctum" in result
        assert "cashier" in result
        assert "authentication" in result


class TestFormatPackageInfo:
    """Test the format_package_info function."""

    def test_format_package_info_basic(self):
        """Test formatting single package info."""
        package = {
            "name": "laravel/horizon",
            "description": "Queue monitoring",
            "installation": "composer require laravel/horizon"
        }
        result = toon_helpers.format_package_info(package)

        assert "horizon" in result
        assert "monitoring" in result


class TestFormatServiceList:
    """Test the format_service_list function."""

    def test_format_service_list_basic(self):
        """Test formatting service list."""
        services = [
            {"name": "forge", "description": "Server management"},
            {"name": "vapor", "description": "Serverless deployment"}
        ]
        result = toon_helpers.format_service_list(services)

        assert "forge" in result
        assert "vapor" in result
        assert "2" in result  # count = 2


class TestFormatCategoryDocs:
    """Test the format_category_docs function."""

    def test_format_category_docs_basic(self):
        """Test formatting category docs."""
        files = [
            {"file": "authentication.md", "description": "Auth system"},
            {"file": "authorization.md", "description": "Gates and policies"}
        ]
        result = toon_helpers.format_category_docs("security", "12.x", files)

        assert "security" in result
        assert "12.x" in result
        assert "authentication.md" in result


class TestFormatDocStructure:
    """Test the format_doc_structure function."""

    def test_format_doc_structure_basic(self):
        """Test formatting document structure."""
        headings = [
            {"level": 1, "text": "Introduction"},
            {"level": 2, "text": "Getting Started"},
            {"level": 2, "text": "Configuration"}
        ]
        result = toon_helpers.format_doc_structure("installation.md", headings)

        assert "installation.md" in result
        assert "Introduction" in result
        assert "Getting Started" in result


class TestFormatError:
    """Test the format_error function."""

    def test_format_error_message_only(self):
        """Test formatting error with message only."""
        result = toon_helpers.format_error("File not found")

        assert "error" in result.lower()
        assert "File not found" in result

    def test_format_error_with_context(self):
        """Test formatting error with context."""
        result = toon_helpers.format_error(
            "Version not found",
            {"requested": "13.x", "available": ["11.x", "12.x"]}
        )

        assert "Version not found" in result
        assert "13.x" in result
        assert "11.x" in result
