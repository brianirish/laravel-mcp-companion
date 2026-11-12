Source: https://inertiajs.com/docs/v3/getting-started/upgrade-guide.md

# Upgrade Guide for v3.0

You can find the legacy docs for Inertia.js v2.0 at [inertiajs.com/docs/v2](https://inertiajs.com/docs/v2).

## What's New

Inertia.js v3.0 is a major release focused on simplicity and developer experience. Axios has been replaced with a built-in XHR client for a smaller bundle, SSR now works out of the box during development without a separate Node.js server, and the new `@inertiajs/vite` plugin handles page resolution and SSR configuration automatically. This release also introduces standalone HTTP requests via the `useHttp` hook, optimistic updates with automatic rollback, layout props for sharing data between pages and layouts, and improved exception handling.

> [card] [Vite Plugin](https://inertiajs.com/docs/v3/installation/client-side-setup.md#installation)
>
> Automatic page resolution, SSR setup, and optional setup/resolve callbacks.

> [card] [HTTP Requests](https://inertiajs.com/docs/v3/the-basics/http-requests.md)
>
> Make standalone HTTP requests with the `useHttp` hook without triggering page visits.

> [card] [Optimistic Updates](https://inertiajs.com/docs/v3/the-basics/optimistic-updates.md)
>
> Apply data changes instantly before the server responds, with automatic rollback on failure.

> [card] [Layout Props](https://inertiajs.com/docs/v3/the-basics/layouts.md#layout-props)
>
> Share dynamic data between pages and persistent layouts with the useLayoutProps hook.

> [card] [Simplified SSR](https://inertiajs.com/docs/v3/advanced/server-side-rendering.md)
>
> SSR works automatically in Vite dev mode. No separate Node.js server needed.

> [card] [Exception Handling](https://inertiajs.com/docs/v3/advanced/error-handling.md#production)
>
> Render custom Inertia error pages directly from your exception handler, with shared data.

This release also includes several additional improvements:

* [Instant visits](https://inertiajs.com/docs/v3/the-basics/instant-visits.md) that swap to the target component before the server responds
* [Form component generics](https://inertiajs.com/docs/v3/advanced/typescript.md#form-component) for type-safe errors and slot props
* [Disable SSR per-route](https://inertiajs.com/docs/v3/advanced/server-side-rendering.md#disabling-ssr) via middleware or facade
* [Improved SSR error messages](https://inertiajs.com/docs/v3/advanced/server-side-rendering.md#error-handling) with component names, URLs, and actionable hints
* [Enum support](https://inertiajs.com/docs/v3/the-basics/responses.md) in `Inertia::render()` responses
* [Page object in resolve callback](https://inertiajs.com/docs/v3/installation/client-side-setup.md#manual-setup) for context-aware component resolution
* [Built-in HTTP interceptors](https://inertiajs.com/docs/v3/installation/client-side-setup.md#interceptors) without Axios
* [Default layout](https://inertiajs.com/docs/v3/the-basics/layouts.md#default-layouts) option in `createInertiaApp`
* [`preserveErrors`](https://inertiajs.com/docs/v3/data-props/partial-reloads#preserving-errors) option to preserve validation errors during partial reloads
* [Blade components](https://inertiajs.com/docs/v3/installation/server-side-setup.md#setup-root-template) as an alternative to the `@inertia` and `@inertiaHead` directives, with SSR head fallback support

## Upgrade Dependencies

To upgrade to Inertia.js v3.0, first use npm to install the client-side adapter of your choice:

```bash Vue icon="vuejs" theme={null}
npm install @inertiajs/vue3@^3.0
```

```bash React icon="react" theme={null}
npm install @inertiajs/react@^3.0
```

```bash Svelte icon="s" theme={null}
npm install @inertiajs/svelte@^3.0
```

You may also install the new optional Vite plugin, which provides a simplified SSR setup and a `pages` shorthand for component resolution:

```bash theme={null}
npm install @inertiajs/vite@^3.0
```

Next, upgrade the `inertiajs/inertia-laravel` package:

```bash theme={null}
composer require inertiajs/inertia-laravel:^3.0
```

After upgrading, republish the Inertia configuration file since it has been restructured in v3. You should review the updated config file and re-apply any customizations:

```bash theme={null}
php artisan vendor:publish --provider="Inertia\\ServiceProvider" --force
```

You should also clear your cached views since the `@inertia` Blade directive output has changed:

```bash theme={null}
php artisan view:clear
```

## Breaking Changes

***

### Requirements

#### PHP 8.2+ and Laravel 11+

The Laravel adapter now requires PHP 8.2 and Laravel 11 at a minimum.

#### React 19+

The React adapter now requires React 19. React 18 and below are no longer supported.

#### Svelte 5+

The Svelte adapter now requires Svelte 5. Svelte 4 and below are no longer supported. All Svelte code should be updated to use Svelte 5's runes syntax (`$props()`, `$state()`, `$effect()`, etc).

### Axios Removed

Inertia no longer ships with or requires Axios. For most applications, this requires no changes. The built-in XHR client supports [interceptors](https://inertiajs.com/docs/v3/installation/client-side-setup.md#interceptors) as well, so Axios interceptors may be migrated directly. You may also continue using Axios via the [Axios adapter](https://inertiajs.com/docs/v3/installation/client-side-setup.md#using-axios), or provide a fully [custom HTTP client](https://inertiajs.com/docs/v3/installation/client-side-setup.md#custom-http-client).

### `qs` Dependency Removed

The `qs` package has been replaced with a built-in query string implementation and is no longer included as a dependency of `@inertiajs/core`. Inertia's internal query string handling remains the same, but you should install `qs` directly if your application imports it.

```bash theme={null}
npm install qs
```

### `lodash-es` Dependency Removed

The `lodash-es` package has been replaced with `es-toolkit` and is no longer included as a dependency of `@inertiajs/core`. You should install `lodash-es` directly if your application imports it.

```bash theme={null}
npm install lodash-es
```

### Event Renames

Two global events have been renamed for clarity:

| v2 Name | v3 Name | Document Event |
| - | - | - |
| `invalid` | `httpException` | `inertia:httpException` |
| `exception` | `networkError` | `inertia:networkError` |

Global event listeners should be updated accordingly:

```js theme={null}
// Before (v2)
router.on('invalid', (event) => { ... })
router.on('exception', (event) => { ... })

// After (v3)
router.on('httpException', (event) => { ... })
router.on('networkError', (event) => { ... })
```

You may also handle these events per-visit using the new `onHttpException` and `onNetworkError` callbacks:

```js theme={null}
router.post('/users', data, {
    onHttpException: (response) => { ... },
    onNetworkError: (error) => { ... },
})
```

Returning `false` from the `onHttpException` callback or calling `event.preventDefault()` on the global `httpException` event will prevent Inertia from navigating to the error page. This allows you to handle HTTP exceptions (4xx and 5xx responses) without leaving the current page.

```js theme={null}
router.post('/users', data, {
    onHttpException: (response) => {
        // Handle the error without navigating
        return false
    },
})
```

### `router.cancel()` Replaced

The `router.cancel()` method has been replaced by `router.cancelAll()`. In v2, `cancel()` only canceled synchronous requests. The new `cancelAll()` method cancels all synchronous, asynchronous, and prefetch requests by default. You may pass options to limit which request types are canceled.

```js theme={null}
// Before (v2) — only canceled sync requests
router.cancel()

// After (v3) — cancels all request types
router.cancelAll()

// To match v2 behavior (sync only)...
router.cancelAll({ async: false, prefetch: false })
```

See the [visit cancellation](https://inertiajs.com/docs/v3/the-basics/manual-visits.md#visit-cancellation) documentation for more details.

### Future Options Removed

The `future` configuration namespace has been removed. All four future options from v2 are now always enabled and no longer configurable:

* `future.preserveEqualProps`
* `future.useDataInertiaHeadAttribute`
* `future.useDialogForErrorModal`
* `future.useScriptElementForInitialPage`

```js theme={null}
// Before (v2)
createInertiaApp({
    defaults: {
        future: {
            preserveEqualProps: true,
            useDataInertiaHeadAttribute: true,
            useDialogForErrorModal: true,
            useScriptElementForInitialPage: true,
        },
    },
})

// After (v3) - just remove the `future` block
createInertiaApp({
    // ...
})
```

Initial page data is now always passed via a `<script type="application/json">` element. The legacy `data-page` attribute approach is no longer supported.

### Head Element Attributes

The `inertia` attribute used on elements in your root Blade template's `<head>` section has been renamed to `data-inertia`. You should update any head elements that use this attribute:

```html theme={null}
<!-- Before (v2) -->
<title inertia>My Website</title>

<!-- After (v3) -->
<title data-inertia>My Website</title>
```

### Progress Indicator Exports Removed

The named exports `hideProgress()` and `revealProgress()` have been removed. If needed, use the `progress` object directly:

```js theme={null}
import { progress } from '@inertiajs/vue3'

progress.hide()
progress.reveal()
```

### Deferred Component Behavior (React)

The React `<Deferred>` component no longer resets to show the fallback during partial reloads. Previously, the fallback was shown each time a partial reload was triggered. Now the existing content remains visible while new data loads, consistent with the Vue and Svelte behavior.

A new `reloading` slot prop is available across all adapters, allowing you to show a loading indicator during partial reloads while keeping the existing content visible. See the [deferred props](https://inertiajs.com/docs/v3/data-props/deferred-props.md#reloading) documentation for details.

### Form Processing Reset Timing

The `useForm` helper now only resets `processing` and `progress` state in the `onFinish` callback, rather than immediately upon receiving a response. This ensures the processing state remains `true` until the visit is fully complete.

### LazyProp Removed

The `Inertia::lazy()` method and `LazyProp` class, deprecated in v2, have been removed. Use `Inertia::optional()` instead, which provides the same functionality:

```php theme={null}
// Before (v2)
return Inertia::render('Users/Index', [
    'users' => Inertia::lazy(fn () => User::all()),
]);

// After (v3)
return Inertia::render('Users/Index', [
    'users' => Inertia::optional(fn () => User::all()),
]);
```

### Config File Restructuring

The Laravel configuration file has been restructured. Page-related settings are now nested under `pages`, and the `testing` section has been simplified:

```php theme={null}
// Before (v2) - config/inertia.php
'testing' => [
    'ensure_pages_exist' => true,
    'page_paths' => [resource_path('js/Pages')],
    'page_extensions' => ['js', 'jsx', 'svelte', 'ts', 'tsx', 'vue'],
],

// After (v3) - config/inertia.php
'pages' => [
    'ensure_pages_exist' => false,
    'paths' => [resource_path('js/Pages')],
    'extensions' => ['js', 'jsx', 'svelte', 'ts', 'tsx', 'vue'],
],

'testing' => [
    'ensure_pages_exist' => true,
],
```

The updated config file should have already been republished as part of the [upgrade dependencies](#upgrade-dependencies) step above.

### Testing Concerns Removed

The deprecated `Inertia\Testing\Concerns\Has`, `Inertia\Testing\Concerns\Matching`, and `Inertia\Testing\Concerns\Debugging` traits have been removed. These traits were deprecated in v1 and replaced by the `AssertableInertia` class. No action is required unless your application references these traits directly.

### React Arrow Function Layout Components

The new layout implementation in v3 no longer supports arrow function components assigned directly to `.layout`. Inertia cannot reliably distinguish them from render functions at runtime. Wrapping the component in an array resolves this:

```jsx theme={null}
const Layout = ({ children }) => <main>{children}</main>

// ❌ does not work — arrow function component assigned directly
Dashboard.layout = Layout

// ✅ wrap in an array instead
Dashboard.layout = [Layout]
```

Function declaration components continue to work without any changes.

## Other Changes

***

### Blade Components

Inertia now provides `<x-inertia::head>` and `<x-inertia::app>` Blade components as an alternative to the `@inertiaHead` and `@inertia` directives. The head component accepts fallback content via its slot that only renders when SSR is not active, solving the long-standing issue of duplicate `<title>` tags in SSR applications.

```blade resources/views/app.blade.php theme={null}
<html>
    <head>
        @vite('resources/js/app.js')
        <x-inertia::head>
            <title>{{ config('app.name') }}</title>
        </x-inertia::head>
    </head>
    <body>
        <x-inertia::app />
    </body>
</html>
```

The existing directives continue to work and require no changes.

### SSR in Development

When using the new `@inertiajs/vite` plugin, SSR works automatically during development by simply running `npm run dev`. You no longer need to build your SSR bundle with `vite build --ssr` or start a separate Node.js server with `php artisan inertia:start-ssr` during development. These commands are now only required for [production deployments](https://inertiajs.com/docs/v3/advanced/server-side-rendering.md#running-the-ssr-server).

### Middleware Priority

The Inertia middleware is now automatically registered in Laravel's [middleware priority](https://laravel.com/docs/middleware#sorting-middleware) list, ensuring it runs before middleware like `ThrottleRequests`. This fixes an issue where `PUT`/`PATCH`/`DELETE` requests that were rate-limited could receive a `302` redirect instead of the correct `303`, causing the browser to retry the original request method on the redirect target. No action is required.

### Nested Prop Types

Prop types like `Inertia::optional()`, `Inertia::defer()`, and `Inertia::merge()` now work inside closures and nested arrays. Inertia resolves them at any depth and uses dot-notation paths in partial reload metadata.

```php theme={null}
return Inertia::render('Dashboard', [
    'auth' => fn () => [
        'user' => Auth::user(),
        'notifications' => Inertia::defer(fn () => Auth::user()->unreadNotifications),
        'invoices' => Inertia::optional(fn () => Auth::user()->invoices),
    ],
]);
```

On the client side, the `only` and `except` options, as well as the `Deferred` and `WhenVisible` components, all support dot-notation for targeting nested props.

```js theme={null}
router.reload({ only: ['auth.notifications'] })
```

Classes implementing the [`ProvidesInertiaProperties`](https://inertiajs.com/docs/v3/the-basics/responses#providesinertiaproperties-interface) interface also work at any nesting level.

```php theme={null}
return Inertia::render('Dashboard', [
    'auth' => [
        new AuthProps,
        'team' => 'Inertia',
    ],
]);
```

### ES2022 Build Target

Inertia packages now target ES2022, up from ES2020 in v2. You may use the [`@vitejs/plugin-legacy`](https://www.npmjs.com/package/@vitejs/plugin-legacy) Vite plugin if your application needs to support older browsers.

### ESM-Only Packages

All Inertia packages now ship as ES Modules only. CommonJS `require()` imports are no longer supported. You should update any `require()` calls to use `import` statements instead.

### Page Object Changes

The `clearHistory` and `encryptHistory` properties in the [page object](https://inertiajs.com/docs/v3/core-concepts/the-protocol.md#the-page-object) are now optional and only included in the response when `true`. Previously, every response included `"clearHistory": false` and `"encryptHistory": false` even when history wasn't being cleared or encrypted.
