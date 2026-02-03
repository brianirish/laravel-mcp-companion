# Forge - Integrations/Aikido

*Source: https://forge.laravel.com/docs/integrations/aikido*

---

[Laravel Forge home page![light logo](https://mintcdn.com/forge-laravel/DhXK7kFkCTo-2V2J/logo/logo.svg?fit=max&auto=format&n=DhXK7kFkCTo-2V2J&q=85&s=a66298a7f876f35c44132183267a2cd6)![dark logo](https://mintcdn.com/forge-laravel/DhXK7kFkCTo-2V2J/logo/logo.svg?fit=max&auto=format&n=DhXK7kFkCTo-2V2J&q=85&s=a66298a7f876f35c44132183267a2cd6)](https://forge.laravel.com)

Search...

⌘KAsk AI

- [Get started](https://forge.laravel.com)
- [Get started](https://forge.laravel.com)

Search...

Navigation

Integrations

Aikido

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
- [Connecting with Aikido](#connecting-with-aikido)
- [Enabling Aikido for sites](#enabling-aikido-for-sites)
- [Viewing security findings](#viewing-security-findings)

Integrations

# Aikido

Copy page

Aikido provides security scanning with Laravel Forge integration.

Copy page

## [​](#introduction) Introduction

[Aikido](https://aikido.dev?utm_source=laravel&utm_medium=referral) provides security scanning for repositories. Laravel Forge has partnered with Aikido to allow for a seamless integration with your Forge sites, enabling you to identify and resolve security vulnerabilities directly from the Forge dashboard.

## [​](#connecting-with-aikido) Connecting with Aikido

To begin using Aikido with Laravel Forge, you’ll need to enable the integration at the organization level. Navigate to your organization’s settings, select the “Integrations” tab, and toggle the Aikido integration on.
Follow the prompts to connect your Forge organization to an Aikido workspace. After creating your Aikido workspace, you may easily check the security findings for any of your Forge-powered sites.

You can connect multiple Aikido workspaces to a single Forge organization, each representing a different organization or group in your source control provider.

## [​](#enabling-aikido-for-sites) Enabling Aikido for sites

Once your organization is connected to Aikido, you can enable Aikido security scanning for individual sites. Navigate to your site’s “Settings / Integrations” panel and toggle the Aikido integration on.
Click “Enable Aikido” to activate security scanning for the site. Laravel Forge will automatically match the site’s repository and source control provider to enable Aikido scanning.

## [​](#viewing-security-findings) Viewing security findings

Once Aikido is enabled for a site, security findings will be displayed directly in the site’s “Integrations” panel. If Aikido has not found any security issues for your repository, you will see a confirmation message. You can click “View on Aikido” to see more detailed information on the Aikido platform.
You may disable Aikido for a site at any time by toggling the integration off. This will deactivate Aikido from the repository, and scanning will be stopped.

The Aikido integration is only supported for GitHub, GitLab, GitLab Self-Hosted, and Bitbucket.

Was this page helpful?

YesNo

[Sentry](/docs/integrations/sentry)[OpenClaw](/docs/integrations/openclaw)

⌘I

[x](https://x.com/laravelphp)[github](https://github.com/laravel)[discord](https://discord.com/invite/laravel)[linkedin](https://linkedin.com/company/laravel)