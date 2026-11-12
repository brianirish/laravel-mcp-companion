Source: https://laravel.com/forge/docs/sites/queues.md

# Queues

> Manage Laravel queue workers.

## Introduction

Laravel Forge's site management dashboard allows you to easily create as many Laravel queue workers as you like. Queue workers will automatically be monitored by Supervisor, and will be restarted if they crash. All workers will start automatically if the server is restarted.

## Creating a queue worker

You can create a new queue worker within the site's management dashboard. The "New Worker" form is a wrapper around the Laravel queue feature. You can read more about queues in the [full Laravel queue documentation](https://laravel.com/docs/queues).

When creating a new queue worker, you may [select a version of PHP](https://forge.laravel.com/docs/servers/php.md) that is already installed on the server. The selected version of PHP will be used to execute the queue worker.

## Laravel Horizon

If your Laravel application is using [Laravel Horizon](https://laravel.com/docs/horizon), you should not setup queue workers as described above. Instead, you may enable Horizon on Laravel Forge using Forge's "daemon" feature.

First, enable the [Laravel Horizon](https://forge.laravel.com/docs/sites/laravel.md#laravel-horizon) integration. Forge will automatically add `php artisan horizon:terminate` Artisan command to your site's deployment script, as described in [Horizon's deployment](https://laravel.com/docs/master/horizon#deploying-horizon) documentation. When using Zero Downtime deployments, the `$RESTART_QUEUES()` macro will handle this automatically.

Finally, if you wish to use Horizon's [metrics graphs](https://laravel.com/docs/master/horizon#metrics), you should configure the scheduled job for `horizon:snapshot` in your application code. In addition, you should define a [Scheduler task](https://forge.laravel.com/docs/resources/scheduler.md#scheduled-jobs) within Laravel Forge for the `php artisan schedule:run` Artisan command if you have not already done so.

## Restarting queue workers after deployment

When deploying your application, it is important that your existing queue workers or Horizon processes reflect the latest changes to your application. This can be achieved by gracefully restarting these services from your deployment script:

When using queue workers:

```bash theme={null}
$FORGE_PHP artisan queue:restart
```

When using Horizon:

```bash theme={null}
$FORGE_PHP artisan horizon:terminate
```

> [!WARNING]
>
> The `queue:restart` command requires a cache driver that persists data between requests. If your application's cache driver is set to `array`, the command will fail silently because the `array` driver stores data in memory that is lost between requests.

## Team permissions

You may grant a team member authority to create and manage queue workers by granting the `site:manage-queues` permission.
