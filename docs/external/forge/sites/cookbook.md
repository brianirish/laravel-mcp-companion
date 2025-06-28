# Forge - Sites/Cookbook

*Source: https://forge.laravel.com/docs/sites/cookbook*

---

- [Laravel Forge home page](https://forge.laravel.com)Search...⌘KAsk AI
[Support](/cdn-cgi/l/email-protection#86e0e9f4e1e3c6eae7f4e7f0e3eaa8e5e9eb)
- [Dashboard](https://forge.laravel.com)
- [Dashboard](https://forge.laravel.com)

Search...NavigationSitesCookbook[Documentation](/docs/introduction)[Changelog](/docs/changelog/changelog)- [Community](https://discord.com/invite/laravel)
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

Sites# Cookbook

Common tasks and solutions for managing your Forge sites.

## [​](#site-is-stuck-deploying)Site Is Stuck Deploying

Rarely, your application may get stuck in a “deploying” state. When this occurs, you can reset the deployment state at the top right of the site management panel using the **Self Help** drop-down menu.

## [​](#using-user-isolation-with-existing-sites)Using User Isolation With Existing Sites

It is not currently possible to use isolated users to manage existing sites that have already been created without user isolation. Instead, you will need to create a new site with the user isolation option enabled.

## [​](#uncommitted-commits-during-deployment)Uncommitted Commits During Deployment

This error may occur when files under source control within the site directory have been changed by the application and will be overwritten by the fresh deployment.

You may discard these changes by accessing the **Self Help** drop-down menu at the top right of the site management panel and triggering the **Reset Git State** action. Please note that the changes made will be lost when this action is run.

You should also review your application and correct any parts of the applications that may be writing to a source controlled directory on your server. Otherwise, you may continue to encounter this error on further deployments.

Was this page helpful?

YesNo[User Isolation](/docs/sites/user-isolation)[Daemons](/docs/resources/daemons)On this page
- [Site Is Stuck Deploying](#site-is-stuck-deploying)
- [Using User Isolation With Existing Sites](#using-user-isolation-with-existing-sites)
- [Uncommitted Commits During Deployment](#uncommitted-commits-during-deployment)

[Laravel Forge home page](https://forge.laravel.com)[x](https://x.com/laravelphp)[github](https://github.com/laravel)[discord](https://discord.com/invite/laravel)[linkedin](https://linkedin.com/company/laravel)[Term of Service](https://forge.laravel.com/terms-of-service)[Privacy Policy](https://forge.laravel.com/privacy-policy)[Data Processing Agreement (DPA)](https://forge.laravel.com/data-processing-agreement)[x](https://x.com/laravelphp)[github](https://github.com/laravel)[discord](https://discord.com/invite/laravel)[linkedin](https://linkedin.com/company/laravel)AssistantResponses are generated using AI and may contain mistakes.