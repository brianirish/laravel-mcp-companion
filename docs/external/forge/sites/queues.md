# Forge - Sites/Queues

*Source: https://forge.laravel.com/docs/sites/queues*

---

## On this page
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
> ## Documentation Index
>
> Fetch the complete documentation index at: <https://forge.laravel.com/docs/llms.txt>
>
> Use this file to discover all available pages before exploring further.
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
```
$FORGE_PHP artisan queue:restart
```
When using Horizon:
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