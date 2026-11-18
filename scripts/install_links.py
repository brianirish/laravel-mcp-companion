#!/usr/bin/env python3
"""Print the one-click install links the README carries.

    python scripts/install_links.py

Paste the output into the Installation section of README.md when the server's
name or launch command changes. tests/unit/test_readme_install_links.py fails
while the README and this script disagree.

Formats, as documented by each client:

  Cursor   cursor://anysphere.cursor-deeplink/mcp/install?name=NAME&config=BASE64
           where BASE64 is the base64 of the server's JSON configuration.
           https://cursor.com/docs/context/mcp/install-links
           GitHub does not render cursor:// links, so the README uses the web
           form, which swaps the prefix for https://cursor.com/link/.
           https://cursor.com/docs/reference/deeplinks

  VS Code  vscode:mcp/install?JSON (vscode-insiders: for Insiders), where JSON
           is {"name": ..., "command": ...} stringified and URL-encoded. For a
           web page the whole URL is wrapped: https://vscode.dev/redirect?url=URL
           https://code.visualstudio.com/api/extension-guides/ai/mcp
"""

import base64
import json
from urllib.parse import quote

SERVER_NAME = "laravel-mcp-companion"
SERVER_CONFIG = {"command": "uvx", "args": ["laravel-mcp-companion"]}

# The characters JavaScript's encodeURIComponent leaves alone, besides
# letters and digits.
ENCODE_URI_COMPONENT_SAFE = "-_.!~*'()"


def stringify(value: object) -> str:
    """JSON as JavaScript's JSON.stringify writes it: no spaces."""
    return json.dumps(value, separators=(",", ":"))


def cursor_link() -> str:
    config = base64.b64encode(stringify(SERVER_CONFIG).encode()).decode()
    return f"https://cursor.com/link/mcp/install?name={quote(SERVER_NAME, safe='')}&config={quote(config, safe='=')}"


def vscode_link(scheme: str) -> str:
    configuration = stringify({"name": SERVER_NAME, **SERVER_CONFIG})
    url = f"{scheme}:mcp/install?{quote(configuration, safe=ENCODE_URI_COMPONENT_SAFE)}"
    return f"https://vscode.dev/redirect?url={quote(url, safe='')}"


def install_links() -> dict[str, str]:
    return {
        "cursor": cursor_link(),
        "vscode": vscode_link("vscode"),
        "vscode-insiders": vscode_link("vscode-insiders"),
    }


if __name__ == "__main__":
    for client, link in install_links().items():
        print(f"{client}\n  {link}\n")
