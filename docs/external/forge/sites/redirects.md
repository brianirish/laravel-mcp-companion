# Forge - Sites/Redirects

*Source: https://forge.laravel.com/docs/sites/redirects*

---

- [Laravel Forge home page](https://forge.laravel.com)Search...⌘KAsk AI
[Support](/cdn-cgi/l/email-protection#1f79706d787a5f737e6d7e697a73317c7072)
- [Dashboard](https://forge.laravel.com)
- [Dashboard](https://forge.laravel.com)

Search...NavigationSitesRedirects[Documentation](/docs/introduction)[Changelog](/docs/changelog/changelog)- [Community](https://discord.com/invite/laravel)
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

Sites# Redirects

Configure redirects for your sites.

## [​](#overview)Overview

Forge allows you to configure redirects that can be configured to automatically redirect visitors from one page to another. These redirect rules can be created via the “Redirects” tab of the site’s management dashboard.

## [​](#creating-redirects)Creating Redirects

Redirects are wrappers around Nginx’s [`rewrite` rules](https://nginx.org/en/docs/http/ngx_http_rewrite_module.html#rewrite) and can use the full redirect syntax supported by Nginx, including regular expressions. For example, you could use `^/$` to only match the root of the domain.

## [​](#temporary-vs-permanent-redirects)Temporary vs. Permanent Redirects

Forge supports two types of redirects:

- Permanent (HTTP Status Code 301)

- Temporary (HTTP Status Code 302)

Although both of these redirect types are typically invisible to the user, the browser will treat them differently and it is important to know the difference.

### [​](#temporary-redirects)Temporary Redirects

When the browser encounters a temporary redirect, it will take you to the destination and forget that it was redirected from the original page. If you were to change the destination page and then visited the original page again, the browser would see the new redirect location and take you there.

### [​](#permanent-redirects)Permanent Redirects

With a permanent redirect, the browser will remember that it was redirected away from the original page. To save making another network request, the next time the browser visits the original page, it will see that it was redirected and immediately visit that page instead.

Although you can change the destination of a permanent redirect, you will need to clear the browser cache before you visit the original page again. It’s considered bad practice to change a permanent redirect, so be careful when doing so.

## [​](#circle-permissions)Circle Permissions

You may grant a circle member authority to create and manage redirects by granting the `site:manage-redirects` permission.

Was this page helpful?

YesNo[Security Rules](/docs/sites/security-rules)[SSL](/docs/sites/ssl)On this page
- [Overview](#overview)
- [Creating Redirects](#creating-redirects)
- [Temporary vs. Permanent Redirects](#temporary-vs-permanent-redirects)
- [Temporary Redirects](#temporary-redirects)
- [Permanent Redirects](#permanent-redirects)
- [Circle Permissions](#circle-permissions)

[Laravel Forge home page](https://forge.laravel.com)[x](https://x.com/laravelphp)[github](https://github.com/laravel)[discord](https://discord.com/invite/laravel)[linkedin](https://linkedin.com/company/laravel)[Term of Service](https://forge.laravel.com/terms-of-service)[Privacy Policy](https://forge.laravel.com/privacy-policy)[Data Processing Agreement (DPA)](https://forge.laravel.com/data-processing-agreement)[x](https://x.com/laravelphp)[github](https://github.com/laravel)[discord](https://discord.com/invite/laravel)[linkedin](https://linkedin.com/company/laravel)AssistantResponses are generated using AI and may contain mistakes.