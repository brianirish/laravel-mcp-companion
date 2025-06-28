# Forge - Introduction

*Source: https://forge.laravel.com/docs/introduction*

---

- [Laravel Forge home page](https://forge.laravel.com)Search...⌘KAsk AI
[Support](/cdn-cgi/l/email-protection#b5d3dac7d2d0f5d9d4c7d4c3d0d99bd6dad8)
- [Dashboard](https://forge.laravel.com)
- [Dashboard](https://forge.laravel.com)

Search...NavigationGet StartedIntroduction[Documentation](/docs/introduction)[Changelog](/docs/changelog/changelog)- [Community](https://discord.com/invite/laravel)
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

Get Started# Introduction

Laravel Forge is a server management and application deployment service.

[## Create An Account

Create your Forge account today

](https://forge.laravel.com/auth/register)[## Watch More

Watch the free Forge series on Laracasts

](https://laracasts.com/series/learn-laravel-forge-2022-edition/)
## [​](#what-is-forge%3F)What is Forge?

Laravel Forge is a server management and application deployment service. Forge takes the pain and hassle out of deploying servers and can be used to launch your next website. Whether your app is built with a framework such as [Laravel](https://github.com/laravel/laravel), [Symfony](https://github.com/symfony/symfony), [Statamic](https://github.com/statamic/cms), [WordPress](https://github.com/WordPress/WordPress), or is a vanilla PHP application - Forge is the solution for you.

We live and breathe PHP here at Forge, but Forge is also ready to handle other tech stacks too, such as Node.js.

After connecting to your preferred [server provider](/docs/servers/providers), Forge will be able to provision new servers for you in minutes. We offer you the ability to provision [multiple server types](/docs/servers/types) (e.g. web servers, database servers, load balancers) with the option of having an array of services configured for you to hit the ground running, including:

- 
Nginx web server

- 
[PHP](/docs/servers/php) (multiple version support)

- 
[Database](/docs/resources/databases) (MySQL, Postgres, or MariaDB)

- 
Logrotate

- 
[UFW Firewall](/docs/resources/network#firewalls)

- 
[OPcache](/docs/servers/php#opcache)

- 
[Memcached](/docs/resources/caches)

- 
[Redis](/docs/resources/caches)

- 
MeiliSearch

- 
[Automatic Security Updates](/docs/servers/provisioning-process#automated-security-updates)

- 
And much more!

In addition, Forge can assist you in managing [scheduled jobs](/docs/resources/scheduler), [queue workers](/docs/sites/queues), [TLS/SSL certificates](/docs/sites/ssl), and more. After your server has provisioned, you can manage and deploy your web applications using the Forge UI dashboard.

## [​](#forge-ip-addresses)Forge IP Addresses

In order to provision and communicate with your servers, Forge requires SSH access to them. If you have set up your servers to restrict SSH access using IP allow lists, you must allow the following Forge IP addresses:

- 
`159.203.150.232`

- 
`159.203.150.216`

- 
`45.55.124.124`

- 
`165.227.248.218`

You can also access the IP addresses via the following URL: [https://forge.laravel.com/ips-v4.txt](https://forge.laravel.com/ips-v4.txt). This is particularly useful if you intend on automating your network or firewall infrastructure.

If you are restricting HTTP traffic, your server must also allow incoming and outgoing traffic from `forge.laravel.com`.

The Forge IP addresses may change from time to time; however, we will always email you several weeks prior to an IP address change.

### [​](#forge-support-jumpbox)Forge Support Jumpbox

To enable the Forge Support team to provide more efficient technical assistance, you can also optionally allow our support jumpbox IP address to access your server in your firewall settings:

- `129.212.144.126`

## [​](#forge-%26-envoyer-integration)Forge & Envoyer Integration

[](https://blog.laravel.com/forge-zero-downtime-deployments)

Forge now offers [zero downtime deployments](https://blog.laravel.com/forge-zero-downtime-deployments), thanks to a seamless first-party integration with [Envoyer](https://envoyer.io).

## [​](#forge-api)Forge API

Forge provides a powerful API that allows you to manage your servers programatically, providing access to the vast majority of Forge features. You can find the Forge API documentation [here](https://forge.laravel.com/api-documentation).

## [​](#legal-and-compliance)Legal and Compliance

Our [Terms of Service](https://forge.laravel.com/terms-of-service), [Privacy Policy](https://forge.laravel.com/privacy-policy) and [Data Processing Agreement (DPA)](https://forge.laravel.com/data-processing-agreement), provide details on the terms, conditions, and privacy practices for using Laravel Forge.

Was this page helpful?

YesNo[Forge CLI](/docs/cli)On this page
- [What is Forge?](#what-is-forge%3F)
- [Forge IP Addresses](#forge-ip-addresses)
- [Forge Support Jumpbox](#forge-support-jumpbox)
- [Forge & Envoyer Integration](#forge-%26-envoyer-integration)
- [Forge API](#forge-api)
- [Legal and Compliance](#legal-and-compliance)

[Laravel Forge home page](https://forge.laravel.com)[x](https://x.com/laravelphp)[github](https://github.com/laravel)[discord](https://discord.com/invite/laravel)[linkedin](https://linkedin.com/company/laravel)[Term of Service](https://forge.laravel.com/terms-of-service)[Privacy Policy](https://forge.laravel.com/privacy-policy)[Data Processing Agreement (DPA)](https://forge.laravel.com/data-processing-agreement)[x](https://x.com/laravelphp)[github](https://github.com/laravel)[discord](https://discord.com/invite/laravel)[linkedin](https://linkedin.com/company/laravel)AssistantResponses are generated using AI and may contain mistakes.