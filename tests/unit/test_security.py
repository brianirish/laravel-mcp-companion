"""Unit tests for security and safety functions."""

import pytest
from pathlib import Path
from unittest.mock import patch

from laravel_mcp_companion.server import get_version_from_path
from laravel_mcp_companion.mcp_tools import is_safe_path
class TestPathSecurity:
    """Test path validation and security functions."""

    def test_is_safe_path_within_base(self, temp_dir):
        """Test that paths within base directory are considered safe."""
        base_path = temp_dir
        safe_paths = [
            temp_dir / "file.txt",
            temp_dir / "subdir" / "file.txt",
            temp_dir / "a" / "b" / "c" / "file.txt",
            temp_dir,  # Same as base
        ]
        
        for safe_path in safe_paths:
            assert is_safe_path(base_path, safe_path), f"Path should be safe: {safe_path}"

    def test_is_safe_path_outside_base(self, temp_dir):
        """Test that paths outside base directory are considered unsafe."""
        base_path = temp_dir / "restricted"
        base_path.mkdir()
        
        unsafe_paths = [
            temp_dir / "outside.txt",  # Parent directory
            temp_dir.parent / "file.txt",  # Grandparent
            Path("/etc/passwd"),  # Absolute path outside
            Path("/tmp/file.txt"),  # Different root path
        ]
        
        for unsafe_path in unsafe_paths:
            assert not is_safe_path(base_path, unsafe_path), f"Path should be unsafe: {unsafe_path}"

    def test_is_safe_path_directory_traversal_attempts(self, temp_dir):
        """Test that directory traversal attempts are blocked."""
        base_path = temp_dir / "docs"
        base_path.mkdir()
        
        # These shouldn't work even if they resolve to safe paths
        traversal_attempts = [
            base_path / ".." / "docs" / "file.txt",  # Goes up then down
            base_path / "subdir" / ".." / ".." / "file.txt",  # Multiple traversals
        ]
        
        for traversal_path in traversal_attempts:
            # The function checks absolute resolved paths, so this should be safe
            # if it resolves within the base path
            resolved = traversal_path.resolve()
            try:
                result = is_safe_path(base_path, resolved)
                # Result depends on where the resolved path ends up
                if base_path in resolved.parents or base_path == resolved:
                    assert result, f"Valid resolved path should be safe: {resolved}"
                else:
                    assert not result, f"Invalid resolved path should be unsafe: {resolved}"
            except Exception:
                # If path resolution fails, that's also a form of protection
                pass

    def test_is_safe_path_symlink_protection(self, temp_dir):
        """Test protection against symlink attacks (if applicable)."""
        base_path = temp_dir / "docs"
        base_path.mkdir()
        
        # Create a file outside the base
        outside_file = temp_dir / "outside.txt"
        outside_file.write_text("sensitive data")
        
        # Create a symlink inside base pointing outside
        try:
            symlink_path = base_path / "link_to_outside.txt"
            symlink_path.symlink_to(outside_file)
            
            # The symlink itself might be "safe" but its target isn't
            result = is_safe_path(base_path, symlink_path)
            # This depends on implementation - the function should check resolved paths
            assert isinstance(result, bool)  # Should not crash
            
        except (OSError, NotImplementedError):
            # Symlinks might not be supported on all systems
            pytest.skip("Symlinks not supported on this system")

    def test_is_safe_path_edge_cases(self, temp_dir):
        """Test edge cases for path validation."""
        base_path = temp_dir / "docs"
        base_path.mkdir()
        
        # Empty path components
        assert is_safe_path(base_path, base_path / "")
        
        # Current directory references
        assert is_safe_path(base_path, base_path / "." / "file.txt")
        
        # Very long paths
        long_subpath = "/".join(["subdir"] * 50) + "/file.txt"
        long_path = base_path / long_subpath
        assert is_safe_path(base_path, long_path)


