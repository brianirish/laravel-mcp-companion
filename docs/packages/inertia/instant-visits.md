Source: https://inertiajs.com/docs/v3/the-basics/instant-visits.md

# Instant Visits

Sometimes you may wish to navigate to a new page without waiting for the server to respond. Instant visits allow Inertia to immediately swap to the target page component while the server request happens in the background. Once the server responds, the real props are merged in.

Unlike [client-side visits](https://inertiajs.com/docs/v3/the-basics/manual-visits.md#client-side-visits), which update the page entirely on the client without making a server request, instant visits still make a full server request. The difference is that the user sees the target page right away instead of waiting for the response.

## Basic Usage

To make an instant visit, provide the target `component` name to a `Link` or to `router.visit()`.

```vue Vue icon="vuejs" theme={null}
import { Link } from '@inertiajs/vue3'

<Link href="/dashboard" component="Dashboard">Dashboard</Link>
```

```jsx React icon="react" theme={null}
import { Link } from "@inertiajs/react";

<Link href="/dashboard" component="Dashboard">
  Dashboard
</Link>;
```

```svelte Svelte icon="s" theme={null}
import { inertia, Link } from '@inertiajs/svelte'

<a href="/dashboard" use:inertia={{ component: 'Dashboard' }}>Dashboard</a>

<Link href="/dashboard" component="Dashboard">Dashboard</Link>
```

When clicked, Inertia immediately renders the `Dashboard` component while the server request fires in the background. The full props are merged in when the response arrives.

The target component must be able to render without its page-specific props, as only [shared props](https://inertiajs.com/docs/v3/data-props/shared-data.md) are available on the intermediate page. You may use optional chaining or conditional rendering to handle missing props.

Programmatic instant visits work the same way via the `component` option on `router.visit()`.

```js theme={null}
router.visit("/dashboard", {
  component: "Dashboard",
});
```

## Shared Props

The Laravel adapter includes a `sharedProps` metadata key in the page response, listing the top-level prop keys registered via `Inertia::share()`.

```json theme={null}
{
  "component": "Dashboard",
  "props": { "auth": { "user": "..." }, "stats": { ... } },
  "sharedProps": ["auth"]
}
```

Inertia reads this list and carries those props over from the current page to the intermediate page. Props like `auth` are available immediately, while page-specific props like `stats` will be `undefined` until the server responds.

## Page Props

You may provide props for the intermediate page using the `pageProps` option. This is useful for passing data you already have on the current page, or for setting placeholder values to display loading states while the server responds.

```vue Vue icon="vuejs" theme={null}
import { Link } from '@inertiajs/vue3'

<Link
  href="/posts/1"
  component="Posts/Show"
  :page-props="{ title: 'Loading...' }"
>
  View Post
</Link>
```

```jsx React icon="react" theme={null}
import { Link } from "@inertiajs/react";

<Link
  href="/posts/1"
  component="Posts/Show"
  pageProps={{ title: "Loading..." }}
>
  View Post
</Link>;
```

```svelte Svelte icon="s" theme={null}
import { Link } from '@inertiajs/svelte'

<Link
  href="/posts/1"
  component="Posts/Show"
  pageProps={{ title: 'Loading...' }}
>
  View Post
</Link>
```

When `pageProps` is provided as an object, shared props are not automatically carried over. You are in full control of the intermediate page's props.

A callback may also be passed to `pageProps`. The callback receives the current page's props and the shared props as arguments, so you may selectively spread them.

```js theme={null}
router.visit("/posts/1", {
  component: "Posts/Show",
  pageProps: (currentProps, sharedProps) => ({
    ...sharedProps,
    title: "Loading...",
  }),
});
```

## Wayfinder Integration

When using [Wayfinder](https://github.com/laravel/wayfinder), you may use the `instant` prop on the `Link` component. Inertia will extract the target component from the Wayfinder route definition, removing the need to manually specify the `component` prop.

```vue Vue icon="vuejs" theme={null}
import { Link } from '@inertiajs/vue3' import { show } from
'App/Http/Controllers/PostController'

<Link :href="show(1)" instant>View Post</Link>
```

```jsx React icon="react" theme={null}
import { Link } from "@inertiajs/react";
import { show } from "App/Http/Controllers/PostController";

<Link href={show(1)} instant>
  View Post
</Link>;
```

```svelte Svelte icon="s" theme={null}
import { Link } from '@inertiajs/svelte'
import { show } from 'App/Http/Controllers/PostController'

<Link href={show(1)} instant>View Post</Link>
```

The `instant` prop is also available on the `Form` component.

```vue Vue icon="vuejs" theme={null}
import { Form } from '@inertiajs/vue3'
import { store } from 'App/Http/Controllers/PostController'

<Form :action="store()" instant>
  <!-- ... -->
</Form>
```

```jsx React icon="react" theme={null}
import { Form } from "@inertiajs/react";
import { store } from "App/Http/Controllers/PostController";

<Form action={store()} instant>
  {/* ... */}
</Form>;
```

```svelte Svelte icon="s" theme={null}
import { Form } from '@inertiajs/svelte'
import { store } from 'App/Http/Controllers/PostController'

<Form action={store()} instant>
  <!-- ... -->
</Form>
```

An explicit `component` prop always takes priority over `instant`.

### Wayfinder Configuration

To include component information in your Wayfinder route definitions, enable the `generate.inertia.component` option in your `config/wayfinder.php` configuration file.

```php config/wayfinder.php theme={null}
return [
    'generate' => [
        'inertia' => [
            'component' => true,
        ],
    ],
];
```

After enabling this option and regenerating your Wayfinder routes, each route definition will include the component name that Inertia renders for that route.

### Conditional Components

A controller action may conditionally render different components, preventing the `instant` prop from determining which component to use. You may call the `withComponent()` method on the Wayfinder route function to specify the target component.

```js theme={null}
import { show } from "App/Http/Controllers/DashboardController";

router.visit(show.withComponent("Dashboard/Admin"));
```

## Disabling Shared Prop Keys

You may disable the `sharedProps` metadata key in your `config/inertia.php` configuration file. The server will still resolve and include shared prop values in the response, but the metadata listing which keys are shared will be omitted. Without this list, the client cannot identify which props to carry over during instant visits.

```php config/inertia.php theme={null}
return [
    'expose_shared_prop_keys' => false,
];
```
