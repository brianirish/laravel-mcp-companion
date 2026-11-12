Source: https://laravel.com/forge/docs/introduction.md

# Welcome to Laravel Forge

> A server management and application deployment service for your Laravel applications and beyond.

> [card] [Create an account](https://forge.laravel.com/sign-up)
>
> Create your Laravel Forge account today

> [card] [Watch more](https://laracasts.com/series/learn-laravel-forge-2022-edition/)
>
> Watch the free Laravel Forge series on Laracasts

## What is Laravel Forge?

Laravel Forge is a server management and application deployment service. Forge takes the pain and hassle out of deploying servers and can be used to launch your next website. Whether your app is built with a framework such as [Laravel](https://github.com/laravel/laravel), [Symfony](https://github.com/symfony/symfony), [Statamic](https://github.com/statamic/cms), [WordPress](https://github.com/WordPress/WordPress), or is a vanilla PHP application - Forge is the solution for you.

We live and breathe PHP here at Laravel Forge, but Forge is also ready to handle other tech stacks too, such as Node.js.

Laravel Forge can provision new servers for you in seconds. We also offer you the ability to provision [multiple server types](https://forge.laravel.com/docs/servers/types.md) (e.g., web servers, database servers, load balancers) with the option of having a variety of services configured for you to hit the ground running, including:

* Nginx web server

* [PHP](https://forge.laravel.com/docs/servers/php.md) (multiple version support)

* [Database](https://forge.laravel.com/docs/resources/databases.md) (MySQL, Postgres, or MariaDB)

* Logrotate

* [Memcached](https://forge.laravel.com/docs/resources/caches.md)

* [Redis](https://forge.laravel.com/docs/resources/caches.md)

* Meilisearch

* [OPcache](https://forge.laravel.com/docs/servers/php.md#opcache)

* [UFW firewall](https://forge.laravel.com/docs/resources/network.md#firewalls)

* [Automatic security updates](https://forge.laravel.com/docs/servers/security.md#automated-security-updates)

* And much more!

In addition, Laravel Forge can assist you in managing [scheduled jobs](https://forge.laravel.com/docs/resources/scheduler.md), [queue workers](https://forge.laravel.com/docs/sites/queues.md), [TLS/SSL certificates](https://forge.laravel.com/docs/sites/domains.md#certificates), and more. After your server has provisioned, you can manage and deploy your web applications using the Forge UI dashboard.

## Laravel Forge IP addresses

In order to provision and communicate with your servers, Laravel Forge requires SSH access to them. If you have set up your servers to restrict SSH access using IP allow lists, you must allow the following Forge IP addresses:

* `159.203.150.232`
* `159.203.150.216`
* `45.55.124.124`
* `165.227.248.218`

You can also access the IP addresses via the following URL: [https://forge.laravel.com/ips-v4.txt](https://forge.laravel.com/ips-v4.txt). This is particularly useful if you intend on automating your network or firewall infrastructure.

If you are restricting HTTP traffic, your server must also allow incoming and outgoing traffic from `forge.laravel.com`.

> [!TIP]
>
> The Laravel Forge IP addresses may change from time to time; however, we will always email you several weeks prior to an IP address change.

#### Forge Terminal

Laravel VPS customers benefit from an [integrated terminal](https://forge.laravel.com/docs/servers/laravel-vps.md#forge-terminal) within the Forge Control Panel. To ensure this is functional, you must allow the following IP:

* `142.93.78.212`

### Laravel Forge support jumpbox

To enable the Laravel Forge Support team to provide more efficient technical assistance, you can optionally allow our support jumpbox IP address to access your server in your firewall settings:

* `129.212.144.126`

## Laravel Forge API

Laravel Forge provides a powerful API that allows you to manage your servers programmatically, providing access to the vast majority of Forge features. To learn more about the Forge API, check out our [API documentation](https://forge.laravel.com/api-documentation).

## Legal and compliance

Our [Legal](https://laravel.com/legal) and [Trust Centers](https://trust.laravel.com/?product=forge) provide details on the terms, conditions, and privacy practices for using Laravel Forge.
