# Contributing to Laravel MCP Companion

Thank you for considering contributing to this project! Here's how you can help.

## Code of Conduct

This project follows a code of conduct that expects all contributors to be respectful and inclusive.

## How to Contribute

### Reporting Bugs

If you find a bug, please create an issue with:

- A clear title and description
- Steps to reproduce the issue
- Expected and actual behavior
- Screenshots if applicable
- Any relevant code snippets

### Suggesting Enhancements

Enhancement suggestions are welcome! Please include:

- A clear title and description of the enhancement
- Step-by-step description of the suggested enhancement
- Any relevant examples
- Why this enhancement would be useful

### Pull Requests

1. Fork the repository
2. Create a new branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests if available
5. Commit your changes (`git commit -m 'Add some amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

#### Pull Request Guidelines

- Update README.md or OPERATIONS.md with details of changes if applicable
- Update the example code if applicable
- The PR should work on Python 3.12, the version the project requires
- A change to a tool's arguments or output changes `tests/protocol/contract.json` and `API.md`; regenerate both and say so in the changelog
- Include relevant tests if possible

## Development

### Prerequisites
- Python 3.12+
- [uv](https://docs.astral.sh/uv/)
- Node.js 22+ (for the MCP Inspector)

### Setup
```bash
git clone https://github.com/brianirish/laravel-mcp-companion
cd laravel-mcp-companion
uv sync                    # creates .venv from uv.lock, development tools included
source .venv/bin/activate  # Windows: .venv\Scripts\activate
```

### Running Tests
```bash
# The default suite, with coverage
pytest --cov --cov-report=html

# Unit tests only
pytest tests/unit/

# Integration tests only
pytest tests/integration/

# Protocol compliance tests
pytest tests/protocol/ -m protocol

# End-to-end and benchmark suites (not run by default)
pytest -m e2e --no-cov
pytest -m bench --no-cov -s
```

### Manual Testing with MCP Inspector
The [MCP Inspector](https://github.com/modelcontextprotocol/inspector) provides a visual UI for testing MCP servers.

```bash
# Launch Inspector (opens browser at http://localhost:6274)
npx @modelcontextprotocol/inspector python -m laravel_mcp_companion --transform-mode none

# With specific version
npx @modelcontextprotocol/inspector python -m laravel_mcp_companion --transform-mode none --version 11.x
```

Use the Inspector to:
- **Tools tab**: Test all tools with auto-generated input forms
- **Resources tab**: Browse `laravel://`, `laravel-external://` and `laravel-package://` resources

### Code Quality
```bash
ruff check --fix .     # Linting
mypy --ignore-missing-imports .  # Type checking
black .                # Formatting
```

## Documentation

If you're adding new features, please update the documentation accordingly.

## License

By contributing, you agree that your contributions will be licensed under the project's MIT License.