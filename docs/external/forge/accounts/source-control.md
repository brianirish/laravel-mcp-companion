# Forge - Accounts/Source-Control

*Source: https://forge.laravel.com/docs/accounts/source-control*

---

- [Laravel Forge home page](https://forge.laravel.com)Search...⌘KAsk AI
[Support](/cdn-cgi/l/email-protection#0b6d64796c6e4b676a796a7d6e6725686466)
- [Dashboard](https://forge.laravel.com)
- [Dashboard](https://forge.laravel.com)

Search...NavigationAccountsSource Control[Documentation](/docs/introduction)[Changelog](/docs/changelog/changelog)- [Community](https://discord.com/invite/laravel)
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

Accounts# Source Control

Source providers allow Forge to access your project’s codebase to help you easily deploy your applications. Forge supports most popular Git providers as well as custom / self-hosted options.

## [​](#introduction)Introduction

Source providers allow Forge to access your project’s codebase to help you easily deploy your applications. Forge supports most popular Git providers as well as custom / self-hosted options.

## [​](#supported-providers)Supported Providers

Forge currently supports the following source control providers:

- [GitHub](https://github.com/)

- [GitLab](https://about.gitlab.com/) (hosted and self-hosted)

- [Bitbucket](https://bitbucket.org/)

- Custom Git Repositories

### [​](#using-a-custom-git-provider)Using A Custom Git Provider

If your Git Provider is not a first-party provider, then you may use the **Custom** option when creating a new site on your server.

First, choose the `Custom` option when creating your Git based site. Next, add the generated SSH key to your source control provider and provide the full repository path (`[[email protected]](/cdn-cgi/l/email-protection):user/repository.git`).

## [​](#provider-management)Provider Management

### [​](#connecting-providers)Connecting Providers

You can connect to any of the supported source control providers at any time through Forge’s [Source Control dashboard](https://forge.laravel.com/user-profile/source-control) within your Forge account profile.

### [​](#unlinking-providers)Unlinking Providers

You may remove a connected source control provider by clicking the **Unlink** button next to a provider.

You won’t be able to unlink your provider if there are sites that depend on it.

### [​](#refreshing-tokens)Refreshing Tokens

If you would like to refresh Forge’s connection to your source control provider, you may do so by clicking the **Refresh Token** button next to the source control provider’s name on the Source Control dashboard within your Forge account profile.

### [​](#updating-source-control-access-and-permissions)Updating Source Control Access and Permissions

To update your source control provider connection for accessing different organizations, repositories, or modifying token permissions:

- Navigate to your source control provider’s settings

- Locate and uninstall the Forge OAuth application

- Return to Forge

- Click the **Refresh Token** button to initiate a new OAuth authentication flow

When you need access to different organizations or repositories, simply refreshing the token may not grant the necessary permissions. Following the complete OAuth authentication flow allows you to explicitly authorize access to your desired organizations and repositories with the appropriate permission scope.

Was this page helpful?

YesNo[Circles](/docs/accounts/circles)[SSH Keys](/docs/accounts/ssh)On this page
- [Introduction](#introduction)
- [Supported Providers](#supported-providers)
- [Using A Custom Git Provider](#using-a-custom-git-provider)
- [Provider Management](#provider-management)
- [Connecting Providers](#connecting-providers)
- [Unlinking Providers](#unlinking-providers)
- [Refreshing Tokens](#refreshing-tokens)
- [Updating Source Control Access and Permissions](#updating-source-control-access-and-permissions)

[Laravel Forge home page](https://forge.laravel.com)[x](https://x.com/laravelphp)[github](https://github.com/laravel)[discord](https://discord.com/invite/laravel)[linkedin](https://linkedin.com/company/laravel)[Term of Service](https://forge.laravel.com/terms-of-service)[Privacy Policy](https://forge.laravel.com/privacy-policy)[Data Processing Agreement (DPA)](https://forge.laravel.com/data-processing-agreement)[x](https://x.com/laravelphp)[github](https://github.com/laravel)[discord](https://discord.com/invite/laravel)[linkedin](https://linkedin.com/company/laravel)AssistantResponses are generated using AI and may contain mistakes.