# Forge - Sites/Deployments

*Source: https://forge.laravel.com/docs/sites/deployments*

---

[Laravel Forge home page![light logo](https://mintcdn.com/forge-laravel/DhXK7kFkCTo-2V2J/logo/logo.svg?fit=max&auto=format&n=DhXK7kFkCTo-2V2J&q=85&s=a66298a7f876f35c44132183267a2cd6)![dark logo](https://mintcdn.com/forge-laravel/DhXK7kFkCTo-2V2J/logo/logo.svg?fit=max&auto=format&n=DhXK7kFkCTo-2V2J&q=85&s=a66298a7f876f35c44132183267a2cd6)](https://forge.laravel.com)

Search...

⌘KAsk AI

- [Get started](https://forge.laravel.com)
- [Get started](https://forge.laravel.com)

Search...

Navigation

Sites

Deployments

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
- [Deployment strategies](#deployment-strategies)
- [Zero-downtime deployments](#zero-downtime-deployments)
- [Release creation and activation](#release-creation-and-activation)
- [Running tasks during deployments](#running-tasks-during-deployments)
- [Configuring deployment retention](#configuring-deployment-retention)
- [Shared paths](#shared-paths)
- [Laravel Octane](#laravel-octane)
- [Standard deployments](#standard-deployments)
- [Push to deploy](#push-to-deploy)
- [Deploy script](#deploy-script)
- [Environment variables](#environment-variables)
- [Making .env variables available](#making-env-variables-available)
- [PHP versions](#php-versions)
- [Restarting background processes](#restarting-background-processes)
- [Deploying from CI](#deploying-from-ci)
- [Deployment hooks](#deployment-hooks)
- [Refreshing the deployment token](#refreshing-the-deployment-token)
- [Using query parameters](#using-query-parameters)
- [Forge CLI](#forge-cli)
- [GitHub Actions example](#github-actions-example)
- [Deployment branch](#deployment-branch)
- [Deployment health checks](#deployment-health-checks)
- [Health check service IP addresses](#health-check-service-ip-addresses)
- [Deployment notifications](#deployment-notifications)
- [Slack](#slack)
- [Telegram](#telegram)
- [Discord](#discord)
- [Webhooks](#webhooks)

Sites

# Deployments

Copy page

Manage code deployments with scripts, queues, and CI tools

Copy page

## [​](#introduction) Introduction

Laravel Forge makes it easy to deploy your applications on demand, whether that be manually, automatically when pushing new code to your source control provider, or via a webhook from your CI platform of choice.
You can see a list of your site’s deployments by navigating to the “Deployments” tab within your site’s management dashboard. Laravel Forge provides a paginated list of your site’s deployments, including what was deployed, when it was deployed, how long it took to be deployed, and also the output of your deploy script.

Deployments are limited to 10 minutes. If a deployment takes longer, it will fail automatically. If your site is integrated with [Envoyer](/docs/integrations/envoyer), Envoyer’s deployment limits apply instead.

## [​](#deployment-strategies) Deployment strategies

Laravel Forge supports two deployment strategies, letting you choose the one that best fits your workflow.

### [​](#zero-downtime-deployments) Zero-downtime deployments

Zero-downtime deployments use a strategy where your new code is cloned into a special `releases` directory, and then a symbolic link is used to “activate” the new code once deployment is completed.
This strategy greatly reduces the risk of your site going down during deployments, as the new code is only activated once all deployment steps have completed successfully. If any step in the deployment process fails, your site will continue to use the previous release.

Zero-downtime deployments are exclusively available for new sites and must be configured at the time of creation — they cannot be added to existing sites later.Laravel Forge automatically enables zero-downtime deployments for all new sites by default. If you prefer not to use this feature, you can disable it by toggling the “Zero-downtime deployments” option in the “Advanced settings” modal during site creation.

#### [​](#release-creation-and-activation) Release creation and activation

If you create a new site with zero-downtime deployments enabled, Laravel Forge will configure your site’s deployment script to include three special “macros”:

- `$CREATE_RELEASE()` – creates the new release directory and clones your site’s code into it.
- `$ACTIVATE_RELEASE()` – activates the new release by creating a symbolic link from the `current` directory to the new release directory.
- `$RESTART_QUEUES()` - restarts any Laravel queues that are running for the site. Additionally, if your site is using Horizon, it will also restart the Horizon process.

It’s important that these commands are included in your deployment script as they are responsible for handling zero-downtime deployments. Failure to include these commands will result in your site not being deployed correctly.

#### [​](#running-tasks-during-deployments) Running tasks during deployments

Forge adds the `cd $FORGE_RELEASE_DIRECTORY` command after the `$CREATE_RELEASE()` macro in the deployment script to make sure all commands located after this code block will be executed in the context of the new release directory. This means that if you need to run any tasks that depend on your new code, you should place those commands after the `cd $FORGE_RELEASE_DIRECTORY` command.
If you need to run any tasks after a new release has been activated, you should place those commands after the `$ACTIVATE_RELEASE()` macro.

For zero-downtime deployments, it is unnecessary to reload the PHP-FPM service because every deployment is deployed to a new, uncached directory.

#### [​](#configuring-deployment-retention) Configuring deployment retention

By default, Laravel Forge retains the last 4 deployments when using zero-downtime deployments. This allows you to quickly rollback to a previous release if needed.
You can change the number of deployments to retain by navigating to your site’s **Settings** tab and clicking **Deployments**. From there, you can adjust the number of deployments that Forge will keep on your server.

#### [​](#shared-paths) Shared paths

When using zero-downtime deployments, shared paths allow you to specify files or directories that should remain consistent across all releases. These paths are automatically symlinked from a shared storage location into each new release directory, ensuring that important data persists between deployments.
Common use cases for shared paths include:

- **Storage directories** – User uploads, generated files, and other application storage
- **Cache directories** – Application caches that should persist between releases
- **Log files** – Application logs that should be preserved across deployments
- **Environment files** – The `.env` file (automatically shared by default)
- **SQLite databases** – SQLite databases that should persist between releases

For example, if you want to share the `storage` directory, you would add `storage` as a shared path. During each deployment, Laravel Forge will create a symbolic link from `/home/forge/example.com/current/storage` to the shared storage directory at `/home/forge/example.com/storage`.
If your application uses an SQLite database, you should add a shared path from `database.sqlite` to `database/database.sqlite`. This ensures that your database persists between deployments, as Forge will symlink `/home/forge/example.com/current/database/database.sqlite` to `/home/forge/example.com/database.sqlite`.

By default, Laravel Forge automatically configures the `.env` file as a shared path for all sites using zero-downtime deployments.

#### [​](#laravel-octane) Laravel Octane

You should not use zero-downtime deployments when using Laravel Octane, as Octane already handles graceful, zero-downtime restarts internally. Enabling Forge’s zero-downtime feature alongside Octane will interfere with this process and cause deployments to behave incorrectly.

### [​](#standard-deployments) Standard deployments

The standard deployment strategy uses a simpler approach where your sit

*[Content truncated for length]*