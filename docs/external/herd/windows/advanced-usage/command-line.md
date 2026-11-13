Source: https://herd.laravel.com/docs/windows/advanced-usage/command-line.md

# Command Line

# Herd Command Line Interface

Herd ships with a powerful CLI that allows you to manage your entire development environment from the terminal. The CLI is also a great tool for AI coding agents that need to interact with your local development setup.

You can get the full list of commands by running `herd list` in your terminal. Run `herd help COMMAND` to see all arguments and options of a command.

Many commands support a `--json` option that prints machine-readable output instead of a table. This is especially useful for scripts and AI agents.

> [!NOTE]
>
> The `status`, `site:info`, `site:services`, `node:list`, `mail:*` and `insights:*` commands talk to the Herd app and require Herd to be running.

## Git Bash

If you want to use the Herd binaries in Git Bash, add these aliases to your `.bash_profile`:

```bash theme={null}
alias php="php.bat"
alias herd="herd.bat"
alias laravel="laravel.bat"
alias composer="composer.bat"
```

## Site Management

### herd park

Park a directory so that all its subdirectories become available as `.test` sites.

```powershell theme={null}
herd park
herd park C:\Users\you\Code
```

### herd parked

List all sites within parked paths.

### herd forget

Remove the current working directory (or a specified directory) from Herd's list of parked paths.

```powershell theme={null}
herd forget
herd forget C:\Users\you\Code
```

### herd link

Register a site outside of a parked path. Supports linking multiple domains to a single application.

```powershell theme={null}
# Link the current directory as some-site.test
herd link some-site
# Link the same application via some-other-domain.test
herd link some-other-domain
```

### herd links

Display all linked sites.

### herd unlink

Remove the configuration for a linked site.

```powershell theme={null}
herd unlink some-site
```

### herd sites

List all sites that Herd is currently serving.

### herd paths

Display all registered paths (parked directories).

### herd open

Open the site for the current (or specified) directory in your browser.

### herd edit

Open the current directory in your configured IDE.

### herd site:info

