# Forge - Servers/Monitoring

*Source: https://forge.laravel.com/docs/servers/monitoring*

---

[Laravel Forge home page](https://forge.laravel.com)
Search...
⌘KAsk AI
- [Get started](https://forge.laravel.com)
- [Get started](https://forge.laravel.com)
Search...
Navigation
Servers
Monitoring
[Documentation](/docs/introduction)[Knowledge Base](/docs/knowledge-base/servers)[API Reference](/docs/api-reference/introduction)
- [Blog](https://blog.laravel.com)
- [Status](https://status.on-forge.com)
##### Get Started
- [Introduction](/docs/introduction)
- [Laravel Forge CLI](/docs/cli)
- [Laravel Forge SDK](/docs/sdk)
##### Basics
- [Organizations](/docs/organizations)
- [Teams](/docs/teams)
- [Server Providers](/docs/server-providers)
- [Storage Providers](/docs/storage-providers)
- [Source Control](/docs/source-control)
- [SSH Keys](/docs/ssh)
- [Recipes](/docs/recipes)
- [API](/docs/api)
##### Servers
- [Managing Servers](/docs/servers/the-basics)
- [Server Types](/docs/servers/types)
- [Laravel VPS](/docs/servers/laravel-vps)
- [PHP](/docs/servers/php)
- [Load Balancing](/docs/servers/load-balancing)
- [Nginx Templates](/docs/servers/nginx-templates)
- [Security](/docs/servers/security)
- [Monitoring](/docs/servers/monitoring)
- [Real-Time Metrics](/docs/servers/real-time-metrics)
##### Sites
- [Managing Sites](/docs/sites/the-basics)
- [Domains](/docs/sites/domains)
- [Deployments](/docs/sites/deployments)
- [Environment Variables](/docs/sites/environment-variables)
- [Commands](/docs/sites/commands)
- [Queues](/docs/sites/queues)
- [Network](/docs/sites/network)
- [Isolation](/docs/sites/user-isolation)
- [Laravel](/docs/sites/laravel)
- [Logs](/docs/sites/logs)
##### Resources
- [Databases](/docs/resources/databases)
- [Database Backups](/docs/resources/database-backups)
- [Caches](/docs/resources/caches)
- [Background Processes](/docs/resources/background-processes)
- [Scheduler](/docs/resources/scheduler)
- [Network](/docs/resources/network)
- [Packages](/docs/resources/packages)
##### Integrations
- [Envoyer](/docs/integrations/envoyer)
- [Sentry](/docs/integrations/sentry)
- [Aikido](/docs/integrations/aikido)
- [OpenClaw](/docs/integrations/openclaw)
##### Other
- [Support](/docs/support)
- [Changelog](/docs/changelog)
- [Abuse](/docs/abuse)
On this page
- [Introduction](#introduction)
- [Managing server monitors](#managing-server-monitors)
- [Creating monitors](#creating-monitors)
- [Deleting monitors](#deleting-monitors)
- [Stat collection frequencies](#stat-collection-frequencies)
Servers
# Monitoring
Copy page
Learn how to configure server monitoring in Laravel Forge.
Copy page
## [​](#introduction) Introduction
Laravel Forge can be configured to monitor the following metrics on your server and email you when their state changes:
- **CPU Load Average** - tracks the server’s load average. This is based on the average system load over a one-minute interval.
- **Used Disk Space** - tracks the amount of disk space that has been used on the primary drive.
- **Used Memory** - tracks how much of the RAM is in active use.
Server monitoring is only available on the Business plan.
## [​](#managing-server-monitors) Managing server monitors
### [​](#creating-monitors) Creating monitors
To create a server monitor, navigate to the server’s dashboard, click the “Observe” tab, and click the “Add monitor” button. Select the metric type, configure the thresholds and provide an email address to notify. Once done, click “Create server monitor”.
Laravel Forge will only accept one email address to notify. If you need to notify multiple people, you should create a distribution list such as `[email protected]`.
### [​](#deleting-monitors) Deleting monitors
To delete a server monitor, navigate to the server’s dashboard and click the “Observe” tab. Locate the server monitor you wish to delete, click the action dropdown next to the server monitor, and select “Delete”.
## [​](#stat-collection-frequencies) Stat collection frequencies
The CPU Load and Used Memory metric data will be collected every minute. The Disk Space metric will be collected hourly.
Was this page helpful?
YesNo
[Security](/docs/servers/security)[Real-Time Metrics](/docs/servers/real-time-metrics)
⌘I
Assistant
Responses are generated using AI and may contain mistakes.