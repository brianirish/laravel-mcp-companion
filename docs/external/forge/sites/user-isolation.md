# Forge - Sites/User-Isolation

*Source: https://forge.laravel.com/docs/sites/user-isolation*

---

- [Laravel Forge home page](https://forge.laravel.com)Search...⌘KAsk AI
[Support](/cdn-cgi/l/email-protection#177178657072577b76657661727b3974787a)
- [Dashboard](https://forge.laravel.com)
- [Dashboard](https://forge.laravel.com)

Search...NavigationSitesUser Isolation[Documentation](/docs/introduction)[Changelog](/docs/changelog/changelog)- [Community](https://discord.com/invite/laravel)
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

Sites# User Isolation

Learn how to isolate your sites on Laravel Forge.

## [​](#overview)Overview

By default, Forge uses the default `forge` user that is created as part of the server’s initial provisioning process for all deployments, daemons, scheduled jobs, PHP-FPM, and other processes.

Via Forge’s “User Isolation” feature, Forge will create a separate user for a given site. This is particularly useful when combined with a project like WordPress in order to prevent plugins from maliciously accessing content in your `forge` user (or other isolated user) owned directories.

The `forge` user is considered a “super user” and is therefore able to read all files within isolated user directories.

## [​](#sudo-access)Sudo Access

Like the `forge` user, newly created isolated users also have limited sudo access. They may reload the PHP-FPM services requiring a password:

CopyAsk AI```
sudo -S service php8.1-fpm reload

```

If you need further sudo access, you should log in as the `forge` user and switch to the `root` user using the `sudo su` or the `sudo -i` command.

## [​](#connecting-via-sftp)Connecting Via SFTP

You can connect to your server via SFTP as the isolated user. We recommend using an SFTP client such as [Transmit](https://panic.com/transmit/) or [Filezilla](https://filezilla-project.org/). However, before getting started, you should first [upload your SSH key to the server](/docs/accounts/ssh) for the isolated user.

Was this page helpful?

YesNo[SSL](/docs/sites/ssl)[Cookbook](/docs/sites/cookbook)On this page
- [Overview](#overview)
- [Sudo Access](#sudo-access)
- [Connecting Via SFTP](#connecting-via-sftp)

[Laravel Forge home page](https://forge.laravel.com)[x](https://x.com/laravelphp)[github](https://github.com/laravel)[discord](https://discord.com/invite/laravel)[linkedin](https://linkedin.com/company/laravel)[Term of Service](https://forge.laravel.com/terms-of-service)[Privacy Policy](https://forge.laravel.com/privacy-policy)[Data Processing Agreement (DPA)](https://forge.laravel.com/data-processing-agreement)[x](https://x.com/laravelphp)[github](https://github.com/laravel)[discord](https://discord.com/invite/laravel)[linkedin](https://linkedin.com/company/laravel)AssistantResponses are generated using AI and may contain mistakes.