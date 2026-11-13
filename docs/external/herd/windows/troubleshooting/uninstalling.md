Source: https://herd.laravel.com/docs/windows/troubleshooting/uninstalling.md

# Uninstalling Herd

# Uninstalling Herd

> [!WARNING]
>
> **Only uninstall Herd if you truly want to remove it from your system.** If something isn't working correctly, uninstalling is almost never the right fix. Instead, check the [troubleshooting docs](https://herd.laravel.com/docs/windows/troubleshooting/common-issues.md) or simply run the [Herd installer](https://herd.laravel.com) again – this will repair your installation without losing any data or settings.

In case you want to uninstall Herd from your machine, perform the following steps:

1. Quit Herd by opening the menu of the Herd system tray icon and clicking the "Quit" button.
2. Uninstall Herd via the Windows uninstaller
3. Delete the Herd config directory at `%USERPROFILE%\.config\herd`
4. Uninstall `nvm` by deleting the `NVM_HOME` and `NVM_SYMLINK` variables from your system environment variables
5. Delete the shortcut `C:\Program Files\nodejs` if it is still present
6. If you are using [Git Bash](https://herd.laravel.com/docs/windows/advanced-usage/command-line.md), make sure to remove the aliases from your `.bash_profile`

## Re-installing Herd

1. Uninstall Herd as described above.
2. Download the latest version of Herd from the website and install it from scratch.
