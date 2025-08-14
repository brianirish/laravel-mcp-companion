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

# Set the entrypoint to the Python script so arguments can be passed
ENTRYPOINT ["python", "laravel_mcp_companion.py"]

# Default command (no arguments) - can be overridden
CMD []
