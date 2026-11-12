Source: https://inertiajs.com/docs/v3/data-props/flash-data.md

# Flash Data

Flash data lets you send one-time data to your front end that won't reappear when users navigate through browser history. Unlike regular props, flash data isn't persisted in history state, making it ideal for success messages, newly created IDs, or other temporary values.

## Flashing Data

You may flash data using the `Inertia::flash()` method, passing a key and value or an array of key-value pairs.

```php theme={null}
public function store(Request $request)
{
    $user = User::create($request->validated());

    Inertia::flash('message', 'User created successfully!');

    // Or flash multiple values at once...
    Inertia::flash([
        'message' => 'User created!',
        'newUserId' => $user->id,
    ]);

    return back();
}
```

Chaining with `back()` is also supported.

```php theme={null}
return Inertia::flash('newUserId', $user->id)->back();
```

You may also chain `flash()` onto `render()`, or vice versa.

```php theme={null}
return Inertia::render('Projects/Index', [
    'projects' => $projects,
])->flash('highlight', $project->id);

// Or...

return Inertia::flash('highlight', $project->id)
    ->render('Projects/Index', ['projects' => $projects]);
```

Flash data is scoped to the current request. The middleware automatically persists it to the session when redirecting. After the flash data is sent to the client, it is cleared and will not appear in subsequent requests.

## Accessing Flash Data

Flash data is available on `page.flash`. You may also listen for the global `flash` event or use the `onFlash` callback.

```vue Vue icon="vuejs" theme={null}
<script setup>
import { usePage } from "@inertiajs/vue3";

const page = usePage();
</script>

<template>
  <div v-if="page.flash.toast" class="toast">
    {{ page.flash.toast.message }}
  </div>
</template>
```

```jsx React icon="react" theme={null}
import { usePage } from "@inertiajs/react";

export default function Layout({ children }) {
  const { flash } = usePage();

  return (
    <>
      {flash.toast && <div className="toast">{flash.toast.message}</div>}
      {children}
    </>
  );
}
```

```svelte Svelte icon="s" theme={null}
<script>
    import { page } from '@inertiajs/svelte'
</script>

{#if page.flash.toast}
    <div class="toast">{page.flash.toast.message}</div>
{/if}
```

## The onFlash Callback

You may use the `onFlash` callback to handle flash data when making requests.

```js Vue icon="vuejs" theme={null}
import { router } from "@inertiajs/vue3";

router.post("/users", data, {
  onFlash: ({ newUserId }) => {
    form.userId = newUserId;
  },
});
```

```js React icon="react" theme={null}
import { router } from "@inertiajs/react";

router.post("/users", data, {
  onFlash: ({ newUserId }) => {
    form.userId = newUserId;
  },
});
```

```js Svelte icon="s" theme={null}
import { router } from "@inertiajs/svelte";

router.post("/users", data, {
  onFlash: ({ newUserId }) => {
    form.userId = newUserId;
  },
});
```

## Global Flash Event

You may use the global `flash` event to handle flash data in a central location, such as a layout component. For more information on events, see the [events documentation](https://inertiajs.com/docs/v3/advanced/events.md).

```js Vue icon="vuejs" theme={null}
import { router } from "@inertiajs/vue3";

router.on("flash", (event) => {
  if (event.detail.flash.toast) {
    showToast(event.detail.flash.toast);
  }
});
```

```js React icon="react" theme={null}
import { router } from "@inertiajs/react";

router.on("flash", (event) => {
  if (event.detail.flash.toast) {
    showToast(event.detail.flash.toast);
  }
});
```

```js Svelte icon="s" theme={null}
import { router } from "@inertiajs/svelte";

router.on("flash", (event) => {
  if (event.detail.flash.toast) {
    showToast(event.detail.flash.toast);
  }
});
```

> [!WARNING]
>
> Event listeners registered inside components should be cleaned up when the
> component unmounts to prevent them from accumulating and firing multiple
> times. This is especially important in non-persistent layouts. See [removing
> event listeners](https://inertiajs.com/docs/v3/advanced/events.md#removing-listeners) for more information.

Native browser events are also supported.

```js Vue icon="vuejs" theme={null}
document.addEventListener("inertia:flash", (event) => {
  console.log(event.detail.flash);
});
```

```js React icon="react" theme={null}
document.addEventListener("inertia:flash", (event) => {
  console.log(event.detail.flash);
});
```

```js Svelte icon="s" theme={null}
document.addEventListener("inertia:flash", (event) => {
  console.log(event.detail.flash);
});
```

The `flash` event is not cancelable and fires on every response that carries flash data.

## Client-Side Flash

You may set flash data on the client without a server request using the `router.flash()` method. Values are merged with existing flash data.

```js Vue icon="vuejs" theme={null}
import { router } from "@inertiajs/vue3";

router.flash("foo", "bar");
router.flash({ foo: "bar" });
```

```js React icon="react" theme={null}
import { router } from "@inertiajs/react";

router.flash("foo", "bar");
router.flash({ foo: "bar" });
```

```js Svelte icon="s" theme={null}
import { router } from "@inertiajs/svelte";

router.flash("foo", "bar");
router.flash({ foo: "bar" });
```

A callback may also be passed to access the current flash data or replace it entirely.

```js Vue icon="vuejs" theme={null}
import { router } from "@inertiajs/vue3";

router.flash((current) => ({ ...current, bar: "baz" }));
router.flash(() => ({}));
```

```js React icon="react" theme={null}
import { router } from "@inertiajs/react";

router.flash((current) => ({ ...current, bar: "baz" }));
router.flash(() => ({}));
```

```js Svelte icon="s" theme={null}
import { router } from "@inertiajs/svelte";

router.flash((current) => ({ ...current, bar: "baz" }));
router.flash(() => ({}));
```

## TypeScript

You may configure the flash data type globally using [TypeScript's declaration merging](https://inertiajs.com/docs/v3/advanced/typescript.md#flash-data).

## Testing

For information on testing flash data, see the [testing documentation](https://inertiajs.com/docs/v3/advanced/testing.md#testing-flash-data).
