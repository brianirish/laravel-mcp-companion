# Forge - Source-Control

*Source: https://forge.laravel.com/docs/source-control*

---

[Laravel Forge home page![light logo](https://mintcdn.com/forge-laravel/DhXK7kFkCTo-2V2J/logo/logo.svg?fit=max&auto=format&n=DhXK7kFkCTo-2V2J&q=85&s=a66298a7f876f35c44132183267a2cd6)![dark logo](https://mintcdn.com/forge-laravel/DhXK7kFkCTo-2V2J/logo/logo.svg?fit=max&auto=format&n=DhXK7kFkCTo-2V2J&q=85&s=a66298a7f876f35c44132183267a2cd6)](https://forge.laravel.com)

Search...

⌘KAsk AI

- [Get started](https://forge.laravel.com)
- [Get started](https://forge.laravel.com)

Search...

Navigation

Basics

Source Control

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
- [Supported providers](#supported-providers)
- [Managing source control providers](#managing-source-control-providers)
- [Connecting to a source control provider](#connecting-to-a-source-control-provider)
- [Removing source control providers](#removing-source-control-providers)
- [Refreshing tokens](#refreshing-tokens)
- [Updating source control access and permissions](#updating-source-control-access-and-permissions)
- [Using custom Git providers](#using-custom-git-providers)

Basics

# Source Control

Copy page

Source control providers allow Laravel Forge to access your project’s codebase and easily deploy your applications.

Copy page

## [​](#introduction) Introduction

Source control providers allow Laravel Forge to access your project’s codebase and easily deploy your applications. Forge supports most popular Git providers as well as custom / self-hosted options.
Source control providers are configured and managed within the [organization’s](/docs/organizations) settings.

## [​](#supported-providers) Supported providers

Laravel Forge supports the following source control providers:

- [GitHub](https://github.com/)
- [GitLab](https://about.gitlab.com/) (hosted and self-hosted)
- [Bitbucket](https://bitbucket.org/)
- Custom Git Repositories

## [​](#managing-source-control-providers) Managing source control providers

### [​](#connecting-to-a-source-control-provider) Connecting to a source control provider

To connect a source control provider, navigate to the organization’s settings. Then, on the “Source control” page, click “Add provider”. Select the provider you wish to connect to and authenticate your chosen account.
You may only configure one account from each provider at a time. If you need to connect a different account from the same provider, you must first remove the existing connection.

### [​](#removing-source-control-providers) Removing source control providers

To unlink a source control provider, navigate to the organization’s settings. Then, on the “Source control” page, click the dropdown menu on the provider and click “Delete”.

Source control providers cannot be unlinked if an active site is using that provider.

### [​](#refreshing-tokens) Refreshing tokens

To refresh a source control provider token, navigate to the organization’s settings. Then, on the “Source control” page, click the dropdown menu on the provider and click “Refresh token”.

### [​](#updating-source-control-access-and-permissions) Updating source control access and permissions

To update your source control provider connection for accessing different organizations, repositories, or modifying token permissions:

1. Navigate to your source control provider’s settings
2. Locate and uninstall the Laravel Forge application
3. Return to Laravel Forge
4. Click the **Refresh Token** button to initiate a new OAuth authentication flow

When you need access to different organizations or repositories, refreshing the token may not grant the necessary permissions.
Following the complete OAuth authentication flow allows you to explicitly authorize access to your desired organizations and repositories with the appropriate permission scope.

### [​](#using-custom-git-providers) Using custom Git providers

If your Git Provider is not a first-party provider, then you may use the **Custom** option when creating a new site on your server.
First, choose the `Custom` option when creating your Git based site. Next, add the generated SSH key to your source control provider and provide the full repository path (`[email protected]:user/repository.git`).

Was this page helpful?

YesNo

[Server Providers](/docs/server-providers)[SSH Keys](/docs/ssh)

⌘I

[x](https://x.com/laravelphp)[github](https://github.com/laravel)[discord](https://discord.com/invite/laravel)[linkedin](https://linkedin.com/company/laravel)