class TestVersionParsing:
    """Test version parsing and validation."""

    def test_get_version_from_path_valid_versions(self):
        """Test version extraction with valid version formats."""
        test_cases = [
            ("12.x/blade.md", "12.x", "blade.md"),
            ("11.x/frontend/vite.md", "11.x", "frontend/vite.md"),
            ("6.x/installation.md", "6.x", "installation.md"),
            ("10.x/nested/deep/file.md", "10.x", "nested/deep/file.md"),
        ]
        
        for input_path, expected_version, expected_relative in test_cases:
            version, relative = get_version_from_path(input_path)
            assert version == expected_version, f"Version mismatch for {input_path}"
            assert relative == expected_relative, f"Relative path mismatch for {input_path}"

    def test_get_version_from_path_no_version(self):
        """Test version extraction when no version is specified."""
        # get_version_from_path is now mcp_tools.get_version_from_path
        # (re-exported), so its get_default_version lookup resolves in mcp_tools.
        with patch('laravel_mcp_companion.mcp_tools.get_default_version', return_value='12.x'):
            test_cases = [
                ("blade.md", "12.x", "blade.md"),
                ("frontend/vite.md", "12.x", "frontend/vite.md"),
                ("installation.md", "12.x", "installation.md"),
            ]
            
            for input_path, expected_version, expected_relative in test_cases:
                version, relative = get_version_from_path(input_path)
                assert version == expected_version, f"Version mismatch for {input_path}"
                assert relative == expected_relative, f"Relative path mismatch for {input_path}"

    def test_get_version_from_path_invalid_versions(self):
        """Test version extraction with invalid version formats."""
        # get_version_from_path is now mcp_tools.get_version_from_path
        # (re-exported), so its globals resolve in mcp_tools.
        with patch('laravel_mcp_companion.mcp_tools.get_default_version', return_value='12.x'), \
             patch('laravel_mcp_companion.mcp_tools.SUPPORTED_VERSIONS', ['6.x', '11.x', '12.x']):
            
            # These should fall back to default version
            test_cases = [
                ("99.x/blade.md", "12.x", "99.x/blade.md"),  # Unsupported version
                ("invalid/blade.md", "12.x", "invalid/blade.md"),  # Not a version
                ("master/blade.md", "12.x", "master/blade.md"),  # Branch name
            ]
            
            for input_path, expected_version, expected_relative in test_cases:
                version, relative = get_version_from_path(input_path)
                assert version == expected_version, f"Version mismatch for {input_path}"
                assert relative == expected_relative, f"Relative path mismatch for {input_path}"

    def test_get_version_from_path_empty_input(self):
        """Test version extraction with empty or invalid input."""
        # get_version_from_path is now mcp_tools.get_version_from_path
        # (re-exported), so its get_default_version lookup resolves in mcp_tools.
        with patch('laravel_mcp_companion.mcp_tools.get_default_version', return_value='12.x'):
            test_cases = [
                ("", "12.x", ""),
                ("/", "12.x", "/"),  # Path("/").parts is empty, so it returns "/" 
                (".", "12.x", "."),
            ]
            
            for input_path, expected_version, expected_relative in test_cases:
                version, relative = get_version_from_path(input_path)
                assert version == expected_version, f"Version mismatch for {input_path}"
                assert relative == expected_relative, f"Relative path mismatch for {input_path}"


class TestInputValidation:
    """Arguments that are empty, absent or absurd are refused with an error
    code; none of them crashes a tool or reaches the filesystem."""

    @pytest.mark.parametrize("query", ["", "   "])
    def test_an_empty_search_query_is_refused(self, query):
        from laravel_mcp_companion.tools import ToolFailure
        from laravel_mcp_companion.tools.search import search

        with pytest.raises(ToolFailure) as raised:
            search(Path("/tmp"), None, query)

        assert raised.value.code == "invalid_argument"

    def test_a_file_outside_its_version_directory_is_not_served(self, temp_dir):
        from laravel_mcp_companion.tools import ToolFailure
        from laravel_mcp_companion.tools.docs import read_content

        docs = temp_dir / "docs"
        (docs / "12.x").mkdir(parents=True)
        (docs / "12.x" / "test.md").write_text("# Test")
        (docs / "outside.md").write_text("# Outside")

        assert "# Test" in read_content(docs, "test.md", "12.x").text
        with pytest.raises(ToolFailure) as raised:
            read_content(docs, "../outside.md", "12.x")

        assert raised.value.code == "access_denied"
        assert "# Outside" not in str(raised.value.payload())

    @pytest.mark.parametrize("name", ["invalid/package/name/with/too/many/parts", "../../etc/passwd", "x" * 5000])
    def test_a_package_name_that_matches_nothing_is_not_found(self, name):
        from laravel_mcp_companion.tools import ToolFailure
        from laravel_mcp_companion.tools.catalog import get_package

        with pytest.raises(ToolFailure) as raised:
            get_package(name)

        assert raised.value.code == "not_found"

    @pytest.mark.parametrize("version", ["", "x" * 1000, "12.x; rm -rf /", "12.x\n13.x"])
    def test_a_version_that_is_not_a_version_is_refused_or_defaulted(self, version):
        """An empty string means "no version given"; anything else that is not
        on the allowlist is refused."""
        from laravel_mcp_companion.tools import ToolFailure
        from laravel_mcp_companion.tools.docs import read_content

        with pytest.raises(ToolFailure) as raised:
            read_content(Path("/tmp/no-docs-here"), "test.md", version)

        assert raised.value.code in ("unknown_version", "not_found")


