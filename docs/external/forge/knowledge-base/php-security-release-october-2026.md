Source: https://laravel.com/forge/docs/knowledge-base/php-security-release-october-2026.md

# PHP security advisory (CVE-2026-109618, CVE-2026-109619)

> Security advisory for the critical PHP vulnerabilities fixed in the October 21, 2026 PHP security release, and how to patch PHP on Laravel Forge servers.

## Overview

On October 21, 2026, the PHP security team [released](https://www.php.net/archive/2026.php) PHP 8.5.12, 8.4.27, 8.3.36, and 8.2.35. These releases fix two critical vulnerabilities, CVE-2026-109618 and CVE-2026-109619. Both are rated **9.2 under CVSS v4.0**.

> [!WARNING]
>
> Laravel Forge's automatic security updates **do not** patch PHP. Forge installs PHP from a dedicated package repository, and Ubuntu's unattended upgrades only apply updates from Ubuntu's own security repository. You must update PHP on each of your servers yourself, using one of the options below.

## Affected PHP versions

| PHP Version | Fixed Version |
| - | - |
| 8.5 | 8.5.12 |
| 8.4 | 8.4.27 |
| 8.3 | 8.3.36 |
| 8.2 | 8.2.35 |
| 8.1 | 8.1.34, package revision `8.1.34-9` |
| 8.0 | 8.0.30, package revision `1:8.0.30-25` |
| 7.4 | 7.4.33, package revision `1:7.4.33-31` |
| 7.3 | 7.3.33, package revision `7.3.33-35` |
| 7.2 | 7.2.34, package revision `7.2.34-66` |
| 7.1 | 7.1.33, package revision `7.1.33-80` |
| 7.0 | 7.0.33, package revision `7.0.33-92` |
| 5.6 | 5.6.40, package revision `5.6.40-105` |

Both vulnerabilities affect PHP versions dating back to 2004, so every PHP version that Forge can install is vulnerable until it is patched.

PHP 8.1 and earlier have reached end of life, so the PHP team did not publish new releases for them. Instead, Ondřej Surý backported the fixes to these versions as new package revisions. The PHP version number stays the same, so `php -v` reports the same version before and after the update. To confirm that one of these versions is patched, check that the installed package revision matches the table above, or is newer:

```bash theme={null}
dpkg -l 'php8.1*' | awk '/^ii/ {print $2, $3}'
```

These backports are a stopgap rather than a long-term fix, as end-of-life PHP versions do not receive regular security updates. If any of your sites still run PHP 8.1 or earlier, we strongly recommend [installing a supported PHP version](https://forge.laravel.com/docs/servers/php.md#installing-php-versions) and [switching your sites to it](https://forge.laravel.com/docs/sites/the-basics.md#php-versions).

## Where Forge installs PHP from

Forge installs PHP from Ondřej Surý's PHP packages. The package source depends on your server's Ubuntu version:

| Ubuntu Version | Package Source | Available PHP Versions |
| - | - | - |
| 26.04 LTS | `packages.sury.org/php` | 8.4, 8.5 |
| 24.04 LTS | `ppa.setup-php.com` (mirror of the `ondrej/php` PPA) | 5.6 to 8.5 |
| 22.04 LTS | `ppa.setup-php.com` (mirror of the `ondrej/php` PPA) | 5.6 to 8.5 |

Patched packages usually reach these repositories shortly after the upstream release, but they may not be available the moment PHP publishes the release. If the update does not install the fixed version, wait a little while and try again.

## What you need to do

### Step 1: Check your current PHP version

SSH into your server and check the PHP version that each site uses. Replace `8.4` with the version you want to check:

```bash theme={null}
php8.4 -v
```

Make a note of the version displayed so that you can verify the upgrade afterward. To list every PHP version installed on the server, run:

```bash theme={null}
ls /etc/php
```

### Step 2: Update PHP

You may update PHP from the Forge dashboard or manually via SSH. We recommend the Forge dashboard because it also repairs the server's PHP package source before upgrading.

> [!NOTE]
>
> Updating PHP restarts the PHP-FPM service for that version. Sites running that version may experience a few seconds of downtime, so you may want to update during a period of low traffic.

> [tab] Forge dashboard
>
> 1. Navigate to your server's dashboard and click the **PHP** tab.
> 2. Locate the PHP version you want to patch, open its dropdown menu and click **Update PHP X.X**.
> 3. Confirm the update. Forge will upgrade that version's PHP packages to the latest patch release and reload Nginx.
>
> Repeat these steps for every PHP version installed on the server, including versions that your sites do not currently use. These steps are the same on Ubuntu 22.04, 24.04 and 26.04.
>
> If you manage many servers, you may also trigger the update through the [Forge API](https://forge.laravel.com/docs/api-reference/introduction.md) rather than the dashboard.

> [tab] Manually via SSH
>
> First, confirm that your server's PHP package source is configured. The file you should see depends on your Ubuntu version:
>
> | Ubuntu Version | Expected file |
> | - | - |
> | 26.04 LTS | `/etc/apt/sources.list.d/php.list` |
> | 24.04 LTS | `/etc/apt/sources.list.d/ondrej-php.list` |
> | 22.04 LTS | `/etc/apt/sources.list.d/ondrej-php.list` |
>
> ```bash theme={null}
> ls /etc/apt/sources.list.d/
> ```
>
> If the expected file is missing, use the **Forge dashboard** option instead. It reconfigures the package source automatically.
>
> Next, refresh the package lists and check which version will be installed. Replace `8.4` with the version you want to patch:
>
> ```bash theme={null}
> sudo apt-get update
> apt-cache policy php8.4-fpm
> ```
>
> The `Candidate` version should match the fixed version listed in the [Affected PHP versions](#affected-php-versions) table. If it does not, the patched packages have not reached the repository yet, so wait and try again later.
>
> Finally, upgrade every installed package for that PHP version. The `--only-upgrade` flag ensures that no new packages are installed, and the `--force-confold` option keeps your existing `php.ini` and PHP-FPM configuration files:
>
> ```bash theme={null}
> sudo apt-get install --only-upgrade -y \
>   -o Dpkg::Options::="--force-confold" \
>   $(dpkg -l 'php8.4*' | awk '/^ii/ {print $2}')
> ```
>
> Repeat these commands for every PHP version installed on the server. These commands are the same on Ubuntu 22.04, 24.04 and 26.04.

To patch many servers at once, you may create a [Recipe](https://forge.laravel.com/docs/recipes.md) that runs as `root` and contains the manual commands above, then run it against all of your servers.

### Step 3: Restart long-running PHP processes

The package upgrade restarts PHP-FPM. However, long-running PHP processes started from the CLI keep running the old version of PHP until they are restarted. These include queue workers, Laravel Horizon, Laravel Octane, Laravel Reverb, and any other [background processes](https://forge.laravel.com/docs/resources/background-processes.md) you have configured.

Restart these processes after updating PHP. For example, you may run the following in each affected Laravel application:

```bash theme={null}
php artisan queue:restart
php artisan horizon:terminate
php artisan octane:reload
```

If PHP-FPM did not restart automatically, you may restart it from your server's dashboard by opening the actions dropdown and selecting **Restart PHP X.X**.

### Step 4: Verify the fix is active

Run the version check from Step 1 again and confirm that the version shown matches the fixed version in the [Affected PHP versions](#affected-php-versions) table:

```bash theme={null}
php8.4 -v
```

To confirm that PHP-FPM is also running the patched version, run:

```bash theme={null}
php-fpm8.4 -v
```

For PHP 8.1 and earlier, the version number does not change, so check the package revision instead, as described in the [Affected PHP versions](#affected-php-versions) section.

## More information

For the official release announcement and full details of both vulnerabilities, see the PHP news archive at [https://www.php.net/archive/2026.php](https://www.php.net/archive/2026.php). To learn more about managing PHP on your servers, see the [PHP documentation](https://forge.laravel.com/docs/servers/php.md).
