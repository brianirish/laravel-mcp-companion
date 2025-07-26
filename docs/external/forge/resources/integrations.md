# Forge - Resources/Integrations

*Source: https://forge.laravel.com/docs/resources/integrations*

---

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

On this page

- [Overview](#overview)
- [Monitoring Integrations](#monitoring-integrations)
- [Blackfire.io](#blackfire-io)
- [Papertrail](#papertrail)
- [Circle Permissions](#circle-permissions)

Resources

# Integrations

Learn how to configure and manage third-party integrations on your Forge server.

## [​](#overview) Overview

Forge provides a few third-party integrations that you can install on your server to provide additional features to your server. We’ll discuss each of these below.

## [​](#monitoring-integrations) Monitoring Integrations

### [​](#blackfire-io) Blackfire.io

[Blackfire](https://blackfire.io/) provides thorough PHP application profiling and is our recommended solution for monitoring your PHP application’s performance. After providing your server ID and token, Blackfire will be installed and configured for your server.

### [​](#papertrail) Papertrail

[Papertrail](https://papertrailapp.com/) provides hosted log monitoring and searching for your PHP application. If you are using Laravel, just configure your application to use the `syslog` driver.

## [​](#circle-permissions) Circle Permissions

You may grant a circle member authority to configure and manage integrations by granting the `server:manage-php` permission.

Was this page helpful?

YesNo

[Scheduler](/docs/resources/scheduler)[Cookbook](/docs/resources/cookbook)

Assistant

Responses are generated using AI and may contain mistakes.