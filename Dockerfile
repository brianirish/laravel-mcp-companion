FROM python:3.12-alpine

# Install build dependencies (if necessary)
RUN apk add --no-cache build-base libffi-dev openssl-dev git

# Set working directory
WORKDIR /app

# Copy project files
COPY . .

# Install Python dependencies including HTTP server requirements
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

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


# Set the entrypoint to the Python script
ENTRYPOINT ["python", "laravel_mcp_companion.py"]

# Default command (no arguments) - can be overridden
CMD []
