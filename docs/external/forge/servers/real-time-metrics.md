# Forge - Servers/Real-Time-Metrics

*Source: https://forge.laravel.com/docs/servers/real-time-metrics*

---

- [Community](https://discord.gg/laravel)
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

##### Other

- [Support](/docs/support)
- [Changelog](/docs/changelog)
- [Abuse](/docs/abuse)

On this page

- [Introduction](#introduction)
- [Available metrics](#available-metrics)
- [Viewing metrics](#viewing-metrics)
- [Time scopes](#time-scopes)

Servers

# Real-Time Metrics

Learn how to view real-time server metrics in Laravel Forge.

## [​](#introduction) Introduction

Laravel Forge provides real-time metrics for servers provisioned through supported providers. These interactive charts allow you to monitor your server’s performance and resource utilization over various time periods, helping you identify trends and respond to issues quickly.

Real-time metrics are only available for Laravel VPS, Hetzner, and DigitalOcean server providers.

## [​](#available-metrics) Available metrics

The following real-time metrics are available for your servers:

- **CPU** - displays the percentage of CPU resources being utilized by your server over time.
- **Memory** - displays the percentage of RAM being used by your server.
- **Disk Usage** - displays the percentage of storage space being consumed on your server’s primary drive.
- **Inbound Bandwidth** - displays the network traffic coming into your server, measured in Mbps.
- **Outbound Bandwidth** - displays the network traffic leaving your server, measured in Mbps.

## [​](#viewing-metrics) Viewing metrics

To view real-time metrics for your server, navigate to the server’s “Observe” tab, and then click “Metrics”. The metrics dashboard will display interactive charts for each available metric.

### [​](#time-scopes) Time scopes

You can adjust the time range displayed in the charts to view metrics over different periods:

- **1 hour** - view metrics for the last hour, ideal for monitoring immediate performance changes.
- **6 hours** - review metrics over the last six hours to identify short-term trends.
- **24 hours** - analyze a full day of metrics to understand daily usage patterns.
- **7 days** - examine a week’s worth of data to spot longer-term trends or recurring issues.
- **1 month** - review a month of metrics for capacity planning and historical analysis.

These time scopes allow you to quickly identify performance issues, correlate events across different metrics, and make informed decisions about server scaling and optimization.

Was this page helpful?

YesNo

[Monitoring](/docs/servers/monitoring)[Managing Sites](/docs/sites/the-basics)

⌘I

[x](https://x.com/laravelphp)[github](https://github.com/laravel)[discord](https://discord.com/invite/laravel)[linkedin](https://linkedin.com/company/laravel)