# Forge - Servers/Provisioning-Process

*Source: https://forge.laravel.com/docs/servers/provisioning-process*

---

- [Laravel Forge home page](https://forge.laravel.com)Search...⌘KAsk AI
[Support](/cdn-cgi/l/email-protection#85e3eaf7e2e0c5e9e4f7e4f3e0e9abe6eae8)
- [Dashboard](https://forge.laravel.com)
- [Dashboard](https://forge.laravel.com)

Search...NavigationServersRoot Access / Security[Documentation](/docs/introduction)[Changelog](/docs/changelog/changelog)- [Community](https://discord.com/invite/laravel)
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

Servers# Root Access / Security

Learn about the security measures Forge takes to protect your server.

## [​](#provisioning)Provisioning

During the initial provisioning of your server, Forge will connect as the `root` user over SSH. This is so that Forge is able to add repositories, install dependencies and configure new services, firewalls, and more.

The provisioning process can take upwards of 15 minutes, but will depend on a variety of factors including the speed of your server, the speed of your network connection, and the number of services that need to be installed.

### [​](#post-provisioning)Post-Provisioning

After initially provisioning your server, Forge continues to use root access so that it can manage your server’s software, services, and configuration. For example, root access is needed to manage:

- Firewalls

- Daemons

- Scheduled tasks

- Isolated users

- PHP configuration and management

- Other operating system dependencies

## [​](#security)Security

We take security very seriously and ensure that we do everything we can to protect customer’s data. Below is a brief overview of some of the steps we take to ensure your server’s security:

- Forge issues a unique SSH key for each server that it connects to.

- Password based server SSH connections are disabled during provisioning.

- Each server is issued a unique root password.

- All ports are blocked by default with UFW, a secure firewall for Ubuntu. We then explicitly open ports: 22 (SSH), 80 (HTTP) and 443 (HTTPS).

- Automated security updates are installed using Ubuntu’s automated security release program.

### [​](#automated-security-updates)Automated Security Updates

Security updates are automatically applied to your server on a weekly basis. Forge accomplishes this by enabling and configuring Ubuntu’s automated security update service that is built in to the operating system.

Forge does not automatically update other software such as PHP or MySQL, as doing so could cause your server to suffer downtime if your application’s code is not compatible with the upgrade. However, it is possible to [install new versions](/docs/servers/php#multiple-php-versions) and [patch existing versions of PHP](/docs/servers/php#updating-php-between-patch-releases) manually via the Forge UI.

Was this page helpful?

YesNo[Management](/docs/servers/management)[SSH Keys / Git Access](/docs/servers/ssh)On this page
- [Provisioning](#provisioning)
- [Post-Provisioning](#post-provisioning)
- [Security](#security)
- [Automated Security Updates](#automated-security-updates)

[Laravel Forge home page](https://forge.laravel.com)[x](https://x.com/laravelphp)[github](https://github.com/laravel)[discord](https://discord.com/invite/laravel)[linkedin](https://linkedin.com/company/laravel)[Term of Service](https://forge.laravel.com/terms-of-service)[Privacy Policy](https://forge.laravel.com/privacy-policy)[Data Processing Agreement (DPA)](https://forge.laravel.com/data-processing-agreement)[x](https://x.com/laravelphp)[github](https://github.com/laravel)[discord](https://discord.com/invite/laravel)[linkedin](https://linkedin.com/company/laravel)AssistantResponses are generated using AI and may contain mistakes.