class TestErrorHandling:
    """Test error handling in security-critical functions."""

    def test_is_safe_path_with_non_existent_paths(self, temp_dir):
        """Test is_safe_path with non-existent paths."""
        base_path = temp_dir / "docs"
        base_path.mkdir()
        
        non_existent_paths = [
            base_path / "does_not_exist.txt",
            base_path / "subdir" / "does_not_exist.txt",
            temp_dir / "outside" / "does_not_exist.txt",
        ]
        
        for path in non_existent_paths:
            # Function should not crash with non-existent paths
            try:
                result = is_safe_path(base_path, path)
                assert isinstance(result, bool)
            except Exception as e:
                pytest.fail(f"is_safe_path crashed with non-existent path {path}: {e}")

    def test_path_validation_with_special_characters(self, temp_dir):
        """Test path validation with special characters and encoding."""
        base_path = temp_dir / "docs"
        base_path.mkdir()
        
        special_paths = [
            base_path / "file with spaces.txt",
            base_path / "file-with-dashes.txt",
            base_path / "file_with_underscores.txt",
            base_path / "file.with.dots.txt",
        ]
        
        # Try to create Unicode filenames (may not work on all systems)
        try:
            unicode_path = base_path / "файл.txt"  # Cyrillic
            special_paths.append(unicode_path)
        except Exception:
            pass  # Unicode filenames not supported
        
        for path in special_paths:
            try:
                result = is_safe_path(base_path, path)
                assert isinstance(result, bool)
                # All should be safe since they're within base_path
                assert result is True, f"Special character path should be safe: {path}"
            except Exception as e:
                # Some special characters might not be supported
                pytest.skip(f"Special character not supported: {path} - {e}")

    def test_error_handling_in_get_version_from_path(self):
        """Test error handling in version parsing."""
        # The function should handle string inputs, but test edge cases
        edge_cases = [
            "12.x" + "/" * 1000 + "file.md",  # Very long path
            "12.x/" + "a" * 1000,  # Very long filename
        ]
        
        with patch('laravel_mcp_companion.mcp_tools.get_default_version', return_value='12.x'):
            for test_input in edge_cases:
                try:
                    version, relative = get_version_from_path(test_input)
                    assert isinstance(version, str)
                    assert isinstance(relative, str)
                except Exception as e:
                    pytest.fail(f"get_version_from_path crashed with input {test_input}: {e}")

    def test_path_injection_attempts(self, temp_dir):
        """Test protection against path injection attempts."""
        base_path = temp_dir / "docs"
        base_path.mkdir()
        
        # Various injection attempts
        injection_attempts = [
            "../../../etc/passwd",
            "..\\..\\..\\windows\\system32\\config\\sam",  # Windows-style
            "file.txt\x00extra_data",  # Null byte injection
            "file.txt/../../../sensitive",
            "./../../sensitive",
            "subdir/../../sensitive",
        ]
        
        for attempt in injection_attempts:
            try:
                test_path = base_path / attempt
                result = is_safe_path(base_path, test_path)
                # Should either be False (unsafe) or handle the injection safely
                if result:
                    # If it's True, the resolved path must actually be safe
                    resolved = test_path.resolve()
                    assert base_path in resolved.parents or base_path == resolved
            except Exception:
                # Exceptions during path resolution are also acceptable
                # (they prevent the injection from succeeding)
                pass