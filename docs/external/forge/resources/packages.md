# Forge - Resources/Packages

*Source: https://forge.laravel.com/docs/resources/packages*

---

[Laravel Forge home page](https://forge.laravel.com)
Search...
⌘KAsk AI
- [Get started](https://forge.laravel.com)
- [Get started](https://forge.laravel.com)
Search...
Navigation
Resources
Packages
[Documentation](/docs/introduction)[Knowledge Base](/docs/knowledge-base/servers)[API Reference](/docs/api-reference/introduction)
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
- [Composer credentials](#composer-credentials)
- [Credential levels](#credential-levels)
- [Server-level credentials](#server-level-credentials)
- [Site-level credentials](#site-level-credentials)
- [Managing credentials](#managing-credentials)
- [Adding credentials](#adding-credentials)
- [Updating credentials](#updating-credentials)
- [Removing credentials](#removing-credentials)
- [npm credentials](#npm-credentials)
- [Credential levels](#credential-levels-2)
- [Server-level credentials](#server-level-credentials-2)
- [Site-level credentials](#site-level-credentials-2)
- [Managing credentials](#managing-credentials-2)
- [Adding credentials](#adding-credentials-2)
- [Updating credentials](#updating-credentials-2)
- [Removing credentials](#removing-credentials-2)
- [Zero-downtime deployments](#zero-downtime-deployments)
Resources
# Packages
Copy page
Learn how Laravel Forge manages Composer and npm credentials for your servers and sites.
Copy page
## [​](#introduction) Introduction
Laravel Forge provides seamless management of authentication credentials for both Composer and npm package registries. Credentials can be configured at the server level or site level, depending on your needs.
## [​](#composer-credentials) Composer credentials
Laravel Forge manages Composer authentication through the “http-basic” configuration in your server’s or site’s `auth.json` file. These credentials are securely stored and automatically applied to your Composer operations.
### [​](#credential-levels) Credential levels
#### [​](#server-level-credentials) Server-level credentials
Server-level Composer credentials are shared across all sites running under the same Ubuntu user account. For instance, if you have multiple sites deployed under the `forge` user, they all have access to the same globally stored credentials located at `~/.config/composer/auth.json`.
To manage server-level credentials, navigate to your server’s dashboard, select the “PHP” tab, then click the “Composer” sidebar item.
#### [​](#site-level-credentials) Site-level credentials
Site-level credentials apply exclusively to individual sites, providing granular control when different sites require unique authentication for the same packages. This is particularly useful when multiple sites under the same user need different access permissions or licensing.
To manage site-level credentials, navigate to your site’s dashboard, select the “Settings” tab, then click the “Composer” sidebar item.
### [​](#managing-credentials) Managing credentials
#### [​](#adding-credentials) Adding credentials
To add new Composer credentials, navigate to the appropriate Composer management page and click the “Add credential” button. Complete the required fields and click “Add credential” to save:
- **Repository URL**: The URL Composer uses to match credentials with the corresponding package provider.
- **Username**: Typically an email address or unique identifier required by the package provider.
- **Password**: The associated password or license key for authentication.
#### [​](#updating-credentials) Updating credentials
To modify existing credentials, navigate to the appropriate Composer page, locate the credential you want to update, open its dropdown menu, and select “Edit.” Make your changes and save the updated information.
#### [​](#removing-credentials) Removing credentials
To delete credentials, navigate to the appropriate Composer dashboard, locate the credential you want to remove, open its dropdown menu, select “Delete”, and confirm the removal when prompted.
## [​](#npm-credentials) npm credentials
Laravel Forge manages npm registry authentication through `.npmrc` files. This allows you to install packages from private registries such as GitHub Packages, npm organizations, or any registry that supports token-based authentication.
Each credential consists of three parts:
- **Registry**: The hostname of the private registry (e.g., `npm.pkg.github.com`).
- **Token**: The authentication token provided by your registry.
- **Scopes**: One or more npm scopes (e.g., `@myorg`) that should be routed to this registry.
### [​](#credential-levels-2) Credential levels
#### [​](#server-level-credentials-2) Server-level credentials
Server-level npm credentials are stored in the `~/.npmrc` file of the selected Ubuntu user. These credentials are shared across all sites running under that user account.
To manage server-level credentials, navigate to your server’s dashboard, select the “Node” tab, then click the “npm” sidebar item. If your server has multiple Ubuntu users with sites, you can select which user’s credentials to manage from the user dropdown.
#### [​](#site-level-credentials-2) Site-level credentials
Site-level npm credentials provide granular control over registry authentication for individual sites. Forge stores site-level credentials in a separate `.npmrc.forge` file to avoid conflicts with any `.npmrc` file that may already be committed to your repository.
During deployments, Forge automatically merges the credentials from `.npmrc.forge` into the site’s `.npmrc` file. If both files contain credentials for the same registry, the Forge-managed credentials take precedence.
To manage site-level credentials, navigate to your site’s dashboard, select the “Settings” tab, then click the “npm” sidebar item.
If Forge detects credentials committed to your repository’s `.npmrc` file, a warning banner will be displayed on the npm credentials page. We recommend migrating these credentials to Forge for centralized management.
### [​](#managing-credentials-2) Managing credentials
#### [​](#adding-credentials-2) Adding credentials
To add new npm credentials, navigate to the appropriate npm management page and click the “Add credential” button. Complete the required fields and click “Add credential” to save:
- **Registry**: The hostname of the private registry (e.g., `npm.pkg.github.com`). Forge automatically normalizes the URL by stripping the protocol and trailing slashes.
- **Token**: The authentication token for the registry (e.g., a GitHub personal access token).
- **Scopes**: Optional npm scopes to route to this registry. Each scope should start with `@` (e.g., `@myorg`). A scope can only be assigned to one registry.
#### [​](#updating-credentials-2) Updating credentials
To modify existing credentials, navigate to the appropriate npm page, locate the credential you want to update, open its dropdown menu, and select “Edit.” Make your changes and save the updated information.
#### [​](#removing-credentials-2) Removing credentials
To delete credentials, navigate to the appropriate npm dashboard, locate the credential you want to remove, open its dropdown menu, select “Delete”, and confirm the removal when prompted.
### [​](#zero-downtime-deployments) Zero-downtime deployments
npm credentials are fully compatible with zero-downtime deployments. When creating a new release, Forge automatically merges the Forge-managed credentials into the release’s `.npmrc` file before installing dependencies. No additional configuration is required.
Was this page helpful?
YesNo
[Network](/docs/resources/network)[Envoyer](/docs/integrations/envoyer)
⌘I
Assistant
Responses are generated using AI and may contain mistakes.