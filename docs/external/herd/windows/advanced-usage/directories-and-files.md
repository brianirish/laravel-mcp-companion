Source: https://herd.laravel.com/docs/windows/advanced-usage/directories-and-files.md

# Directories and Files

# Herd Directories and Files

You may find the following files and directories helpful while you are troubleshooting issues with Herd.

## Herd application

The files of the application are at this location.

```bash theme={null}
C:\Program Files\herd
```

## Main directory

The main directory contains all the following config files and directories and is a good start when troubleshooting issues with Herd. You may delete this folder if you plan to re-install Herd from scratch.

```bash theme={null}
%USERPROFILE%\.config\herd
```

## Binaries

You can find all binaries of Herd in this directory. This includes binaries like composer or expose that ship with Herd and also downloaded binaries like the latest PHP versions.

```bash theme={null}
%USERPROFILE%\.config\herd\bin
```

### Tools

Herd keeps the coding tools of [Herd Studio](https://herd.laravel.com/docs/windows/herd-studio/overview.md), like opencode and the Herd Devtools helper, in this directory. Herd updates the Herd Studio tools independently from the app.

```bash theme={null}
%USERPROFILE%\.config\herd\bin\tools
```

## Herd Studio

The Herd Studio interface and the data of your agent sessions live in these directories.

```bash theme={null}
%USERPROFILE%\.config\herd\herd-ai-widget
%USERPROFILE%\.config\herd\devtools
```

## Config

All config files for all Herd services live in this directory. You can open it via "Open Configuration Files" in the Herd menu in the system tray: right-click the open menu and select "Show Advanced Details", or press the `Alt` key, to reveal this entry.

```bash theme={null}
%USERPROFILE%\.config\herd\config
```

The `herd.json` file in this directory contains the settings that Herd shares between the app and the CLI.

### nginx

The nginx directory contains a `herd.conf` and the `nginx.conf`. Herd uses both to decide which sites is serves and what happens to files. In case that you see a `Bad Gateway` error, there could be an issue in one of these files.

```bash theme={null}
%USERPROFILE%\.config\herd\config\nginx
```

Site-specific Nginx configuration files are located in the following directory:

```bash theme={null}
%USERPROFILE%\.config\herd\config\valet\Nginx
```

### Workspaces

Herd keeps track of all [workspaces](https://herd.laravel.com/docs/windows/sites/workspaces.md) in a `workspaces.json` file next to the site-specific nginx configuration files.

```bash theme={null}
%USERPROFILE%\.config\herd\config\valet\workspaces.json
```

### php

This directory contains all `php.ini` files for all PHP versions on your machine. If you use Herd Pro, it also contains `debug.ini` files that Xdebug uses when you enable it for a request.

```bash theme={null}
%USERPROFILE%\.config\herd\config\php
```

### Log

Herd stores all logs of nginx and php-fpm in this directory. It may also contain mail logs if you use Herd Pro.

```bash theme={null}
%USERPROFILE%\.config\herd\Log
```

General application logs of the main Herd application are in this directory.

```bash theme={null}
%USERPROFILE%\AppData\Roaming\Herd\logs
```

If enabled in the general settings, the HerdHelper service that is responsive for managing the hosts file with your `*.test` domains writes logs into this folder.

```bash theme={null}
C:\Windows\System32\logs
```

### Updater files

Downloaded updates go into this directory. If you have trouble installing an update, try deleting these files and download it again or use a fresh copy from the Herd website.

```bash theme={null}
%USERPROFILE%\AppData\Local\herd-updater
```
