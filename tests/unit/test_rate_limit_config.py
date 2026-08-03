"""Rate limit configuration: opt-in, loud on misconfiguration, stdio-inert.

The burst default matters more than it looks: FastMCP's limiter counts the
MCP initialize handshake against the bucket, so a small burst self-throttles
before the first tool call ever runs.
"""

import argparse

import pytest

from laravel_mcp_companion import build_rate_limiter, parse_arguments


def make_args(**overrides):
    defaults = {"transport": "http", "rate_limit": None, "rate_limit_burst": None}
    defaults.update(overrides)
    return argparse.Namespace(**defaults)


class TestBuildRateLimiter:
    def test_unset_returns_none(self):
        assert build_rate_limiter(make_args()) is None

    def test_configured_returns_middleware(self):
        from fastmcp.server.middleware.rate_limiting import RateLimitingMiddleware

        limiter = build_rate_limiter(make_args(rate_limit=5.0))
        assert isinstance(limiter, RateLimitingMiddleware)

    @pytest.mark.parametrize("rps", [0.0, -1.0])
    def test_nonpositive_rps_exits(self, rps):
        with pytest.raises(SystemExit):
            build_rate_limiter(make_args(rate_limit=rps))

    @pytest.mark.parametrize("rps", [float("nan"), float("inf")])
    def test_nonfinite_rps_exits_cleanly(self, rps):
        """nan/inf pass a <=0 check (neither compares below zero) and float()
        parses both from env, so a config typo must die loudly here rather
        than as a math.ceil traceback or an infinite bucket."""
        with pytest.raises(SystemExit):
            build_rate_limiter(make_args(rate_limit=rps))

    def test_nonfinite_rps_with_explicit_burst_still_exits(self):
        with pytest.raises(SystemExit):
            build_rate_limiter(make_args(rate_limit=float("inf"), rate_limit_burst=10))

    def test_burst_below_one_exits(self):
        with pytest.raises(SystemExit):
            build_rate_limiter(make_args(rate_limit=5.0, rate_limit_burst=0))

    @pytest.mark.parametrize("rps,expected_burst", [(2.0, 10), (20.0, 40), (0.4, 10)])
    def test_default_burst_covers_the_handshake(self, rps, expected_burst, monkeypatch):
        captured = {}
        from fastmcp.server.middleware import rate_limiting

        original = rate_limiting.RateLimitingMiddleware.__init__

        def spy(self, max_requests_per_second, burst_capacity=None, **kwargs):
            captured["rps"] = max_requests_per_second
            captured["burst"] = burst_capacity
            original(self, max_requests_per_second, burst_capacity=burst_capacity, **kwargs)

        monkeypatch.setattr(rate_limiting.RateLimitingMiddleware, "__init__", spy)
        build_rate_limiter(make_args(rate_limit=rps))
        assert captured["rps"] == rps
        assert captured["burst"] == expected_burst

    def test_explicit_burst_honored(self):
        limiter = build_rate_limiter(make_args(rate_limit=5.0, rate_limit_burst=3))
        assert limiter is not None

    def test_stdio_warns_and_ignores(self, caplog):
        result = build_rate_limiter(make_args(transport="stdio", rate_limit=5.0))
        assert result is None
        assert any("stdio" in r.message for r in caplog.records)


class TestRateLimitArgs:
    def test_env_fallback_parses_float(self, monkeypatch):
        monkeypatch.setattr("sys.argv", ["prog"])
        monkeypatch.setenv("RATE_LIMIT_RPS", "12.5")
        monkeypatch.setenv("RATE_LIMIT_BURST", "30")
        args = parse_arguments()
        assert args.rate_limit == 12.5
        assert args.rate_limit_burst == 30

    def test_unset_env_means_none(self, monkeypatch):
        monkeypatch.setattr("sys.argv", ["prog"])
        monkeypatch.delenv("RATE_LIMIT_RPS", raising=False)
        args = parse_arguments()
        assert args.rate_limit is None
        assert args.rate_limit_burst is None

    def test_invalid_env_value_errors(self, monkeypatch):
        monkeypatch.setattr("sys.argv", ["prog"])
        monkeypatch.setenv("RATE_LIMIT_RPS", "lots")
        with pytest.raises(SystemExit):
            parse_arguments()

    @pytest.mark.parametrize("value", ["inf", "nan", "-inf"])
    def test_nonfinite_env_value_rejected_at_build(self, monkeypatch, value):
        """float() happily parses these strings; the builder must not."""
        monkeypatch.setattr("sys.argv", ["prog"])
        monkeypatch.setenv("TRANSPORT", "http")
        monkeypatch.setenv("RATE_LIMIT_RPS", value)
        args = parse_arguments()
        with pytest.raises(SystemExit):
            build_rate_limiter(args)
