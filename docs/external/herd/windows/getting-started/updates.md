Source: https://herd.laravel.com/docs/windows/getting-started/updates.md

# Updates

# Updating Herd

Herd asks you if you want to check for updates automatically when you open it for the first time.
When enabled, Herd regularly checks for updates in the background and notifies you when a new version is available.
You can change this configuration in the "General" tab of the preferences window.

You can also manually check for updates by clicking on the update icon in the context menu of the Herd system tray icon. This checks for Herd, PHP and Node.js updates at the same time.

The coding tools of [Herd Studio](https://herd.laravel.com/docs/windows/herd-studio/overview.md) update independently from Herd in the background. Learn more in [Herd Studio updates](https://herd.laravel.com/docs/windows/herd-studio/overview.md#updates).

## Updating PHP versions

Herd allows you to download and install different PHP versions with a single click.
When a new PHP version is available, Herd automatically detects the new version and shows a notification.

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

## Laravel Installer

You can create new Laravel applications via the `laravel` command line utility or the [Applications window](https://herd.laravel.com/docs/windows/sites/managing-sites.md).

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

## Updating Node.js versions

Herd ships with [nvm](https://github.com/nvm-sh/nvm) and allows you to install and update multiple Node.js versions at the same time. Officially, Herd supports the latest versions of the following major versions:

* 24.x
* 22.x
* 20.x
* 18.x
* 16.x

However, you may manually install any available Node.js version via the [CLI](https://herd.laravel.com/docs/windows/technology/node-versions.md#via-the-cli).

If you want to learn more about Node.js versions and their management in Herd, go to [Manage Node.js versions](https://herd.laravel.com/docs/windows/technology/node-versions.md).
