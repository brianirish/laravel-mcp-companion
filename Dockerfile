FROM python:3.12-alpine

# Install build dependencies (if necessary)
RUN apk add --no-cache build-base libffi-dev openssl-dev

# Set working directory
WORKDIR /app

# Copy project files
COPY . .

# Install Python dependencies
RUN pip install --upgrade pip && \
    pip install --no-cache-dir fastmcp mcp[cli,client]

# Default environment
ENV PYTHONUNBUFFERED=1

# Run the MCP server with HTTP transport
CMD ["python", "laravel_docs_server.py"]
