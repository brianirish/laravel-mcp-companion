# Forge - Servers/Monitoring

*Source: https://forge.laravel.com/docs/servers/monitoring*

---

- [Laravel Forge home page](https://forge.laravel.com)Search...⌘KAsk AI

- [Dashboard](https://forge.laravel.com)
- [Dashboard](https://forge.laravel.com)

Search...NavigationServersMonitoring[Documentation](/docs/introduction)[Changelog](/docs/changelog/changelog)- [Community](https://discord.com/invite/laravel)
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

Servers# Monitoring

Learn how to configure server monitoring in Forge.

## [​](#overview)Overview

Forge can be configured to monitor the following metrics on your server and email you when their state changes:

- CPU Load Average

- Used Disk Space

- Used Memory

Server monitoring is only available on our “business” plan.

## [​](#monitor-types)Monitor Types

### [​](#cpu-load-average)CPU Load Average

The **CPU Load Average** monitor will track the server’s load average. This is based on the average system load over a one minute interval.

### [​](#used-disk-space)Used Disk Space

The **Used Disk Space** monitor tracks the amount of disk space that has been used on the primary drive.

### [​](#used-memory)Used Memory

The **Used Memory** monitor tracks how much of the RAM is in active use.

## [​](#creating-monitors)Creating Monitors

You may configure a new monitor from the **Monitoring** tab within a server’s management dashboard. Below is a brief overview of how to create and configure a monitoring metric:

- Select the metric to monitor.

- Select whether the value of the metric should be `>=` or `<=` a threshold.

- Enter the threshold percentage that the metric would need to meet before notifying you.

- Enter how long (in minutes) the metric needs to exceed the threshold criteria for before you are notified.

- Enter an email address to notify when the monitor’s state changes.

- Click **Install Monitor**.

Once the monitor is installed, your server will begin collecting metric data and notify you once the state changes.

Forge will only accept one email address to notify. If you need to notify multiple people, you should create a distribution list such as `[[email protected]](/cdn-cgi/l/email-protection)`.

### [​](#stat-collection-frequencies)Stat Collection Frequencies

The CPU Load and Used Memory metric data will be collected every minute. The Disk Space metric will be collected hourly.

## [​](#circle-permissions)Circle Permissions

The ability to manage server monitors is split into two permissions:

- `server:create-monitors`

- `server:delete-monitors`

Was this page helpful?

YesNo[Database Backups](/docs/servers/backups)[Cookbook](/docs/servers/cookbook)On this page
- [Overview](#overview)
- [Monitor Types](#monitor-types)
- [CPU Load Average](#cpu-load-average)
- [Used Disk Space](#used-disk-space)
- [Used Memory](#used-memory)
- [Creating Monitors](#creating-monitors)
- [Stat Collection Frequencies](#stat-collection-frequencies)
- [Circle Permissions](#circle-permissions)

[Laravel Forge home page](https://forge.laravel.com)[x](https://x.com/laravelphp)[github](https://github.com/laravel)[discord](https://discord.com/invite/laravel)[linkedin](https://linkedin.com/company/laravel)[Term of Service](https://forge.laravel.com/terms-of-service)[Privacy Policy](https://forge.laravel.com/privacy-policy)[Data Processing Agreement (DPA)](https://forge.laravel.com/data-processing-agreement)[x](https://x.com/laravelphp)[github](https://github.com/laravel)[discord](https://discord.com/invite/laravel)[linkedin](https://linkedin.com/company/laravel)AssistantResponses are generated using AI and may contain mistakes.