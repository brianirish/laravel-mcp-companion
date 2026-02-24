# Forge - Sites/Logs

*Source: https://forge.laravel.com/docs/sites/logs*

---

[Laravel Forge home page](https://forge.laravel.com)
Search...
⌘KAsk AI
- [Get started](https://forge.laravel.com)
- [Get started](https://forge.laravel.com)
Search...
Navigation
Sites
Logs
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
- [Logrotate](#logrotate)
Sites
# Logs
Copy page
Understand and manage logs for your sites in Laravel Forge
Copy page
## [​](#introduction) Introduction
Laravel Forge allows you to view a site’s log files from within the dashboard.
If your site is a Laravel application, Forge will automatically detect and display the log files located in the `storage/logs` directory.
Both `daily` and `single` log formats are supported, and Forge will automatically read the last updated file.
For performance reasons, Laravel Forge will only return the last 500 lines from a file.
## [​](#logrotate) Logrotate
When provisioning your server, Laravel Forge automatically installs and configures Logrotate on the server to ensure log files don’t grow indefinitely and consume excessive disk space.
The configuration files for Logrotate can be found in `/etc/logrotate.d/`. The primary configuration file is located at `/etc/logrotate.conf`.
To view older “rotate” or “compressed” logs, you can use `cat` for non-compressed files or `zcat` for compressed files.
Was this page helpful?
YesNo
[Laravel](/docs/sites/laravel)[Databases](/docs/resources/databases)
⌘I
Assistant
Responses are generated using AI and may contain mistakes.