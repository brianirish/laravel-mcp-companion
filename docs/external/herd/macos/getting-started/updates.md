Source: https://herd.laravel.com/docs/macos/getting-started/updates.md

# Updates

# Herd Updates

Herd regularly checks for new updates in the background and notifies you when a new version is available. You can disable the updater in the settings if you prefer to do that manually but we recommend to always keep Herd up to date.

To manually check for updates, click the "Check for Updates" button in the Herd menu in the macOS menu bar. This checks for Herd, PHP and Node.js updates at the same time.

The coding tools of [Herd Studio](https://herd.laravel.com/docs/macos/herd-studio/overview.md) update independently from Herd in the background. Learn more in [Herd Studio updates](https://herd.laravel.com/docs/macos/herd-studio/overview.md#updates).

## PHP versions

Herd allows you to download and install different PHP versions with a single click.
When a new PHP version is available, Herd notifies you about the update in the menu bar.

Minor PHP patch versions in Herd can lag a few days behind their official release because they get tested extensively after they've been compiled specifically for Herd.

You can choose the PHP versions which you want to install or update in the "PHP" tab of the preferences.

The supported PHP versions are:

* 8.6
* 8.5
* 8.4 (default)
* 8.3
* 8.2
* 8.1
* 8.0
* 7.4

If you want to learn more about PHP versions and their management in Herd, go to [Manage PHP versions](https://herd.laravel.com/docs/macos/technology/php-versions.md).

## Laravel Installer

You can create new Laravel applications via the `laravel` command line utility or the [Applications window](https://herd.laravel.com/docs/macos/sites/managing-sites.md).

While Herd always ships with the latest version of the Laravel CLI, you may want to update in between Herd updates if there's a nightly change.
You can install this update via the PHP Settings tab.


## Composer and Expose

Herd bundles the version of Composer and Expose that was current when that Herd release was built, and newer versions usually arrive with the next Herd update.

When a newer version is released before that – for example a Composer security fix – you don't have to wait for a Herd update. Run their built-in `self-update` commands to get the latest version right away:

```bash theme={null}
composer self-update
expose self-update
```

If you run Composer through Herd's isolated PHP, use `herd composer self-update` instead.

## Node.js versions

Herd ships with [nvm](https://github.com/nvm-sh/nvm) and allows you to install and use multiple Node.js versions at the same time. Officially, Herd supports the latest versions of the following major versions:

* 24.x
* 22.x
* 20.x
* 18.x
* 16.x

However, you may manually install any available Node.js version via the [CLI](https://herd.laravel.com/docs/macos/technology/node-versions.md#via-the-cli).

If you want to learn more about Node.js versions and their management in Herd, go to [Manage Node.js versions](https://herd.laravel.com/docs/macos/technology/node-versions.md).
