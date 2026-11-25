"""What the updater refuses from the network, and what a failed update leaves.

An update fetches from GitHub and from a dozen documentation sites, and
stores what comes back where the read and search tools return it. If one of
those sites were compromised, three things used to follow from that. A
redirect was followed to any address, so the page stored could be the answer
of an internal service. A response or an archive of any size was read into
memory or onto the disk. And the pages of a Laravel version were deleted
before their replacements were copied, so a copy that failed left the
version empty.
"""

import http.server
import io
import re
import tempfile
import threading
import urllib.error
import urllib.request
import zipfile
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from laravel_mcp_companion import docs_updater
from laravel_mcp_companion.docs_updater import DocsUpdater

COMMIT = {"sha": "abc1234def", "date": "2026-01-01T00:00:00Z", "message": "Update", "url": "https://github.com/laravel/docs/commit/abc1234def"}


def archive(files: dict[str, str], top_level: str = "docs-12.x") -> bytes:
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w") as zipped:
        for name, text in files.items():
            zipped.writestr(f"{top_level}/{name}", text)
    return buffer.getvalue()


def response(body: bytes) -> MagicMock:
    served = MagicMock()
    served.__enter__.return_value = io.BytesIO(body)
    return served


@pytest.fixture
def scratch(tmp_path, monkeypatch):
    """Send the updater's temporary directories somewhere a test can count them."""
    where = tmp_path / "scratch"
    where.mkdir()
    monkeypatch.setattr(tempfile, "tempdir", str(where))
    return where


@pytest.fixture
def no_waiting():
    import time

    clock = MagicMock(wraps=time)
    clock.sleep = MagicMock()
    with patch("laravel_mcp_companion.docs_updater.time", clock):
        yield clock.sleep


@pytest.fixture
def updater(tmp_path):
    docs = tmp_path / "docs"
    docs.mkdir()
    instance = DocsUpdater(docs, "12.x")
    (instance.version_dir / "old.md").write_text("# Old page\n")
    instance.write_local_metadata({"version": "12.x", "commit_sha": "old"})
    return instance


class TestRedirects:
    def follow(self, origin: str, target: str):
        guard = docs_updater.RedirectGuard()
        request = urllib.request.Request(origin)
        return guard.redirect_request(request, io.BytesIO(b""), 302, "Found", {}, target)

    def test_github_may_send_an_archive_to_its_download_host(self):
        followed = self.follow(
            "https://github.com/laravel/docs/archive/refs/heads/13.x.zip",
            "https://codeload.github.com/laravel/docs/zip/refs/heads/13.x",
        )

        assert followed.full_url.startswith("https://codeload.github.com/")

    def test_a_site_may_redirect_within_itself(self):
        followed = self.follow("https://spatie.be/docs/laravel-permission", "https://spatie.be/docs/laravel-permission/v8/introduction")

        assert followed is not None

    @pytest.mark.parametrize("target", [
        "http://169.254.169.254/latest/meta-data/iam/security-credentials/",
        "https://169.254.169.254/latest/meta-data/",
        "http://localhost:8500/v1/kv/",
        "https://internal.example/secrets",
        "http://spatie.be/docs/laravel-permission",
        "file:///etc/passwd",
        "https://spatie.be.evil.example/docs",
    ])
    def test_a_redirect_anywhere_else_is_refused(self, target):
        with pytest.raises(urllib.error.HTTPError, match="redirect"):
            self.follow("https://spatie.be/docs/laravel-permission", target)

    def test_every_site_the_updater_names_is_one_a_redirect_may_reach(self):
        """A source added without its host here would fail on its first
        same-site redirect."""
        source = Path(docs_updater.__file__).read_text(encoding="utf-8")
        named = set(re.findall(r'"https://([a-z0-9.-]+\.[a-z]+)[/"]', source))

        assert named, "found no sites in the updater"
        assert named <= docs_updater.ALLOWED_FETCH_HOSTS, sorted(named - docs_updater.ALLOWED_FETCH_HOSTS)

    def test_a_fetch_does_not_follow_a_redirect_to_another_server(self):
        """Through the real opener: the second server must not hear from us."""
        reached = []

        class Internal(http.server.BaseHTTPRequestHandler):
            def do_GET(self):
                reached.append(self.path)
                self.send_response(200)
                self.end_headers()
                self.wfile.write(b'{"AccessKeyId": "secret"}' * 10)

            def log_message(self, *args):
                pass

        internal = http.server.HTTPServer(("127.0.0.1", 0), Internal)

        class Compromised(http.server.BaseHTTPRequestHandler):
            def do_GET(self):
                self.send_response(302)
                self.send_header("Location", f"http://127.0.0.1:{internal.server_port}/credentials")
                self.end_headers()

            def log_message(self, *args):
                pass

        compromised = http.server.HTTPServer(("127.0.0.1", 0), Compromised)
        for server in (internal, compromised):
            threading.Thread(target=server.serve_forever, daemon=True).start()
        try:
            with pytest.raises(urllib.error.HTTPError):
                urllib.request.urlopen(f"http://127.0.0.1:{compromised.server_port}/page", timeout=5)
        finally:
            for server in (internal, compromised):
                server.shutdown()
                server.server_close()

        assert reached == []


