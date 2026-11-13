Source: https://herd.laravel.com/docs/windows/troubleshooting/restarting-services.md

# Restarting Services

# Restarting Herd Services

It might happen that Herd displays that a service like `CGI-PHP` is not running for a specific PHP version. This can happen if Herd is unable to properly shut down all background services when you close the app.

## Via the GUI

You may force a restart of all Herd services by opening the menu of the Herd system tray icon and selecting `Restart Services`. Herd forcefully stops all of its services, including nginx, PHP and your Herd Pro services, and starts them again. Under the hood, this stops all existing instances of a service and might even stop services that you've installed separately.

If you need to stop and start the services separately, press the `Alt` key while the Herd menu is open, or right-click the menu and select "Show Advanced Details". The menu then shows `Force Stop All` and `Start All` as well as the status of every service.

## Via the terminal

To kill all stray services, open Powershell with admin privileges and perform the `taskkill` command for every service that is still running, naming the services.

## Force a shutdown of all Herd services

```shell theme={null}
# Stop main services
taskkill /F /IM php-cgi.exe
taskkill /F /IM nginx.exe

# Stop Pro services
taskkill /F /IM mysqld.exe
...
```

## Restarting the HerdHelper Windows Service

Herd uses a Windows Service to manage your `hosts` file and add or remove domains to this file. If the HerdHelper isn't running, you can not access your sites via their domain.

You can restart the HerdHelper via the system Services window.
