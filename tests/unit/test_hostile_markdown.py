"""Text an upstream site controls must not stall the regexes it goes through.

A fetched page, or a `section` argument, made of unclosed brackets sent
several link-matching patterns quadratic or cubic: twenty kilobytes was
enough to hold the process for minutes. Python's `re` holds the interpreter
lock while it matches, so a stalled pattern stops the server answering
anyone. Each cleaner gets input of the shapes that were slow, and a second to
finish; before the patterns were bounded the fastest of these took several.
"""

import time

import pytest

from laravel_mcp_companion import docs_updater
from laravel_mcp_companion.tools.common import slugify

HOSTILE = {
    "a run of opening brackets": "[" * 40000,
    "unclosed links": "[a" * 20000,
    "links that never close their address": "[x](" * 10000,
    "images that never close": "![" * 20000,
    "a protected-email address that never closes": "[" * 20000 + "](/cdn-cgi/l/email-protection" + "[" * 20000,
}

CLEANERS = {
    "slugify": slugify,
    "remove_social_media_lines": docs_updater.remove_social_media_lines,
    "remove_image_references": docs_updater.remove_image_references,
    "replace_protected_emails": docs_updater.replace_protected_emails,
}


@pytest.mark.parametrize("cleaner", sorted(CLEANERS))
@pytest.mark.parametrize("shape", sorted(HOSTILE))
def test_a_cleaner_finishes_on_hostile_text(cleaner, shape):
    started = time.perf_counter()

    CLEANERS[cleaner](HOSTILE[shape])

    assert time.perf_counter() - started < 1.0


class TestTheCleanersStillClean:
    def test_a_heading_with_a_link_slugs_to_its_text(self):
        assert slugify("Using [Laravel Pint](https://laravel.com/docs/pint) here") == "using-laravel-pint-here"

    def test_a_protected_email_link_becomes_the_placeholder(self):
        text = "Write to [[email protected]](/cdn-cgi/l/email-protection#abc123) today."

        assert docs_updater.replace_protected_emails(text) == "Write to [email protected] today."

    def test_an_ordinary_link_is_not_mistaken_for_a_protected_email(self):
        text = "See [the docs](https://laravel.com/docs) for more."

        assert docs_updater.replace_protected_emails(text) == text

    def test_a_line_of_social_links_is_still_removed(self):
        line = "[X](https://x.com/laravelphp) [Discord](https://discord.gg/laravel) [GitHub](https://github.com/laravel)"

        assert docs_updater.remove_social_media_lines(f"Intro\n{line}\nOutro") == "Intro\nOutro"

    def test_an_image_is_still_removed_and_its_line_with_it(self):
        assert docs_updater.remove_image_references("Before\n![logo](https://example.com/a.png)\nAfter") == "Before\nAfter"
