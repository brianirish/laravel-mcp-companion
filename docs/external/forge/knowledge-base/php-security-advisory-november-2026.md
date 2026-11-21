Source: https://laravel.com/forge/docs/knowledge-base/php-security-advisory-november-2026.md

# PHP security advisory (November 2026)

> Security advisory for the critical PHP vulnerabilities fixed in PHP 8.5.13, 8.4.28, 8.3.37, and 8.2.36, and how to patch PHP on Laravel Forge servers.

## Overview

The PHP security team has released PHP 8.5.13, 8.4.28, 8.3.37, and 8.2.36. These releases fix seven critical vulnerabilities, each rated **9.2 under CVSS v4.0**, along with four high-severity vulnerabilities. Several of the critical vulnerabilities can lead to remote code execution.

Most of these vulnerabilities are only exploitable under specific configurations, but some of them affect default PHP setups. We recommend updating every PHP version on every server.

> [!WARNING]
>
> Laravel Forge's automatic security updates **do not** patch PHP. Forge installs PHP from a dedicated package repository, and Ubuntu's unattended upgrades only apply updates from Ubuntu's own security repository. You must update PHP on each of your servers yourself, using one of the options below.

## Affected PHP versions

| PHP Version | Fixed Version |
| - | - |
| 8.5 | 8.5.13 |
| 8.4 | 8.4.28 |
| 8.3 | 8.3.37 |
| 8.2 | 8.2.36 |
| 8.1 | 8.1.34, package revision `8.1.34-13` |
| 8.0 | 8.0.30, package revision `1:8.0.30-30` |
| 7.4 | 7.4.33, package revision `1:7.4.33-36` |
| 7.3 | 7.3.33, package revision `7.3.33-40` |
| 7.2 | 7.2.34, package revision `7.2.34-69` |
| 7.1 | 7.1.33, package revision `7.1.33-84` |
| 7.0 | 7.0.33, package revision `7.0.33-96` |
| 5.6 | 5.6.40, package revision `5.6.40-108` |

PHP 8.1 and earlier have reached end of life, so the PHP team did not publish new releases for them. Instead, Ondřej Surý backported the fixes to these versions as new package revisions. The PHP version number stays the same, so `php -v` reports the same version before and after the update. To confirm that one of these versions is patched, check that the installed package revision matches the table above, or is newer:

```bash theme={null}
dpkg -l 'php8.1*' | awk '/^ii/ {print $2, $3}'
```

