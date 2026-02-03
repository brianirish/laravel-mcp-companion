# Forge - Integrations/Envoyer

*Source: https://forge.laravel.com/docs/integrations/envoyer*

---

[Laravel Forge home page![light logo](https://mintcdn.com/forge-laravel/DhXK7kFkCTo-2V2J/logo/logo.svg?fit=max&auto=format&n=DhXK7kFkCTo-2V2J&q=85&s=a66298a7f876f35c44132183267a2cd6)![dark logo](https://mintcdn.com/forge-laravel/DhXK7kFkCTo-2V2J/logo/logo.svg?fit=max&auto=format&n=DhXK7kFkCTo-2V2J&q=85&s=a66298a7f876f35c44132183267a2cd6)](https://forge.laravel.com)

Search...

⌘KAsk AI

- [Get started](https://forge.laravel.com)
- [Get started](https://forge.laravel.com)

Search...

Navigation

Integrations

Envoyer

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
- [Creating an Envoyer API token](#creating-an-envoyer-api-token)
- [Linking your Envoyer account to Laravel Forge](#linking-your-envoyer-account-to-laravel-forge)
- [Envoyer sites in Laravel Forge](#envoyer-sites-in-laravel-forge)
- [Migrating existing sites to Forge](#migrating-existing-sites-to-forge)
- [Requirements](#requirements)

Integrations

# Envoyer

Copy page

Zero-downtime deployments with Laravel Forge and Envoyer.

Copy page

## [​](#introduction) Introduction

Laravel Forge now offers zero-downtime deployments for all new sites.

While Laravel Forge now offers [zero-downtime deployments](/docs/sites/deployments), you may choose to use the first-party integration with [Envoyer](https://envoyer.io) to simultaneously deploy projects across multiple servers. Zero-downtime deployments ensure you avoid those brief milliseconds of downtime while the server updates your code.

## [​](#creating-an-envoyer-api-token) Creating an Envoyer API token

To kick things off, you’ll need active subscriptions for both [Laravel Forge](https://forge.laravel.com/sign-up) and [Envoyer](https://envoyer.io/auth/register). Once you’re set up, navigate to your Envoyer dashboard and [create a new API token](https://envoyer.io/user/profile?name=Laravel%20Forge&scopes=projects:create,deployments:create,servers:create#/api). At a minimum, Laravel Forge requires the following scopes:

Copy

Ask AI

```
deployments:create
projects:create
servers:create
```

To future-proof the integration, consider providing Laravel Forge with additional access permissions. You can update your Envoyer’s API token in Forge at any point.

## [​](#linking-your-envoyer-account-to-laravel-forge) Linking your Envoyer account to Laravel Forge

To link Laravel Forge with your Envoyer API token, navigate to your organization’s settings and toggle on the “Envoyer” option. You’ll be prompted to enter your Envoyer API token. After submitting the token, Forge will first verify it and then enable the integration.

## [​](#envoyer-sites-in-laravel-forge) Envoyer sites in Laravel Forge

It is no longer possible to link newly created Laravel Forge sites to Envoyer projects. Instead, you should create a new Envoyer project and then import your Laravel Forge server and site into that project. For more information, see the “Migrating an existing site to Envoyer” section below.

To deploy your Envoyer project within Laravel Forge, click the “Deploy” button, as you would with any other site in Forge. The “Deployment Trigger URL” is also available for use in a CI environment.
Additionally, Laravel Forge has been updated to align perfectly with Envoyer projects:

- Commands are executed from the `/current` directory.
- The site’s “Environment” panel will display a read-only version of the `.env` file. Continue to use Envoyer to manage your environment file, especially since it may need to be synchronized across multiple servers.
- The site’s “Packages” panel is disabled to ensure the `auth.json` file remains intact through future deployments.

## [​](#migrating-existing-sites-to-forge) Migrating existing sites to Forge

Sites previously connected to Envoyer can be migrated to Laravel Forge’s native zero-downtime deployment system. To do so, navigate to the site’s “Overview” panel and click “Migrate to Forge”.
The Envoyer project will first be checked for compatibility. If compatible, the migration can be completed.
To complete the migration, you will need to provide your environment key for the Envoyer project. This allows Laravel Forge to access the `.env` file for the project.
If the Envoyer project is configured to use Heartbeats, Laravel Forge will also provide you with a list of new heartbeat URLs. You will need to update your application to use these new URLs.

### [​](#requirements) Requirements

There are a few requirements that must be met before migrating an existing Envoyer site to Laravel Forge:

1. Your Envoyer project must be connected to a single server.
2. Must not be using GitLab Self-Hosted as the Git repository.
3. Your organization must be connected to the Envoyer integration.
4. Forge deployments are limited to [10 minutes](/docs/sites/deployments#introduction), compared to Envoyer’s 15-minute limit. Ensure your deployment process completes within this timeframe.

Was this page helpful?

YesNo

[Packages](/docs/resources/packages)[Sentry](/docs/integrations/sentry)

⌘I

[x](https://x.com/laravelphp)[github](https://github.com/laravel)[discord](https://discord.com/invite/laravel)[linkedin](https://linkedin.com/company/laravel)