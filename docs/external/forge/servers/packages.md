# Forge - Servers/Packages

*Source: https://forge.laravel.com/docs/servers/packages*

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
- [Global Composer Credentials](#global-composer-credentials)
- [User Selection](#user-selection)
- [Managing Credentials](#managing-credentials)
- [Add Credentials](#add-credentials)
- [Remove Credentials](#remove-credentials)
- [Update Credentials](#update-credentials)
- [Circle Permissions](#circle-permissions)

Servers

# Packages

Manage Composer credentials on your server.

## [​](#overview) Overview

Forge allows you to manage the “http-basic” portion of the selected server user’s `auth.json` Composer configuration file. The provided credentials are only stored on the server being managed by Forge - not in Forge itself.

## [​](#global-composer-credentials) Global Composer Credentials

The Composer credentials that you can manage on the server level will apply to all sites that are served by the same Ubuntu user account. For example, if you have two sites installed under the `forge` user, both these sites will benefit from the globally stored credentials. If you need fine-grained control, please see the [Packages](/docs/sites/packages) documentation for sites.

## [​](#user-selection) User Selection

If you have sites configured with user isolation, you will first need to select the appropriate server user. The `auth.json` file is global within each individual server user account.

## [​](#managing-credentials) Managing Credentials

Forge makes it easy to manage Composer credentials across all sites on your server. You can add, remove, and update credentials directly from the Forge UI.

### [​](#add-credentials) Add Credentials

Additional credentials can be added by clicking the “Add Credentials” button. You need to provide:

- Repository URL - this is how Composer matches the credentials to the package for which the provider wants to authenticate users
- Username - this is often an email address, but can also be any kind of unique identifier that the provider of the package uses
- Password - this is generally the password associated with the username, however in some case, this may also be a license key

Click “Save” in order to store these credentials in the user’s global Composer configuration directory (`~/.config/composer/auth.json`).

### [​](#remove-credentials) Remove Credentials

In order to remove Composer credentials, you can click on the red **X** button.
After removing credentials, you must click “Save” in order to update the credentials configuration on the server.

### [​](#update-credentials) Update Credentials

Any credentials that are shown on the screen can be updated with any new adequate value.
After updating the credential, you must click “Save” in order to update the credentials configuration on the server.

## [​](#circle-permissions) Circle Permissions

The ability to manage a server’s Composer packages is determined by the `server:manage-packages` permission. This permission will also allow the circle member to manage a site’s Composer packages too.

Was this page helpful?

YesNo

[PHP](/docs/servers/php)[Recipes](/docs/servers/recipes)

Assistant

Responses are generated using AI and may contain mistakes.