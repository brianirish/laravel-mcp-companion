Source: https://herd.laravel.com/docs/macos/debugging/profiler.md

# Profiler

# Profiling Applications

Herd supports a customized version of the [SPX profiler](https://github.com/beyondcode/php-spx) for PHP. The profiler allows you to identify bottlenecks in your application and supports profiling web and CLI requests.

## Installing the profiler extension

You can download and install the profiler extension by running this command in your terminal:

```bash theme={null}
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/beyondcode/php-spx/HEAD/install.sh)"
```

This command downloads the extension and moves it to your Herd application directory and also adds it to all your existing `php.ini` files. If you install a new version, please run this command again to add it to this version automatically.

The extension does not profile requests automatically and requires environment variables or specific headers to record and profile the request, so you can keep it enabled without slowing down your normal setup.

## Profiling Web Requests

You can open the profiler dashboard by opening the `/herd-profiler` route of your application, for example `https://my-app.test/herd-profiler`. This route is dynamically added to requests when you enable the profiler in the settings.

### The Profiler Dashboard

Herd uses the SPX extension for PHP to profile your application and display a customized dashboard of your requests. Please make sure to enable the profiling on the top left.


### Results

If you click on a web request in the dashboard, it loads a breakdown of the request and allows you to inspect function calls and other operations in great detail.


## Profiling CLI scripts

While you can profile web requests via the dashboard, SPX has a profiler for CLI requests as well. When the SPX extension is active, you can run PHP scripts with `herd profile` to trigger the profiling process. As an example, you can profile artisan commands with this command:

```bash theme={null}
herd profile artisan inspire
```

This profiles the command and displays the results directly in your terminal.


## Profiling long-running CLI scripts

When you have long-running CLI scripts, such as daemonized processes, you might want to see profiling information regularly, instead of only seeing them once you end your PHP script.

You can do this by running:

```bash theme={null}
herd profile --live artisan long-running-task
```

You can learn more about SPX in the [official documentation](https://github.com/NoiseByNorthwest/php-spx).
