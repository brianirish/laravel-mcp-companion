# Forge - Integrations/Sentry

*Source: https://forge.laravel.com/docs/integrations/sentry*

---

- [Community](https://discord.com/invite/laravel)
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

On this page

- [Overview](#overview)
- [Connect with Sentry](#connect-with-sentry)
- [Creating Sentry Projects](#creating-sentry-projects)
- [Circle Permissions](#circle-permissions)

Integrations

# Sentry

Sentry provides error monitoring and tracing for Laravel apps with Forge integration for creating Sentry organizations.

## [​](#overview) Overview

[Sentry](https://sentry.io) provides error monitoring and tracing for Laravel applications. Forge has partnered with Sentry to allow you to create new Sentry organizations without leaving Forge.
After creating your Sentry organization, you may easily add Sentry error monitoring to any of your Forge powered sites.

## [​](#connect-with-sentry) Connect with Sentry

Before you can use Sentry with Forge, you must connect your Forge account to a Sentry account. To do this,
visit the [Sentry panel](https://forge.laravel.com/user-profile/sentry) in the Forge dashboard.

![Connect with Sentry User Profile form](https://mintlify.s3.us-west-1.amazonaws.com/forge-laravel/images/sentry-user-profile.png)

Clicking “Connect with Sentry” will create a new, Forge-linked Sentry organization with the email address shown under
“Sentry Account Email”. You will receive an email from Sentry confirming your new organization.

It is not possible to use an existing Sentry organization with the Forge integration. Forge created Sentry projects will be added
to the new organization.

## [​](#creating-sentry-projects) Creating Sentry Projects

Forge allows you to create new Sentry projects directly from the Forge dashboard. To create a new Sentry project,
visit the site’s Sentry dashboard.

![Sentry Panel](https://mintlify.s3.us-west-1.amazonaws.com/forge-laravel/images/sentry-project-form.png)

Clicking “Create Sentry Project” will create a new project within the server owner’s connected Sentry organization.
Once the project is created, you will be provided with a DSN key that you may use to configure your Laravel application.

Forge does not automatically install Sentry into your Laravel application. You should install the
[Sentry SDK for Laravel](https://github.com/getsentry/sentry-laravel) via Composer and define the `SENTRY_DSN` environment variable.

## [​](#circle-permissions) Circle Permissions

The ability to manage a site’s Sentry project is determined by the `site:manage-integrations` permission.

Was this page helpful?

YesNo

[Envoyer](/docs/integrations/envoyer)[Aikido](/docs/integrations/aikido)

Assistant

Responses are generated using AI and may contain mistakes.