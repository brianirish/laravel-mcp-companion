Source: https://herd.laravel.com/docs/macos/technology/php-versions.md

# Manage PHP

# Using different PHP versions

Herd ships with the latest stable PHP version by default. Currently, that's PHP 8.5.
However, you may install and use different PHP versions for your sites and configure Herd that every project uses the version that it needs.

## Using different PHP versions via the GUI

You can manage your PHP versions in the "PHP" tab of the preferences window. This window allows you to install and update PHP versions with a single click.


In order to change the global PHP version that Herd uses by default, select it in the dropdown menu in the menu bar.


Herd uses the global PHP version for all sites that are not [isolated](#per-site-php-versions).

## Using different PHP versions via the CLI

If you prefer to use the CLI, you can use the `herd use` command to set the global PHP version.

```shell theme={null}
herd use 8.2
```

### Installing and updating PHP versions via the CLI

You can list all available PHP versions and their status with `herd php:list`:

```shell theme={null}
herd php:list
```

To install a new PHP version:

```shell theme={null}
herd php:install 8.3
```

To update an installed PHP version to the latest patch release:

```shell theme={null}
herd php:update 8.4
```

# Per-site PHP versions

By default, Herd uses the global PHP version to serve all your sites. However, if you need to support different PHP versions for different sites, you may use the isolate function.  This configures Herd to use a specific PHP version for a site, regardless of the global PHP version.

## Per site PHP versions via the GUI

You can configure the PHP version per site in the [Applications window](https://herd.laravel.com/docs/macos/sites/managing-sites.md). Select a site and choose the PHP version in the "Environment" section of the inspector.


## Per site PHP versions via the CLI

If you prefer to use the CLI, you can use the `herd isolate` command to specify which PHP version a particular site should use.
The `isolate` command configures Herd to use the specified PHP version for the site located in your current working directory:

```shell theme={null}
cd ~/Herd/example-site

herd isolate 8.0
```

If your site name does not match the name of the directory that contains it, you may specify the name using the `--site` option:

```shell theme={null}
herd isolate 8.0 --site="site-name"
```

For convenience, you may use the `herd php`, `composer`, and `which-php` commands to proxy calls to the appropriate PHP CLI or tool based on the configured PHP version for the current directly and site:

```shell theme={null}
herd php
herd composer
herd which-php
```

You may execute the `isolated` command to display a list of all of your isolated sites and their PHP and Node.js versions:

```shell theme={null}
herd isolated
```

To revert a site back to Herd's globally installed PHP version, you may invoke the `unisolate` command from the root directory of the site:

```shell theme={null}
herd unisolate
```

## Uninstalling PHP versions

You can uninstall PHP versions from the PHP settings. Simply right-click on a version and delete it via the context menu.


If you prefer deleting a PHP version manually, you can go into the Herd application directory and delete the files from your system. Once you reopen the settings, you can reinstall them.

```
~/Library/Application Support/Herd/bin
```
