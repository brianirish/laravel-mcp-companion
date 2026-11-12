Source: https://inertiajs.com/docs/v3/data-props/shared-data.md

# Shared Data

Sometimes you need to access specific pieces of data on numerous pages within your application. For example, you may need to display the current user in the site header. Passing this data manually in each response across your entire application is cumbersome. Thankfully, there is a better option: shared data.

## Sharing Data

All of Inertia's server-side adapters provide a method to make shared data available for every request. This is typically done outside of your controllers. Shared data is automatically merged with the page props provided in your controller.

In Laravel applications, this is typically handled by the `HandleInertiaRequests` middleware that is automatically installed when installing the [server-side adapter](https://inertiajs.com/docs/v3/installation/server-side-setup.md#middleware).

```php theme={null}
class HandleInertiaRequests extends Middleware
{
    public function share(Request $request)
    {
        return array_merge(parent::share($request), [
            // Synchronously...
            'appName' => config('app.name'),

            // Lazily...
            'auth.user' => fn () => $request->user()
                ? $request->user()->only('id', 'name', 'email')
                : null,
        ]);
    }
}
```

Alternatively, you can manually share data using the `Inertia::share` method.

```php theme={null}
use Inertia\Inertia;

// Synchronously...
Inertia::share('appName', config('app.name'));

// Lazily...
Inertia::share('user', fn (Request $request) => $request->user()
    ? $request->user()->only('id', 'name', 'email')
    : null
);
```

Shared data should be used sparingly as all shared data is included with every response.

Page props and shared data are merged together, so be sure to namespace your shared data appropriately to avoid collisions.

## Sharing Once Props

You may share data that is resolved only once and remembered by the client across subsequent navigations using [once props](https://inertiajs.com/docs/v3/data-props/once-props.md).

```php theme={null}
class HandleInertiaRequests extends Middleware
{
    public function share(Request $request)
    {
        return array_merge(parent::share($request), [
            'countries' => Inertia::once(fn () => Country::all()),
        ]);
    }
}
```

Alternatively, you may define a dedicated `shareOnce()` method in the middleware. The middleware will evaluate both `share()` and `shareOnce()`, merging the results.

```php theme={null}
class HandleInertiaRequests extends Middleware
{
    public function shareOnce(Request $request): array
    {
        return array_merge(parent::shareOnce($request), [
            'countries' => fn () => Country::all(),
        ]);
    }
}
```

You may also share once props manually using the `Inertia::shareOnce()` method.

```php theme={null}
Inertia::shareOnce('countries', fn () => Country::all());
```

## Accessing Shared Data

Once you have shared the data server-side, you will be able to access it within any of your pages or components. Here's an example of how to access shared data in a layout component.

```vue Vue icon="vuejs" theme={null}
<script setup>
import { computed } from "vue";
import { usePage } from "@inertiajs/vue3";

const page = usePage();

const user = computed(() => page.props.auth.user);
</script>

<template>
  <main>
    <header>You are logged in as: {{ user.name }}</header>
    <article>
      <slot />
    </article>
  </main>
</template>
```

```jsx React icon="react" theme={null}
import { usePage } from "@inertiajs/react";

export default function Layout({ children }) {
  const { auth } = usePage().props;

  return (
    <main>
      <header>You are logged in as: {auth.user.name}</header>
      <article>{children}</article>
    </main>
  );
}
```

```svelte Svelte icon="s" theme={null}
<script>
    import { page } from '@inertiajs/svelte'
</script>

<main>
    <header>
        You are logged in as: {page.props.auth.user.name}
    </header>
    <article>
        <slot />
    </article>
</main>
```

## TypeScript

You may configure the shared props type globally using [TypeScript's declaration merging](https://inertiajs.com/docs/v3/advanced/typescript.md#shared-page-props).

## Flash Data

For one-time notifications like toast messages or success alerts, you may use [flash data](https://inertiajs.com/docs/v3/data-props/flash-data.md). Unlike shared data, flash data is not persisted in the browser's history state, so it won't reappear when navigating through history.
