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
- [Credential levels](#credential-levels)
- [Server-level credentials](#server-level-credentials)
- [Site-level credentials](#site-level-credentials)
- [Managing credentials](#managing-credentials)
- [Adding credentials](#adding-credentials)
- [Updating credentials](#updating-credentials)
- [Removing credentials](#removing-credentials)
Resources
# Packages
Copy page
Learn how Laravel Forge manages Composer credentials for your servers and sites.
Copy page
## [​](#introduction) Introduction
Laravel Forge provides seamless management of Composer authentication credentials through the “http-basic” configuration in your server or site’s `auth.json` file. These credentials are securely stored and automatically applied to your Composer operations.
## [​](#credential-levels) Credential levels
### [​](#server-level-credentials) Server-level credentials
Server-level Composer credentials are shared across all sites running under the same Ubuntu user account. For instance, if you have multiple sites deployed under the `forge` user, they’ll all have access to the same globally stored credentials located at `~/.config/composer/auth.json`.
To manage server-level credentials, navigate to your server’s dashboard, select the “PHP” tab, then click the “Composer” sidebar item.
### [​](#site-level-credentials) Site-level credentials
Site-level credentials apply exclusively to individual sites, providing granular control when different sites require unique authentication for the same packages. This is particularly useful when multiple sites under the same user need different access permissions or licensing.
To manage site-level credentials, navigate to your site’s dashboard, select the “Settings” tab, then click the “Composer” sidebar item.
## [​](#managing-credentials) Managing credentials
### [​](#adding-credentials) Adding credentials
To add new Composer credentials, navigate to the appropriate Composer management page and click the “Add credential” button. Complete the required fields and click “Add credential” to save:
- **Repository URL:** The URL Composer uses to match credentials with the corresponding package provider
- **Username:** Typically an email address or unique identifier required by the package provider
- **Password:** The associated password or license key for authentication
### [​](#updating-credentials) Updating credentials
To modify existing credentials, navigate to the appropriate Composer dashboard, locate the credential you want to update, open its dropdown menu, and select “Edit”. Make your changes and save the updated information.
### [​](#removing-credentials) Removing credentials
To delete credentials, navigate to the appropriate Composer dashboard, locate the credential you want to remove, open its dropdown menu, select “Delete”, and confirm the removal when prompted.
Was this page helpful?
YesNo
[Network](/docs/resources/network)[Envoyer](/docs/integrations/envoyer)
Assistant
Responses are generated using AI and may contain mistakes.