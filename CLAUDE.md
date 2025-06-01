# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

**IMPORTANT**: Always activate the virtual environment first with `source .venv/bin/activate` before running any Python commands.

### Development and Testing
- **Run type checking**: `mypy .` (temporarily install with `uv pip install mypy`)
- **Run linting**: `ruff check .` (temporarily install with `uv pip install ruff`)
- **Format code**: `black .` (temporarily install with `uv pip install black`)
- **Run tests**: `pytest` (if tests are added)
- **Run tests with coverage**: `pytest --cov` (if tests are added)

### Running the MCP Server
- **Basic server start**: `python laravel_docs_server.py`
- **Start with documentation update**: `python laravel_docs_server.py --update-docs`
- **Start with specific Laravel version**: `python laravel_docs_server.py --version 11.x`
- **Full example**: `python laravel_docs_server.py --docs-path ./docs --version 11.x --update-docs --transport stdio`

### Documentation Management
- **Update latest version**: `python docs_updater.py`
- **Update specific version**: `python docs_updater.py --version 11.x`
- **Update all versions**: `python docs_updater.py --all-versions`
- **Force update**: `python docs_updater.py --force`
- **Check if update needed**: `python docs_updater.py --check-only`

### Installation Commands
- **Install dependencies**: `uv pip install .`
- **Install development dependencies**: `uv pip install -r requirements-dev.txt`
- **Create virtual environment**: `uv venv`

## Architecture

This is a Model Context Protocol (MCP) server that provides Laravel documentation and package recommendations to AI assistants.

### Core Components
- **`laravel_docs_server.py`**: Main MCP server with documentation and package recommendation tools
- **`docs_updater.py`**: Automatic fetching/updating of Laravel docs from GitHub
- **`shutdown_handler.py`**: Graceful shutdown handling
- **`docs/`**: Version-organized documentation storage (e.g., `docs/12.x/`, `docs/11.x/`)

### Key Features
- **Multi-Version Support**: Supports Laravel 6.x through latest (auto-detects new versions)
- **Documentation Tools**: `list_laravel_docs()`, `search_laravel_docs()`, `update_laravel_docs()`, `laravel_docs_info()`
- **Package Tools**: `get_laravel_package_recommendations()`, `get_laravel_package_info()`, `get_laravel_package_categories()`, `get_features_for_laravel_package()`
- **Resource Access**: Documentation via `laravel://{path}` or `laravel://{version}/{path}`
- **Dynamic Version Detection**: Automatically detects new Laravel releases via GitHub API
- **Automatic Updates**: Daily sync with Laravel's official docs repository

### Version System
- **Supported Versions**: 6.x through latest (dynamically detected)
- **Default Version**: Always latest available
- **Directory Structure**: `docs/{version}/` with version-specific metadata
- **Future-Proof**: Automatically supports new releases (13.x, 14.x, etc.)

### GitHub Actions
- **Daily Updates**: `docs-update.yaml` runs daily, updates all versions, auto-merges PRs
- **Auto Releases**: Creates patch releases when docs are updated
- **Branch Protection**: Requires status checks, enables auto-merge

## Commit Style

When asked to commit changes, use simple, direct commit messages without Claude Code attribution. Write as if the user wrote them. Use lowercase, be brief but clear about what changed.

Examples:
- "add multi-version laravel docs support"
- "fix version detection api call"  
- "update readme with new tool names"