class TestResponseSize:
    def test_a_response_over_the_limit_is_refused(self):
        with pytest.raises(docs_updater.ResponseTooLarge):
            docs_updater.read_limited(io.BytesIO(b"x" * 11), limit=10)

    def test_a_response_at_the_limit_is_returned_whole(self):
        assert docs_updater.read_limited(io.BytesIO(b"x" * 10), limit=10) == b"x" * 10

    @patch("laravel_mcp_companion.docs_updater.urllib.request.urlopen")
    def test_an_oversized_page_is_refused_once_and_not_retried(self, mock_urlopen, tmp_path, monkeypatch, no_waiting):
        monkeypatch.setattr(docs_updater, "MAX_RESPONSE_BYTES", 1000)
        mock_urlopen.side_effect = lambda *args, **kwargs: response(b"x" * 5000)
        fetcher = docs_updater.ExternalDocsFetcher(tmp_path)

        with pytest.raises(docs_updater.ResponseTooLarge):
            fetcher._retry_request("https://docs.vapor.build/introduction.md")

        assert mock_urlopen.call_count == 1
        assert no_waiting.call_count == 0


class TestArchiveSize:
    @patch("laravel_mcp_companion.docs_updater.urllib.request.urlopen")
    def test_a_download_over_the_limit_is_refused(self, mock_urlopen, updater, scratch, monkeypatch, no_waiting):
        monkeypatch.setattr(docs_updater, "MAX_ARCHIVE_BYTES", 100)
        mock_urlopen.side_effect = lambda *args, **kwargs: response(archive({"a.md": "x" * 5000}))

        with pytest.raises(docs_updater.ResponseTooLarge):
            updater.download_documentation()

        assert mock_urlopen.call_count == 1

    @patch("laravel_mcp_companion.docs_updater.urllib.request.urlopen")
    def test_an_archive_that_unpacks_past_the_limit_is_refused_before_it_is_unpacked(self, mock_urlopen, updater, scratch, monkeypatch):
        monkeypatch.setattr(docs_updater, "MAX_EXTRACTED_BYTES", 10_000)
        bomb = io.BytesIO()
        with zipfile.ZipFile(bomb, "w", zipfile.ZIP_DEFLATED) as zipped:
            zipped.writestr("docs-12.x/big.md", "0" * 1_000_000)
        assert len(bomb.getvalue()) < 10_000
        mock_urlopen.return_value = response(bomb.getvalue())

        with pytest.raises(docs_updater.ResponseTooLarge):
            updater.download_documentation()

        assert not list(scratch.rglob("big.md"))


