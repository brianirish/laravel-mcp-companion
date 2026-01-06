# Forge - Sites/Environment-Variables

*Source: https://forge.laravel.com/docs/sites/environment-variables*

---

[Laravel Forge home page![light logo](https://mintcdn.com/forge-laravel/DhXK7kFkCTo-2V2J/logo/logo.svg?fit=max&auto=format&n=DhXK7kFkCTo-2V2J&q=85&s=a66298a7f876f35c44132183267a2cd6)![dark logo](https://mintcdn.com/forge-laravel/DhXK7kFkCTo-2V2J/logo/logo.svg?fit=max&auto=format&n=DhXK7kFkCTo-2V2J&q=85&s=a66298a7f876f35c44132183267a2cd6)](https://forge.laravel.com)

Search...

⌘KAsk AI

- [Get started](https://forge.laravel.com)
- [Get started](https://forge.laravel.com)

Search...

Navigation

Sites

Environment Variables

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
- [Modifying environment variables](#modifying-environment-variables)
- [Encrypted environment files](#encrypted-environment-files)
- [Laravel integrations](#laravel-integrations)

Sites

# Environment Variables

Copy page

Learn how to manage environment variables for your sites.

Copy page

## [​](#introduction) Introduction

Laravel Forge makes it easy to manage environment variables for your sites.
If your project contains a `.env` file, you can easily create and edit environment variables from the “Environment” tab of your site’s settings.

If Laravel Forge detects a `.env.example` file in your project, it will automatically copy this and replace some of the settings to match your server’s database settings during site creation.An empty `.env.example` file could result in an empty environment file on the first deployment of your site.

## [​](#modifying-environment-variables) Modifying environment variables

To modify your site’s environment variables, navigate to your site’s “Settings” panel and click on the “Environment” sidebar item.
When you modify environment variables through Forge, the changes are written directly to the `.env` file within your application. If you’re using [zero-downtime deployments](/docs/sites/deployments#zero-downtime-deployments), this file will be symlinked into the current release directory, ensuring your environment configuration is consistent across deployments.
After modifying your environment variables, you can optionally choose to automatically run:

- **php artisan config:cache** - Caches your configuration files for improved performance.
- **php artisan queue:restart** - Gracefully restarts your queue workers to pick up the new environment values.

These options help ensure your application immediately reflects the updated environment configuration without requiring manual intervention.

## [​](#encrypted-environment-files) Encrypted environment files

Laravel Forge provides support for Laravel’s [encrypted environment files](https://laravel.com/docs/configuration#encrypting-environment-files) without requiring you to include your encryption key within your deployment script.
To leverage this feature, add your encryption key to the “Encrypted environment files” section of your site’s “Environment” tab.
Once added, Laravel Forge will inject the value into the `LARAVEL_ENV_ENCRYPTION_KEY` environment variable during deployments, allowing you to add the `env:decrypt` Artisan command to your deployment script without needing to specify the `--key` option manually.

Copy

Ask AI

```
php artisan env:decrypt --force
```

## [​](#laravel-integrations) Laravel integrations

The following Laravel-specific features are only available to sites using the Laravel or Statamic project type:

- **php artisan config:cache** - Automatically cache configuration files after updating environment variables.
- **php artisan queue:restart** - Automatically restart queue workers after updating environment variables.
- **Encrypted environment files** - Support for Laravel’s encrypted environment files feature.

If your site is using a different project type, these features will not be available.

Was this page helpful?

YesNo

[Deployments](/docs/sites/deployments)[Commands](/docs/sites/commands)

⌘I

[x](https://x.com/laravelphp)[github](https://github.com/laravel)[discord](https://discord.com/invite/laravel)[linkedin](https://linkedin.com/company/laravel)