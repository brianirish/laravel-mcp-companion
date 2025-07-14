# Forge - Sites/Queues

*Source: https://forge.laravel.com/docs/sites/queues*

---

- [Laravel Forge home page](https://forge.laravel.com)Search...⌘KAsk AI
[Support](/cdn-cgi/l/email-protection#e88e879a8f8da884899a899e8d84c68b8785)
- [Dashboard](https://forge.laravel.com)
- [Dashboard](https://forge.laravel.com)

Search...NavigationSitesQueues[Documentation](/docs/introduction)[Changelog](/docs/changelog/changelog)- [Community](https://discord.com/invite/laravel)
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

Sites# Queues

Manage Laravel queue workers.

## [​](#overview)Overview

Forge’s site management dashboard allows you to easily create as many Laravel queue workers as you like. Queue workers will automatically be monitored by Supervisor, and will be restarted if they crash. All workers will start automatically if the server is restarted.

## [​](#creating-a-queue-worker)Creating A Queue Worker

You can create a new queue worker within the site’s management dashboard. The “New Worker” form is a wrapper around the Laravel queue feature. You can read more about queues in the [full Laravel queue documentation](https://laravel.com/docs/queues).

When creating a new queue worker, you may [select a version of PHP](/docs/servers/php) that is already installed on the server. The selected version of PHP will be used to execute the queue worker.

## [​](#laravel-horizon)Laravel Horizon

If your Laravel application is using [Laravel Horizon](https://laravel.com/docs/horizon), you should not setup queue workers as described above. Instead, you may enable Horizon on Forge using Forge’s “daemon” feature.

First, create a [server daemon](/docs/resources/daemons#configuring-daemons) that executes the `php artisan horizon` Artisan command from your site’s root directory.

Next, add the `php artisan horizon:terminate` Artisan command to your site’s deployment script, as described in [Horizon’s deployment](https://laravel.com/docs/master/horizon#deploying-horizon) documentation.

Finally, if you wish to use Horizon’s [metrics graphs](https://laravel.com/docs/master/horizon#metrics), you should configure the scheduled job for `horizon:snapshot` in your application code. In addition, you should define a [Scheduler task](/docs/resources/scheduler#scheduled-jobs) within Forge for the `php artisan schedule:run` Artisan command if you have not already done so.

## [​](#restarting-queue-workers-after-deployment)Restarting Queue Workers After Deployment

When deploying your application, it is important that your existing queue workers or Horizon processes reflect the latest changes to your application. This can be achieved by gracefully restarting these services from your deployment script:

When using queue workers:

CopyAsk AI```
$FORGE_PHP artisan queue:restart

```

When using Horizon:

CopyAsk AI```
$FORGE_PHP artisan horizon:terminate

```

## [​](#circle-permissions)Circle Permissions

You may grant a circle member authority to create and manage queue workers by granting the `site:manage-queues` permission.

Was this page helpful?

YesNo[Packages](/docs/sites/packages)[Security Rules](/docs/sites/security-rules)On this page
- [Overview](#overview)
- [Creating A Queue Worker](#creating-a-queue-worker)
- [Laravel Horizon](#laravel-horizon)
- [Restarting Queue Workers After Deployment](#restarting-queue-workers-after-deployment)
- [Circle Permissions](#circle-permissions)

[Laravel Forge home page](https://forge.laravel.com)[x](https://x.com/laravelphp)[github](https://github.com/laravel)[discord](https://discord.com/invite/laravel)[linkedin](https://linkedin.com/company/laravel)[Term of Service](https://forge.laravel.com/terms-of-service)[Privacy Policy](https://forge.laravel.com/privacy-policy)[Data Processing Agreement (DPA)](https://forge.laravel.com/data-processing-agreement)[x](https://x.com/laravelphp)[github](https://github.com/laravel)[discord](https://discord.com/invite/laravel)[linkedin](https://linkedin.com/company/laravel)AssistantResponses are generated using AI and may contain mistakes.