Source: https://herd.laravel.com/docs/windows/sites/nginx-configuration.md

# Nginx Configuration

# Advanced Nginx Configuration

Herd ships with a default Nginx configurations that is suitable for most projects. However, you can customize the
Nginx settings to fit your specific needs. You can do this in multiple ways and depending on your requirements. Some
settings can (and **must**) be configured via the Herd UI, while others require you to edit the Nginx configuration files directly.

## Via Herd

The most common configurations that usually require changes in your Nginx configuration are the maximum file upload size and the memory limit.
You can change these settings via the Herd UI within the PHP settings section. You can either configure them for all
PHP versions or set specific values per PHP version.


You can also change the PHP version for a specific site via the Herd UI. You can either do that in the [Applications window](https://herd.laravel.com/docs/windows/sites/managing-sites.md) or
via the command line by running `herd isolate 8.3` (or any other version you want to use). This creates a dedicated nginx
configuration file for the specified PHP version and use this version for all web request of the current site.

To use the same version via the command line, you can run `herd php artisan ...` or `herd composer ...` instead of just using `php artisan ...` or `composer ...`.
This will ensure that the correct PHP version is used for the command.

If you secure a site with a TLS/SSL certificate, this creates a dedicated Nginx configuration file for the site and you
can make further changes to the Nginx configuration for this site in this file (see below).


## Customizing the global nginx configuration

Herd comes with default configuration files that are in your Herd configuration directory a `%USERPROFILE%\.config\herd\config\nginx`.
This directory contains the files `nginx.conf` and `herd.conf` that Herd loads on every request. You can edit these files
to make global changes to all projects – but we recommend only changing site-specific files because we might rewrite these files in future updates.

## Customizing the site-specific nginx configuration

If you isolate the PHP version for a site or secure it with a TLS/SSL certificate, Herd creates a dedicated Nginx
configuration file for this site. This file is located at `%USERPROFILE%\.config\herd\config\valet\Nginx` and named
after the site domain. For example, if your site is `herd.laravel.com.test`, the file will be named `herd.laravel.com.test.conf`.

You can edit this file to make site-specific changes to the Nginx configuration but make sure to keep Herd specific elements like the
isolated PHP version or references to the TLS/SSL certificate intact.

## CORS

Herd does not ship with a specific CORS configuration because we believe that your local environment should match your
standard production environment as closely as possible. If you need to configure CORS for your project, you can do that similar to
how you would do it in production. Either create a global CORS configuration for all sites or add the required header in your site-specific file.

```
# CORS Rules
add_header Access-Control-Allow-Origin *;
# END of CORS Rules #
```

### CORS in Laravel

For the Laravel framework, you publish the CORS middleware as described
in the [Laravel documentation](https://laravel.com/docs/12.x/routing#cors).
