# Forge - Integrations/Envoyer

*Source: https://forge.laravel.com/docs/integrations/envoyer*

---

- [Laravel Forge home page](https://forge.laravel.com)Search...⌘KAsk AI
[Support](/cdn-cgi/l/email-protection#761019041113361a17041700131a5815191b)
- [Dashboard](https://forge.laravel.com)
- [Dashboard](https://forge.laravel.com)

Search...NavigationIntegrationsEnvoyer[Documentation](/docs/introduction)[Changelog](/docs/changelog/changelog)- [Community](https://discord.com/invite/laravel)
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

Integrations# Envoyer

Zero downtime deployments with Laravel Forge and Envoyer

## [​](#overview)Overview

Forge now offers zero downtime deployments, thanks to a seamless first-party integration with [Envoyer](https://envoyer.io). Envoyer’s zero downtime deployments ensure you avoid even those brief milliseconds of downtime while the server updates your code.

## [​](#creating-an-envoyer-api-token)Creating An Envoyer API Token

To kick things off, you’ll need active subscriptions for both [Laravel Forge](https://forge.laravel.com/auth/register) and [Envoyer](https://envoyer.io/auth/register). Once you’re set up, navigate to your Envoyer dashboard and [create a new API token](https://envoyer.io/user/profile?name=Laravel%20Forge&scopes=projects:create,deployments:create,servers:create#/api). At a minimum, Forge requires the following scopes:

CopyAsk AI```
deployments:create
projects:create
servers:create

```

To future-proof the integration, consider providing Forge with additional access permissions. You can update your Envoyer’s API token in Forge at any point.

## [​](#linking-your-envoyer-account-to-forge)Linking Your Envoyer Account To Forge

Next, it’s time to link Forge with your Envoyer API token. Navigate to your account settings in Forge and click on the [Envoyer navigation item](https://forge.laravel.com/user-profile/envoyer).

## [​](#creating-new-sites-with-envoyer)Creating New Sites With Envoyer

When creating a new site in Forge, you’ll notice a new option labeled “Configure with Envoyer”. Toggle this option to reveal a dropdown menu, where you can either select an existing Envoyer project or create a brand new one.

## [​](#envoyer-sites-in-forge)Envoyer Sites In Forge

To deploy your Envoyer project within Forge, simply click the “Deploy Now” button, just as you would with any other site in Forge. The “Deployment Trigger URL” is also available for use in a CI environment.

Additionally, Forge has been updated to align perfectly with Envoyer projects:

- Commands are executed from the `/current` directory.

- The Environment panel will display a read-only version of the `.env` file. Continue to use Envoyer to manage your environment file, especially since it may need to be synchronized across multiple servers.

- The site’s Packages panel is disabled to ensure the `auth.json` file remains intact through subsequent deployments.

## [​](#migrating-an-existing-site-to-envoyer)Migrating An Existing Site To Envoyer

Before migrating your Forge site to Envoyer, ensure your site directory does not contain a directory named `releases` or `current`. This is essential in allowing Envoyer to create these directories during the project’s installation on your server.

Next, access the Envoyer dashboard and navigate to the relevant project. Within the project settings, select “Import Forge Server”, then choose the appropriate server and site before clicking “Import Server.”

After adding the server details, it’s crucial to test the connection to ensure that Envoyer can communicate with your server effectively. You can test the connection status from the server overview.

Next, click the “Manage Environment” button, unlock your environment, and sync it to the new server. This action will replace the contents of the existing `.env` file in the site directory on the server.

Now, you should initiate a deployment from Envoyer. Once the deployment is complete, Envoyer will download the latest version of your application into the releases directory of your site and add a symlink to `/current`.

Your site should still be accessible, but the old version is still being served. To address this, navigate to the “Settings” panel in Forge and prefix the web directory with `/current`. For example, if your site’s web directory is currently `/public`, update it to `/current/public`. Doing so will instruct Nginx to serve your application from `/home/forge/example.com/current/public` – the location where Envoyer has installed the latest version of your application.

You should now tidy your site directory by ensuring it only contains the `.env` file, along with the `releases`, `current`, and `storage` directories. After **ensuring you have backed up anything you need**, you may remove everything else, including any dotfiles and directories such as `.git`, `.gitattributes`, etc.

Now that the web directory includes `/current`, Forge will recognize your site as being managed by Envoyer in the “Envoyer” panel. You can now link Forge and Envoyer together by selecting the relevant project from the project list.

Finally, now that your application is being served from the `/current` directory, you should update your scheduler, queue workers, and any daemons to ensure they are running from the correct path.

Was this page helpful?

YesNo[Cookbook](/docs/resources/cookbook)[Sentry](/docs/integrations/sentry)On this page
- [Overview](#overview)
- [Creating An Envoyer API Token](#creating-an-envoyer-api-token)
- [Linking Your Envoyer Account To Forge](#linking-your-envoyer-account-to-forge)
- [Creating New Sites With Envoyer](#creating-new-sites-with-envoyer)
- [Envoyer Sites In Forge](#envoyer-sites-in-forge)
- [Migrating An Existing Site To Envoyer](#migrating-an-existing-site-to-envoyer)

[Laravel Forge home page](https://forge.laravel.com)[x](https://x.com/laravelphp)[github](https://github.com/laravel)[discord](https://discord.com/invite/laravel)[linkedin](https://linkedin.com/company/laravel)[Term of Service](https://forge.laravel.com/terms-of-service)[Privacy Policy](https://forge.laravel.com/privacy-policy)[Data Processing Agreement (DPA)](https://forge.laravel.com/data-processing-agreement)[x](https://x.com/laravelphp)[github](https://github.com/laravel)[discord](https://discord.com/invite/laravel)[linkedin](https://linkedin.com/company/laravel)AssistantResponses are generated using AI and may contain mistakes.