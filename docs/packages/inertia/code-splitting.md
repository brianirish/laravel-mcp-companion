Source: https://inertiajs.com/docs/v3/advanced/code-splitting.md

# Code Splitting

By default, Inertia lazy-loads page components, splitting each page into its own bundle that is loaded on demand. This reduces the initial JavaScript bundle size but requires additional requests when visiting new pages.

You may disable lazy loading to eagerly bundle all pages into a single file. Eager loading eliminates per-page requests but increases the initial bundle size.

## Vite Plugin

The `lazy` option in the `pages` shorthand controls how page components are loaded. It defaults to `true`.

```js theme={null}
createInertiaApp({
    pages: {
        lazy: false, // Bundle all pages into a single file
    },
    // ...
})
```

## Manual Vite

You may configure code splitting manually using Vite's `import.meta.glob()` function when not using the Inertia Vite plugin. Pass `{ eager: true }` to bundle all pages, or omit it to lazy-load them.

```js Vue icon="vuejs" theme={null}
resolve: name => {
    const pages = import.meta.glob('./Pages/**/*.vue') // [!code --:2]
    return pages[`./Pages/${name}.vue`]()
    const pages = import.meta.glob('./Pages/**/*.vue', { eager: true }) // [!code ++:2]
    return pages[`./Pages/${name}.vue`]
},
```

```js React icon="react" theme={null}
resolve: name => {
    const pages = import.meta.glob('./Pages/**/*.jsx') // [!code --:2]
    return pages[`./Pages/${name}.jsx`]()
    const pages = import.meta.glob('./Pages/**/*.jsx', { eager: true }) // [!code ++:2]
    return pages[`./Pages/${name}.jsx`]
},
```

```js Svelte icon="s" theme={null}
resolve: name => {
    const pages = import.meta.glob('./Pages/**/*.svelte') // [!code --:2]
    return pages[`./Pages/${name}.svelte`]()
    const pages = import.meta.glob('./Pages/**/*.svelte', { eager: true }) // [!code ++:2]
    return pages[`./Pages/${name}.svelte`]
},
```

## Preloading the Initial Page

On the first visit to your application, the browser must download and execute your main JavaScript bundle before it knows which page component to load. You may avoid this extra round trip by passing the current page component to the `@vite` directive in your root template, which preloads the page component and its dependencies alongside your main bundle.

```blade Vue icon="vuejs" theme={null}
@vite(['resources/js/app.js', "resources/js/Pages/{$page['component']}.vue"])
```

```blade React icon="react" theme={null}
@vite(['resources/js/app.jsx', "resources/js/Pages/{$page['component']}.jsx"])
```

```blade Svelte icon="s" theme={null}
@vite(['resources/js/app.js', "resources/js/Pages/{$page['component']}.svelte"])
```

The `$page` variable is available in your root template and contains the [page object](https://inertiajs.com/docs/v3/core-concepts/the-protocol.md#the-page-object).

### Link Headers

Laravel's `AddLinkHeadersForPreloadedAssets` middleware, included in the Laravel starter kits, adds every preloaded asset to a `Link` response header, allowing the browser to start downloading them before parsing the HTML. Since the dependencies of the page component are included as well, this header may exceed your web server's response header buffer on larger pages, causing the initial page load to fail. Subsequent Inertia visits are not affected, as they return JSON without rendering the root template.

You may limit the number of assets included in the header using the middleware's `using()` method, which is available as of Laravel 12.12.

```php theme={null}
use App\Http\Middleware\HandleInertiaRequests;
use Illuminate\Http\Middleware\AddLinkHeadersForPreloadedAssets;

->withMiddleware(function (Middleware $middleware) {
    $middleware->web(append: [
        HandleInertiaRequests::class,
        AddLinkHeadersForPreloadedAssets::using(limit: 10),
    ]);
})
```

Assets beyond the limit are still preloaded by the `<link>` tags rendered by the `@vite` directive, so removing the middleware entirely has little impact. Alternatively, you may increase your web server's response header buffer, such as Nginx's `fastcgi_buffer_size` directive, or `proxy_buffer_size` when proxying requests to [Laravel Octane](https://laravel.com/docs/octane).

## Webpack

To use code splitting with Webpack, enable [dynamic imports](https://github.com/tc39/proposal-dynamic-import) with a Babel plugin:

```bash theme={null}
npm install @babel/plugin-syntax-dynamic-import
```

Next, create a `.babelrc` file in your project with the following configuration:

```json theme={null}
{
    "plugins": ["@babel/plugin-syntax-dynamic-import"]
}
```

If you're using Laravel Mix, the Babel plugin for dynamic imports is already installed and configured, and you can skip these steps. We recommend using Laravel Mix 6 or later, as there are known issues with older versions.

Finally, update the `resolve` callback in your app's initialization code to use `import` instead of `require`.

```js Vue icon="vuejs" theme={null}
resolve: name => require(`./Pages/${name}`), // [!code --]
resolve: name => import(`./Pages/${name}`), // [!code ++]
```

```js React icon="react" theme={null}
resolve: name => require(`./Pages/${name}`), // [!code --]
resolve: name => import(`./Pages/${name}`), // [!code ++]
```

```js Svelte icon="s" theme={null}
resolve: name => require(`./Pages/${name}.svelte`), // [!code --]
resolve: name => import(`./Pages/${name}.svelte`), // [!code ++]
```

You should also consider using cache busting to force browsers to load the latest version of your assets. To accomplish this, add the following configuration to your Webpack configuration file.

```js theme={null}
output: {
    chunkFilename: 'js/[name].js?id=[chunkhash]',
}
```