These backports are a stopgap rather than a long-term fix, as end-of-life PHP versions do not receive regular security updates. If any of your sites still run PHP 8.1 or earlier, we strongly recommend [installing a supported PHP version](https://forge.laravel.com/docs/servers/php.md#installing-php-versions) and [switching your sites to it](https://forge.laravel.com/docs/sites/the-basics.md#php-versions).

## Vulnerabilities

### Critical

| CVE | Vulnerability | PHP Versions | When it is exploitable |
| - | - | - | - |
| CVE-2026-129289 | PHP-FPM request smuggling, allowing unauthenticated remote code execution | 8.2 to 8.5 | The web server keeps FastCGI connections open between requests, and the application opens the request body without reading all of it |
| CVE-2026-129496 | Use-after-free in the timezone cache, which can lead to code execution | 8.2 to 8.5 | PHP logs errors to a file and a warning is raised at startup. A crafted request can crash a PHP-FPM worker |
| CVE-2026-126714 | Session files partly overwritten, which can lead to code execution | 8.2 to 8.5 | The application uses file-based sessions (PHP's default), a session write is interrupted, and the application contains an exploitable class |
| CVE-2026-115560 | Session serializer mismatch | 8.2 to 8.5 | `session.upload_progress` is enabled and a non-default session serializer is configured |
| CVE-2026-129481 | Use-after-free after an interrupted session shutdown | 8.3 to 8.5 | A fatal error occurs inside a session callback |
| CVE-2026-129474 | Use-after-free in magic method backtraces, allowing unauthenticated code execution | 8.5 | `zend.exception_ignore_args` is set to `Off` |
| CVE-2026-129182 | Use-after-free in fatal error backtraces, caused by an incomplete fix in the October 2026 release | 8.5 | Specific combinations of PHP settings |

### High severity

* A local privilege escalation in PHP-FPM.
* A PHAR signature verification bypass.
* URLs with a mixed-case scheme, such as `HTTPS://`, being sent in plaintext.
* A denial of service through folded HTTP headers.

## Where Forge installs PHP from

Forge installs PHP from Ondřej Surý's PHP packages. The package source depends on your server's Ubuntu version:

| Ubuntu Version | Package Source | Available PHP Versions |
| - | - | - |
| 26.04 LTS | `packages.sury.org/php` | 8.3 to 8.5 |
| 24.04 LTS | `ppa.setup-php.com` (mirror of the `ondrej/php` PPA) | 7.0 to 8.5 |
| 22.04 LTS | `ppa.setup-php.com` (mirror of the `ondrej/php` PPA) | 7.0 to 8.5 |

Patched packages usually reach these repositories shortly after the upstream release, but they may not be available the moment PHP publishes the release. For this release, packages for Ubuntu 22.04 and 24.04 took several hours to reach the `ppa.setup-php.com` mirror.

### Patch status by Ubuntu version

Patched PHP packages are now available for every supported Ubuntu version on both x86 and ARM servers:

| Ubuntu Version | x86 (amd64) | ARM (arm64) |
| - | - | - |
| 26.04 LTS | **Patched** | **Patched** |
| 24.04 LTS | **Patched** | **Patched** |
| 22.04 LTS | **Patched** | **Patched** |
| 20.04 LTS and earlier | **Not patched** | **Not patched** |

To check your server's architecture, run:

```bash theme={null}
dpkg --print-architecture
```

If your server runs Ubuntu 20.04 or earlier, these versions have reached end of life and will not receive a fix, so we recommend [creating a new server](https://forge.laravel.com/docs/servers/the-basics.md) on a supported Ubuntu version and migrating your sites to it.

## Checking your exposure

The steps below help you understand how exposed your servers are before you patch. They do not replace the update: every server running PHP 8.2 or later should be updated, regardless of these results.

### FastCGI connection reuse

The PHP-FPM request smuggling vulnerability (CVE-2026-129289) is fully exploitable when Nginx keeps FastCGI connections open between requests. Check whether any of your Nginx configuration files enable this option:

```bash theme={null}
sudo grep -rn "fastcgi_keep_conn" /etc/nginx/
```

If the command returns a line containing `fastcgi_keep_conn on;`, remove that line from the site's Nginx configuration file and update PHP as soon as possible. If you use [Nginx templates](https://forge.laravel.com/docs/servers/nginx-templates.md), remove the line from those templates as well so that new sites do not inherit it.

### Session upload progress

The session serializer mismatch (CVE-2026-115560) requires `session.upload_progress` to be enabled. PHP installations created by Forge since October 31, 2026 disable this option by default, but older installations may still have it enabled. Check every installed PHP version with:

```bash theme={null}
grep -rn "session.upload_progress.enabled" /etc/php/*/fpm/
```

### Exception arguments

The magic method backtrace vulnerability (CVE-2026-129474) only affects PHP 8.5 when `zend.exception_ignore_args` is set to `Off`. Check the PHP-FPM configuration with:

```bash theme={null}
grep -rn "zend.exception_ignore_args" /etc/php/8.5/fpm/
```

## What you need to do

### Step 1: Check your current PHP version

SSH into your server and run the following command. It checks every PHP version installed on the server and prints the version used by both the CLI and PHP-FPM, along with the installed package version:

```bash theme={null}
for v in $(ls /etc/php); do
  cli=$(php$v -r 'echo PHP_VERSION;' 2>/dev/null || echo "not installed")
  fpm=$(php-fpm$v -v 2>/dev/null | awk 'NR==1 {print $2}')
  pkg=$(dpkg-query -W -f='${Version}' php$v-cli 2>/dev/null | sed 's/^[0-9]*://; s/+.*//')
  echo "PHP $v: CLI ${cli}, FPM ${fpm:-not installed}, package ${pkg:-unknown}"
done
```

The output looks similar to the following:

```text theme={null}
PHP 8.1: CLI 8.1.34, FPM 8.1.34, package 8.1.34-9
PHP 8.4: CLI 8.4.27, FPM 8.4.27, package 8.4.27-1
```

Make a note of the versions displayed so that you can verify the upgrade afterward.

### Step 2: Update PHP

You may update PHP from the Forge dashboard or manually via SSH. We recommend the Forge dashboard because it also repairs the server's PHP package source before upgrading.

If the update does not install the fixed version listed in the [Affected PHP versions](#affected-php-versions) table, run the update again. If it still does not install the fixed version, contact support.

> [!NOTE]
>
> Updating PHP restarts the PHP-FPM service for that version. Sites running that version may experience a few seconds of downtime, so you may want to update during a period of low traffic.

> [tab] Forge dashboard
>
> 1. Navigate to your server in the Forge dashboard and open **Runtime** > **PHP**.
> 2. Click the **...** menu next to the PHP version you want to patch.
> 3. Click **Update PHP X.X** and confirm the update.
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

Run the command from [Step 1](#step-1-check-your-current-php-version) again. For PHP 8.2 and later, confirm that the CLI and FPM versions match the fixed versions in the [Affected PHP versions](#affected-php-versions) table. For PHP 8.1 and earlier, the version number does not change, so confirm that the package version matches the package revision in the same table, or is newer.

## More information

For the official release announcement, see the PHP news archive at [https://www.php.net/archive/2026.php](https://www.php.net/archive/2026.php). To learn more about managing PHP on your servers, see the [PHP documentation](https://forge.laravel.com/docs/servers/php.md).
