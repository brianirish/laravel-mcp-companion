Source: https://herd.laravel.com/docs/windows/debugging/xdebug-detection.md

# Xdebug Detection

# Automatically use Xdebug

Herd Pro is able to detect Xdebug headers in your requests and it enables the Xdebug extension on demand for these requests so that all other requests bypass the extension and are super-fast.

## Setup with browser extensions

Herd uses the headers of Xdebug browser extensions that you can install via the [Chrome Web Store](https://chromewebstore.google.com/detail/xdebug-extension/aoelhdemabeimdhedkidlnbkfhnhgnhm) or [Firefox Addons](https://addons.mozilla.org/firefox/addon/xdebug-helper-for-firefox).

Once you enable an Xdebug feature in the browser extension, Herd serves the request via a PHP process with an enabled Xdebug extensions.

## Using Xdebug on the command line

You can run CLI commands via `herd debug ..` instead of using `php ...` to use the php binary with Xdebug enabled. So if you are debugging an artisan command, you can run `herd debug artisan your:command` to trigger your breakpoint.

### Configure PhpStorm to ignore the dump loader

Herd serves sites via a PHP script and if you've dumps enabled, it also uses a `dump-loader.php` file for custom bootstrapping of your application. If you want to debug with Xdebug, it makes sense to configure PHPStorm to ignore this dump loader. You can do that in the settings of PhpStorm by unchecking the boxes for:

* Force break at first line when no path mapping specified
* Force break at first line when a script is outside the project


## Code Coverage

Herd has a `coverage` command that allows you to run Xdebug's coverage mode on your test suite:

```bash theme={null}
herd coverage ./vendor/bin/pest --coverage
```
