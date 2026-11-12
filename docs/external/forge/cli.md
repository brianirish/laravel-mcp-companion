Source: https://laravel.com/forge/docs/cli.md

# Laravel Forge CLI

> Laravel Forge CLI is a command-line tool that you may use to manage your Forge resources from the command-line.

> [card] [Laravel Forge CLI](https://github.com/laravel/forge-cli)
>
> View the Laravel Forge CLI on GitHub

> [card] [Laravel Forge API](https://forge.laravel.com/api-documentation)
>
> View the Laravel Forge API documentation

## Introduction

Laravel Forge provides a command-line tool that you may use to manage your Forge servers, sites, and resources from the command-line.

## Installation

> **Requires [PHP 8.2+](https://php.net/releases/)**

You may install the **[Laravel Forge CLI](https://github.com/laravel/forge-cli)** as a global [Composer](https://getcomposer.org) dependency:

```bash theme={null}
composer global require laravel/forge-cli
```

## Get started

To view a list of all available Laravel Forge CLI commands and view the current version of your installation, you may run the `forge` command from the command-line:

```bash theme={null}
forge
```

## Authenticating

You will need to generate an API token to interact with the Laravel Forge CLI. Tokens are used to authenticate your account without providing personal details. API tokens can be created from [Forge's API dashboard](https://forge.laravel.com/profile/api).

After you have generated an API token, you should authenticate with your Laravel Forge account using the login command:

```bash theme={null}
forge login
forge login --token="your-api-token"
```

To remove your stored credentials and log out, use the `logout` command:

```bash theme={null}
forge logout
```

Alternatively, if you plan to authenticate with Laravel Forge from your CI platform, you may set a `FORGE_API_TOKEN` environment variable in your CI build environment.

## Current organization & switching organizations

Laravel Forge groups your servers and resources within organizations. CLI commands run against your currently active organization, so you should ensure the correct organization is selected before managing servers or sites.

When you log in, if your account belongs to a single organization it is selected automatically. Otherwise, you should select one using the `organization:switch` command.

You may view your current organization using the `organization:current` command:

```bash theme={null}
forge organization:current  # org:current is available as a shorter alias
```

To view a list of all organizations your account belongs to, use the `organization:list` command:

```bash theme={null}
forge organization:list  # org:list is available as a shorter alias
```

To change your active organization, use the `organization:switch` command:

```bash theme={null}
forge organization:switch        # org:switch is available as a shorter alias
forge organization:switch acme
```

Switching organizations resets your active server, since each server belongs to a specific organization. After switching, select a server using the `server:switch` command.

## Current server & switching servers

When managing Laravel Forge servers, sites, and resources via the CLI, you will need to be aware of your currently active server. You may view your current server using the `server:current` command. Typically, most of the commands you execute using the Forge CLI will be executed against the active server.

```bash theme={null}
forge server:current
```

Of course, you may switch your active server at any time. To change your active server, use the `server:switch` command:

```bash theme={null}
forge server:switch
forge server:switch staging
```

To view a list of all available servers, you may use the `server:list` command:

```bash theme={null}
forge server:list
```

## SSH key authentication

Before performing any tasks using the Laravel Forge CLI, you should ensure that you have added an SSH key for the `forge` user to your servers so that you can securely connect to them. You may have already done this via the Forge UI. You may test that SSH is configured correctly by running the `ssh:test` command:

```bash theme={null}
forge ssh:test
```

To configure SSH key authentication, you may use the `ssh:configure` command. The `ssh:configure` command accepts a `--key` option which instructs the CLI which public key to add to the server. In addition, you may provide a `--name` option to specify the name that should be assigned to the key:

```bash theme={null}
forge ssh:configure

forge ssh:configure --key=/path/to/public/key.pub --name=sallys-macbook
```

After you have configured SSH key authentication, you may use the `ssh` command to create a secure connection to your server:

```bash theme={null}
forge ssh

forge ssh server-name
```

## Sites

To view the list of all available sites, you may use the `site:list` command:

```bash theme={null}
forge site:list
```

### Initiating deployments

One of the primary features of Laravel Forge is deployments. Deployments may be initiated via the Forge CLI using the `deploy` command:

```bash theme={null}
forge deploy

forge deploy example.com
```

### Updating environment variables

You may update a site's environment variables using the `env:pull` and `env:push` commands. The `env:pull` command may be used to pull down an environment file for a given site:

```bash theme={null}
forge env:pull
forge env:pull pestphp.com
forge env:pull pestphp.com .env
```

Once this command has been executed, the site's environment file will be placed in your current directory. To update the site's environment variables, open and edit this file. When you are done editing the variables, use the `env:push` command to push the variables back to your site:

```bash theme={null}
forge env:push
forge env:push pestphp.com
forge env:push pestphp.com .env
```

If your site is utilizing Laravel's "configuration caching" feature or has queue workers, the new variables will not be used until the site is deployed again.

### Viewing application logs

You may also view a site's logs directly from the command-line. To do so, use the `site:logs` command:

```bash theme={null}
forge site:logs
forge site:logs --follow              # View logs in realtime

forge site:logs example.com
forge site:logs example.com --follow  # View logs in realtime
```

### Reviewing deployment output / logs

When a deployment fails, you may review the output / logs via the Laravel Forge UI's deployment history screen. You may also review the output at any time on the command-line using the `deploy:logs` command, which displays the logs for the site's latest deployment:

```bash theme={null}
forge deploy:logs

forge deploy:logs example.com
```

### Running commands

Sometimes you may wish to run an arbitrary shell command against a site. The `command` command will prompt you for the command you would like to run. The command will be run relative to the site's root directory.

```bash theme={null}
forge command

forge command example.com

forge command example.com --command="php artisan inspire"
```

### Tinker

As you may know, all Laravel applications include "Tinker" by default. To enter a Tinker environment on a remote server using the Laravel Forge CLI, run the `tinker` command:

```bash theme={null}
forge tinker

forge tinker example.com
```

### Opening a site in the dashboard

To quickly open a site within the Forge dashboard in your browser, use the `open` command:

```bash theme={null}
forge open

forge open example.com
```

## Resources

Laravel Forge provisions servers with a variety of resources and additional software, such as Nginx, MySQL, etc. You may use the Forge CLI to perform common actions on those resources.

### Checking resource status

To check the current status of a resource, you may use the `{resource}:status` command:

```bash theme={null}
forge background-process:status  # daemon:status is available as a legacy alias
forge database:status

forge nginx:status

forge php:status      # View PHP status (default PHP version)
forge php:status 8.5  # View PHP 8.5 status
```

### Viewing resources logs

You may also view logs directly from the command-line. To do so, use the `{resource}:logs` command:

```bash theme={null}
forge background-process:logs           # daemon:logs is available as a legacy alias
forge background-process:logs --follow  # View logs in realtime

forge database:logs

forge nginx:logs         # View error logs
forge nginx:logs access  # View access logs

forge php:logs           # View PHP logs (default PHP version)
forge php:logs 8.5       # View PHP 8.5 logs
```

### Restarting resources

Resources may be restarted using the `{resource}:restart` command:

```bash theme={null}
forge background-process:restart  # daemon:restart is available as a legacy alias

forge database:restart

forge nginx:restart

forge php:restart      # Restarts PHP (default PHP version)
forge php:restart 8.5  # Restarts PHP 8.5
```

### Connecting to resources locally

You may use the `{resource}:shell` command to quickly access a command line shell that lets you interact with a given resource:

```bash theme={null}
forge database:shell
forge database:shell my-database-name
forge database:shell my-database-name --user=my-user
```
