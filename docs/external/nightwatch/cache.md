Source: https://nightwatch.laravel.com/docs/cache.md

# Cache

> Interactions with Laravel's Cache layer

Nightwatch captures the `hit`, `miss`, `delete`, `write` and `fail` events from Laravel's Cache layer, making it simple to see which keys are being used and how they're performing.

## Cache List

The Cache page surfaces the top 100 keys used in your application, sorted by the metric you choose. Total calls is shown by default, but you can sort by hits, misses, writes, deletes or failures.

## Sampling

There are no direct sampling controls for cache events, they are automatically captured when their [parent execution](https://nightwatch.laravel.com/docs/events.md#execution-contexts) context is sampled.

## Filtering

Applications that make extensive use of the Cache layer may find it beneficial to filter out low-value events to conserve your event quota.

### Filter vendor cache keys

For convenience, Nightwatch automatically ignores cache events generated from Laravel's internal systems and first-party packages. These are low-level events that are not typically of interest to most applications. They include:

* Laravel framework internals (e.g. scheduler, queue worker)
* Laravel Vapor job attempts
* Laravel Pulse
* Laravel Reverb
* Laravel Nova
* Laravel Telescope

You can inspect the full list of ignored patterns by running `php artisan tinker` and calling `Nightwatch::defaultVendorCacheKeys()`.

You can opt in to collecting these using `captureDefaultVendorCacheKeys`, but be cautioned that this can significantly increase the number of events captured:

```php AppServiceProvider.php theme={null}
use Laravel\Nightwatch\Facades\Nightwatch;

public function boot(): void
{
    Nightwatch::captureDefaultVendorCacheKeys();
}
```

### Filter all cache events

To completely disable the collection of cache events by setting the `NIGHTWATCH_IGNORE_CACHE_EVENTS` environment variable to `true`:

```bash theme={null}
NIGHTWATCH_IGNORE_CACHE_EVENTS=true
```

### Filter using cache keys

Cache events may be filtered by their cache key or key patterns:

```php AppServiceProvider.php theme={null}
use Laravel\Nightwatch\Facades\Nightwatch;

public function boot(): void
{
    Nightwatch::rejectCacheKeys([
        'my-app:users',        // Matches the exact cache key 'my-app:users'
        '/^my-app:posts:/',    // Matches any cache key starting with 'my-app:posts:'
        '/^[a-zA-Z0-9]{40}$/', // Session IDs
    ]);
}
```

### Filter using a callback

You can filter each cache event using a callback for more specific logic:

```php AppServiceProvider.php theme={null}
use Laravel\Nightwatch\Facades\Nightwatch;
use Laravel\Nightwatch\Records\CacheEvent;

public function boot(): void
{
    Nightwatch::rejectCacheEvents(function (CacheEvent $cacheEvent) {
        return str_starts_with($cacheEvent->key, 'temp:');
    });
}
```

## Redaction

You can manually redact sensitive information from cache keys with `redactCacheEvents`:

```php theme={null}
use Laravel\Nightwatch\Facades\Nightwatch;
use Laravel\Nightwatch\Records\CacheEvent;

Nightwatch::redactCacheEvents(function (CacheEvent $cacheEvent) {
    $cacheEvent->key = str_replace('secret', '***', $cacheEvent->key);
});
```
