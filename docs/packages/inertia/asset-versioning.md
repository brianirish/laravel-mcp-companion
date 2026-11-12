Source: https://inertiajs.com/docs/v3/advanced/asset-versioning.md

# Asset Versioning

One common challenge when building single-page apps is refreshing site assets when they've been changed. Thankfully, Inertia makes this easy by optionally tracking the current version of your site assets. When an asset changes, Inertia will automatically make a full-page visit instead of an XHR visit on the next request.

## Configuration

To enable automatic asset refreshing, you need to tell Inertia the current version of your assets. This can be any arbitrary string (letters, numbers, or a file hash), as long as it changes when your assets have been updated.

Typically, your application's asset version can be specified within the `version` method of the Inertia `HandleInertiaRequests` middleware.

```php theme={null}
class HandleInertiaRequests extends Middleware
{
    public function version(Request $request)
    {
        return parent::version($request);
    }
}
```

Alternatively, the asset version can be provided manually using the `Inertia::version()` method.

```php theme={null}
use Inertia\Inertia;

Inertia::version($version);
Inertia::version(fn () => $version); // Lazily...
```

## Cache Busting

Asset refreshing in Inertia works on the assumption that a full-page visit will trigger your assets to reload. However, Inertia doesn't actually do anything to force this. Typically this is done with some form of cache busting. For example, appending a version query parameter to the end of your asset URLs.

With Laravel's Vite integration, asset versioning is done automatically. If you're using Laravel Mix, you can do this automatically by enabling [versioning](https://laravel.com/docs/mix#versioning-and-cache-busting) in your `webpack.mix.js` file.

## Background Requests

v3.6.0+

A version change detected on a background request, such as polling or a `router.reload()`, does not force a full-page navigation. Reloading a request the user never initiated could wipe out unsaved state, so the current page stays untouched and the next user-initiated visit picks up the new assets. You may hook into the [`location` event](https://inertiajs.com/docs/v3/advanced/events#location) to detect an asset version change and show a notification instead of reloading.

## Manual Refreshing

If you want to take control of asset refreshing, you can return a fixed value from the `version` method in the `HandleInertiaRequests` middleware. This disables Inertia's automatic asset versioning.

For example, if you want to notify users when a new version of your front end is available, you can still expose the actual asset version to the front end by including it as [shared data](https://inertiajs.com/docs/v3/data-props/shared-data.md).

```php theme={null}
class HandleInertiaRequests extends Middleware
{
    public function version(Request $request)
    {
        return null;
    }

    public function share(Request $request)
    {
        return array_merge(parent::share($request), [
            'version' => parent::version($request),
        ]);
    }
}
```

On the front end, you can watch the `version` property and show a notification when a new version is detected.
