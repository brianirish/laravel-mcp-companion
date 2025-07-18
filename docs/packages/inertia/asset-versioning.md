# Inertia - Asset Versioning

Source: https://inertiajs.com/asset-versioning

# Asset versioning

## Configuration

## Cache busting

## Manual refreshing

One common challenge when building single-page apps is refreshing site assets when they've been changed. Thankfully, Inertia makes this easy by optionally tracking the current version of your site assets. When an asset changes, Inertia will automatically make a full page visit instead of a XHR visit on the next request.

To enable automatic asset refreshing, you need to tell Inertia the current version of your assets. This can be any arbitrary string (letters, numbers, or a file hash), as long as it changes when your assets have been updated.

Typically, your application's asset version can be specified within the version method of the Inertia HandleInertiaRequests middleware.

Alternatively, the asset version can be provided manually using the Inertia::version() method.

Asset refreshing in Inertia works on the assumption that a hard page visit will trigger your assets to reload. However, Inertia doesn't actually do anything to force this. Typically this is done with some form of cache busting. For example, appending a version query parameter to the end of your asset URLs.

With Laravel's Vite integration, asset versioning is done automatically. If you're using Laravel Mix, you can do this automatically by enabling versioning in your webpack.mix.js file.

If you want to take asset refreshing into your control, you can return a fixed value from the version method in the HandleInertiaRequests middleware. This disables Inertia's automatic asset versioning.

For example, if you want to notify users when a new version of your frontend is available, you can still expose the actual asset version to the frontend by including it as shared data.

On the frontend, you can watch the version property and show a notification when a new version is detected.

`version`
`HandleInertiaRequests`
`Inertia::version()`
`webpack.mix.js`
[versioning](https://laravel.com/docs/mix#versioning-and-cache-busting)
[shared data](/shared-data)
The HandleInertiaRequests middleware provides a sensible default for Laravel applications, which uses either a hash of the

file. When using Vite, Inertia will use a hash of the
