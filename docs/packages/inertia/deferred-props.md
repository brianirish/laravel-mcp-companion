Source: https://inertiajs.com/docs/v3/data-props/deferred-props.md

# Deferred Props

Inertia's deferred props feature allows you to defer the loading of certain page data until after the initial page render. This can be useful for improving the perceived performance of your app by allowing the initial page render to happen as quickly as possible.

## Server-Side

To defer a prop, you can use the `Inertia::defer()` method when returning your response. This method receives a callback that returns the prop data. The callback will be executed in a separate request after the initial page render.

```php theme={null}
Route::get('/users', function () {
    return Inertia::render('Users/Index', [
        'users' => User::all(),
        'roles' => Role::all(),
        'permissions' => Inertia::defer(fn () => Permission::all()),
    ]);
});
```

### Grouping Requests

By default, all deferred props are fetched in a single request after the initial page is rendered. However, you may fetch props in parallel by grouping them.

```php theme={null}
Route::get('/users', function () {
    return Inertia::render('Users/Index', [
        'users' => User::all(),
        'roles' => Role::all(),
        'permissions' => Inertia::defer(fn () => Permission::all()),
        'teams' => Inertia::defer(fn () => Team::all(), 'attributes'),
        'projects' => Inertia::defer(fn () => Project::all(), 'attributes'),
        'tasks' => Inertia::defer(fn () => Task::all(), 'attributes'),
    ]);
});
```

In the example above, the `teams`, `projects`, and `tasks` props will be fetched in one request, while the `permissions` prop will be fetched in a separate request in parallel. Group names are arbitrary strings and can be anything you choose.

## Client-Side

On the client side, Inertia provides the `Deferred` component to help you manage deferred props. This component will automatically wait for the specified deferred props to be available before rendering its children.

```vue Vue icon="vuejs" theme={null}
<script setup>
import { Deferred } from "@inertiajs/vue3";
</script>

<template>
  <Deferred data="permissions">
    <template #fallback>
      <div>Loading...</div>
    </template>

    <div v-for="permission in permissions">
      <!-- ... -->
    </div>
  </Deferred>
</template>
```

```jsx React icon="react" theme={null}
import { Deferred } from "@inertiajs/react";

export default () => (
  <Deferred data="permissions" fallback={<div>Loading...</div>}>
    <PermissionsChildComponent />
  </Deferred>
);
```

```svelte Svelte icon="s" theme={null}
<script>
    import { Deferred } from '@inertiajs/svelte'

    let { permissions } = $props()
</script>

<Deferred data="permissions">
    {#snippet fallback()}
        <div>Loading...</div>
    {/snippet}

    {#each permissions as permission}
        <!-- ... -->
    {/each}
</Deferred>
```

## Multiple Deferred Props

If you need to wait for multiple deferred props to become available, you can specify an array to the `data` prop.

```vue Vue icon="vuejs" theme={null}
<script setup>
import { Deferred } from "@inertiajs/vue3";
</script>

<template>
  <Deferred :data="['teams', 'users']">
    <template #fallback>
      <div>Loading...</div>
    </template>

    <!-- Props are now loaded -->
  </Deferred>
</template>
```

```jsx React icon="react" theme={null}
import { Deferred } from "@inertiajs/react";

export default () => (
  <Deferred data={["teams", "users"]} fallback={<div>Loading...</div>}>
    <ChildComponent />
  </Deferred>
);
```

```svelte Svelte icon="s" theme={null}
<script>
    import { Deferred } from '@inertiajs/svelte'

    let { teams, users } = $props()
</script>

<Deferred data={['teams', 'users']}>
    {#snippet fallback()}
        <div>Loading...</div>
    {/snippet}

    <!-- Props are now loaded -->
</Deferred>
```

## Reloading Indicator

When deferred props are being reloaded via a partial reload, the `Deferred` component exposes a `reloading` boolean through its slot. This allows you to show a loading indicator while still displaying the previously loaded data.

