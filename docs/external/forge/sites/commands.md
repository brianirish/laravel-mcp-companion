# Forge - Sites/Commands

*Source: https://forge.laravel.com/docs/sites/commands*

---

- [Laravel Forge home page](https://forge.laravel.com)Search...⌘KAsk AI
[Support](/cdn-cgi/l/email-protection#c7a1a8b5a0a287aba6b5a6b1a2abe9a4a8aa)
- [Dashboard](https://forge.laravel.com)
- [Dashboard](https://forge.laravel.com)

Search...NavigationSitesCommands[Documentation](/docs/introduction)[Changelog](/docs/changelog/changelog)- [Community](https://discord.com/invite/laravel)
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

Sites# Commands

Learn how to run arbitrary commands from the Commands panel.

## [​](#overview)Overview

You may execute arbitrary Bash commands from the Commands panel. Commands are executed from within the site’s root directory, e.g. `/home/forge/site.com`. If you need to run commands within another directory you may prefix the command with a `cd` operation:

CopyAsk AI```
cd bin && ./run-command.sh

```

## [​](#running-commands)Running Commands

Commands can be executed from the Site’s **Commands** panel.

Sites that were created with the **General PHP / Laravel** project type will automatically suggest common Laravel Artisan commands.

Commands are not executed within a tty, which means that input / passwords cannot be provided.

## [​](#command-history)Command History

The last 10 previously executed commands will be shown within the **Command History** table. Alongside the command that was run, Forge will also display:

- The user who initiated the command. This is particularly helpful when using Forge within [Circles](/docs/accounts/circles).

- The command that was executed.

- The date and time of execution.

- The status of the command.

From the Command History table, it’s also possible to view the output of the command and re-run the command.

## [​](#commands-vs-recipes)Commands vs. Recipes

While [Recipes](/docs/servers/recipes.md) also allow you to run arbitrary Bash scripts on your servers, Commands differ in a few, but important ways:

- Recipes run at a server level. In other words, they cannot dynamically change into a site’s directory unless you already know the directory ahead of time.

- Recipes can run using the `root` user. Commands only run as the site’s user, which in most cases will be `forge` unless the site is “isolated”.

- Recipes are better equipped for running larger Bash scripts. Commands focus on running short commands, such as `php artisan config:cache`.

## [​](#circle-permissions)Circle Permissions

You may grant a circle member authority to run arbitrary commands in a site’s directory by granting the `site:manage-commands` permission.

Was this page helpful?

YesNo[Deployments](/docs/sites/deployments)[Packages](/docs/sites/packages)On this page
- [Overview](#overview)
- [Running Commands](#running-commands)
- [Command History](#command-history)
- [Commands vs. Recipes](#commands-vs-recipes)
- [Circle Permissions](#circle-permissions)

[Laravel Forge home page](https://forge.laravel.com)[x](https://x.com/laravelphp)[github](https://github.com/laravel)[discord](https://discord.com/invite/laravel)[linkedin](https://linkedin.com/company/laravel)[Term of Service](https://forge.laravel.com/terms-of-service)[Privacy Policy](https://forge.laravel.com/privacy-policy)[Data Processing Agreement (DPA)](https://forge.laravel.com/data-processing-agreement)[x](https://x.com/laravelphp)[github](https://github.com/laravel)[discord](https://discord.com/invite/laravel)[linkedin](https://linkedin.com/company/laravel)AssistantResponses are generated using AI and may contain mistakes.