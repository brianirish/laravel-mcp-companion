Source: https://inertiajs.com/docs/v3/advanced/scroll-management.md

# Scroll Management

## Scroll Resetting

When navigating between pages, Inertia mimics default browser behavior by automatically resetting the scroll position of the document body (as well as any [scroll regions](#scroll-regions) you've defined) back to the top.

In addition, Inertia keeps track of the scroll position of each page and automatically restores that scroll position as you navigate forward and back in history.

## Scroll Preservation

Sometimes it's desirable to prevent the default scroll resetting when making visits. You can disable this behavior by setting the `preserveScroll` option to `true`.

```js Vue icon="vuejs" theme={null}
import { router } from "@inertiajs/vue3";

router.visit(url, { preserveScroll: true });
```

```js React icon="react" theme={null}
import { router } from "@inertiajs/react";

router.visit(url, { preserveScroll: true });
```

```js Svelte icon="s" theme={null}
import { router } from "@inertiajs/svelte";

router.visit(url, { preserveScroll: true });
```

If you'd like to only preserve the scroll position if the response includes validation errors, set the `preserveScroll` option to "errors".

```js Vue icon="vuejs" theme={null}
import { router } from "@inertiajs/vue3";

router.visit(url, { preserveScroll: "errors" });
```

```js React icon="react" theme={null}
import { router } from "@inertiajs/react";

router.visit(url, { preserveScroll: "errors" });
```

```js Svelte icon="s" theme={null}
import { router } from "@inertiajs/svelte";

router.visit(url, { preserveScroll: "errors" });
```

You can also lazily evaluate the `preserveScroll` option based on the response by providing a callback.

```js Vue icon="vuejs" theme={null}
import { router } from "@inertiajs/vue3";

router.post("/users", data, {
  preserveScroll: (page) => page.props.someProp === "value",
});
```

```js React icon="react" theme={null}
import { router } from "@inertiajs/react";

router.post("/users", data, {
  preserveScroll: (page) => page.props.someProp === "value",
});
```

```js Svelte icon="s" theme={null}
import { router } from "@inertiajs/svelte";

router.post("/users", data, {
  preserveScroll: (page) => page.props.someProp === "value",
});
```

When using an [Inertia link](https://inertiajs.com/docs/v3/the-basics/links.md), you can preserve the scroll position using the `preserveScroll` prop.

```vue Vue icon="vuejs" theme={null}
import { Link } from '@inertiajs/vue3'

<Link href="/" preserve-scroll>Home</Link>
```

```jsx React icon="react" theme={null}
import { Link } from "@inertiajs/react";

<Link preserveScroll href="/">
  Home
</Link>;
```

```svelte Svelte icon="s" theme={null}
import { inertia, Link } from '@inertiajs/svelte'

<a href="/" use:inertia={{ preserveScroll: true }}>Home</a>

<Link href="/" preserveScroll>Home</Link>
```

## Scroll Regions

If your app doesn't use document body scrolling, but instead has scrollable elements (using the `overflow` CSS property), scroll resetting will not work.

In these situations, you must tell Inertia which scrollable elements to manage by adding the `scroll-region` attribute to the element.

```html theme={null}
<div class="overflow-y-auto" scroll-region="">
  <!-- Your page content -->
</div>
```

## Text Fragments

[Text fragments](https://developer.mozilla.org/en-US/docs/Web/URI/Reference/Fragment/Text_fragments) allow you to link directly to specific text on a page using a special URL syntax like `#:~:text=term`. However, the browser removes the fragment directive before any JavaScript runs, so text fragments only work if the targeted text is present in the initial HTML response.

To use text fragments with your Inertia pages, enable [server-side rendering](https://inertiajs.com/docs/v3/advanced/server-side-rendering.md).
