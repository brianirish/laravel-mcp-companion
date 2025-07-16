# Forge - Sites/Security-Rules

*Source: https://forge.laravel.com/docs/sites/security-rules*

---

- [Laravel Forge home page](https://forge.laravel.com)Search...⌘KAsk AI
[Support](/cdn-cgi/l/email-protection#f0969f829795b09c91829186959cde939f9d)
- [Dashboard](https://forge.laravel.com)
- [Dashboard](https://forge.laravel.com)

Search...NavigationSitesSecurity Rules[Documentation](/docs/introduction)[Changelog](/docs/changelog/changelog)- [Community](https://discord.com/invite/laravel)
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

Sites# Security Rules

Configure password protection on your sites.

## [​](#overview)Overview

Forge can configure password protection on your sites using [basic access authentication](https://en.wikipedia.org/wiki/Basic_access_authentication). You can choose whether to protect your entire site or a specific path.

## [​](#managing-security-rules)Managing Security Rules

### [​](#creating-a-security-rule)Creating a Security Rule

You may create a new Security Rule from your site’s management dashboard in Forge. You must supply a security rule name, which some browsers will display in their authentication prompt, as well as at least one set of credentials. If you need to add multiple credentials, you can click the **+** button to add a new username and password combination.

Once you’ve configured your security rule, click the **Add Security Rule** button.

## [​](#credentials)Credentials

Forge creates a unique `.htpasswd` file for each security rule, meaning each secured path may have its own set of credentials. This also means that you will need to re-enter the same credentials when securing multiple paths. If you need to modify the credentials, you can find the `.htpasswd` file at `/etc/nginx/forge-conf/.../server/.htpasswd-{ruleId}` on your servers.

Forge does not store your security Rule passwords on our servers.

## [​](#customization)Customization

Nginx allows you to add further access restrictions such as allowing and denying access to users by IP address. Forge does not provide the ability to configure this, but you are free to customize your own protected site configuration. Forge creates a `/etc/nginx/forge-conf/.../server/protected_site-{ruleId}.conf` configuration file for protected sites. You can read more about Nginx and basic access authentication [in the Nginx documentation](https://docs.nginx.com/nginx/admin-guide/security-controls/configuring-http-basic-authentication/#).

## [​](#circle-permissions)Circle Permissions

You may grant a circle member authority to create and manage security rules by granting the `site:manage-security` permission.

Was this page helpful?

YesNo[Queues](/docs/sites/queues)[Redirects](/docs/sites/redirects)On this page
- [Overview](#overview)
- [Managing Security Rules](#managing-security-rules)
- [Creating a Security Rule](#creating-a-security-rule)
- [Credentials](#credentials)
- [Customization](#customization)
- [Circle Permissions](#circle-permissions)

[Laravel Forge home page](https://forge.laravel.com)[x](https://x.com/laravelphp)[github](https://github.com/laravel)[discord](https://discord.com/invite/laravel)[linkedin](https://linkedin.com/company/laravel)[Term of Service](https://forge.laravel.com/terms-of-service)[Privacy Policy](https://forge.laravel.com/privacy-policy)[Data Processing Agreement (DPA)](https://forge.laravel.com/data-processing-agreement)[x](https://x.com/laravelphp)[github](https://github.com/laravel)[discord](https://discord.com/invite/laravel)[linkedin](https://linkedin.com/company/laravel)AssistantResponses are generated using AI and may contain mistakes.