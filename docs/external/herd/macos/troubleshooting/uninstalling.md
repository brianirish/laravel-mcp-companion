Source: https://herd.laravel.com/docs/macos/troubleshooting/uninstalling.md

# Uninstalling Herd

# Uninstalling Herd

> [!WARNING]
>
> **Do not use third-party cleaners like CleanMyMac, AppCleaner, or similar tools to uninstall Herd.** These tools will delete all data from your Herd Pro services (databases, Redis, etc.) and may even remove your local projects. If you are experiencing issues with Herd, check the [troubleshooting docs](https://herd.laravel.com/docs/macos/troubleshooting/common-issues.md) first – uninstalling is rarely the right fix and often makes things worse.

In case you want to uninstall Herd from your machine, you may use the uninstall script that Herd provides:

> [!WARNING]
>
> Please backup your data of Herd Pro services before running the uninstaller. The uninstaller deletes all application files, configurations and services like databases and storage.

To automatically uninstall Herd, all data within Herd Pro services and all of its settings, run the following command in your terminal:

```bash bash theme={null}
/Applications/Herd.app/Contents/Resources/uninstall
```

> [accordion] Manual Uninstall Steps
>
> 1. Quit Herd by clicking on the icon in the menu bar and selecting "Quit".
> 2. Run the following command in your shell. This will reset the permissions of Herd to start its services.
>    ```shell theme={null}
>    $ sudo rm /etc/sudoers.d/herd
>    ```
> 3. Make a backup of your Herd Pro services `~/Library/Application Support/Herd/config/services`
> 4. Delete the `~/Library/Application Support/Herd` folder.
> 5. Remove Herd from your Applications folder.
> 6. Open your `~/.zshrc` or `~/.bashrc` file and remove the modifications to the `PATH` environment variable that Herd injected as well as all other Herd related modifications that are marked with `# Herd`.
> 7. Go to `/etc/resolver/test` and either delete this file or check its contents. This maps all domains with `.test` to a local nameserver and can be removed if it's only pointing to 127.0.0.1.
> 8. Delete the last config traces from the system defaults with `defaults delete de.beyondco.herd`

## Re-installing Herd

1. Uninstall Herd as described above.
2. Download the latest version of Herd from the website and install it from scratch.
