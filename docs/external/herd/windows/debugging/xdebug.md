Source: https://herd.laravel.com/docs/windows/debugging/xdebug.md

# Xdebug

# Using Xdebug with Herd

Herd includes support for [Xdebug](https://xdebug.org/), a popular and powerful debugger for PHP. The free version of Herd ships with Xdebug's PHP extensions out-of-the-box, but you need to manually enable the extension when you need it.

If Xdebug is too much for you and you prefer debugging via dumps, check out [Insights](https://herd.laravel.com/docs/windows/debugging/insights.md) of Herd Pro.

> [!NOTE]
>
> Looking for an even easier way to debug your applications? Check out [Herd Pro's Xdebug integration](https://herd.laravel.com/docs/windows/debugging/xdebug-detection.md).
> It can automatically enable Xdebug if you send the Xdebug request header via the official Xdebug browser extensions.

## Enabling Xdebug manually

In order to activate Xdebug, you need to add the appropriate PHP extension to your `php.ini` file. The extensions are located in the Herd application bundle, which you can find in your application folder. The application bundle is at:

```
C:\Program Files\Herd\resources\app.asar.unpacked\resources\bin\xdebug
```

After locating the correct version of Xdebug, you can append the necessary configuration to your `php.ini` file. For example, the `php.ini` for PHP 8.3 is at:

```
"%USERPROFILE%\.config\herd\bin\php83\php.ini"
```

You can add the Xdebug configuration to this file by adding these lines:

```bash theme={null}
zend_extension=C:\Program Files\Herd\resources\app.asar.unpacked\resources\bin\xdebug\xdebug-8.3.dll
xdebug.mode=debug,develop
xdebug.start_with_request=yes
xdebug.start_upon_error=yes
```

After saving the changes to your `php.ini` file, you need to restart Herd's services by selecting "Restart Services" in the Herd system tray menu, or by running the following command in your terminal:

```bash theme={null}
herd restart
```

For more information about the available Xdebug settings, please refer to the [official Xdebug documentation](https://xdebug.org/docs/).
