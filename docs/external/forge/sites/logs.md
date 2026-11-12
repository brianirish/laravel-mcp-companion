Source: https://laravel.com/forge/docs/sites/logs.md

# Logs

> Understand and manage logs for your sites in Laravel Forge

## Introduction

Laravel Forge allows you to view a site's log files from within the dashboard.

If your site is a Laravel application, Forge will automatically detect and display the log files located in the `storage/logs` directory.

Both `daily` and `single` log formats are supported, and Forge will automatically read the last updated file.

> [!NOTE]
>
> For performance reasons, Laravel Forge will only return the last 500 lines from a file.

## Logrotate

When provisioning your server, Laravel Forge automatically installs and configures Logrotate on the server to ensure log files don't grow indefinitely and consume excessive disk space.

The configuration files for Logrotate can be found in `/etc/logrotate.d/`. The primary configuration file is located at `/etc/logrotate.conf`.

To view older "rotate" or "compressed" logs, you can use `cat` for non-compressed files or `zcat` for compressed files.
