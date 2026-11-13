# ---- Build stage -------------------------------------------------------------
# The compiler toolchain and git are needed to install the dependencies and
# for nothing after that, so they stay in this stage.
FROM python:3.12-alpine AS build

RUN apk add --no-cache build-base libffi-dev openssl-dev git && \
    pip install --no-cache-dir uv==0.13.7

WORKDIR /app

# Install exactly what uv.lock pins. The image used to install from
# requirements.txt, which lists only the direct dependencies with open ranges,
# so two builds of the same tag could contain different versions of everything
# underneath them.
ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_PYTHON_DOWNLOADS=never
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev --no-install-project

# ---- Runtime stage -----------------------------------------------------------
FROM python:3.12-alpine

# Run as an unprivileged user with a fixed id, so volume ownership is
# predictable across image versions.
RUN addgroup -S -g 10001 app && adduser -S -u 10001 -G app -h /app app

WORKDIR /app

# Dependencies first, and on their own. Documentation syncs land daily and touch
# only docs/, so this layer is identical from one nightly image to the next and
# users pulling :latest re-download only the layer below it.
COPY --from=build /app/.venv /app/.venv
ENV PATH="/app/.venv/bin:$PATH"

# Now the source and the documentation corpus. Owned by the app user because
# --update-docs writes into docs/.
COPY --chown=app:app . .

USER app

# The MCP Registry validates OCI ownership through this label: it must match
# the "name" in server.json or registry publishes are rejected.
LABEL io.modelcontextprotocol.server.name="io.github.brianirish/laravel-mcp-companion"

# Default environment
ENV PYTHONUNBUFFERED=1

# HTTP server environment variables
ENV PORT=8081
ENV TRANSPORT=stdio
ENV DOCS_PATH="./docs"
ENV SERVER_NAME="LaravelMCPCompanion"
ENV LOG_LEVEL="INFO"

# Bind all interfaces inside the container; the container network boundary and
# explicit port publishing are the access control. Outside Docker the server
# defaults to loopback. The server has no built-in authentication, so only
# publish this port to networks you trust, and set ALLOWED_HOSTS when serving
# under a hostname other than localhost.
ENV HOST=0.0.0.0


# Over HTTP this asks the server's own /healthz. Over stdio it passes: there is
# no port to ask, and a stdio container lasts one client session.
HEALTHCHECK --interval=30s --timeout=5s --start-period=20s --retries=3 \
    CMD ["python", "healthcheck.py"]

# Set the entrypoint to the Python script
ENTRYPOINT ["python", "laravel_mcp_companion.py"]

# Default command (no arguments) - can be overridden
CMD []
