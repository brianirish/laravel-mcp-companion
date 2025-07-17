# Forge - Cli

*Source: https://forge.laravel.com/docs/cli*

---

[Laravel Forge home page![light logo](https://mintlify.s3.us-west-1.amazonaws.com/forge-laravel/logo/logo.svg)![dark logo](https://mintlify.s3.us-west-1.amazonaws.com/forge-laravel/logo/logo.svg)](https://forge.laravel.com)

Search...

⌘KAsk AI

- Support
- [Dashboard](https://forge.laravel.com)
- [Dashboard](https://forge.laravel.com)

Search...

Navigation

Get Started

Forge CLI

[Documentation](/docs/introduction)[Changelog](/docs/changelog/changelog)

- [Community](https://discord.com/invite/laravel)
- [Blog](https://blog.laravel.com/forge)

##### Get Started

- [Introduction](/docs/introduction)
- [Forge CLI](/docs/cli)
- [Forge SDK](/docs/sdk)

##### Accounts

- [Your Account](/docs/accounts/your-account)
- [Circles](/docs/accounts/circles)
- [Source Control](/docs/accounts/source-control)
- [SSH Keys](/docs/accounts/ssh)
- [API](/docs/accounts/api)
- [Tags](/docs/accounts/tags)
- [Troubleshooting](/docs/accounts/cookbook)

##### Servers

- [Server Providers](/docs/servers/providers)
- [Server Types](/docs/servers/types)
- [Management](/docs/servers/management)
- [Root Access / Security](/docs/servers/provisioning-process)
- [SSH Keys / Git Access](/docs/servers/ssh)
- [PHP](/docs/servers/php)
- [Packages](/docs/servers/packages)
- [Recipes](/docs/servers/recipes)
- [Load Balancing](/docs/servers/load-balancing)
- [Nginx Templates](/docs/servers/nginx-templates)
- [Database Backups](/docs/servers/backups)
- [Monitoring](/docs/servers/monitoring)
- [Cookbook](/docs/servers/cookbook)

##### Sites

- [The Basics](/docs/sites/the-basics)
- [Applications](/docs/sites/applications)
- [Deployments](/docs/sites/deployments)
- [Commands](/docs/sites/commands)
- [Packages](/docs/sites/packages)
- [Queues](/docs/sites/queues)
- [Security Rules](/docs/sites/security-rules)
- [Redirects](/docs/sites/redirects)
- [SSL](/docs/sites/ssl)
- [User Isolation](/docs/sites/user-isolation)
- [Cookbook](/docs/sites/cookbook)

##### Resources

- [Daemons](/docs/resources/daemons)
- [Databases](/docs/resources/databases)
- [Caches](/docs/resources/caches)
- [Network](/docs/resources/network)
- [Scheduler](/docs/resources/scheduler)
- [Integrations](/docs/resources/integrations)
- [Cookbook](/docs/resources/cookbook)

##### Integrations

- [Envoyer](/docs/integrations/envoyer)
- [Sentry](/docs/integrations/sentry)
- [Aikido](/docs/integrations/aikido)

##### Other

- [Abuse](/docs/abuse)

Get Started

# Forge CLI

Forge CLI is a command-line tool that you may use to manage your Forge resources from the command-line.

[## Forge CLI

View the Forge CLI on GitHub](https://github.com/laravel/forge-cli)[## Forge API

View the Forge API Documentation](https://forge.laravel.com/api-documentation)

## [​](#overview) Overview

Forge provides a command-line tool that you may use to manage your Forge servers, sites, and resources from the command-line.

## [​](#installation) Installation

> **Requires [PHP 8.0+](https://php.net/releases/)**

You may install the **[Forge CLI](https://github.com/laravel/forge-cli)** as a global [Composer](https://getcomposer.org) dependency:

Copy

Ask AI

```
composer global require laravel/forge-cli

```

## [​](#get-started) Get Started

To view a list of all available Forge CLI commands and view the current version of your installation, you may run the `forge` command from the command-line:

Copy

Ask AI

```
forge

```

## [​](#authenticating) Authenticating

You will need to generate an API token to interact with the Forge CLI. Tokens are used to authenticate your account without providing personal details. API tokens can be created from [Forge’s API dashboard](https://forge.laravel.com/user-profile/api).

After you have generated an API token, you should authenticate with your Forge account using the login command:

Copy

Ask AI

```
forge login
forge login --token=your-api-token

```

Alternatively, if you plan to authenticate with Forge from your CI platform, you may set a `FORGE_API_TOKEN` environment variable in your CI build environment.

## [​](#current-server-%26-switching-servers) Current Server & Switching Servers

When managing Forge servers, sites, and resources via the CLI, you will need to be aware of your currently active server. You may view your current server using the `server:current` command. Typically, most of the commands you execute using the Forge CLI will be executed against the active server.

Copy

Ask AI

```
forge server:current

```

Of course, you may switch your active server at any time. To change your active server, use the `server:switch` command:

Copy

Ask AI

```
forge server:switch
forge server:switch staging

```

To view a list of all available servers, you may use the `server:list` command:

Copy

Ask AI

```
forge server:list

```

## [​](#ssh-key-authentication) SSH Key Authentication

Before performing any tasks using the Forge CLI, you should ensure that you have added an SSH key for the `forge` user to your servers so that you can securely connect to them. You may have already done this via the Forge UI. You may test that SSH is configured correctly by running the `ssh:test` command:

Copy

Ask AI

```
forge ssh:test

```

To configure SSH key authentication, you may use the `ssh:configure` command. The `ssh:configure` command accepts a `--key` option which instructs the CLI which public key to add to the server. In addition, you may provide a `--name` option to specify the name that should be assigned to the key:

Copy

Ask AI

```
forge ssh:configure

forge ssh:configure --key=/path/to/public/key.pub --name=sallys-macbook

```

After you have configured SSH key authentication, you may use the `ssh` command to create a secure connection to your server:

Copy

Ask AI

```
forge ssh

forge ssh server-name

```

## [​](#sites) Sites

To view the list of all available sites, you may use the `site:list` command:

Copy

Ask AI

```
forge site:list

```

### [​](#initiating-deployments) Initiating Deployments

One of the primary features of Laravel Forge is deployments. Deployments may be initiated via the Forge CLI using the `deploy` command:

Copy

Ask AI

```
forge deploy

forge deploy example.com

```

### [​](#updating-environment-variables) Updating Environment Variables

You may update a site’s environment variables using the `env:pull` and `env:push` commands. The `env:pull` command may be used to pull down an environment file for a given site:

Copy

Ask AI

```
forge env:pull
forge env:pull pestphp.com
forge env:pull pestphp.com .env

```

Once this command has been executed the site’s environment file will be placed in your current directory. To update the site’s environment variables, simply open and edit this file. When you are done editing the variables, use the `env:push` command to push the variables back to your site:

Copy

Ask AI

```
forge env:push
forge env:push pestphp.com
forge env:push pestphp.com .env

```

If your site is utilizing Laravel’s “configuration caching” feature or has queue workers, the new variables will not be utilized until the site is deployed again.

### [​](#viewing-application-logs) Viewing Application Logs

You may also view a site’s logs directly from the command-line. To do so, use the `site:logs` command:

Copy

Ask AI

```
forge site:logs
forge site:logs --follow              # View logs in realtime

forge site:logs example.com
forge site:logs example.com --follow  # View logs in realtime

```

### [​](#reviewing-deployment-output-%2F-logs) Reviewing Deployment Output / Logs

When a deployment fails, you may review the output / logs via the Forge UI’s deployment history screen. You may also review the output at any time on the command-line using the `deploy:logs` command. If the `deploy:logs` command is called with no additional arguments, the logs for the latest deployment will be displayed. Or, you may pass the deployment ID to the `deploy:logs` command to display the logs for a particular deployment:

Copy

Ask AI

```
forge deploy:logs

forge deploy:logs 12345

```

### [​](#running-commands) Running Commands

Sometimes you may wish to run an arbitrary shell command against a site. The `command` command will prompt you for the command you would like to run. The command will be run relative to the site’s root directory.

Copy

Ask AI

```
forge command

forge command example.com

forge command example.com --command="php artisan inspire"

```

### [​](#tinker) Tinker

As you may know, all Laravel applications include “Tinker” by default. To enter a Tinker environment on a remote server using the Forge CLI, run the `tinker` command:

Copy

Ask AI

```
forge tinker

forge tinker example.com

```

## [​](#resources) Resources

Forge provisions servers with a variety of resources and additional software, such as Nginx, MySQL, etc. You may use the Forge CLI to perform common actions on those resources.

### [​](#checking-resource-status) Checking Resource Status

To check the current status of a resource, you may use the `{resource}:status` command:

Copy

Ask AI

```
forge daemon:status
forge database:status

forge nginx:status

forge php:status      # View PHP status (default PHP version)
forge php:status 8.4  # View PHP 8.4 status

```

### [​](#viewing-resources-logs) Viewing Resources Logs

You may also view logs directly from the command-line. To do so, use the `{resource}:logs` command:

Copy

Ask AI

```
forge daemon:logs
forge daemon:logs --follow  # View logs in realtime

forge database:logs

forge nginx:logs         # View error logs
forge nginx:logs access  # View access logs

forge php:logs           # View PHP logs (default PHP version)
forge php:logs 8.4       # View PHP 8.4 logs

```

### [​](#restarting-resources) Restarting Resources

Resources may be restarted using the `{resource}:restart` command:

Copy

Ask AI

```
forge daemon:restart

forge database:restart

forge nginx:restart

forge php:restart      # Restarts PHP (default PHP version)
forge php:restart 8.4  # Restarts PHP 8.4

```

### [​

*[Content truncated for length]*