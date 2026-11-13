Source: https://herd.laravel.com/docs/macos/sites/securing-sites.md

# Securing Sites

# Securing Sites with TLS

By default, Herd serves sites over HTTP.
However, if you would like to serve a site over encrypted TLS using HTTP/2, you may secure your sites. This is sometimes necessary when working with redirect URLs and other scenarios.

## Via the GUI

You can secure/unsecure a site in the [Applications window](https://herd.laravel.com/docs/macos/sites/managing-sites.md). You can open it via the Herd menu bar icon and selecting "Applications".

Select the site and use the "HTTPS" toggle in the "Environment" section of the inspector. If you're securing the site, you may need to confirm one or more permission related popups to create the local certificate.

## Via the CLI

If you prefer to use the CLI, you can use the `herd secure` command to secure/unsecure a site.
For example, if Herd serves your site via the `example-site.test` domain, you need run the following command to secure it:

```shell theme={null}
# secure the current working directory
herd secure

# secure example-site.test from anywhere
herd secure example-site 
```

To "unsecure" a site and revert back to serving its traffic over plain HTTP, use the `unsecure` command.
Like the `secure` command, this command accepts the sitename that you wish to unsecure:

```shell theme={null}
# unsecure the current working directory
herd unsecure

# unsecure example-site.test from anywhere
herd unsecure example-site 
```

After unsecuring a site, you man need to restart your browser session because many browsers like Google Chrome cache redirects to HTTPS and will give you a hard time.

## Listing all secure sites

The Herd CLI has a command to list all sites that have a local TLS certificate. You may want to use that for debugging purposes.

```shell theme={null}
herd secured
```

This gives you a similar output to this:

```
+----------------------------+----------------------------+
| Site                       | Valid Until                |
+----------------------------+----------------------------+
| expose.dev.test            | 2024-08-10 12:07:38 GMT    |
| herd-templates.test        | 2024-09-05 25:12:77 GMT    |
| reverb-110.test            | 2024-09-11 13:44:56 GMT    |
| tinkerwell.app.test        | 2024-10-16 19:53:32 GMT    |
+----------------------------+----------------------------+
```
