"""TOON encoding of tool payloads.

The cases pin the output of toon-format 1.x, which this project froze on.
Three of them differ from the 0.9 beta the project used to pin: an empty
list, a whole float, and a string that begins with `#`.
"""

import pytest

from laravel_mcp_companion.toon_helpers import toon_encode


class TestShapes:
    def test_a_flat_object_is_key_value_lines(self):
        assert toon_encode({"version": "12.x", "count": 3, "stale": False}) == "version: 12.x\ncount: 3\nstale: false"

    def test_a_list_of_strings_is_one_line_with_its_length(self):
        assert toon_encode({"files": ["a.md", "b.md"]}) == "files[2]: a.md,b.md"

    def test_a_list_of_like_objects_is_a_table(self):
        encoded = toon_encode({"packages": [{"id": "a/b", "name": "A"}, {"id": "c/d", "name": "C"}]})

        assert encoded == "packages[2]{id,name}:\n  a/b,A\n  c/d,C"

    def test_a_nested_object_is_indented(self):
        assert toon_encode({"error": {"code": "not_found", "message": "gone"}}) == "error:\n  code: not_found\n  message: gone"

    def test_an_empty_list_is_written_as_brackets(self):
        assert toon_encode({"results": [], "count": 0}) == "results: []\ncount: 0"

    def test_a_whole_float_loses_its_point_zero(self):
        assert toon_encode({"score": 3.0, "ratio": 2.5}) == "score: 3\nratio: 2.5"

    def test_a_value_with_a_comma_or_colon_is_quoted(self):
        assert toon_encode({"note": "a, b: c"}) == 'note: "a, b: c"'

    def test_a_string_starting_with_a_hash_is_quoted(self):
        assert toon_encode({"heading": "#top"}) == 'heading: "#top"'

    def test_a_line_break_is_escaped(self):
        assert toon_encode({"text": "one\ntwo"}) == 'text: "one\\ntwo"'


class TestFailure:
    def test_a_value_that_cannot_be_encoded_is_an_error_not_a_python_repr(self):
        """It used to fall back to str(data), which put a Python repr in a
        field documented as TOON."""
        class Opaque:
            pass

        with pytest.raises(Exception):
            toon_encode({"thing": Opaque()})
