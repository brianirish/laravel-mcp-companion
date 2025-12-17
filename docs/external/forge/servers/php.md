# Forge - Servers/Php

*Source: https://forge.laravel.com/docs/servers/php*

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
- [Managing PHP versions](#managing-php-versions)
- [Installing PHP versions](#installing-php-versions)
- [Uninstalling PHP versions](#uninstalling-php-versions)
- [PHP on the CLI](#php-on-the-cli)
- [Default PHP installation](#default-php-installation)
- [Patching PHP versions](#patching-php-versions)
- [Common PHP configuration settings](#common-php-configuration-settings)
- [Max file upload size](#max-file-upload-size)
- [Max execution time](#max-execution-time)
- [OPcache](#opcache)
- [Editing PHP and FPM configuration settings](#editing-php-and-fpm-configuration-settings)
- [Beta and release candidates](#beta-and-release-candidates)

Servers

# PHP

Copy page

Learn how to manage PHP versions on your Laravel Forge server.

Copy page

## [​](#introduction) Introduction

Laravel Forge makes it easy to install and configure multiple versions of PHP on your server. Each installed PHP version runs its own FPM process. In addition, you may [update the PHP version used by specific sites at any time](/docs/sites/the-basics#php-version).

Laravel Forge is only aware of PHP installations that are managed through the Forge dashboard and not manually installed on the server.

## [​](#managing-php-versions) Managing PHP versions

When provisioning a server, you must decide which version of PHP you want to install by default. The `php` binary on your server will point to the installed version selected at the time of its creation.
Once the server has been created, Laravel Forge makes it easy to install additional versions alongside the default version.

### [​](#installing-php-versions) Installing PHP versions

To install a PHP version, navigate to the server’s dashboard and click the PHP tab. Then, click the Install version button, select the version to install and decide whether you want it to become the CLI default. Click Install to begin the installation process.
When you install a new version of PHP onto your server, Laravel Forge will create and configure the PHP-FPM process for that version. This means that your server will be running multiple versions of PHP at once.

### [​](#uninstalling-php-versions) Uninstalling PHP versions

To uninstall a PHP version, navigate to the server’s dashboard and click the PHP tab. Locate the version of PHP you want to remove, open the dropdown menu and click Uninstall PHP X.X and confirm the removal.
PHP versions may be removed so long as:

- There are other versions installed
- The version you wish to uninstall is not the server’s default version for new sites
- The version you wish to uninstall is not the server’s default version on the CLI
- The version you wish to uninstall is not used by any sites

### [​](#php-on-the-cli) PHP on the CLI

When an additional version of PHP has been installed, you may reference it on the CLI via `phpx.x`, replacing the `x.x` with the version number (e.g., `php8.5`). The `php` binary will always point to the active CLI version (if changed from the default).

### [​](#default-php-installation) Default PHP installation

The “default” PHP version is the version of PHP that will be used by default when creating a new site on the server.
When selecting a new version of PHP as your server’s “default” version, the PHP versions used by existing sites **will not be updated**.

### [​](#patching-php-versions) Patching PHP versions

To patch a PHP version, navigate to the server’s dashboard and click the PHP tab. Identify the version of PHP you want to patch, open the dropdown menu and click Update.

Typically, patch updates should not cause any breaking changes to your server, although a few seconds of downtime is possible. We recommend that you exercise caution when patching PHP.

## [​](#common-php-configuration-settings) Common PHP configuration settings

Changing the following settings will apply the changes to all versions of PHP installed on the server.

### [​](#max-file-upload-size) Max file upload size

You may configure the maximum file upload size through the PHP tab of the server management dashboard. This value should be provided in megabytes. For reference, `1024MB` is `1GB`.

### [​](#max-execution-time) Max execution time

You may configure the maximum execution time through the PHP tab of the server management dashboard. This value should be provided in seconds.

### [​](#opcache) OPcache

Optimizing the PHP OPcache for production will configure OPcache to store your compiled PHP code in memory to greatly improve performance. If you choose to optimize OPcache for production, you should verify that your deployment script [reloads the PHP-FPM service](/docs/knowledge-base/servers#restarting-php-fpm) at the end of each deployment unless you’re using zero-downtime deployments.

OPcache is enabled by default for all newly created servers.

### [​](#editing-php-and-fpm-configuration-settings) Editing PHP and FPM configuration settings

You can customize the `php.ini` and FPM settings for individual PHP versions. To edit these settings, navigate to the server’s dashboard and click the “PHP” tab. Locate the version of PHP you want to configure, open the dropdown menu next to that version, and select either:

- **Edit PHP-FPM configuration** - Modify the PHP FPM (web) configuration for this specific PHP version
- **Edit PHP CLI configuration** - Modify the PHP CLI (command-line interface) configuration for this specific PHP version

These settings apply only to the individual version of PHP selected and will not affect other PHP versions installed on your server.

## [​](#beta-and-release-candidates) Beta and release candidates

PHP “beta” and “release candidate” releases are often available on Laravel Forge weeks before their final release. This allows you to experiment with upcoming major PHP versions on sites that are not in production. However, some Forge features, PHP features, and PHP extensions may not work as expected during that period.

Once that PHP version becomes stable, you will need to fully uninstall and re-install the PHP version.

Was this page helpful?

YesNo

[Laravel VPS](/docs/servers/laravel-vps)[Load Balancing](/docs/servers/load-balancing)

⌘I

[x](https://x.com/laravelphp)[github](https://github.com/laravel)[discord](https://discord.com/invite/laravel)[linkedin](https://linkedin.com/company/laravel)