Source: https://herd.laravel.com/docs/windows/technology/php-extensions.md

# PHP Extensions

# Installing additional PHP extensions

You may add additional PHP extensions that are not included out of the box with Herd, by downloading their dlls files from [php.net](https://php.net) and loading them via your `php.ini` file.

## Adding extensions

You can browse the [official pecl site](https://pecl.php.net/packages.php) and download the non-thread-safe Windows versions of the PHP extensions there.

## Activating extensions

You may activate your custom extensions by editing your `php.ini` file.
This file is located at `%USERPROFILE%\.config\herd\bin\<version>\php.ini`.
