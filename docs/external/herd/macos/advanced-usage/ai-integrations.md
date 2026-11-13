Source: https://herd.laravel.com/docs/macos/advanced-usage/ai-integrations.md

# AI Integrations

# AI Integrations

Laravel Herd ships with a powerful MCP (Model Context Protocol) server that can speed up your development process, by providing useful tools to your AI agents.

> [!NOTE]
>
> If you want to build and change applications with coding agents right from your browser, take a look at [Herd Studio](https://herd.laravel.com/docs/macos/herd-studio/overview.md). The [Herd CLI](https://herd.laravel.com/docs/macos/advanced-usage/herd-cli.md) also provides many commands with `--json` output that agents can use to read mails, dumps and site information.

Your AI agent should make use of the tools automatically (when needed), but you can also manually trigger and use the available tools in your MCP client/IDE.

## Installation

The easiest way to install the Herd MCP server is by making use of [Laravel Boost](https://boost.laravel.com). Boost automatically installs the Herd MCP server and makes it available in your IDEs.
If you are not using Boost, you may manually install the Herd MCP server.

## Manual Installation

> [!NOTE]
>
> While you may install the Herd MCP server globally, we recommend installing it per-project. This way, you gain access to more fine-grained tools which leads to better AI agent results.

## Manual configuration

This is the standard configuration that works in most MCP clients.
Make sure to replace `YOUR-SITE-PATH` with the base path to your Laravel project or remove the `env` key with the site path if you're using the global installation.

```json theme={null}
{
    "herd": {
        "command": "php",
        "args": [
            "/Applications/Herd.app/Contents/Resources/herd-mcp.phar"
        ],
        "env": {
            "SITE_PATH": "YOUR-SITE-PATH"
        }
    }
}
```

> [accordion] Claude Code
>
> Use the Claude Code CLI to add the Herd MCP server. In the root of your project, run the following command:
>
> ```bash theme={null}
> claude mcp add herd php /Applications/Herd.app/Contents/Resources/herd-mcp.phar -e SITE_PATH="$(pwd)"
> ```
>
> This will automatically set the `SITE_PATH` to the project root.

> [accordion] Cursor
>
> Go to `Cursor Settings` -> `Tools & Integrations` -> `New MCP Server`.
>
> Then, paste the MCP server configuration.

> [accordion] Junie
>
> Follow the instructions in the [Junie documentation](https://www.jetbrains.com/help/junie/model-context-protocol-mcp.html#bksdkr_21) to install the Herd MCP server using the standard configuration above.

> [accordion] Windsurf
>
> Follow the instructions in the [Windsurf documentation](https://docs.windsurf.com/windsurf/cascade/mcp) to install the Herd MCP server using the standard configuration above.

## Available Prompts

### `debug_site`

Perform debug operations on a site. This includes retrieving executed query information, dispatched jobs, logs, dumps calls, outgoing HTTP requests and more.

## Available Resources

### `site_information`

Returns information about the current site, such as the correct local URL, environment variables, used PHP versions and Node versions.

## Available Tools

The Herd MCP server provides the following tools to your AI agents:

### `find_available_services`

Get a list of available services (such as MySQL, Typesense, Redis, Laravel Reverb, Typesense, etc.) on your system. This will also return the environment variables needed for each service to connect and configure it.

### `install_service`

Install a service on your system. This will download the service's binary, configure it, and start it.

**Parameters:**

* `type`: The type of service to install.
* `port`: The port to use for the service.

### `start_or_stop_service`

Start or stop a Herd provided service on your system.

**Parameters:**

* `shouldStart`: Whether to start or stop the service.
* `type`: The type of service to start/stop.
* `port`: The port of the service to start/stop.
* `version`: The version of the service to start/stop.

### `get_all_php_versions`

Get a list of all PHP versions and their status (installed, in-use, etc.) from Herd.

### `install_php_version`

Installs or updates a specific PHP version on your system

**Parameters:**

* `version`: The PHP version to install (e.g. `8.3`).

### `get_all_sites`

Get a list of all sites provided by Laravel Herd on your system. This includes information such as site names, URLs, paths, secure status, environment variables, the PHP version that is used, and more.

### `secure_or_unsecure_site`

Secure or unsecure a site by enabling or disabling HTTPS. The site will then be available at `https://{siteName}.test`.

**Parameters:**

* `shouldSecure`: Whether to secure or unsecure the site.
* `siteName`: The name of the site to secure/unsecure.

### `isolate_or_unisolate_site`

Isolate or Un-isolate a site. Isolating means that the site will use a specific PHP version, rather than the global PHP version. Un-isolating removes this isolation and uses the global PHP version for the site.

**Parameters:**

* `shouldIsolate`: Whether to isolate or unisolate the site.
* `siteName`: The name of the site to isolate/unisolate.
* `phpVersion`: The PHP version to use for the site.

### `get_last_deployment_information`

Returns information about the last deployment from Laravel Forge, if the local site is linked with a Forge site.
