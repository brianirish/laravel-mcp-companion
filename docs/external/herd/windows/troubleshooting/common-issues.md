Source: https://herd.laravel.com/docs/windows/troubleshooting/common-issues.md

# Common Issues

# Resolving Common Issues

If you are on this site, we're sorry. We are working to create the most robust and easiest to use local development environment for Laravel – but Herd is still a tool early in its lifecycle, and we aren't there yet. On this page, you'll find common issues and a solution to resolve them.

If the documentation and the following tips don't resolve your issue, please head over to the [support section](https://herd.laravel.com/docs/windows/troubleshooting/support.md).

## Restarting Herd

In some rare scenarios, Herd doesn't start after it has been quit previously. Please check your Task Manager if there are still running instances of Herd and stop them manually before opening Herd again.

## Herd Debug Logs

The Herd app writes all output to a `main.log` log file but keeps this file to a maximum of 1MB, so if you want to get the debug information for Herd, you can check this file. If you encounter a problem that you can reproduce, please check the logs and share them with us via the [support](https://herd.laravel.com/docs/windows/troubleshooting/support.md) if you can't fix the problem with this information.

```ps1 theme={null}
%USERPROFILE%\AppData\Roaming\Herd\logs\main.log
```

## 404 Errors

If Herd can not properly detect a driver for your site or can't find the site at all, Herd displays a custom 404 error page. Herd adds the domain of every site to your hosts file, so a `.test` domain that doesn't belong to any site doesn't resolve at all and your browser can't reach it.

The error page mostly has a useful hint how to fix the problem but in case it does not, the most common problem is that the directory of the project includes `www` in the name.

Herd strips `www` from directory names so that all sites are accessible via their domain with and without `www` prefix.

The solution to this is renaming the directory from `www.your-site.com` to `your-site.com`. This allows you to access the site at `http://your-site.com.test`. If the site had specific configurations, you need to apply them again after this change because Herd treats this site as a new one.

## Bad Gateway

These errors happen if there is something wrong with the nginx web server. This could be an old PHP process or a broken configuration file. A good practice to fix the config file for a single site is by isolating the site to a specific PHP version or securing it with a TLS certificate. You can always switch back to the previous PHP version or unsecure the site but all these commands regenerate the configuration file to fix the issue.

You can access the individual configuration files for nginx at the following path:

```ps1 theme={null}
%USERPROFILE%\.config\herd\config\valet\Nginx
```

If this does not help, please create an issue with the broken config file in the [community repository](https://herd.laravel.com/docs/windows/troubleshooting/support.md#community-support).

## DNS Errors

While the macOS version of Herd is running dnsmasq as a local DNS server, the Windows version regularly updates the hosts file of your machine. It's located at the following path:

```ps1 theme={null}
C:\Windows\System32\drivers\etc\hosts
```

If everything works as expected, the HerdHelper Windows Service writes something like this to the file:

```bash theme={null}
# Herd generated Hosts. Do not change.
127.0.0.1 database.herd.test
127.0.0.1 your-site.test
# End Herd generated Hosts
```

This tells your browser to look for these domains on your local machine and redirect them to nginx from Herd. If you don't see the generated hosts in your hosts file, there is something wrong with the HerdHelper. There are multiple scenarios why the helper service isn't working properly, so we have put together a dedicated section: [HerdHelper](https://herd.laravel.com/docs/windows/troubleshooting/herdhelper.md).
