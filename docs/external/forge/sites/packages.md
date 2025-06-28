# Forge - Sites/Packages

*Source: https://forge.laravel.com/docs/sites/packages*

---

- [Laravel Forge home page](https://forge.laravel.com)Search...⌘KAsk AI
[Support](/cdn-cgi/l/email-protection#4f29203d282a0f232e3d2e392a23612c2022)
- [Dashboard](https://forge.laravel.com)
- [Dashboard](https://forge.laravel.com)

Search...NavigationSitesPackages[Documentation](/docs/introduction)[Changelog](/docs/changelog/changelog)- [Community](https://discord.com/invite/laravel)
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

Sites# Packages

Manage Composer credentials on your site.

## [​](#overview)Overview

Forge allows you to manage the “http-basic” portion of the selected site’s user’s `auth.json` Composer configuration file. The provided credentials are only stored on the server being managed by Forge - not within Forge itself.

### [​](#site-composer-credentials)Site Composer Credentials

The Composer Credentials that you can manage on the site level only apply to this site . For example, if you have two sites installed under the `forge` user, and you need both sites to use different credentials for the same Composer package, you should use the site’s packages. If you want to store one set of credentials that applies to all sites with a user’s home directory, please see [Packages](/docs/servers/packages) for more details.

### [​](#adding-credentials-before-installing-a-repository)Adding Credentials Before Installing a Repository

Forge does not allow you to install credentials before you have installed a repository; instead, it will redirect you back to the “App” tab. This is because Forge recreates the site’s base directory if the initial installation does not finish successfully. So, if you need to provide local Composer credentials, you first need to install a repository without the “Install Composer Dependencies” checked so that you can update the credentials after the repository is installed.

## [​](#managing-credentials)Managing Credentials

Forge makes it easy to manage Composer credentials for a site. You can add, remove, and update credentials directly from the Forge UI.

### [​](#add-credentials)Add Credentials

Additional credentials can be added by clicking the “Add Credentials” button. You need to provide:

- Repository URL - this is how Composer matches the credentials to the package for which the provider wants to authenticate users

- Username - this is often an email address, but can also be any kind of unique identifier that the provider of the package uses

- Password - this is generally the password associated with the username, however in some case, this may also be a license key

Click “Save” in order to store these credentials in the user’s global Composer configuration directory (`~/.config/composer/auth.json`).

### [​](#remove-credentials)Remove Credentials

In order to remove Composer credentials, you can simply click on the red button displayed on the same line as the Repository URL.

After removing credentials, please do not forget to click “Save” in order to store your new credentials configuration on the server.

### [​](#update-credentials)Update Credentials

Any credentials that are shown on the screen can be updated with any new adequate value.

After updating the value, please do not forget to click the “Save” button in order your new credentials configuration on the server.

## [​](#circle-permissions)Circle Permissions

The ability to manage a site’s Composer packages is determined by the `server:manage-packages` permission. This permission will also allow the circle member to manage a server’s Composer packages too.

Was this page helpful?

YesNo[Commands](/docs/sites/commands)[Queues](/docs/sites/queues)On this page
- [Overview](#overview)
- [Site Composer Credentials](#site-composer-credentials)
- [Adding Credentials Before Installing a Repository](#adding-credentials-before-installing-a-repository)
- [Managing Credentials](#managing-credentials)
- [Add Credentials](#add-credentials)
- [Remove Credentials](#remove-credentials)
- [Update Credentials](#update-credentials)
- [Circle Permissions](#circle-permissions)

[Laravel Forge home page](https://forge.laravel.com)[x](https://x.com/laravelphp)[github](https://github.com/laravel)[discord](https://discord.com/invite/laravel)[linkedin](https://linkedin.com/company/laravel)[Term of Service](https://forge.laravel.com/terms-of-service)[Privacy Policy](https://forge.laravel.com/privacy-policy)[Data Processing Agreement (DPA)](https://forge.laravel.com/data-processing-agreement)[x](https://x.com/laravelphp)[github](https://github.com/laravel)[discord](https://discord.com/invite/laravel)[linkedin](https://linkedin.com/company/laravel)AssistantResponses are generated using AI and may contain mistakes.