# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

**IMPORTANT**: Always activate the virtual environment first with `source .venv/bin/activate` before running any Python commands.

### Development and Testing
- **Run type checking**: `mypy .`
- **Run linting**: `ruff check .`
- **Format code**: `black .`
- **Run tests**: `pytest` (if tests are added)
- **Run tests with coverage**: `pytest --cov` (if tests are added)

### Running the MCP Server
- **Basic server start**: `python laravel_docs_server.py`
- **Start with documentation update**: `python laravel_docs_server.py --update-docs`
- **Start with specific Laravel version**: `python laravel_docs_server.py --version 11.x`
- **Full example**: `python laravel_docs_server.py --docs-path ./docs --version 12.x --update-docs --transport stdio`

### Documentation Management
- **Update documentation**: `python docs_updater.py --target-dir ./docs --version 12.x`
- **Force documentation update**: `python docs_updater.py --force`
- **Check if update needed**: `python docs_updater.py --check-only`

### Installation Commands
- **Install dependencies**: `uv pip install .`
- **Install development dependencies**: `uv pip install -r requirements-dev.txt`
- **Create virtual environment**: `uv venv`

## Architecture

This is a Model Context Protocol (MCP) server that provides Laravel documentation and package recommendations to AI assistants. The architecture consists of:

### Core Components
- **`laravel_docs_server.py`**: Main MCP server implementing FastMCP with documentation and package recommendation tools
- **`docs_updater.py`**: Handles automatic fetching/updating of Laravel docs from GitHub repository
- **`shutdown_handler.py`**: Graceful shutdown handling for the server
- **`docs/`**: Local storage for Laravel documentation files (auto-updated from laravel/docs repo)

### Key Features
- **Documentation Tools**: `list_docs()`, `search_docs()`, `read_doc()` (via resources), `update_docs()`, `docs_info()`
- **Package Recommendation Tools**: `get_package_recommendations()`, `get_package_info()`, `get_package_categories()`, `get_features_for_package()`
- **Resource Access**: Documentation accessible via `laravel://{path}` URI scheme
- **Version Management**: Supports multiple Laravel version branches (12.x, 11.x, etc.)
- **Automatic Updates**: Can sync with Laravel's official docs repository

### Data Structures
- **PACKAGE_CATALOG**: Hardcoded catalog of popular Laravel packages with descriptions, use cases, and categories
- **FEATURE_MAP**: Maps packages to common implementation patterns
- **TOOL_DESCRIPTIONS**: Detailed descriptions for when to use each MCP tool

### Transport Support
- Supports stdio (default), websocket, and SSE transports
- Command-line configurable for different deployment scenarios

### Metadata System
- Stores sync information in `.metadata/sync_info.json`
- Tracks commit SHA, sync time, and version information for documentation updates