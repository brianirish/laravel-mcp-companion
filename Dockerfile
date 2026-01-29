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
ENV VERSION="12.x"

# Set the entrypoint to the Python script
ENTRYPOINT ["python", "laravel_mcp_companion.py"]

# Default command (no arguments) - can be overridden
CMD []
