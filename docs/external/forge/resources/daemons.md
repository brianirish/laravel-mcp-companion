# Forge - Resources/Daemons

*Source: https://forge.laravel.com/docs/resources/daemons*

---

- [Laravel Forge home page](https://forge.laravel.com)Search...⌘KAsk AI

- [Dashboard](https://forge.laravel.com)
- [Dashboard](https://forge.laravel.com)

Search...NavigationResourcesDaemons[Documentation](/docs/introduction)[Changelog](/docs/changelog/changelog)- [Community](https://discord.com/invite/laravel)
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

Resources# Daemons

Learn how to configure and manage background processes on your Forge server.

## [​](#overview)Overview

Powered by [Supervisor](http://supervisord.org), daemons are used to keep long-running scripts alive. For instance, you could start a daemon to keep a [ReactPHP](http://reactphp.org/) application running. If the process stops executing, Supervisor will automatically restart the process.

## [​](#configuring-daemons)Configuring Daemons

When creating a new daemon you need to provide Forge with the following information:

**Command:** The command that should be run by the daemon. For example: `php artisan websockets:serve`.

**User:** The operating system user that should be used to invoke the command. By default, the `forge` user will be used.

**Directory:** The directory in which to run your command from. This can be left empty.

**Processes:** This option determines how many instances of the process should be kept running.

**Start Seconds**: The total number of seconds the program must stay running in order to consider the start successful.

**Stop Seconds**: The number of seconds Supervisor will allow for the daemon to gracefully stop before forced termination.

**Stop Signal**: The signal used to kill the program when a stop is requested.

### [​](#manually-restarting-daemons)Manually Restarting Daemons

You may manually restart a daemon using `sudo -S supervisorctl restart daemon-{id}:*`, where `{id}` is the daemon’s ID. For example, if the daemon’s ID is `65654` you may restart it by running `sudo -S supervisorctl restart daemon-65654:*`.

You may also run this command within your application’s deployment script to restart the daemon during a deployment.

## [​](#log-files)Log Files

Forge automatically configures your daemon to write to its own log file. Logs can be found within the `/home/forge/.forge/` directory. Log files are named `daemon-*.log`.

If you are using Forge’s user isolation features, you should navigate to the `.forge` directory within the `/home/{username}` directory based on the user that the process belongs to in order to locate the daemon’s log files.

## [​](#circle-permissions)Circle Permissions

You may grant a circle member authority to create and manage daemons by granting the `server:create-daemons` and `server:delete-daemons` permissions.

Was this page helpful?

YesNo[Cookbook](/docs/sites/cookbook)[Databases](/docs/resources/databases)On this page
- [Overview](#overview)
- [Configuring Daemons](#configuring-daemons)
- [Manually Restarting Daemons](#manually-restarting-daemons)
- [Log Files](#log-files)
- [Circle Permissions](#circle-permissions)

[Laravel Forge home page](https://forge.laravel.com)[x](https://x.com/laravelphp)[github](https://github.com/laravel)[discord](https://discord.com/invite/laravel)[linkedin](https://linkedin.com/company/laravel)[Term of Service](https://forge.laravel.com/terms-of-service)[Privacy Policy](https://forge.laravel.com/privacy-policy)[Data Processing Agreement (DPA)](https://forge.laravel.com/data-processing-agreement)[x](https://x.com/laravelphp)[github](https://github.com/laravel)[discord](https://discord.com/invite/laravel)[linkedin](https://linkedin.com/company/laravel)AssistantResponses are generated using AI and may contain mistakes.