Show everything about a site: its URL, PHP and Node.js versions, the services that its `.env` file points to, detected capabilities like `php artisan dev`, Pail or queues, and its [workspaces](https://herd.laravel.com/docs/windows/sites/workspaces.md).

```powershell theme={null}
herd site:info
herd site:info --site=my-app
```

### herd site:env

Read and edit the `.env` file of a site. Herd keeps comments and the order of your variables, and quotes values with spaces.

```powershell theme={null}
herd site:env list
herd site:env get APP_URL
herd site:env set APP_NAME "My App"
herd site:env unset DEBUGBAR_ENABLED
```

### herd site:services

Show or change which service a site uses for its database, queue, cache and broadcasting (Herd Pro). See [Per-Site Services](https://herd.laravel.com/docs/windows/herd-pro-services/per-site-services.md).

```powershell theme={null}
herd site:services
herd site:services queue redis
```

### herd site-information

Display information about the specified site as JSON. For Laravel applications, this shows the result of `php artisan about`, but you can replace that with a custom driver.

### herd which

Display which Herd driver serves the current working directory. Useful when debugging issues with custom Herd drivers.

## Herd Studio

### herd studio

Open [Herd Studio](https://herd.laravel.com/docs/windows/herd-studio/overview.md) for the current or given site in your browser.

```powershell theme={null}
herd studio
herd studio my-app
```

## Workspaces

[Workspaces](https://herd.laravel.com/docs/windows/sites/workspaces.md) are isolated copies of a site on their own git branch and domain.

### herd workspace

Create a new workspace for the site in the current directory. Inside an existing git worktree, this command registers the worktree as a workspace.

```powershell theme={null}
herd workspace feature-auth
herd workspace feature-auth --database=clone
```

### herd workspaces

List the workspaces of the site in the current directory. Use `--site=` for another site or `--all` for the workspaces of all sites.

### herd workspace:switch

Switch your terminal to the directory of a workspace. In the Command Prompt, Herd changes the current directory of your session. In PowerShell, Herd prints the path of the workspace so that you can `cd` into it.

### herd workspace:open

Open a workspace in your browser.

### herd workspace:merge

Merge the branch of a workspace into its base branch. Use `--push` to push the base branch afterwards and `--delete` to delete the workspace.

### herd workspace:delete

Delete a workspace including its site, certificate and isolated database. The branch stays in your repository.

## Databases

The database commands use the database connection of the site's `.env` file and work with MySQL, MariaDB, PostgreSQL and SQLite.

### herd db

Open the database of the current or given site in your database client like TablePlus, using the credentials from the `.env` file.

### herd db:connection

Show the database connection of a site – driver, host, port, database and user – and a ready-to-use connection URL.

```powershell theme={null}
herd db:connection
```

### herd db:list

List all databases on the server that the site uses.

### herd db:use

Point the site at another database on the same server by updating `DB_DATABASE`. If the database doesn't exist, Herd asks whether to create it. Use `--create` to create it without asking.

```powershell theme={null}
herd db:use shop_testing --create
```

### herd db:create

Create a database on the server that the site uses. Without a name, Herd creates the database from `DB_DATABASE`. For SQLite, Herd creates the database file.

### herd db:drop

Drop a database on the server that the site uses. Herd refuses to drop the database from the site's `DB_DATABASE` unless you pass `--force`.

## PHP Version Management

### herd use

Change the global PHP version that Herd uses to serve all sites that don't have an isolated version.

```powershell theme={null}
herd use 8.3
herd use 8.4
```

### herd isolate

Tell Herd to use a specific PHP version for the current directory when serving sites or using the `herd composer` or `herd php` commands.

```powershell theme={null}
herd isolate 8.2
herd isolate 8.3 --site="site-name"
```

### herd unisolate

Revert a site back to Herd's global PHP version.

### herd isolated

List all sites using isolated PHP versions.

### herd php

Proxy PHP commands using the isolated site's PHP executable.

```powershell theme={null}
herd php artisan inspire
herd php -v
```

### herd composer

Proxy Composer commands using the isolated site's PHP executable. We recommend setting up a shell alias so that running `composer` always uses `herd composer` and picks up the correct PHP version for your site.

### herd which-php

Display which PHP binary Herd uses to serve the application at your current terminal path.

### herd ini

Open the `php.ini` file for your current global PHP version in your configured IDE. When running this command in an isolated project path, Herd opens the php.ini for the isolated PHP version.

```powershell theme={null}
herd ini
herd ini 8.0
```

### herd php:list

List all PHP versions and their installation status.

```powershell theme={null}
herd php:list

+---------+-----------+------------------+
| Version | Status    | Update Available |
+---------+-----------+------------------+
| 8.5     | Installed |                  |
| 8.4 *   | Installed |                  |
| 8.3     | Installed |                  |
| 8.2     | Installed |                  |
| 8.1     | Installed |                  |
| 8.0     | Installed |                  |
| 7.4     | Installed |                  |
+---------+-----------+------------------+
```

### herd php:install

Install a PHP version.

```powershell theme={null}
herd php:install 8.3
```

### herd php:update

Update a PHP version to the latest patch release.

```powershell theme={null}
herd php:update 8.4
```

## Node.js Version Management

### herd node:list

List the Node.js versions that you installed via Herd's nvm and the version that your shell currently uses.

### herd node:install

Install a Node.js version via nvm, or update an installed major version to its latest release.

```powershell theme={null}
herd node:install 22
herd node:install 22.11.0
```

## SSL/TLS

### herd secure

Generate a trusted TLS certificate for the site in the current directory.

### herd unsecure

Remove the TLS certificate and the HTTPS redirect from nginx. Make sure to restart your browser session or clear your redirect cache afterwards.

### herd secured

List all currently secured sites with certificate expiration dates.

## Proxies

### herd proxy

Create an Nginx proxy site for the specified host. Useful for services like Reverb or Docker containers.

```powershell theme={null}
herd proxy my-app http://localhost:8080
```

### herd unproxy

Remove an Nginx proxy configuration.

```powershell theme={null}
herd unproxy my-app
```

### herd proxies

Display all configured proxy sites.

## Services (Herd Pro) ✨

Herd Pro users can manage services like MySQL, PostgreSQL, Redis, and more entirely from the CLI. See [Services](https://herd.laravel.com/docs/windows/herd-pro-services/services.md) for more details.

### herd services:list

List all installed service instances and their current status.

```powershell theme={null}
herd services:list
```

### herd services:available

List all available service types that can be created.

```powershell theme={null}
herd services:available
```

### herd services:versions

List all available versions for a service type.

```powershell theme={null}
herd services:versions mysql
```

### herd services:create

Create a new service instance.

```powershell theme={null}
herd services:create mysql
```

### herd services:start

Start a service instance.

```powershell theme={null}
herd services:start mysql
```

### herd services:stop

Stop a service instance.

```powershell theme={null}
herd services:stop mysql
```

### herd services:clone

Clone an existing service instance including its data and configuration.

```powershell theme={null}
herd services:clone mysql
```

### herd services:delete

Delete a service and all its data.

```powershell theme={null}
herd services:delete mysql
```

## Mail (Herd Pro) ✨

The mail commands read the mails that Herd's [local mail server](https://herd.laravel.com/docs/windows/herd-pro-services/mail.md) captured. They are great for testing sign-up or password-reset flows from the terminal or with an AI agent.

`mail:list`, `mail:latest` and `mail:wait` accept filters: `--mailbox=`, `--to=`, `--from=` and `--subject=`. All filters are case-insensitive, and all except `--mailbox` match parts of the value.

### herd mail:list

List captured mails, newest first. Use `--since=` to only show mails received after a date or a time like `"5 minutes ago"`, and `--limit=` to change the number of mails (default 50).

```powershell theme={null}
herd mail:list --to=taylor@laravel.com
```

### herd mail:show

Show a mail with its sender, recipients, subject, attachments and body as plain text. Use `--format=html`, `--format=raw` or `--format=json` for other formats, and `--headers` to print all headers.

```powershell theme={null}
herd mail:show 3f2a9c...
```

### herd mail:latest

Show the newest mail. This is handy right after an action that sends a mail.

```powershell theme={null}
herd mail:latest --subject="Reset Password"
```

### herd mail:wait

Wait until a new mail arrives that matches the filters, and show it. Only mails that arrive after you start the command count. The command exits with code 1 after a timeout of 30 seconds, which you can change with `--timeout=`.

```powershell theme={null}
herd mail:wait --to=taylor@laravel.com --timeout=60
```

### herd mail:links

Print all links of a mail, one per line – for example the verification or password-reset URL.

### herd mail:attachments

List the attachments of a mail with the path where Herd stored each file.

### herd mail:attachment

Copy an attachment of a mail into the current directory or the path from `--out=`.

```powershell theme={null}
herd mail:attachment 3f2a9c... invoice.pdf --out=C:\Users\you\Downloads
```

### herd mail:mailboxes

List all mailboxes. A mailbox is the SMTP username that an application used to send the mail.

### herd mail:delete

Delete a mail and its attachments.

### herd mail:clear

Delete all captured mails, or only the mails of a mailbox.

```powershell theme={null}
herd mail:clear
herd mail:clear my-app
```

### herd mail:config

Show the host and port of Herd's mail server and the `.env` values that an application needs to send mails to Herd.

## Insights (Herd Pro) ✨

The insights commands read the runtime context that Herd captured for [Insights](https://herd.laravel.com/docs/windows/debugging/insights.md) – `dump()` and `dd()` output, queries, logs, jobs, HTTP requests and cache events. By default, they show the entries of the site in the current directory. Use `--site=` for another site or `--all` for all sites, and `--type=` to only show one type like `query` or `log`.

### herd insights:list

Show the captured entries of a site, grouped by request. Each request starts with a summary line with the route, status, time, number of queries and issues.

```powershell theme={null}
herd insights:list --type=query
```

### herd insights:watch

Stream new entries as they arrive. Stop the command with `Ctrl+C`. With `--json`, Herd prints one JSON object per line.

### herd insights:analyze

Find N+1 queries, duplicate queries, slow queries, errors and slow requests, with the file and line and a hint how to fix them. To verify a fix, load the page again and pass the cursor that the previous run printed to `--after`.

```powershell theme={null}
herd insights:analyze
herd insights:analyze --after=CURSOR
```

### herd insights:clear

Discard the captured entries of the current site, or of all sites with `--all`.

### herd insights:status

Show whether Herd captures runtime context and which sites have captured entries.

### herd insights:capture

Show whether Herd captures runtime context, or turn capturing on or off.

```powershell theme={null}
herd insights:capture on
herd insights:capture off
```

## Debugging

### herd debug

Proxy PHP commands with the isolated site's PHP executable and automatically load your `debug.ini`. The `debug.ini` usually includes Xdebug, so this is how to debug artisan commands from your terminal.

### herd coverage

Run PHP commands with Xdebug coverage enabled using the isolated PHP executable.

### herd debug:start

Start a debug session (Herd Pro).

### herd debug:stop

Stop a debug session and display the captured data (Herd Pro). Use `--json` to only print the captured data as JSON.

### herd log

Tail log files from Herd. Without arguments, it displays all available log files. Specify a service to tail its logs.

```powershell theme={null}
herd log
herd log nginx
```

### herd tinker

Start a Tinker session with your Laravel application. If Herd detects [Tinkerwell](https://tinkerwell.app) on your machine, it automatically opens the application in Tinkerwell.

## Sharing

### herd share

Share a local application via an [Expose](https://expose.dev) tunnel.

### herd fetch-share-url

Get the URL to the current Expose share tunnel.

## Configuration

### herd loopback

Get or set the loopback address used for Herd sites.

```powershell theme={null}
herd loopback
herd loopback 127.0.0.1
```

### herd directory-listing

Determine directory-listing behavior. Default is off, which means a 404 will display.

## Core Services

### herd status

Show a health check of your Herd setup: the Herd version, the default PHP and Node.js versions, the mail and dump servers, and the state of every service.

```powershell theme={null}
herd status
herd status --json
```

### herd start

Start all Herd services, or one of `nginx`, `dnsmasq` or `php`.

### herd stop

Stop all Herd services – from nginx to all Herd Pro services.

### herd restart

Restart all Herd services.

## Initialization & Tooling

### herd init

If a `herd.yml` file is present in the directory, Herd configures your application according to the manifest file. Without a `herd.yml`, the command starts the wizard to create one.

### herd init:fresh

Initialize a fresh `herd.yml` manifest file.

### herd laravel:update

Update the Laravel Installer to the latest version.
