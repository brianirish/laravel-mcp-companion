Source: https://herd.laravel.com/docs/windows/extending-herd/custom-drivers.md

# Custom Drivers

# Custom Drivers

You can extend Herd with your own drivers to support customized setups of supported frameworks or to add new frameworks and applications that Herd doesn't support out of the box. You can also change the application information that `herd site-information` returns or add additional log file directories for the [Log Viewer](https://herd.laravel.com/docs/windows/debugging/logs.md).

## What is a driver?

A driver is a PHP class that tells Herd how to serve a site. When a request comes in, Herd goes through its drivers and uses the first one that recognizes the site directory — a Laravel site is detected by its `artisan` file, a WordPress site by `wp-config.php`, and so on.

Once a driver has claimed the site, it decides how the request is handled: whether it's a static file like an image or a stylesheet that can be served straight from disk, and which PHP file should handle everything else. For Laravel, that front controller is `public/index.php`.

Herd ships with drivers for every framework it supports, so a standard Laravel, Statamic, or WordPress site just works and you never have to think about drivers. You only need your own when a site breaks those conventions — it's served from a `web` directory instead of `public`, for example — or when you use a framework Herd doesn't know yet.

Drivers also decide which log files the [Log Viewer](https://herd.laravel.com/docs/windows/debugging/logs.md) scans and what `herd site-information` returns for a site. Both can be customized per site, as described below.

## Creating a driver

Herd internally leverages a heavily customized version of [Laravel Valet](https://laravel.com/docs/11.x/valet) for serving sites, and it includes all [drivers](https://github.com/laravel/valet/tree/master/cli/Valet/Drivers) that Valet provides. These drivers are a good start when creating your own custom driver, and it often makes sense to further extend them than starting from scratch.

> [!NOTE]
>
> Please make sure to name the custom driver according to the driver convention. It needs to end on `ValetDriver.php` and a good name for a custom Laravel driver would be `MyLaravelValetDriver.php`.

Place your custom driver in the related valet directory on your machine and Herd loads it before serving a site automatically.

```
%USERPROFILE%\.config\herd\config\valet\Drivers
```

## Customize Herds behaviour

### Log paths

You can customize the paths that are checked for the [log viewer](https://herd.laravel.com/docs/windows/debugging/logs.md) by adjusting the `logFilesPaths()` method in the driver. The default looks like this:

```php theme={null}
    /**
     * Get the logs paths for the application to show in Herds log viewer.
     */
    public function logFilesPaths() {
        return [
            "/storage/logs"
        ];
    }
```

The given paths are relative to the application root.

### Application Information

The `herd site-information` command returns an overview of your application and you can customize this information to your needs. The default for Laravel applications is the output of the `php artisan about` command.

If you want to customize the overview table, you can do so by defining this method in your applications' custom driver and returning an array like the following:

```php theme={null}
    public function siteInformation(string $sitePath, string $phpBinary): array
    {
        return [
            "Overview" => [
                "Site Name" => "Laravel Airport",
                "Runway operational" => true,
            ],
            "Flights" => [
                "Today" => 10,
                "Yesterday" => 5,
                "This week" => 22,
            ],
        ];
    }
```

Herd injects the path to the current site and the PHP binary to this method so that you can perform more specific commands and even run code with the correct php version.

## Custom Laravel Driver

This example of a custom driver extends the existing Laravel Driver and modifies it to serve the application from a `web` instead of the `public` directory.

```php theme={null}

namespace Valet\Drivers\Custom;

use Valet\Drivers\LaravelValetDriver;

class CustomLaravelValetDriver extends LaravelValetDriver
{
    /**
     * Determine if the driver serves the request.
     */
    public function serves(string $sitePath, string $siteName, string $uri): bool
    {
        return file_exists($sitePath.'/web/index.php') &&
               file_exists($sitePath.'/artisan');
    }

    /**
     * Determine if the incoming request is for a static file.
     */
    public function isStaticFile(string $sitePath, string $siteName, string $uri)/*: string|false */
    {
        if (file_exists($staticFilePath = $sitePath.'/web'.$uri)
           && is_file($staticFilePath)) {
            return $staticFilePath;
        }

        $storageUri = $uri;

        if (strpos($uri, '/storage/') === 0) {
            $storageUri = substr($uri, 8);
        }

        if ($this->isActualFile($storagePath = $sitePath.'/storage/app/public'.$storageUri)) {
            return $storagePath;
        }

        return false;
    }

    /**
     * Get the fully resolved path to the application's front controller.
     */
    public function frontControllerPath(string $sitePath, string $siteName, string $uri): ?string
    {
        if (file_exists($staticFilePath = $sitePath.'/web'.$uri)
           && $this->isActualFile($staticFilePath)) {
            return $staticFilePath;
        }

        return $sitePath.'/web/index.php';
    }

    /**
     * Get the logs paths for the application to show in Herds log viewer.
     */
    public function logFilesPaths() {
        return ["/storage/logs"];
    }

    /**
     * Return information about the application for the `herd site-information` command.
     * For Laravel, it's the output of the `php artisan about` command.
     */
    public function siteInformation(string $sitePath, string $phpBinary): array
    {
        try {
            $process = new Process([
                $phpBinary,
                'artisan',
                'about',
                '--json'
            ], $sitePath);

            $process->mustRun();

            $result = json_decode($process->getOutput(), true);
        } catch (\Exception $e) {
            $result = [];
        }

        return [
            ...$result,
        ];
    }
}
```

This example driver provides a good overview about the possibilities and make use of the `phpBinary` and `$sitePath` variables.
