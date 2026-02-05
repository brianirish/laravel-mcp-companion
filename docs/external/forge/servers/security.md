# Forge - Servers/Security

*Source: https://forge.laravel.com/docs/servers/security*

---

[Laravel Forge home page](https://forge.laravel.com)
Search...
⌘KAsk AI
- [Get started](https://forge.laravel.com)
- [Get started](https://forge.laravel.com)
Search...
Navigation
Servers
Root Access / Security
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
- [Overview](#overview)
- [Post-provisioning](#post-provisioning)
- [Security](#security)
- [Automated security updates](#automated-security-updates)
Servers
# Root Access / Security
Copy page
Learn about the security measures Laravel Forge takes to protect your server.
Copy page
## [​](#overview) Overview
During the initial provisioning of your server, Laravel Forge connects as the `root` user over SSH. This is so that Laravel Forge is able to add repositories, install dependencies and configure new services, firewalls, and more.
The provisioning process can take anywhere from a few seconds to 10 minutes when using an external server provider, but will depend on a variety of factors including the speed of your server, the speed of your network connection, and the number of services that need to be installed.
### [​](#post-provisioning) Post-provisioning
After initially provisioning your server, Laravel Forge continues to use root access so that it can manage your server’s software, services, and configuration. For example, root access is needed to manage:
- Background processes
- Firewalls
- PHP configuration and management
- Scheduled tasks
- Website isolation
- Other operating system dependencies
## [​](#security) Security
We take security very seriously and ensure that we do everything we can to protect customer’s data. Below is a brief overview of some of the steps we take to ensure your server’s security:
- Laravel Forge issues a unique SSH key for each server that it connects to
- Password based server SSH connections are disabled during provisioning
- Each server is issued a unique root password
- All ports are blocked by default with UFW, a secure firewall for Ubuntu. We then explicitly open ports: `22` (SSH), `80` (HTTP) and `443` (HTTPS)
- Automated security updates are installed using Ubuntu’s automated security release program
### [​](#automated-security-updates) Automated security updates
Security updates are automatically applied to your server on a weekly basis. Laravel Forge accomplishes this by enabling and configuring Ubuntu’s automated security update service that is built in to the operating system.
Laravel Forge does not automatically update w software such as PHP or MySQL, as doing so could cause your server to suffer downtime if your application’s code is not compatible with the upgrade. However, it is possible to [install new versions](/docs/servers/php#multiple-php-versions) and [patch existing versions of PHP](/docs/servers/php#updating-php-between-patch-releases) manually via the Laravel Forge dashboard.
Was this page helpful?
YesNo
[Nginx Templates](/docs/servers/nginx-templates)[Monitoring](/docs/servers/monitoring)
⌘I