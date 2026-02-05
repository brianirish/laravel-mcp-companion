# Forge - Integrations/Sentry

*Source: https://forge.laravel.com/docs/integrations/sentry*

---

[Laravel Forge home page](https://forge.laravel.com)
Search...
⌘KAsk AI
- [Get started](https://forge.laravel.com)
- [Get started](https://forge.laravel.com)
Search...
Navigation
Integrations
Sentry
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
- [Connecting with Sentry](#connecting-with-sentry)
- [Creating Sentry projects](#creating-sentry-projects)
Integrations
# Sentry
Copy page
Sentry provides error monitoring and tracing for your apps with Laravel Forge integration for creating Sentry organizations.
Copy page
## [​](#introduction) Introduction
[Sentry](https://sentry.io) delivers comprehensive error monitoring and application tracing for your applications. Through Laravel Forge’s partnership with Sentry, you can seamlessly create new Sentry organizations and projects directly from the Forge dashboard, eliminating the need to switch between platforms.
This integration streamlines error tracking implementation for applications hosted on Forge-managed servers while maintaining a unified development workflow.
## [​](#connecting-with-sentry) Connecting with Sentry
To begin using Sentry with Laravel Forge, you’ll need to enable the integration at the organization level. Navigate to your organization’s settings, select the **Integrations** tab, and toggle the Sentry integration on. Complete the setup by providing the required information and clicking Save to create your new Sentry organization.
The Laravel Forge integration requires creating a new Sentry organization. Existing Sentry organizations cannot be connected to this integration—all Forge-created projects will be added to your new organization.
## [​](#creating-sentry-projects) Creating Sentry projects
Once your organization is connected to Sentry, you can create projects for individual sites. Navigate to your site’s **Settings / Integrations** panel and toggle the Sentry integration on. Select your target platform from the available options and follow the provided configuration instructions.
Click Enable Sentry to create the project, then follow the additional setup instructions to properly configure error monitoring for your specific application requirements.
Laravel Forge doesn’t automatically install Sentry into your application. You must manually install the [Sentry SDK for Laravel](https://github.com/getsentry/sentry-laravel) via Composer and configure the `SENTRY_DSN` environment variable with your provided DSN key.
Was this page helpful?
YesNo
[Envoyer](/docs/integrations/envoyer)[Aikido](/docs/integrations/aikido)
⌘I