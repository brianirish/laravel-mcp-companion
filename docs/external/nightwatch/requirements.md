Source: https://nightwatch.laravel.com/docs/requirements.md

# Requirements

> Prerequisites for running the Nightwatch Agent

## Recommended versions

We strongly recommend running the latest versions of Laravel 10, 11, or 12 for the best experience and full feature support.

## Minimum requirements

The [Laravel Nightwatch Agent](https://github.com/laravel/nightwatch) requires:

* Laravel 10.0 or higher
* PHP 8.2 or higher

## Feature support by version

Different features of Nightwatch are available depending on your Laravel version:

* **Cache event durations and cache failures**: Requires Laravel `11.11` or higher
* **Queue names and cache store names**: Supported from Laravel `11.0` onwards
* **Mailable class name capturing**: Requires Laravel `11.27` or higher
* **Queued job durations**: Requires Laravel `10.42` or higher
* **Scheduled task sampling**: Requires Laravel `12.40.2` or higher for the sampling rate to propagate to child artisan commands
* **Query connection type (read or write)**: Requires Laravel `12.45.0` or higher