```vue Vue icon="vuejs" theme={null}
<script setup>
import { Deferred } from "@inertiajs/vue3";
</script>

<template>
  <Deferred data="permissions" #default="{ reloading }">
    <template #fallback>
      <div>Loading...</div>
    </template>

    <div :class="{ 'opacity-50': reloading }">
      <div v-for="permission in permissions">
        <!-- ... -->
      </div>
    </div>
  </Deferred>
</template>
```

```jsx React icon="react" theme={null}
import { Deferred } from "@inertiajs/react";

export default () => (
  <Deferred data="permissions" fallback={<div>Loading...</div>}>
    {({ reloading }) => (
      <div className={reloading ? "opacity-50" : ""}>
        <PermissionsChildComponent />
      </div>
    )}
  </Deferred>
);
```

```svelte Svelte icon="s" theme={null}
<script>
    import { Deferred } from '@inertiajs/svelte'

    let { permissions } = $props()
</script>

<Deferred data="permissions">
    {#snippet fallback()}
        <div>Loading...</div>
    {/snippet}

    {#snippet children({ reloading })}
        <div class:opacity-50={reloading}>
            {#each permissions as permission}
                <!-- ... -->
            {/each}
        </div>
    {/snippet}
</Deferred>
```

The `reloading` prop is `false` on the initial load and becomes `true` whenever a partial reload is in progress for the deferred keys. It returns to `false` once the reload completes.

## Error Handling

By default, exceptions thrown while resolving a deferred prop result in an error response. You may instruct Inertia to rescue these exceptions by passing `rescue: true` to `Inertia::defer()`.

```php theme={null}
Route::get('/users', function () {
    return Inertia::render('Users/Index', [
        'permissions' => Inertia::defer(fn () => Permission::all(), rescue: true),
    ]);
});
```

When a deferred prop is rescued, it is omitted from the response and the exception is reported via Laravel's exception handler.

On the client side, you may provide a `rescue` slot to the `Deferred` component to render a fallback UI when a prop fails to load.

```vue Vue icon="vuejs" theme={null}
<script setup>
import { Deferred, router } from "@inertiajs/vue3";
</script>

<template>
  <Deferred data="permissions">
    <template #fallback>
      <div>Loading...</div>
    </template>

    <template #rescue="{ reloading }">
      <div>
        <p>Failed to load permissions.</p>
        <button :disabled="reloading" @click="router.reload({ only: ['permissions'] })">Retry</button>
      </div>
    </template>

    <div v-for="permission in permissions">
      <!-- ... -->
    </div>
  </Deferred>
</template>
```

```jsx React icon="react" theme={null}
import { Deferred, router } from "@inertiajs/react";

export default () => (
  <Deferred
    data="permissions"
    fallback={<div>Loading...</div>}
    rescue={({ reloading }) => (
      <div>
        <p>Failed to load permissions.</p>
        <button disabled={reloading} onClick={() => router.reload({ only: ["permissions"] })}>Retry</button>
      </div>
    )}
  >
    <PermissionsChildComponent />
  </Deferred>
);
```

```svelte Svelte icon="s" theme={null}
<script>
    import { Deferred, router } from '@inertiajs/svelte'

    let { permissions } = $props()
</script>

<Deferred data="permissions">
    {#snippet fallback()}
        <div>Loading...</div>
    {/snippet}

    {#snippet rescue({ reloading })}
        <div>
            <p>Failed to load permissions.</p>
            <button disabled={reloading} onclick={() => router.reload({ only: ['permissions'] })}>Retry</button>
        </div>
    {/snippet}

    {#each permissions as permission}
        <!-- ... -->
    {/each}
</Deferred>
```

The rescue state is preserved until you explicitly reload the rescued prop. The `rescue` slot receives a `reloading` boolean, allowing you to disable the retry button or show a loading indicator while the reload is in progress.

## Combining with Once Props

You may chain the `once()` modifier onto a deferred prop to ensure the data is resolved only once and remembered by the client across subsequent navigations.

```php theme={null}
return Inertia::render('Dashboard', [
    'stats' => Inertia::defer(fn () => Stats::generate())->once(),
]);
```

For more information on once props, see the [once props](https://inertiajs.com/docs/v3/data-props/once-props.md) documentation.
