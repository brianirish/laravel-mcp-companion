Source: https://laravel.com/forge/docs/servers/security.md

# Root Access / Security

> Learn about the security measures Laravel Forge takes to protect your server.

## Overview

During the initial provisioning of your server, Laravel Forge connects as the `root` user over SSH. This is so that Laravel Forge is able to add repositories, install dependencies and configure new services, firewalls, and more.

The provisioning process can take anywhere from a few seconds to 10 minutes when using an external server provider, but will depend on a variety of factors including the speed of your server, the speed of your network connection, and the number of services that need to be installed.

### Post-provisioning

After initially provisioning your server, Laravel Forge continues to use root access so that it can manage your server's software, services, and configuration. For example, root access is needed to manage:

* Background processes
* Firewalls
* PHP configuration and management
* Scheduled tasks
* Website isolation
* Other operating system dependencies

## Security

We take security very seriously and ensure that we do everything we can to protect customer's data. Below is a brief overview of some of the steps we take to ensure your server's security:

* Laravel Forge issues a unique SSH key for each server that it connects to
* Password based server SSH connections are disabled during provisioning
* Each server is issued a unique root password
* All ports are blocked by default with UFW, a secure firewall for Ubuntu. We then explicitly open ports: `22` (SSH), `80` (HTTP) and `443` (HTTPS)
* Automated security updates are installed using Ubuntu's automated security release program

### Automated security updates

Security updates are automatically applied to your server on a weekly basis. Laravel Forge accomplishes this by enabling and configuring Ubuntu's automated security update service that is built in to the operating system.

Laravel Forge does not automatically update w software such as PHP or MySQL, as doing so could cause your server to suffer downtime if your application's code is not compatible with the upgrade. However, it is possible to [install new versions](https://forge.laravel.com/docs/servers/php.md#multiple-php-versions) and [patch existing versions of PHP](https://forge.laravel.com/docs/servers/php.md#updating-php-between-patch-releases) manually via the Laravel Forge dashboard.
