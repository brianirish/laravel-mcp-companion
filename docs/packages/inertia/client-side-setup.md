Source: https://inertiajs.com/docs/v3/installation/client-side-setup.md

# Client-Side Setup

Once you have your [server-side framework configured](https://inertiajs.com/docs/v3/installation/server-side-setup.md), you then need to set up your client-side framework. Inertia currently provides support for React, Vue, and Svelte.

> [card] [Laravel Starter Kits](https://laravel.com/docs/starter-kits)
>
> Laravel's starter kits provide out-of-the-box scaffolding for new Inertia applications.
>
> These starter kits are the absolute fastest way to start building a new Inertia project using Laravel and Vue or React. However, if you would like to manually install Inertia into your application, please consult the documentation below.

## Prerequisites

Inertia requires your client-side framework and its corresponding [Vite plugin](https://laravel.com/docs/vite#vue) to be installed and configured. You may skip this section if your application already has these set up.

```bash Vue icon="vuejs" theme={null}
npm install vue @vitejs/plugin-vue
```

```bash React icon="react" theme={null}
npm install react react-dom @vitejs/plugin-react
```

```bash Svelte icon="s" theme={null}
npm install svelte @sveltejs/vite-plugin-svelte
```

Then, add the framework plugin to your `vite.config.js` file.

```js Vue icon="vuejs" theme={null}
import { defineConfig } from 'vite'
import laravel from 'laravel-vite-plugin'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
    plugins: [
        laravel({
            input: ['resources/js/app.js'],
            refresh: true,
        }),
        vue(),
    ],
})
```

```js React icon="react" theme={null}
import { defineConfig } from 'vite'
import laravel from 'laravel-vite-plugin'
import react from '@vitejs/plugin-react'

export default defineConfig({
    plugins: [
        laravel({
            input: ['resources/js/app.jsx'],
            refresh: true,
        }),
        react(),
    ],
})
```

```js Svelte icon="s" theme={null}
import { defineConfig } from 'vite'
import laravel from 'laravel-vite-plugin'
import { svelte } from '@sveltejs/vite-plugin-svelte'

export default defineConfig({
    plugins: [
        laravel({
            input: ['resources/js/app.js'],
            refresh: true,
        }),
        svelte(),
    ],
})
```

For more information on configuring these plugins, consult Laravel's [Vite documentation](https://laravel.com/docs/vite#vue).

## Installation

The `@inertiajs/vite` plugin supports Vite 7 and Vite 8.

**1. Install dependencies**

Install the Inertia client-side adapter and Vite plugin.

```bash Vue icon="vuejs" theme={null}
npm install @inertiajs/vue3 @inertiajs/vite
```

```bash React icon="react" theme={null}
npm install @inertiajs/react @inertiajs/vite
```

```bash Svelte icon="s" theme={null}
npm install @inertiajs/svelte @inertiajs/vite
```

**2. Configure Vite**

Add the Inertia plugin to your `vite.config.js` file.

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

**3. Initialize the Inertia app**

Update your main JavaScript file to boot your Inertia app. The Vite plugin handles page resolution and mounting automatically, so a minimal entry point is all you need.

```js Vue icon="vuejs" theme={null}
import { createInertiaApp } from '@inertiajs/vue3'

createInertiaApp()
```

```jsx React icon="react" theme={null}
import { createInertiaApp } from '@inertiajs/react'

createInertiaApp()
```

```js Svelte icon="s" theme={null}
import { createInertiaApp } from '@inertiajs/svelte'

createInertiaApp()
```

The plugin generates a default resolver that looks for pages in both `./pages` and `./Pages` directories, and the app mounts automatically.

### React Strict Mode

The React adapter supports enabling React's [Strict Mode](https://react.dev/reference/react/StrictMode) via the `strictMode` option.

```jsx theme={null}
createInertiaApp({
    strictMode: true,
    // ...
})
```

### Pages Shorthand

You may use the `pages` shorthand to customize which directory to search for page components.

```js Vue icon="vuejs" theme={null}
createInertiaApp({
    pages: './AppPages',
    // ...
})
```

```jsx React icon="react" theme={null}
createInertiaApp({
    pages: './AppPages',
    // ...
})
```

```js Svelte icon="s" theme={null}
createInertiaApp({
    pages: './AppPages',
    // ...
})
```

An object may also be provided for more control over how pages are resolved. You only need to include the options you wish to customize.

```js theme={null}
createInertiaApp({
    pages: {
        path: './Pages',
        extension: '.tsx',
        lazy: true,
        transform: (name, page) => name.replace('/', '-'),
    },
})
```

| Option | Description |
| - | - |
| `path` | The directory to search for page components. |
| `extension` | A string or array of file extensions (e.g., `'.tsx'` or `['.tsx', '.jsx']`). Defaults to your framework's extension. |
| `lazy` | Whether to lazy-load page components. Defaults to `true`. See [code splitting](https://inertiajs.com/docs/v3/advanced/code-splitting.md). |
| `transform` | A callback that receives the page name and page object, returning a transformed name. |

## Customizing the App

Sometimes, you may wish to customize the app instance, for example, to register plugins, wrap it with providers, or set context values. Pass the `withApp` callback to `createInertiaApp` to customize the app before it renders.

```js Vue icon="vuejs" theme={null}
import { createInertiaApp } from '@inertiajs/vue3'
import { createI18n } from 'vue-i18n'

const i18n = createI18n({
    // ...
})

createInertiaApp({
    withApp(app) {
        app.use(i18n)
    },
})
```

```jsx React icon="react" theme={null}
import { createInertiaApp } from '@inertiajs/react'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'

const queryClient = new QueryClient()

createInertiaApp({
    withApp(app) {
        return (
            <QueryClientProvider client={queryClient}>
                {app}
            </QueryClientProvider>
        )
    },
})
```

```js Svelte icon="s" theme={null}
import { createInertiaApp } from '@inertiajs/svelte'

createInertiaApp({
    withApp(context) {
        context.set('theme', 'dark')
    },
})
```

The callback receives the Vue app instance, allowing you to call `app.use()`, `app.provide()`, `app.component()`, and any other app-level method.

The callback receives the React element and must return a new element. This is where you may wrap your app with context providers.

The callback receives a `Map` that serves as Svelte's component context. Values set here are accessible in your components via `getContext()`.

A second argument provides the current rendering environment via `ssr`, allowing you to conditionally apply logic based on where the app is running.

```js Vue icon="vuejs" theme={null}
createInertiaApp({
    withApp(app, { ssr }) {
        app.use(i18n)

        if (!ssr) {
            app.use(browserOnlyPlugin)
        }
    },
})
```

```jsx React icon="react" theme={null}
createInertiaApp({
    withApp(app, { ssr }) {
        if (!ssr) {
            return <BrowserProvider>{app}</BrowserProvider>
        }

        return app
    },
})
```

```js Svelte icon="s" theme={null}
createInertiaApp({
    withApp(context, { ssr }) {
        context.set('theme', 'dark')

        if (!ssr) {
            context.set('analytics', createAnalytics())
        }
    },
})
```

The second argument also includes the current `page` object, giving you access to the component name, URL, version, and shared props before the app renders. This is useful for configuring plugins or providers with server-driven state, such as the user's locale.

```js Vue icon="vuejs" theme={null}
createInertiaApp({
    withApp(app, { page }) {
        const i18n = createI18n({ locale: page.props.locale })

        app.use(i18n)
    },
})
```

```jsx React icon="react" theme={null}
createInertiaApp({
    withApp(app, { page }) {
        const i18n = createI18n({ locale: page.props.locale })

        return <I18nProvider i18n={i18n}>{app}</I18nProvider>
    },
})
```

```js Svelte icon="s" theme={null}
createInertiaApp({
    withApp(context, { page }) {
        context.set('locale', page.props.locale)
    },
})
```

## AI Assistants and IDE Integrations

AI assistants and IDE integrations often write state files into your project root. With `laravel-vite-plugin`'s `refresh: true` enabled, these writes may trigger unexpected full page reloads, since Vite's watcher only ignores `node_modules` and `.git` by default.

You may extend Vite's `server.watch.ignored` option to exclude these paths.

```js vite.config.js theme={null}
export default defineConfig({
    server: {
        watch: {
            ignored: [
                '**/.junie/**',
                '**/.cursor/**',
                '**/.claude/**',
            ],
        },
    },
    // ...
})
```

Adjust the list to match your installed tools. See Vite's [server.watch](https://vite.dev/config/server-options.html#server-watch) documentation for additional options.

## Manual Setup

If you prefer not to use the Vite plugin, you may provide the `resolve` and `setup` callbacks manually. The `resolve` callback tells Inertia how to load a page component and receives the component name and the full [page object](https://inertiajs.com/docs/v3/core-concepts/the-protocol.md). The `setup` callback initializes the client-side framework.

> [!NOTE]
>
> A manual `setup` callback prevents the Vite plugin from auto-generating [SSR](https://inertiajs.com/docs/v3/advanced/server-side-rendering.md) handling. You should create a [separate SSR entry point](https://inertiajs.com/docs/v3/advanced/server-side-rendering.md#ssr-entry-point) and update your app to use [client-side hydration](https://inertiajs.com/docs/v3/advanced/server-side-rendering.md#client-side-hydration).

```js Vue icon="vuejs" theme={null}
import { createApp, h } from 'vue'
import { createInertiaApp } from '@inertiajs/vue3'

createInertiaApp({
    resolve: name => {
        const pages = import.meta.glob('./Pages/**/*.vue')
        return pages[`./Pages/${name}.vue`]()
    },
    setup({ el, App, props, plugin }) {
        createApp({ render: () => h(App, props) })
            .use(plugin)
            .mount(el)
    },
})
```

```jsx React icon="react" theme={null}
import { createInertiaApp } from '@inertiajs/react'
import { createRoot } from 'react-dom/client'

createInertiaApp({
    resolve: name => {
        const pages = import.meta.glob('./Pages/**/*.jsx')
        return pages[`./Pages/${name}.jsx`]()
    },
    setup({ el, App, props }) {
        createRoot(el).render(<App {...props} />)
    },
})
```

```js Svelte icon="s" theme={null}
import { createInertiaApp } from '@inertiajs/svelte'
import { mount } from 'svelte'

createInertiaApp({
    resolve: name => {
        const pages = import.meta.glob('./Pages/**/*.svelte')
        return pages[`./Pages/${name}.svelte`]()
    },
    setup({ el, App, props }) {
        mount(App, { target: el, props })
    },
})
```

By default, page components are lazy-loaded, splitting each page into its own bundle. To eagerly bundle all pages into a single file instead, see the [code splitting](https://inertiajs.com/docs/v3/advanced/code-splitting.md) documentation.

The `laravel-vite-plugin` package also provides a [`resolvePageComponent`](https://laravel.com/docs/vite#inertia) helper that may be used to resolve page components.

```js Vue icon="vuejs" theme={null}
import { resolvePageComponent } from 'laravel-vite-plugin/inertia-helpers'

resolve: name => resolvePageComponent(`./Pages/${name}.vue`, import.meta.glob('./Pages/**/*.vue')),
```

```js React icon="react" theme={null}
import { resolvePageComponent } from 'laravel-vite-plugin/inertia-helpers'

resolve: name => resolvePageComponent(`./Pages/${name}.jsx`, import.meta.glob('./Pages/**/*.jsx')),
```

```js Svelte icon="s" theme={null}
import { resolvePageComponent } from 'laravel-vite-plugin/inertia-helpers'

resolve: name => resolvePageComponent(`./Pages/${name}.svelte`, import.meta.glob('./Pages/**/*.svelte')),
```

## Configuring Defaults

You may pass a `defaults` object to `createInertiaApp()` to configure default settings for various features. You don't have to pass a default for every key, just the ones you want to tweak.

```js theme={null}
createInertiaApp({
  defaults: {
    form: {
      recentlySuccessfulDuration: 5000,
    },
    prefetch: {
      cacheFor: "1m",
      hoverDelay: 150,
    },
    visitOptions: (href, options) => {
      return {
        headers: {
          ...options.headers,
          "X-Custom-Header": "value",
        },
      };
    },
  },
  // ...
});
```

The `visitOptions` callback receives the target URL and the current visit options, and should return an object with any options you want to override. For more details on the available configuration options, see the [forms](https://inertiajs.com/docs/v3/the-basics/forms.md#form-errors), [prefetching](https://inertiajs.com/docs/v3/data-props/prefetching.md), and [manual visits](https://inertiajs.com/docs/v3/the-basics/manual-visits.md#global-visit-options) documentation.

### Updating Configuration at Runtime

You may also update configuration values at runtime using the exported `config` instance. This is particularly useful when you need to adjust settings based on user preferences or application state.

```js Vue icon="vuejs" theme={null}
import { config } from "@inertiajs/vue3";

// Set a single value using dot notation...
config.set("form.recentlySuccessfulDuration", 1000);
config.set("prefetch.cacheFor", "5m");

// Set multiple values at once...
config.set({
  "form.recentlySuccessfulDuration": 1000,
  "prefetch.cacheFor": "5m",
});
```

```js React icon="react" theme={null}
import { config } from "@inertiajs/react";

// Set a single value using dot notation...
config.set("form.recentlySuccessfulDuration", 1000);
config.set("prefetch.cacheFor", "5m");

// Set multiple values at once...
config.set({
  "form.recentlySuccessfulDuration": 1000,
  "prefetch.cacheFor": "5m",
});

// Get a configuration value...
const duration = config.get("form.recentlySuccessfulDuration");
```

```js Svelte icon="s" theme={null}
import { config } from "@inertiajs/svelte";

// Set a single value using dot notation...
config.set("form.recentlySuccessfulDuration", 1000);
config.set("prefetch.cacheFor", "5m");

// Set multiple values at once...
config.set({
  "form.recentlySuccessfulDuration": 1000,
  "prefetch.cacheFor": "5m",
});

// Get a configuration value...
const duration = config.get("form.recentlySuccessfulDuration");
```

## Defining a Root Element

By default, Inertia assumes that your application's root template has a root element with an `id` of `app`. If your application's root element has a different `id`, you can provide it using the `id` property.

```js theme={null}
createInertiaApp({
  id: "my-app",
  // ...
});
```

If you change the `id` of the root element, be sure to update it [server-side](https://inertiajs.com/docs/v3/installation/server-side-setup.md#root-template) as well.

## Content Security Policy

For applications using a [Content Security Policy](https://developer.mozilla.org/en-US/docs/Web/HTTP/CSP) that restricts inline styles, you may pass a `nonce` to `createInertiaApp()`. The nonce is applied to the inline styles Inertia injects for the [progress bar](https://inertiajs.com/docs/v3/advanced/progress-indicators.md) and the [error modal](https://inertiajs.com/docs/v3/advanced/error-handling.md), allowing them through your CSP.

```js theme={null}
createInertiaApp({
  nonce: "your-csp-nonce",
  // ...
});
```

## HTTP Client

Unlike Inertia 2 and earlier, Inertia 3 uses a built-in XHR client for all requests. No additional HTTP libraries like Axios are required.

### Using Axios

You may provide the `axiosAdapter` as the `http` option when creating your Inertia app. This is useful when your application requires a custom Axios instance.

```js theme={null}
import { axiosAdapter } from '@inertiajs/core'

createInertiaApp({
  http: axiosAdapter(),
  // ...
})
```

A custom Axios instance may also be provided to the adapter.

```js theme={null}
import axios from 'axios'
import { axiosAdapter } from '@inertiajs/core'

const instance = axios.create({
  // ...
})

createInertiaApp({
  http: axiosAdapter(instance),
  // ...
})
```

### Interceptors

The built-in XHR client supports interceptors for modifying requests, inspecting responses, or handling errors. These interceptors apply to all HTTP requests made by Inertia, including those from the router, `useForm`, `<Form>`, and `useHttp`.

```js Vue icon="vuejs" theme={null}
import { http } from '@inertiajs/vue3'

const removeRequestHandler = http.onRequest((config) => {
  config.headers['X-Custom-Header'] = 'value'
  return config
})

const removeResponseHandler = http.onResponse((response) => {
  console.log('Response status:', response.status)
  return response
})

const removeErrorHandler = http.onError((error) => {
  console.error('Request failed:', error)
})

// Remove a handler when it's no longer needed...
removeRequestHandler()
```

```js React icon="react" theme={null}
import { http } from '@inertiajs/react'

const removeRequestHandler = http.onRequest((config) => {
  config.headers['X-Custom-Header'] = 'value'
  return config
})

const removeResponseHandler = http.onResponse((response) => {
  console.log('Response status:', response.status)
  return response
})

const removeErrorHandler = http.onError((error) => {
  console.error('Request failed:', error)
})

// Remove a handler when it's no longer needed...
removeRequestHandler()
```

```js Svelte icon="s" theme={null}
import { http } from '@inertiajs/svelte'

const removeRequestHandler = http.onRequest((config) => {
  config.headers['X-Custom-Header'] = 'value'
  return config
})

const removeResponseHandler = http.onResponse((response) => {
  console.log('Response status:', response.status)
  return response
})

const removeErrorHandler = http.onError((error) => {
  console.error('Request failed:', error)
})

// Remove a handler when it's no longer needed...
removeRequestHandler()
```

Each `on*` method returns a cleanup function that removes the handler when called. Request handlers receive the request config and must return it (modified or not). Response handlers receive the response and must also return it. Handlers may be asynchronous.

### Custom HTTP Client

For full control over how requests are made, you may provide a completely custom HTTP client via the `http` option. A custom client must implement the `request` method, which receives an `HttpRequestConfig` and returns a promise resolving to an `HttpResponse`. Review the [xhrHttpClient.ts](https://github.com/inertiajs/inertia/blob/3.x/packages/core/src/xhrHttpClient.ts) source for a reference implementation.
