Source: https://inertiajs.com/docs/v3/the-basics/pages.md

# Pages

When building applications using Inertia, each page in your application typically has its own controller or route and a corresponding JavaScript component. This allows you to retrieve just the data necessary for that page - no API required.

In addition, all of the data needed for the page can be retrieved before the page is ever rendered by the browser, eliminating the need for displaying "loading" states when users visit your application.

## Creating Pages

Inertia pages are simply JavaScript components. If you have ever written a Vue, React, or Svelte component, you will feel right at home. As you can see in the example below, pages receive data from your application's controllers as props.

```vue Vue icon="vuejs" theme={null}
<script setup>
import Layout from "./Layout";
import { Head } from "@inertiajs/vue3";

defineProps({ user: Object });
</script>

<template>
  <Layout>
    <Head title="Welcome" />
    <h1>Welcome</h1>
    <p>Hello {{ user.name }}, welcome to your first Inertia app!</p>
  </Layout>
</template>
```

```jsx React icon="react" theme={null}
import Layout from "./Layout";
import { Head } from "@inertiajs/react";

export default function Welcome({ user }) {
  return (
    <Layout>
      <Head title="Welcome" />
      <h1>Welcome</h1>
      <p>Hello {user.name}, welcome to your first Inertia app!</p>
    </Layout>
  );
}
```

```svelte Svelte icon="s" theme={null}
<script>
    import Layout from './Layout.svelte'

    let { user } = $props()
</script>

<svelte:head>
    <title>Welcome</title>
</svelte:head>

<Layout>
    <h1>Welcome</h1>
    <p>Hello {user.name}, welcome to your first Inertia app!</p>
</Layout>
```

Given the page above, you can render the page by returning an [Inertia
response](https://inertiajs.com/docs/v3/the-basics/responses.md) from a controller or route. In this
example, let's assume this page is stored at&#x20;
`resources/js/Pages/User/Show.vue`
`resources/js/Pages/User/Show.jsx`
`resources/js/Pages/User/Show.svelte`within a
Laravel application.

```php theme={null}
use Inertia\Inertia;

class UserController extends Controller
{
    public function show(User $user)
    {
        return Inertia::render('User/Show', [
            'user' => $user
        ]);
    }
}
```

If you attempt to render a page that does not exist, the response will typically be a blank screen. To prevent this, you may set the `inertia.ensure_pages_exist` configuration option to `true`. The Laravel adapter will then throw an `Inertia\ComponentNotFoundException` when a page cannot be found.

## Transforming Component Names

Sometimes you may wish to transform component names. This may be done on the client side using the [`pages.transform`](https://inertiajs.com/docs/v3/installation/client-side-setup#pages-shorthand) option, or on the server using the `Inertia::transformComponentUsing()` method. The transformed name is sent to the browser and used for `ensure_pages_exist` checks.

```php theme={null}
use Inertia\Inertia;

Inertia::transformComponentUsing(function (string $name): string {
    return "{$name}/Page";
});
```

## Layouts

Most applications share common UI elements across pages. Inertia provides persistent layouts that survive page navigations, along with layout props for passing dynamic data between pages and their layouts. Visit the [layouts documentation](https://inertiajs.com/docs/v3/the-basics/layouts.md) to learn more.
