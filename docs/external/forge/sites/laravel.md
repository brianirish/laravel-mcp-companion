# Forge - Sites/Laravel

*Source: https://forge.laravel.com/docs/sites/laravel*

---

[Laravel Forge home page![light logo](https://mintcdn.com/forge-laravel/DhXK7kFkCTo-2V2J/logo/logo.svg?fit=max&auto=format&n=DhXK7kFkCTo-2V2J&q=85&s=a66298a7f876f35c44132183267a2cd6)![dark logo](https://mintcdn.com/forge-laravel/DhXK7kFkCTo-2V2J/logo/logo.svg?fit=max&auto=format&n=DhXK7kFkCTo-2V2J&q=85&s=a66298a7f876f35c44132183267a2cd6)](https://forge.laravel.com)

Search...

⌘KAsk AI

- [Get started](https://forge.laravel.com)
- [Get started](https://forge.laravel.com)

Search...

Navigation

Sites

Laravel

[Documentation](/docs/introduction)[Knowledge Base](/docs/knowledge-base/servers)[API Reference](/docs/api-reference/introduction)

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
- [Requirements](#requirements)
- [Laravel Scheduler](#laravel-scheduler)
- [Maintenance mode](#maintenance-mode)
- [Maintenance mode “secret”](#maintenance-mode-%E2%80%9Csecret%E2%80%9D)
- [Laravel Horizon](#laravel-horizon)
- [Converting existing daemons](#converting-existing-daemons)
- [Laravel Octane](#laravel-octane)
- [Converting existing daemons](#converting-existing-daemons-2)
- [Laravel Reverb](#laravel-reverb)
- [SSL](#ssl)
- [Converting existing daemons](#converting-existing-daemons-3)
- [Inertia server-side rendering (SSR)](#inertia-server-side-rendering-ssr)
- [Converting existing daemons](#converting-existing-daemons-4)

Sites

# Laravel

Copy page

Laravel Forge provides first-class support for Laravel applications.

Copy page

## [​](#introduction) Introduction

Laravel Forge provides first-class support for applications running [Laravel](https://laravel.com), allowing you to quickly toggle and configure:

- Laravel’s Task Scheduler
- Laravel’s Maintenance Mode
- Laravel Horizon
- Laravel Octane
- Laravel Reverb
- Laravel Nightwatch
- Inertia.js Server Side Rendering (SSR)

To accomplish this, Laravel Forge parses the `composer.lock` file from your application and inspects for the presence and version of the packages above.

### [​](#requirements) Requirements

Laravel Forge will only show the application panel for Laravel framework installations of version `5.0` or later. In addition, the panel’s supported packages must meet the following version requirements:

| Dependency | Minimum Version |
| --- | --- |
| `laravel/framework` | `5.0` |
| `laravel/horizon` | `1.0` |
| `laravel/octane` | `1.0` |
| `laravel/pulse` | `1.0` |
| `laravel/reverb` | `*` |
| `inertiajs/inertia-laravel` | `0.6.6` |

## [​](#laravel-scheduler) Laravel Scheduler

You may quickly enable or disable the Laravel scheduler via the “Laravel Scheduler” toggle. Laravel Forge will create the required [Scheduler](/docs/resources/scheduler) for you.

Laravel Forge will automatically configure the scheduler to run every minute using the site’s configured PHP version.

## [​](#maintenance-mode) Maintenance mode

If you have deployed a Laravel application, Laravel Forge allows you to make use of Laravel’s maintenance mode feature. Clicking the “Laravel Maintenance Mode” toggle within the site’s “Application” tab will run the `php artisan down` Artisan command within your application, which will make your site unavailable. When the site is in maintenance mode, you can then toggle it off to make your site available again.

### [​](#maintenance-mode-“secret”) Maintenance mode “secret”

Laravel 8.0+ applications can make use of the “secret” option to bypass maintenance mode. Using this option with older versions of Laravel is not supported.

## [​](#laravel-horizon) Laravel Horizon

You may quickly enable or disable the Laravel Horizon daemon via the “Laravel Horizon” toggle. Laravel Forge will create the required Horizon daemon for you.
If the site’s deploy script does not contain the `horizon:terminate` command, Laravel Forge will automatically append it for you.

### [​](#converting-existing-daemons) Converting existing daemons

If your server is already configured with a daemon that runs Laravel Horizon, Laravel Forge will offer to convert the daemon for you. This process links the site’s ID and the daemon’s ID together, allowing Forge to manage the daemon for you.

## [​](#laravel-octane) Laravel Octane

You may quickly enable or disable the Laravel Octane daemon via the “Laravel Octane” toggle. Laravel Forge will create the required Octane daemon and install Octane dependencies for you.
When enabling the Octane daemon, Laravel Forge will ask you to provide the port number you would like to use for the Octane server as well as your Octane server of choice.
If the site’s deploy script does not contain the `octane:reload` command, Laravel Forge will automatically append it for you.

Before enabling Laravel Octane, you must set the `OCTANE_SERVER` environment variable to the Octane server you choose.

### [​](#converting-existing-daemons-2) Converting existing daemons

If your server is already configured with a daemon that runs Laravel Octane, Laravel Forge will offer to convert the daemon for you. This process links the site’s ID and the daemon’s ID together, allowing Forge to manage the daemon for you.

## [​](#laravel-reverb) Laravel Reverb

Determining the correct server type for hosting Laravel Reverb depends on your configuration requirements. You may use the table below to help inform your decision:

| Configuration | App Server | Web Server |
| --- | --- | --- |
| Reverb server alongside Laravel application | ⊙ |  |
| Dedicated Reverb server |  | ⊙ |
| Dedicated Reverb server with Pulse | ⊙ |  |
| Dedicated Reverb server with Pulse (separate ingest and / or database) |  | ⊙ |

Once your preferred server has been provisioned, you should [add a new site](/docs/sites/the-basics#creating-sites) and [install your Reverb-enabled Laravel application](/docs/sites/the-basics#apps-projects) from your version control provider of choice.
Now, you may quickly enable or disable Laravel Reverb via the “Laravel Reverb” toggle within Laravel Forge’s application panel. When enabling Reverb, Forge will create the Reverb daemon, install the required dependencies, and configure the server for optimum performance.
Additionally, Laravel Forge will prompt for additional information required to setup the server per your requirements.

- **Public Hostname:** Used to update the Nginx configuration of the site, allowing Reverb connections to be accepted by the server on the given hostname. Laravel Forge will default to a subdomain of the site’s current hostname, but you are free to customize this value. For example, if the site’s hostname is `example.com`, Forge will default Reverb’s hostname to `ws.example.com`.
- **Port:** Used to instruct the Reverb daemon which server port it should run on. Laravel Forge will proxy requests for the given public hostname to this port.
- **Maximum Concurrent Connections:** The number of connections your Reverb server can handle will depend on a combination of the resources available on the server and the amount of connections and messages being processed. You should enter the number of connections the server can manage before it should prevent new connections. This option will update the server’s allowed open file limit, Nginx’s allowed open file and connection limit, and install the `ev` event loop if required.

Laravel Forge ensures the hostname provided during Reverb’s installation process is publicly accessible by adding a new server block to your existing site’s Nginx configuration. This server block is contained within a new file and is not available to edit from the Forge UI dashboard.

If the site’s deploy script does not contain the `reverb:restart` command, Laravel Forge will automatically append it for you.

### [​](#ssl) SSL

If an SSL certificate exists for your site which protects Reverb’s configured hostname, Laravel Forge will automatically install it when enabling Reverb, ensuring your Reverb server is accessible via secure WebSockets (`wss`).
If Reverb is installed before a valid certificate is available, you may request a new certificate for Reverb’s configured hostname from your site’s “SSL” tab. Laravel Forge will automatically conf

*[Content truncated for length]*