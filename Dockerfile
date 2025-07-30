FROM python:3.12-alpine

# Install build dependencies (if necessary)
RUN apk add --no-cache build-base libffi-dev openssl-dev

# Set working directory
WORKDIR /app

# Copy requirements file first (for better layer caching)
COPY requirements.txt .

# Install Python dependencies from requirements.txt
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy rest of the project files
COPY . .

# Default environment
ENV PYTHONUNBUFFERED=1

# Run the MCP server with HTTP transport
CMD ["python", "laravel_mcp_companion.py"]
