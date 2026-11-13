Source: https://herd.laravel.com/docs/macos/technology/php-settings.md

# PHP Settings

# Changing PHP settings

The values that most developers change are the memory limit and the max upload size. You can modify them in the settings and don't need to go deep into configuration files.


Herd gives you easy access to the PHP configuration files on your machine, the easiest way to get to the file is to select the php.ini directory from the context menu of the settings.


Each PHP version has its own `php.ini` file at `~/Library/Application Support/Herd/config/php/<version>/php.ini`.
You can edit this file to change or add PHP settings for a specific PHP version.

> [!NOTE]
>
> If you want to quickly access your php.ini file via the CLI, you may use the `herd ini` command.

All saved changes are immediately available in the CLI, but you need to restart all Herd services to apply the changes to HTTP requests via nginx.

You can restart all services by clicking "Restart" in the Herd dropdown menu in the menu bar – it just takes a few seconds. You can also run `herd restart` in your terminal. If a service does not restart properly, see [Restarting Services](https://herd.laravel.com/docs/macos/troubleshooting/restarting-services.md).

Alternatively, you can use the `herd restart` command in the terminal.

```shell theme={null}
herd restart
```
