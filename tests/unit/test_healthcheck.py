"""The container health check.

The image's HEALTHCHECK runs `healthcheck.py`. Over HTTP it asks the server's
own /healthz. Over stdio there is no port to ask, and the usual stdio container
lives for one client session, so the check passes rather than marking every
such container unhealthy.
"""

import http.server
import threading

import pytest

from laravel_mcp_companion import healthcheck
class TestWhereToAsk:
    def test_stdio_has_no_endpoint(self):
        assert healthcheck.target(["python", "laravel_mcp_companion.py"], {}) is None

    def test_http_from_the_environment(self):
        env = {"TRANSPORT": "http", "PORT": "8081"}

        assert healthcheck.target(["python", "laravel_mcp_companion.py"], env) == "http://127.0.0.1:8081/healthz"

    def test_http_from_the_command_line(self):
        argv = ["python", "laravel_mcp_companion.py", "--transport", "http", "--port", "9000"]

        assert healthcheck.target(argv, {}) == "http://127.0.0.1:9000/healthz"

    def test_the_command_line_wins_over_the_environment(self):
        argv = ["python", "laravel_mcp_companion.py", "--transport=http", "--port=9000"]

        assert healthcheck.target(argv, {"TRANSPORT": "stdio", "PORT": "8081"}) == "http://127.0.0.1:9000/healthz"

    def test_stdio_on_the_command_line_overrides_http_in_the_environment(self):
        argv = ["python", "laravel_mcp_companion.py", "--transport", "stdio"]

        assert healthcheck.target(argv, {"TRANSPORT": "http", "PORT": "8081"}) is None

    def test_http_without_a_port_uses_the_servers_default(self):
        assert healthcheck.target([], {"TRANSPORT": "http"}) == f"http://127.0.0.1:{healthcheck.DEFAULT_HTTP_PORT}/healthz"

    def test_a_specific_bind_address_is_the_one_asked(self):
        argv = ["--transport", "http", "--port", "9000", "--host", "10.1.2.3"]

        assert healthcheck.target(argv, {}) == "http://10.1.2.3:9000/healthz"

    def test_the_wildcard_address_is_asked_over_loopback(self):
        assert healthcheck.target([], {"TRANSPORT": "http", "PORT": "8081", "HOST": "0.0.0.0"}) == "http://127.0.0.1:8081/healthz"


@pytest.fixture
def server():
    """A local endpoint whose /healthz status the test chooses."""
    state = {"status": 200}

    class Handler(http.server.BaseHTTPRequestHandler):
        def do_GET(self):
            self.send_response(state["status"])
            self.end_headers()
            self.wfile.write(b"{}")

        def log_message(self, *args):
            pass

    httpd = http.server.HTTPServer(("127.0.0.1", 0), Handler)
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    yield state, f"http://127.0.0.1:{httpd.server_port}/healthz"
    httpd.shutdown()


class TestVerdict:
    def test_stdio_is_healthy(self):
        assert healthcheck.run([], {}) == 0

    def test_an_endpoint_answering_200_is_healthy(self, server):
        _, url = server

        assert healthcheck.check(url) == 0

    def test_an_endpoint_answering_503_is_unhealthy(self, server):
        state, url = server
        state["status"] = 503

        assert healthcheck.check(url) == 1

    def test_nothing_listening_is_unhealthy(self):
        assert healthcheck.check("http://127.0.0.1:1/healthz") == 1
