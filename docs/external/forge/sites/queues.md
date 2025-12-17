# Forge - Sites/Queues

*Source: https://forge.laravel.com/docs/sites/queues*

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
- [Creating a queue worker](#creating-a-queue-worker)
- [Laravel Horizon](#laravel-horizon)
- [Restarting queue workers after deployment](#restarting-queue-workers-after-deployment)
- [Team permissions](#team-permissions)

Sites

# Queues

Copy page

Manage Laravel queue workers.

Copy page

## [​](#introduction) Introduction

Laravel Forge’s site management dashboard allows you to easily create as many Laravel queue workers as you like. Queue workers will automatically be monitored by Supervisor, and will be restarted if they crash. All workers will start automatically if the server is restarted.

## [​](#creating-a-queue-worker) Creating a queue worker

You can create a new queue worker within the site’s management dashboard. The “New Worker” form is a wrapper around the Laravel queue feature. You can read more about queues in the [full Laravel queue documentation](https://laravel.com/docs/queues).
When creating a new queue worker, you may [select a version of PHP](/docs/servers/php) that is already installed on the server. The selected version of PHP will be used to execute the queue worker.

## [​](#laravel-horizon) Laravel Horizon

If your Laravel application is using [Laravel Horizon](https://laravel.com/docs/horizon), you should not setup queue workers as described above. Instead, you may enable Horizon on Laravel Forge using Forge’s “daemon” feature.
First, enable the [Laravel Horizon](/docs/sites/laravel#laravel-horizon) integration. Forge will automatically add `php artisan horizon:terminate` Artisan command to your site’s deployment script, as described in [Horizon’s deployment](https://laravel.com/docs/master/horizon#deploying-horizon) documentation. When using Zero Downtime deployments, the `$RESTART_QUEUES()` macro will handle this automatically.
Finally, if you wish to use Horizon’s [metrics graphs](https://laravel.com/docs/master/horizon#metrics), you should configure the scheduled job for `horizon:snapshot` in your application code. In addition, you should define a [Scheduler task](/docs/resources/scheduler#scheduled-jobs) within Laravel Forge for the `php artisan schedule:run` Artisan command if you have not already done so.

## [​](#restarting-queue-workers-after-deployment) Restarting queue workers after deployment

When deploying your application, it is important that your existing queue workers or Horizon processes reflect the latest changes to your application. This can be achieved by gracefully restarting these services from your deployment script:
When using queue workers:

Copy

Ask AI

```
$FORGE_PHP artisan queue:restart
```

When using Horizon:

Copy

Ask AI

```
$FORGE_PHP artisan horizon:terminate
```

The `queue:restart` command requires a cache driver that persists data between requests. If your application’s cache driver is set to `array`, the command will fail silently because the `array` driver stores data in memory that is lost between requests.

## [​](#team-permissions) Team permissions

You may grant a team member authority to create and manage queue workers by granting the `site:manage-queues` permission.

Was this page helpful?

YesNo

[Commands](/docs/sites/commands)[Network](/docs/sites/network)

⌘I

[x](https://x.com/laravelphp)[github](https://github.com/laravel)[discord](https://discord.com/invite/laravel)[linkedin](https://linkedin.com/company/laravel)