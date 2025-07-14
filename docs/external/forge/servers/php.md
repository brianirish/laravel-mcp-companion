# Forge - Servers/Php

*Source: https://forge.laravel.com/docs/servers/php*

---

- [Laravel Forge home page](https://forge.laravel.com)Search...⌘KAsk AI
[Support](/cdn-cgi/l/email-protection#40262f322725002c21322136252c6e232f2d)
- [Dashboard](https://forge.laravel.com)
- [Dashboard](https://forge.laravel.com)

Search...NavigationServersPHP[Documentation](/docs/introduction)[Changelog](/docs/changelog/changelog)- [Community](https://discord.com/invite/laravel)
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

Servers# PHP

Learn how to manage PHP versions on your Forge server.

## [​](#overview)Overview

Forge makes it easy to install and configure multiple versions of PHP on your server. Each installed PHP version runs its own FPM process. In addition, you may [update the PHP version used by specific sites at any time](/docs/sites/the-basics#php-version).

If you choose to manually install PHP versions on your server, Forge will not be aware of those PHP installations. Forge is only aware of PHP installations that are managed through the Forge dashboard.

## [​](#multiple-php-versions)Multiple PHP Versions

When provisioning a server, you must decide which version of PHP you want to install by default. The `php` binary on your server will point to the installed version selected at the time of its creation.

Once the server has been created, Forge makes it easy to install additional versions alongside the default version. In the following documentation we will discuss how to manage these additional PHP versions.

### [​](#installation)Installation

You can install additional versions of PHP via the **PHP** tab on a server’s management dashboard. Once an additional version of PHP has been installed, you may select it when creating a site or when switching a site’s PHP version.

When you install a new version of PHP onto your server, Forge will create and configure the PHP-FPM process for that version. This means that your server will be running multiple versions of PHP at once.

### [​](#uninstalling-additional-php-versions)Uninstalling Additional PHP Versions

You can choose to uninstall a version of PHP so long as:

- There are other versions installed.

- The version you wish to uninstall is not the server’s default version for new sites.

- The version you wish to uninstall is not the server’s default version on the CLI.

- The version you wish to uninstall is not used by any sites.

### [​](#cli)CLI

When an additional version of PHP has been installed, you may reference it on the CLI via `phpx.x`, replacing the `x.x` with the version number (e.g. `php8.1`). The `php` binary will always point to the active CLI version (if changed from the default).

### [​](#default-php-installation)Default PHP Installation

The “default” PHP version is the version of PHP that will be used by default when creating a new site on the server.

When selecting a new version of PHP as your server’s “default” version, the PHP versions used by existing sites **will not be updated**.

### [​](#updating-php-between-patch-releases)Updating PHP Between Patch Releases

You can upgrade your PHP installations between patch releases of PHP at any time using the **Patch Version** button. Typically, these updates should not cause any breaking changes to your server, although a few seconds of downtime is possible.

### [​](#php-betas-%2F-release-candidates)PHP Betas / Release Candidates

PHP “beta” and “release candidate” releases are often available on Forge weeks before their final release. This allows you to experiment with upcoming major PHP versions on sites that are not in production. However, some Forge features, PHP features, and PHP extensions may not work as expected during that period. In addition, once that PHP version becomes stable, **you will need to fully uninstall and re-install** the PHP version.

## [​](#common-php-configuration-settings)Common PHP Configuration Settings

Changing the following settings will apply the changes to all versions of PHP installed on the server.

### [​](#max-file-upload-size)Max File Upload Size

You may configure the maximum file upload size through the **PHP** tab of the server management dashboard. This value should be provided in megabytes. For reference, `1024MB` is `1GB`.

### [​](#max-execution-time)Max Execution Time

You may configure the maximum execution time through the **PHP** tab of the server management dashboard. This value should be provided in seconds.

### [​](#opcache)OPcache

Optimizing the PHP OPcache for production will configure OPcache to store your compiled PHP code in memory to greatly improve performance. If you choose to optimize OPcache for production, you should verify that your deployment script [reloads the PHP-FPM service](/docs/servers/cookbook#restarting-php-fpm) at the end of each deployment.

## [​](#circle-permissions)Circle Permissions

Circle members will require the `server:manage-php` permission to manage PHP installations and configurations. This permission is also required to manage integrations with Blackfire.io and Papertrail.

Was this page helpful?

YesNo[SSH Keys / Git Access](/docs/servers/ssh)[Packages](/docs/servers/packages)On this page
- [Overview](#overview)
- [Multiple PHP Versions](#multiple-php-versions)
- [Installation](#installation)
- [Uninstalling Additional PHP Versions](#uninstalling-additional-php-versions)
- [CLI](#cli)
- [Default PHP Installation](#default-php-installation)
- [Updating PHP Between Patch Releases](#updating-php-between-patch-releases)
- [PHP Betas / Release Candidates](#php-betas-%2F-release-candidates)
- [Common PHP Configuration Settings](#common-php-configuration-settings)
- [Max File Upload Size](#max-file-upload-size)
- [Max Execution Time](#max-execution-time)
- [OPcache](#opcache)
- [Circle Permissions](#circle-permissions)

[Laravel Forge home page](https://forge.laravel.com)[x](https://x.com/laravelphp)[github](https://github.com/laravel)[discord](https://discord.com/invite/laravel)[linkedin](https://linkedin.com/company/laravel)[Term of Service](https://forge.laravel.com/terms-of-service)[Privacy Policy](https://forge.laravel.com/privacy-policy)[Data Processing Agreement (DPA)](https://forge.laravel.com/data-processing-agreement)[x](https://x.com/laravelphp)[github](https://github.com/laravel)[discord](https://discord.com/invite/laravel)[linkedin](https://linkedin.com/company/laravel)AssistantResponses are generated using AI and may contain mistakes.