class TestNothingIsLeftBehind:
    @patch("laravel_mcp_companion.docs_updater.urllib.request.urlopen")
    def test_a_failed_download_removes_its_temporary_directory(self, mock_urlopen, updater, scratch, no_waiting):
        mock_urlopen.return_value = response(b"this is not a zip file")

        with pytest.raises(Exception):
            updater.download_documentation()

        assert list(scratch.iterdir()) == []

    @patch("laravel_mcp_companion.docs_updater.urllib.request.urlopen")
    def test_a_failed_update_removes_its_temporary_directory(self, mock_urlopen, updater, scratch):
        mock_urlopen.return_value = response(archive({"new.md": "# New\n"}))

        with patch.object(DocsUpdater, "get_latest_commit", return_value=COMMIT), \
             patch.object(DocsUpdater, "write_local_metadata", side_effect=OSError("disk full")), \
             pytest.raises(OSError):
            updater.update(force=True)

        assert list(scratch.iterdir()) == []

    @patch("laravel_mcp_companion.docs_updater.urllib.request.urlopen")
    def test_a_successful_update_leaves_only_the_versions_in_the_docs_directory(self, mock_urlopen, updater, scratch):
        mock_urlopen.return_value = response(archive({"new.md": "# New\n"}))

        with patch.object(DocsUpdater, "get_latest_commit", return_value=COMMIT):
            assert updater.update(force=True) is True

        assert [p.name for p in updater.version_dir.parent.iterdir()] == ["12.x"]
        assert list(scratch.iterdir()) == []


class TestAnUpdateIsAllOrNothing:
    def run_update(self, updater, files):
        with patch("laravel_mcp_companion.docs_updater.urllib.request.urlopen", return_value=response(archive(files))), \
             patch.object(DocsUpdater, "get_latest_commit", return_value=COMMIT):
            return updater.update(force=True)

    def test_the_new_pages_replace_the_old(self, updater, scratch):
        self.run_update(updater, {"new.md": "# New\n", "guides/deep.md": "# Deep\n"})

        assert sorted(p.name for p in updater.version_dir.iterdir()) == [".metadata", "guides", "new.md"]
        assert (updater.version_dir / "guides" / "deep.md").read_text() == "# Deep\n"
        assert updater.read_local_metadata()["commit_sha"] == COMMIT["sha"]

    def test_a_copy_that_fails_leaves_the_old_pages_in_place(self, updater, scratch):
        real_copy = docs_updater.shutil.copy2
        copied = []

        def failing_copy(source, destination, **kwargs):
            if copied:
                raise OSError("disk full")
            copied.append(source)
            return real_copy(source, destination, **kwargs)

        with patch("laravel_mcp_companion.docs_updater.shutil.copy2", side_effect=failing_copy), \
             pytest.raises(OSError):
            self.run_update(updater, {"a.md": "# A\n", "b.md": "# B\n", "c.md": "# C\n"})

        assert sorted(p.name for p in updater.version_dir.iterdir()) == [".metadata", "old.md"]
        assert updater.read_local_metadata()["commit_sha"] == "old"
        assert [p.name for p in updater.version_dir.parent.iterdir()] == ["12.x"]

    def test_an_archive_cannot_supply_the_metadata_directory(self, updater, scratch):
        """An archive carrying its own .metadata used to stop the copy part
        way, after the old pages were gone."""
        self.run_update(updater, {"new.md": "# New\n", ".metadata/sync_info.json": '{"commit_sha": "forged"}'})

        assert (updater.version_dir / "new.md").exists()
        assert updater.read_local_metadata()["commit_sha"] == COMMIT["sha"]

    def test_a_version_directory_that_is_a_symlink_stays_one(self, tmp_path, scratch):
        elsewhere = tmp_path / "elsewhere" / "12.x"
        elsewhere.mkdir(parents=True)
        (elsewhere / "old.md").write_text("# Old\n")
        docs = tmp_path / "docs"
        docs.mkdir()
        (docs / "12.x").symlink_to(elsewhere, target_is_directory=True)
        updater = DocsUpdater(docs, "12.x")

        self.run_update(updater, {"new.md": "# New\n"})

        assert (docs / "12.x").is_symlink()
        assert sorted(p.name for p in elsewhere.iterdir()) == [".metadata", "new.md"]

    def test_the_updated_directory_keeps_its_permissions(self, updater, scratch):
        before = updater.version_dir.stat().st_mode

        self.run_update(updater, {"new.md": "# New\n"})

        assert updater.version_dir.stat().st_mode == before
