Source: https://nightwatch.laravel.com/docs/mcp-server.md

# MCP Server

> Connect AI assistants to Nightwatch using the Model Context Protocol

Nightwatch provides a [Model Context Protocol](https://modelcontextprotocol.io/) (MCP) server that allows AI assistants to list applications, browse issues, view stack traces, update issue status, and add comments.

## Getting started

Nightwatch uses OAuth to securely connect AI assistants to your account. When you first connect, your AI assistant will open a browser window for you to authorize access.

### Automatic setup via Boost

If your application uses [Laravel Boost](https://github.com/laravel/boost), the Nightwatch MCP server can be automatically configured during installation. Boost detects the `laravel/nightwatch` package and offers to set up the MCP server for your AI assistant:

```bash theme={null}
php artisan boost:install
```

### Manual setup

> [tab] Claude Code
>
> Run in your terminal:
>
> ```bash theme={null}
> claude mcp add --transport http nightwatch https://nightwatch.laravel.com/mcp
> ```
>
> Then run `/mcp` in a Claude Code session to complete the authentication flow.

> [tab] Codex
>
> Run in your terminal:
>
> ```bash theme={null}
> codex mcp add nightwatch --url https://nightwatch.laravel.com/mcp
> ```

> [tab] Cursor
>
> Add to `.cursor/mcp.json`:
>
> ```json theme={null}
> {
>   "mcpServers": {
>     "nightwatch": {
>       "command": "npx",
>       "args": ["-y", "mcp-remote", "https://nightwatch.laravel.com/mcp"]
>     }
>   }
> }
> ```

> [tab] Gemini
>
> Add to `.gemini/settings.json`:
>
> ```json theme={null}
> {
>   "mcpServers": {
>     "nightwatch": {
>       "command": "npx",
>       "args": ["-y", "mcp-remote", "https://nightwatch.laravel.com/mcp"]
>     }
>   }
> }
> ```

> [tab] Junie
>
> Add to `.junie/mcp/mcp.json`:
>
> ```json theme={null}
> {
>   "mcpServers": {
>     "nightwatch": {
>       "command": "npx",
>       "args": ["-y", "mcp-remote", "https://nightwatch.laravel.com/mcp"]
>     }
>   }
> }
> ```

> [tab] OpenCode
>
> Run `opencode mcp add`, select **remote** when prompted, and enter `https://nightwatch.laravel.com/mcp` as the URL. Then authenticate:
>
> ```bash theme={null}
> opencode mcp auth nightwatch
> ```

> [tab] VS Code
>
> Open the Command Palette (`Cmd/Ctrl + Shift + P`), select **MCP: Add Server**, and enter:
>
> ```
> https://nightwatch.laravel.com/mcp
> ```

> [tab] Other
>
> For other MCP-compatible tools, use the server URL:
>
> ```
> https://nightwatch.laravel.com/mcp
> ```
>
> If your client doesn't support remote servers natively, use [mcp-remote](https://github.com/geelen/mcp-remote):
>
> ```bash theme={null}
> npx -y mcp-remote https://nightwatch.laravel.com/mcp
> ```

## Example workflows

### Investigating an exception

Ask your AI assistant to investigate an issue by its ref number:

> "Can you look at issue #456 and tell me what's causing it?"

Your assistant will retrieve the full stack trace, code context, and occurrence statistics, then analyze the problem and suggest fixes.

> [!NOTE]
>
> If you have multiple applications, you can reference them by name (e.g.,
> "issue #456 in Beep"). Otherwise, your assistant will prompt you to choose.
> You can also paste issue URLs directly from Nightwatch.

### Triaging recent issues

Ask your assistant to help prioritize your issue backlog:

> "What are the most recent exceptions in my production environment? Help me prioritize which ones to fix first."

Your assistant will gather information about your issues and provide recommendations based on frequency, user impact, and severity.

### Resolving issues

After fixing a bug, you can ask your assistant to update the issue:

> "Mark issue #123 as resolved and include a brief comment summarizing the fix"

Your assistant will change the status and add a comment describing what caused the issue and how it was fixed.

## Security

* **Authentication:** The MCP server uses OAuth to securely connect to your account.
* **Authorization:** You can only access applications and issues within organizations you belong to.
* **Audit Trail:** All actions are logged in the issue activity history with attribution to your user account and the AI agent used.
