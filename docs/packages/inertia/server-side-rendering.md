Source: https://inertiajs.com/docs/v3/advanced/server-side-rendering.md

# Server-Side Rendering (SSR)

Server-side rendering pre-renders your JavaScript pages on the server, allowing your visitors to receive fully rendered HTML when they visit your application. Since fully rendered HTML is served by your application, it's also easier for search engines to index your site.

Server-side rendering uses Node.js to render your pages in a background process; therefore, Node must be available on your server for server-side rendering to function properly. Inertia's SSR server requires Node.js 22 or higher.

## Laravel Starter Kits

If you are using [Laravel Starter Kits](https://laravel.com/docs/starter-kits), Inertia SSR is [supported](https://laravel.com/docs/starter-kits#inertia-ssr) through a build command:

```bash theme={null}
npm run build:ssr
```

## Vite Plugin Setup

The recommended way to configure SSR is with the [`@inertiajs/vite` plugin](https://inertiajs.com/docs/v3/installation/client-side-setup#installation). This approach handles SSR configuration automatically, including development mode SSR without a separate Node.js server.

**1. Install the Vite plugin**

```bash theme={null}
npm install @inertiajs/vite
```

**2. Configure Vite**

Add the Inertia plugin to your `vite.config.js` file. The plugin will automatically detect your SSR entry point.

```js vite.config.js theme={null}
import inertia from '@inertiajs/vite'
import laravel from 'laravel-vite-plugin'
import { defineConfig } from 'vite'

export default defineConfig({
    plugins: [
        laravel({
            input: ['resources/js/app.js'],
            refresh: true,
        }),
        inertia(),
    ],
})
```

You may also configure SSR options explicitly.

```js vite.config.js theme={null}
inertia({
    ssr: {
        entry: 'resources/js/ssr.js',
        port: 13714,
        host: '127.0.0.1',
        cluster: true,
    },
})
```

You may pass `false` to opt out of the plugin's automatic SSR handling, for example if you prefer to [configure SSR manually](#manual-setup) or [disable SSR entirely](#disabling-ssr).

```js vite.config.js theme={null}
inertia({
    ssr: false,
})
```

**3. Update your build script**

Update the `build` script in your `package.json` to build both bundles.

```json package.json theme={null}
"scripts": {
    "dev": "vite",
   "build": "vite build" // [!code --]
   "build": "vite build && vite build --ssr" // [!code ++]
},
```

### Development Mode

The Vite plugin handles SSR automatically during development. There is no need to build your SSR bundle or start a separate Node.js server. Simply run your Vite dev server as usual:

```bash theme={null}
npm run dev
```

The Vite plugin exposes a server endpoint that Laravel uses for rendering, complete with HMR support.

### Production

For production, build both bundles and start the SSR server.

```bash theme={null}
npm run build
php artisan inertia:start-ssr
```

### Clustering

By default, the SSR server runs on a single thread. You may enable clustering to start multiple Node servers on the same port, with requests handled by each thread in a round-robin fashion.

```js vite.config.js theme={null}
inertia({
    ssr: {
        cluster: true,
    },
})
```

### Host

By default, the SSR server binds to `0.0.0.0`, making it accessible on all network interfaces. You may restrict it to a specific interface using the `host` option.

```js vite.config.js theme={null}
inertia({
    ssr: {
        host: '127.0.0.1',
    },
})
```

## Manual Setup

The Vite plugin reuses your `app.js` entry point for SSR by default, so no separate file is needed. Most customizations may be handled using the [`withApp` callback](https://inertiajs.com/docs/v3/installation/client-side-setup#customizing-the-app).

For more control, such as providing a [manual `setup` callback](https://inertiajs.com/docs/v3/installation/client-side-setup#manual-setup), you may create a separate `resources/js/ssr.js` entry point and update your `app.js` to use [client-side hydration](#client-side-hydration).

### SSR Entry Point

```js Vue icon="vuejs" theme={null}
import { createInertiaApp } from '@inertiajs/vue3'
import createServer from '@inertiajs/vue3/server'
import { createSSRApp, h } from 'vue'
import { renderToString } from 'vue/server-renderer'

createServer(page =>
    createInertiaApp({
        page,
        render: renderToString,
        resolve: name => {
            const pages = import.meta.glob('./Pages/**/*.vue')
            return pages[`./Pages/${name}.vue`]()
        },
        setup({ App, props, plugin }) {
            return createSSRApp({
                render: () => h(App, props),
            }).use(plugin)
        },
    }),
)
```

```jsx React icon="react" theme={null}
import { createInertiaApp } from '@inertiajs/react'
import createServer from '@inertiajs/react/server'
import ReactDOMServer from 'react-dom/server'

createServer(page =>
    createInertiaApp({
        page,
        render: ReactDOMServer.renderToString,
        resolve: name => {
            const pages = import.meta.glob('./Pages/**/*.jsx')
            return pages[`./Pages/${name}.jsx`]()
        },
        setup: ({ App, props }) => <App {...props} />,
    }),
)
```

```js Svelte icon="s" theme={null}
import { createInertiaApp } from '@inertiajs/svelte'
import createServer from '@inertiajs/svelte/server'
import { render } from 'svelte/server'

createServer(page =>
    createInertiaApp({
        page,
        resolve: name => {
            const pages = import.meta.glob('./Pages/**/*.svelte')
            return pages[`./Pages/${name}.svelte`]()
        },
        setup({ App, props }) {
            return render(App, { props })
        },
    }),
)
```

Be sure to add anything that's missing from your `app.js` file that makes sense to run in SSR mode, such as plugins or custom mixins.

### Client-Side Hydration

You should also update your `app.js` to use hydration instead of normal rendering. This allows VueReactSvelte to pick up the server-rendered HTML and make it interactive without re-rendering it.

```js Vue icon="vuejs" theme={null}
import { createApp, h } from 'vue' // [!code --]
import { createSSRApp, h } from 'vue' // [!code ++]
import { createInertiaApp } from '@inertiajs/vue3'

createInertiaApp({
    resolve: name => {
        const pages = import.meta.glob('./Pages/**/*.vue')
        return pages[`./Pages/${name}.vue`]()
    },
    setup({ el, App, props, plugin }) {
    createApp({ render: () => h(App, props) }) // [!code --]
    createSSRApp({ render: () => h(App, props) }) // [!code ++]
        .use(plugin)
        .mount(el)
    },
})
```

```js React icon="react" theme={null}
import { createInertiaApp } from '@inertiajs/react'
import { createRoot } from 'react-dom/client' // [!code --]
import { hydrateRoot } from 'react-dom/client' // [!code ++]

createInertiaApp({
    resolve: name => {
        const pages = import.meta.glob('./Pages/**/*.jsx')
        return pages[`./Pages/${name}.jsx`]()
    },
    setup({ el, App, props }) {
        createRoot(el).render(<App {...props} />) // [!code --]
        hydrateRoot(el, <App {...props} />) // [!code ++]
    },
})
```

```js Svelte icon="s" theme={null}
import { createInertiaApp } from '@inertiajs/svelte'
import { mount } from 'svelte' // [!code --]
import { hydrate, mount } from 'svelte' // [!code ++]

createInertiaApp({
    resolve: name => {
        const pages = import.meta.glob('./Pages/**/*.svelte')
        return pages[`./Pages/${name}.svelte`]()
    },
    setup({ el, App, props }) {
        mount(App, { target: el, props }) // [!code --]
        if (el.dataset.serverRendered === 'true') { // [!code ++:5]
            hydrate(App, { target: el, props })
        } else {
            mount(App, { target: el, props })
        }
    },
})
```

### Opting Out of the Vite Plugin

You may pass `ssr: false` to the Inertia plugin to disable its automatic SSR handling and manage the SSR build yourself. You should also add the `ssr` property to the Laravel Vite plugin configuration so it knows about your entry point.

```js Vue icon="vuejs" vite.config.js theme={null}
export default defineConfig({
    plugins: [
        laravel({
            input: ['resources/js/app.js'],
            ssr: 'resources/js/ssr.js', // [!code ++]
            refresh: true,
        }),
        inertia({
            ssr: false, // [!code ++]
        }),
    ],
})
```

```js React icon="react" vite.config.js theme={null}
export default defineConfig({
    plugins: [
        laravel({
            input: ['resources/js/app.jsx'],
            ssr: 'resources/js/ssr.jsx', // [!code ++]
            refresh: true,
        }),
        inertia({
            ssr: false, // [!code ++]
        }),
    ],
})
```

```js Svelte icon="s" vite.config.js theme={null}
export default defineConfig({
    plugins: [
        laravel({
            input: ['resources/js/app.js'],
            ssr: 'resources/js/ssr.js', // [!code ++]
            refresh: true,
        }),
        inertia({
            ssr: false, // [!code ++]
        }),
    ],
})
```

### Clustering

You may pass the `cluster` option to `createServer` to start multiple Node servers on the same port, with requests handled by each thread in a round-robin fashion.

```js Vue icon="vuejs" theme={null}
createServer(page =>
    createInertiaApp({
        // ...
    }),
    { cluster: true },
)
```

```jsx React icon="react" theme={null}
createServer(page =>
    createInertiaApp({
        // ...
    }),
    { cluster: true },
)
```

```js Svelte icon="s" theme={null}
createServer(page =>
    createInertiaApp({
        // ...
    }),
    { cluster: true },
)
```

### Host

By default, the SSR server binds to `0.0.0.0`, making it accessible on all network interfaces. You may pass the `host` option to `createServer` to restrict it to a specific interface.

```js Vue icon="vuejs" theme={null}
createServer(page =>
    createInertiaApp({
        // ...
    }),
    { host: '127.0.0.1' },
)
```

```jsx React icon="react" theme={null}
createServer(page =>
    createInertiaApp({
        // ...
    }),
    { host: '127.0.0.1' },
)
```

```js Svelte icon="s" theme={null}
createServer(page =>
    createInertiaApp({
        // ...
    }),
    { host: '127.0.0.1' },
)
```

## Running the SSR Server

> [!NOTE]
>
> The SSR server is only required in production. During development, the [Vite plugin](#development-mode) handles SSR automatically.

Once you have built both your client-side and server-side bundles, you may start the SSR server using the following Artisan command.

```bash theme={null}
php artisan inertia:start-ssr
```

By default, the SSR server uses `node` as its runtime. You may change this by setting the `runtime` option in your `config/inertia.php` file. An absolute path to the runtime binary is also supported.

```php theme={null}
'ssr' => [
    'runtime' => env('INERTIA_SSR_RUNTIME', 'node'),
],
```

The `--runtime` flag on the Artisan command overrides the configured value for a single invocation.

```bash theme={null}
php artisan inertia:start-ssr --runtime=bun
```

You may also enable the `ensure_runtime_exists` option to verify the runtime binary exists before attempting to start the SSR server. The command will exit with an error if the binary cannot be found.

```php theme={null}
'ssr' => [
    'ensure_runtime_exists' => (bool) env('INERTIA_SSR_ENSURE_RUNTIME_EXISTS', false),
],
```

With the server running, you should be able to access your app in the browser with server-side rendering enabled. In fact, you should be able to disable JavaScript entirely and still navigate around your application.

## Error Handling

When SSR rendering fails, Inertia gracefully falls back to client-side rendering. The Vite plugin logs detailed error information to the console, including the component name, request URL, source location, and a tailored hint to help you resolve the issue.

Common SSR errors are automatically classified. Browser API errors (such as referencing `window` or `document` in server-rendered code) include guidance on moving the code to a lifecycle hook. Components that depend on browser APIs may also be wrapped in [`WhenMounted`](#client-only-components). Component resolution errors suggest checking file paths and casing.

Inertia also dispatches an `SsrRenderFailed` event on the server. You may listen for this event to log failures or send them to an error tracking service.

```php theme={null}
use Illuminate\Support\Facades\Log;
use Inertia\Ssr\SsrRenderFailed;

Event::listen(SsrRenderFailed::class, function (SsrRenderFailed $event) {
    Log::warning('SSR failed', $event->toArray());
});
```

### Throwing on Error

Since Inertia gracefully falls back to client-side rendering, SSR failures may go unnoticed. Your tests pass because the client-side render succeeds, but your users never receive server-rendered HTML. This is especially common in E2E tests with tools like Laravel Dusk or Pest Browser Testing.

You may set the `throw_on_error` option in your `config/inertia.php` file to throw an exception instead of falling back silently, allowing you to catch SSR issues early.

```php theme={null}
'ssr' => [
    'throw_on_error' => (bool) env('INERTIA_SSR_THROW_ON_ERROR', false),
],
```

> [!WARNING]
>
> This option is not recommended for production, as it will cause SSR failures to return an error response instead of falling back to client-side rendering.

You may set the environment variable in your `phpunit.xml` to enable this only during testing.

```xml theme={null}
<env name="INERTIA_SSR_THROW_ON_ERROR" value="true"/>
```

## Configuring the SSR Request

Laravel Adapter v3.4.0+

The request to the SSR server uses Laravel's HTTP client defaults. You may set the `timeout` option in your `config/inertia.php` file so a slow or unresponsive SSR server doesn't delay your responses, as Inertia falls back to client-side rendering when the request fails.

```php config/inertia.php theme={null}
'ssr' => [
    'timeout' => env('INERTIA_SSR_TIMEOUT'),
],
```

For more control, you may use the `Inertia::configureSsrRequestUsing()` method, typically from a service provider. The callback receives the `PendingRequest` before it is sent, so you may add retries, headers, or any other option supported by Laravel's HTTP client.

```php theme={null}
use Illuminate\Http\Client\PendingRequest;
use Inertia\Inertia;

Inertia::configureSsrRequestUsing(function (PendingRequest $request) {
    $request->timeout(5)->retry(2, throw: false);
});
```

> [!NOTE]
>
> When using `retry()`, pass `throw: false` so failed renders are still reported with the error details from the SSR server.

Both the timeout and the callback apply to the render request and the health check used by the [`inertia:check-ssr`](#deployment) command.

## Disabling SSR

SSR has two layers: the **Vite plugin** serves SSR during development and builds the SSR bundle for production, while the **Laravel adapter** dispatches rendering requests to the SSR server. To fully disable SSR, you should disable both.

```js vite.config.js theme={null}
inertia({
    ssr: false,
})
```

```php config/inertia.php theme={null}
'ssr' => [
    'enabled' => false,
],
```

You may also prevent the Laravel adapter from dispatching SSR requests programmatically using the `Inertia::disableSsr()` method. This is useful when you want to keep SSR in your build but [disable it during tests](https://inertiajs.com/docs/v3/advanced/testing.md#disabling-ssr-during-tests) or in specific environments.

```php theme={null}
use Inertia\Inertia;

Inertia::disableSsr();
```

A boolean or closure may be provided to disable SSR conditionally.

```php theme={null}
Inertia::disableSsr(app()->runningUnitTests());

Inertia::disableSsr(fn () => app()->runningUnitTests());
```

## Excluding Routes from SSR

Sometimes you may wish to skip server-side rendering for certain routes while keeping SSR enabled for the rest of your application.

### Via Middleware

You may use the `$withoutSsr` property on your Inertia middleware to disable SSR for specific route patterns.

```php theme={null}
use Inertia\Middleware;

class HandleInertiaRequests extends Middleware
{
    /**
     * Defines the routes that should not use SSR.
     *
     * @var array<int, string>
     */
    protected $withoutSsr = [
        'admin/*',
        'dashboard',
    ];
}
```

### Via Facade

You may also exclude specific routes using the `Inertia::withoutSsr()` method, typically called from a service provider.

```php theme={null}
use Inertia\Inertia;

Inertia::withoutSsr(['admin/*', 'dashboard']);
```

### Per-Request

You may disable SSR for the current request by setting the `inertia.ssr.enabled` configuration value to `false`.

```php theme={null}
if (request()->is('admin/*')) {
    config(['inertia.ssr.enabled' => false]);
}
```

## Client-Only Components

v3.8.0+

Sometimes, a component relies on browser APIs such as `window` or `document` and cannot be rendered on the server. Instead of disabling SSR for the entire page, you may wrap the component in `WhenMounted`, which renders its children only after mounting in the browser. The `fallback` is rendered on the server and during hydration instead.

```vue Vue icon="vuejs" theme={null}
<script setup>
import { WhenMounted } from "@inertiajs/vue3";
import Chart from "@/Components/Chart.vue";
</script>

<template>
  <WhenMounted>
    <template #fallback>
      <div>Loading chart...</div>
    </template>

    <Chart />
  </WhenMounted>
</template>
```

```jsx React icon="react" theme={null}
import { WhenMounted } from "@inertiajs/react";
import Chart from "@/Components/Chart";

export default () => (
  <WhenMounted fallback={<div>Loading chart...</div>}>
    <Chart />
  </WhenMounted>
);
```

```svelte Svelte icon="s" theme={null}
<script>
  import { WhenMounted } from "@inertiajs/svelte";
  import Chart from "@/Components/Chart.svelte";
</script>

<WhenMounted>
  {#snippet fallback()}
    <div>Loading chart...</div>
  {/snippet}

  <Chart />
</WhenMounted>
```

The fallback only appears on the initial server-rendered page load. Subsequent visits, as well as applications not using SSR, render the children immediately.

JSX children are evaluated before `WhenMounted` renders, so expressions that access `window` directly still run on the server. You may pass a function as the children to defer their evaluation until the component mounts.

```jsx theme={null}
<WhenMounted fallback={<div>Loading chart...</div>}>
  {() => <Chart width={window.innerWidth} />}
</WhenMounted>
```

Note that `WhenMounted` only skips rendering on the server. The wrapped component is still part of your SSR bundle, so its module must be safe to import on the server.

## Deployment

When deploying your SSR-enabled app to production, you'll need to build both the client-side (`app.js`) and server-side bundles (`ssr.js`), and then run the SSR server as a background process, typically using a process monitoring tool such as Supervisor.

```bash theme={null}
php artisan inertia:start-ssr
```

To stop the SSR server, for instance when you deploy a new version of your website, you may utilize the `inertia:stop-ssr` Artisan command. Your process monitor (such as Supervisor) should be responsible for automatically restarting the SSR server after it has stopped.

```bash theme={null}
php artisan inertia:stop-ssr
```

Laravel Adapter v3.4.0+

By default, the command fails when the SSR server is not running. You may pass the `--graceful` option to return a successful exit code instead, making it ideal for deployment scripts where the SSR server is not yet running.

```bash theme={null}
php artisan inertia:stop-ssr --graceful
```

Laravel Adapter v3.6.0+

Before starting, the `inertia:start-ssr` command sends a shutdown request to the configured SSR URL to stop any server that is still running. Behind a load balancer, where several SSR servers share the same URL, this request may stop a different server that is still serving requests. You may pass the `--no-stop-before-start` option to skip the shutdown request.

```bash theme={null}
php artisan inertia:start-ssr --no-stop-before-start
```

You may use the `inertia:check-ssr` Artisan command to verify that the SSR server is running. This can be helpful after deployment and works well as a Docker health check to ensure the server is responding as expected.

```bash theme={null}
php artisan inertia:check-ssr
```

By default, a check is performed to ensure the server-side bundle exists before dispatching a request to the SSR server. In some cases, such as when your app runs on multiple servers or is containerized, the web server may not have access to the SSR bundle. To disable this check, you may set the `inertia.ssr.ensure_bundle_exists` configuration value to `false`.

### Laravel Cloud

To run the SSR server on Laravel Cloud, you may use Cloud's [native support for Inertia SSR](https://cloud.laravel.com/docs/compute#inertia-ssr).

### Laravel Forge

To run the SSR server on Forge, you may enable it via the [Inertia SSR toggle](https://forge.laravel.com/docs/sites/laravel#inertia-server-side-rendering-ssr) in your site's application panel. Forge will create the required daemon and, optionally, update your deploy script to restart the SSR server on each deployment.
