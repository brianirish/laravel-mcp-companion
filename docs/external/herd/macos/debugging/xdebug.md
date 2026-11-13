Source: https://herd.laravel.com/docs/macos/debugging/xdebug.md

# Xdebug

# Using Xdebug with Herd

Herd includes support for [Xdebug](https://xdebug.org/), a popular and powerful debugger for PHP.
The free version of Herd ships with Xdebug's PHP extensions out-of-the-box, but you need to manually enable the extension when you need it.

If Xdebug is too much for you and you prefer debugging via dumps, check out [Insights](https://herd.laravel.com/docs/macos/debugging/insights.md) of Herd Pro.

> [!NOTE]
>
> Looking for an even easier way to debug your applications? Check out [Herd Pro's Xdebug integration](https://herd.laravel.com/docs/macos/debugging/xdebug-detection.md).
> It can automatically detect breakpoints in your application and enable Xdebug on-the-fly when necessary.

## Enabling Xdebug manually

In order to activate Xdebug, you need to add the appropriate PHP extension to your `php.ini` file. The extensions are located in the Herd application bundle, which you can find in your Applications folder.
The exact location depends on your PHP version and device architecture.

The following extensions are available:

```bash theme={null}
# Apple Silicon
/Applications/Herd.app/Contents/Resources/xdebug/xdebug-74-arm64.so
/Applications/Herd.app/Contents/Resources/xdebug/xdebug-80-arm64.so
/Applications/Herd.app/Contents/Resources/xdebug/xdebug-81-arm64.so
/Applications/Herd.app/Contents/Resources/xdebug/xdebug-82-arm64.so
/Applications/Herd.app/Contents/Resources/xdebug/xdebug-83-arm64.so
```

After you have located the correct version of Xdebug, you need to append the necessary configuration to your `php.ini` file. For example, the setup for PHP 8.3 on an Apple Silicon Mac looks like this:

```ini php.ini theme={null}
zend_extension=/Applications/Herd.app/Contents/Resources/xdebug/xdebug-83-arm64.so
xdebug.mode=debug,develop
xdebug.start_with_request=yes
xdebug.start_upon_error=yes
```

After saving the changes to your `php.ini` file, you need to restart Herd's services from the menu bar icon, or by running the following command in your terminal:

```bash theme={null}
herd restart
```

For more information about the available Xdebug settings, please refer to the [official Xdebug documentation](https://xdebug.org/docs/).
