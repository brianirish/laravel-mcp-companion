# Forge - Sites/User-Isolation

*Source: https://forge.laravel.com/docs/sites/user-isolation*

---

- [Community](https://discord.gg/laravel)
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

##### Other

- [Support](/docs/support)
- [Changelog](/docs/changelog)
- [Abuse](/docs/abuse)

On this page

- [Introduction](#introduction)
- [Sudo access](#sudo-access)
- [Connecting via SFTP](#connecting-via-sftp)

Sites

# User Isolation

Copy page

Learn how to isolate your sites on Laravel Forge.

Copy page

## [​](#introduction) Introduction

By default, Laravel Forge uses the default `forge` user that is created as part of the server’s initial provisioning process for all deployments, daemons, scheduled jobs, PHP-FPM, and other processes.
Via Laravel Forge’s “User Isolation” feature, Forge will create a separate user for a given site. This is particularly useful when combined with a project like WordPress in order to prevent plugins from maliciously accessing content in your `forge` user (or other isolated user) owned directories.

The `forge` user is considered a “super user” and is therefore able to read all files within isolated user directories.

## [​](#sudo-access) Sudo access

Like the `forge` user, newly created isolated users also have limited sudo access. They may reload the PHP-FPM services requiring a password:

Copy

Ask AI

```
sudo -S service php8.5-fpm reload
```

If you need further sudo access, you should log in as the `forge` user and switch to the `root` user using the `sudo su` or the `sudo -i` command.

## [​](#connecting-via-sftp) Connecting via SFTP

You can connect to your server via SFTP as the isolated user. We recommend using an SFTP client such as [Transmit](https://panic.com/transmit/) or [Filezilla](https://filezilla-project.org/). However, before getting started, you should first [upload your SSH key to the server](/docs/ssh) for the isolated user.

Was this page helpful?

YesNo

[Network](/docs/sites/network)[Laravel](/docs/sites/laravel)

⌘I

[x](https://x.com/laravelphp)[github](https://github.com/laravel)[discord](https://discord.com/invite/laravel)[linkedin](https://linkedin.com/company/laravel)