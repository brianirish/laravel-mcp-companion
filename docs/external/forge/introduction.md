# Forge - Introduction

*Source: https://forge.laravel.com/docs/introduction*

---

[Laravel Forge home page![light logo](https://mintcdn.com/forge-laravel/DhXK7kFkCTo-2V2J/logo/logo.svg?fit=max&auto=format&n=DhXK7kFkCTo-2V2J&q=85&s=a66298a7f876f35c44132183267a2cd6)![dark logo](https://mintcdn.com/forge-laravel/DhXK7kFkCTo-2V2J/logo/logo.svg?fit=max&auto=format&n=DhXK7kFkCTo-2V2J&q=85&s=a66298a7f876f35c44132183267a2cd6)](https://forge.laravel.com)

Search...

⌘KAsk AI

- [Get started](https://forge.laravel.com)
- [Get started](https://forge.laravel.com)

Search...

Navigation

Get Started

Welcome to Laravel Forge

[Documentation](/docs/introduction)[Knowledge Base](/docs/knowledge-base/servers)[API Reference](/docs/api-reference/introduction)

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

- [What is Laravel Forge?](#what-is-laravel-forge)
- [Laravel Forge IP addresses](#laravel-forge-ip-addresses)
- [Laravel Forge support jumpbox](#laravel-forge-support-jumpbox)
- [Laravel Forge API](#laravel-forge-api)
- [Legal and compliance](#legal-and-compliance)

Get Started

# Welcome to Laravel Forge

Copy page

A server management and application deployment service for your Laravel applications and beyond.

Copy page

[## Create an account

Create your Laravel Forge account today](https://forge.laravel.com/sign-up)[## Watch more

Watch the free Laravel Forge series on Laracasts](https://laracasts.com/series/learn-laravel-forge-2022-edition/)

## [​](#what-is-laravel-forge) What is Laravel Forge?

Laravel Forge is a server management and application deployment service. Forge takes the pain and hassle out of deploying servers and can be used to launch your next website. Whether your app is built with a framework such as [Laravel](https://github.com/laravel/laravel), [Symfony](https://github.com/symfony/symfony), [Statamic](https://github.com/statamic/cms), [WordPress](https://github.com/WordPress/WordPress), or is a vanilla PHP application - Forge is the solution for you.
We live and breathe PHP here at Laravel Forge, but Forge is also ready to handle other tech stacks too, such as Node.js.
Laravel Forge can provision new servers for you in seconds. We also offer you the ability to provision [multiple server types](/docs/servers/types) (e.g., web servers, database servers, load balancers) with the option of having a variety of services configured for you to hit the ground running, including:

- Nginx web server
- [PHP](/docs/servers/php) (multiple version support)
- [Database](/docs/resources/databases) (MySQL, Postgres, or MariaDB)
- Logrotate
- [Memcached](/docs/resources/caches)
- [Redis](/docs/resources/caches)
- Meilisearch
- [OPcache](/docs/servers/php#opcache)
- [UFW firewall](/docs/resources/network#firewalls)
- [Automatic security updates](/docs/servers/security#automated-security-updates)
- And much more!

In addition, Laravel Forge can assist you in managing [scheduled jobs](/docs/resources/scheduler), [queue workers](/docs/sites/queues), [TLS/SSL certificates](/docs/sites/domains#certificates), and more. After your server has provisioned, you can manage and deploy your web applications using the Forge UI dashboard.

## [​](#laravel-forge-ip-addresses) Laravel Forge IP addresses

In order to provision and communicate with your servers, Laravel Forge requires SSH access to them. If you have set up your servers to restrict SSH access using IP allow lists, you must allow the following Forge IP addresses:

- `159.203.150.232`
- `159.203.150.216`
- `45.55.124.124`
- `165.227.248.218`

You can also access the IP addresses via the following URL: <https://forge.laravel.com/ips-v4.txt>. This is particularly useful if you intend on automating your network or firewall infrastructure.
If you are restricting HTTP traffic, your server must also allow incoming and outgoing traffic from `forge.laravel.com`.

The Laravel Forge IP addresses may change from time to time; however, we will always email you several weeks prior to an IP address change.

### [​](#laravel-forge-support-jumpbox) Laravel Forge support jumpbox

To enable the Laravel Forge Support team to provide more efficient technical assistance, you can optionally allow our support jumpbox IP address to access your server in your firewall settings:

- `129.212.144.126`

## [​](#laravel-forge-api) Laravel Forge API

Laravel Forge provides a powerful API that allows you to manage your servers programmatically, providing access to the vast majority of Forge features. To learn more about the Forge API, check out our [API documentation](https://forge.laravel.com/api-documentation).

## [​](#legal-and-compliance) Legal and compliance

Our [Legal](https://laravel.com/legal) and [Trust Centers](https://trust.laravel.com/?product=forge) provide details on the terms, conditions, and privacy practices for using Laravel Forge.

Was this page helpful?

YesNo

[Laravel Forge CLI](/docs/cli)

⌘I

[x](https://x.com/laravelphp)[github](https://github.com/laravel)[discord](https://discord.com/invite/laravel)[linkedin](https://linkedin.com/company/laravel)