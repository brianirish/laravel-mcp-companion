Source: https://inertiajs.com/docs/v3/the-basics/links.md

# Links

To create links to other pages within an Inertia app, you will typically use the Inertia `<Link>` component. This component is a light wrapper around a standard anchor `<a>` link that intercepts click events and prevents full page reloads. This is [how Inertia provides a single-page app experience](https://inertiajs.com/docs/v3/core-concepts/how-it-works.md) once your application has been loaded.

## Creating Links

To create an Inertia link, use the Inertia `<Link>` component. Any attributes you provide to this component will be proxied to the underlying HTML tag.

```vue Vue icon="vuejs" theme={null}
import { Link } from '@inertiajs/vue3'

<Link href="/">Home</Link>
```

```jsx React icon="react" theme={null}
import { Link } from "@inertiajs/react";

<Link href="/">Home</Link>;
```

```svelte Svelte icon="s" theme={null}
import { inertia, Link } from '@inertiajs/svelte'

<a href="/" use:inertia>Home</a>

<Link href="/">Home</Link>
```

By default, Inertia renders links as anchor `<a>` elements. However, you can change the tag using the `as` prop.

```vue Vue icon="vuejs" theme={null}
import { Link } from '@inertiajs/vue3'

<Link href="/logout" method="post" as="button">Logout</Link>

// Renders as...
<button type="button">Logout</button>
```

```jsx React icon="react" theme={null}
import { Link } from '@inertiajs/react'

<Link href="/logout" method="post" as="button">Logout</Link>

// Renders as...
<button type="button">Logout</button>
```

```svelte Svelte icon="s" theme={null}
import { Link } from '@inertiajs/svelte'

<Link href="/logout" method="post" as="button">Logout</Link>

// Renders as...
<button type="button">Logout</button>
```

> [!NOTE]
>
> Creating anchor (`<a>`) links that issue `POST`, `PUT`, `PATCH`, `DELETE`, or `QUERY` requests is discouraged because it causes accessibility issues with "Open Link in New Tab / Window". The component automatically renders a `<button>` element when using these methods.

## Method

You may specify the HTTP request method for an Inertia link request using the `method` prop. Links use `GET` by default, but the `method` prop also accepts `POST`, `PUT`, `PATCH`, `DELETE`, and `QUERY`.

```vue Vue icon="vuejs" theme={null}
import { Link } from '@inertiajs/vue3'

<Link href="/logout" method="post" as="button">Logout</Link>
```

```jsx React icon="react" theme={null}
import { Link } from "@inertiajs/react";

<Link href="/logout" method="post" as="button">
  Logout
</Link>;
```

```svelte Svelte icon="s" theme={null}
import { inertia, Link } from '@inertiajs/svelte'

<button use:inertia={{ href: '/logout', method: 'post' }} type="button">Logout</button>

<Link href="/logout" method="post">Logout</Link>
```

v3.10.0+

Links using the `query` method send their [data](#data) in the request body instead of the query string. See the [QUERY method](https://inertiajs.com/docs/v3/the-basics/manual-visits.md#query-method) documentation for more information.

```vue Vue icon="vuejs" theme={null}
import { Link } from '@inertiajs/vue3'

<Link href="/products" method="query" :data="{ brand: 'Acme' }">Acme products</Link>
```

```jsx React icon="react" theme={null}
import { Link } from "@inertiajs/react";

<Link href="/products" method="query" data={{ brand: "Acme" }}>
  Acme products
</Link>;
```

```svelte Svelte icon="s" theme={null}
import { Link } from '@inertiajs/svelte'

<Link href="/products" method="query" data={{ brand: 'Acme' }}>Acme products</Link>
```

## Wayfinder

When using [Wayfinder](https://github.com/laravel/wayfinder) in conjunction with the `Link` component, you can simply pass the resulting object directly to the `href` prop. The `Link` will infer the HTTP method and URL directly from the Wayfinder object.

```vue Vue icon="vuejs" theme={null}
import { Link } from '@inertiajs/vue3' import { show } from
'App/Http/Controllers/UserController'

<Link :href="show(1)">John Doe</Link>
```

```jsx React icon="react" theme={null}
import { Link } from "@inertiajs/react";
import { show } from "App/Http/Controllers/UserController";

<Link href={show(1)}>John Doe</Link>;
```

```svelte Svelte icon="s" theme={null}
import { inertia, Link } from '@inertiajs/svelte'
import { show } from 'App/Http/Controllers/UserController'

<button use:inertia={{ href: show(1) }} type="button">John Doe</button>

<Link href={show(1)}>John Doe</Link>
```

## Data

When making `POST` or `PUT` requests, you may wish to add additional data to the request. You can accomplish this using the `data` prop. The provided data can be an `object` or `FormData` instance.

```vue Vue icon="vuejs" theme={null}
import { Link } from '@inertiajs/vue3'

<Link href="/endpoint" method="post" :data="{ foo: bar }">Save</Link>
```

```jsx React icon="react" theme={null}
import { Link } from "@inertiajs/react";

<Link href="/endpoint" method="post" data={{ foo: bar }}>
  Save
</Link>;
```

```svelte Svelte icon="s" theme={null}
import { inertia, Link } from '@inertiajs/svelte'

<button use:inertia={{ href: '/endpoint', method: 'post', data: { foo: bar } }} type="button">Save</button>

<Link href="/endpoint" method="post" data={{ foo: bar }}>Save</Link>
```

## Custom Headers

The `headers` prop allows you to add custom headers to an Inertia link. However, the headers Inertia uses internally to communicate its state to the server take priority and therefore cannot be overwritten.

```vue Vue icon="vuejs" theme={null}
import { Link } from '@inertiajs/vue3'

<Link href="/endpoint" :headers="{ foo: bar }">Save</Link>
```

```jsx React icon="react" theme={null}
import { Link } from "@inertiajs/react";

<Link href="/endpoint" headers={{ foo: bar }}>
  Save
</Link>;
```

```svelte Svelte icon="s" theme={null}
import { inertia, Link } from '@inertiajs/svelte'

<button use:inertia={{ href: '/endpoint', headers: { foo: bar } }}>Save</button>

<Link href="/endpoint" headers={{ foo: bar }}>Save</Link>
```

## Browser History

The `replace` prop allows you to specify the browser's history behavior. By default, page visits push (new) state (`window.history.pushState`) into the history; however, it's also possible to replace state (`window.history.replaceState`) by setting the `replace` prop to `true`. This will cause the visit to replace the current history state instead of adding a new history state to the stack.

```vue Vue icon="vuejs" theme={null}
import { Link } from '@inertiajs/vue3'

<Link href="/" replace>Home</Link>
```

```jsx React icon="react" theme={null}
import { Link } from "@inertiajs/react";

<Link replace href="/">
  Home
</Link>;
```

```svelte Svelte icon="s" theme={null}
import { inertia, Link } from '@inertiajs/svelte'

<a href="/" use:inertia={{ replace: true }}>Home</a>

<Link href="/" replace>Home</Link>
```

## State Preservation

You can preserve a page component's local state using the `preserve-state` prop. This will prevent a page component from fully re-rendering. The `preserve-state` prop is especially helpful on pages that contain forms, since you can avoid manually repopulating input fields and can also maintain a focused input.

```vue Vue icon="vuejs" theme={null}
import { Link } from '@inertiajs/vue3'

<input v-model="query" type="text" />

<Link href="/search" :data="{ query }" preserve-state>Search</Link>
```

```jsx React icon="react" theme={null}
import { Link } from '@inertiajs/react'

<input onChange={this.handleChange} value={query} type="text" />

<Link href="/search" data={query} preserveState>Search</Link>
```

```svelte Svelte icon="s" theme={null}
import { inertia, Link } from '@inertiajs/svelte'

<input bind:value={query} type="text" />

<button use:inertia={{ href: '/search', data: { query }, preserveState: true }}>Search</button>

<Link href="/search" data={{ query }} preserveState>Search</Link>
```

## Scroll Preservation

You can use the `preserveScroll` prop to prevent Inertia from automatically resetting the scroll position when making a page visit.

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

For more information on managing scroll position, check out the documentation on [scroll management](https://inertiajs.com/docs/v3/advanced/scroll-management.md).

## Partial Reloads

The `only` prop allows you to specify that only a subset of a page's props (data) should be retrieved from the server on subsequent visits to that page.

```vue Vue icon="vuejs" theme={null}
import { Link } from '@inertiajs/vue3'

<Link href="/users?active=true" :only="['users']">Show active</Link>
```

```jsx React icon="react" theme={null}
import { Link } from "@inertiajs/react";

<Link href="/users?active=true" only={["users"]}>
  Show active
</Link>;
```

```svelte Svelte icon="s" theme={null}
import { inertia, Link } from '@inertiajs/svelte'

<a href="/users?active=true" use:inertia={{ only: ['users'] }}>Show active</a>

<Link href="/users?active=true" only={['users']}>Show active</Link>
```

For more information on this topic, check out the complete documentation on [partial reloads](https://inertiajs.com/docs/v3/data-props/partial-reloads.md).

## View Transitions

You may enable [View transitions](https://inertiajs.com/docs/v3/the-basics/view-transitions.md) for a link by setting the `viewTransition` prop to `true`. This will use the browser's View Transitions API to animate the page transition.

```vue Vue icon="vuejs" theme={null}
import { Link } from '@inertiajs/vue3'

<Link href="/another-page" view-transition>Navigate</Link>
```

```jsx React icon="react" theme={null}
import { Link } from "@inertiajs/react";

<Link href="/another-page" viewTransition>
  Navigate
</Link>;
```

```svelte Svelte icon="s" theme={null}
import { Link } from '@inertiajs/svelte'

<Link href="/another-page" viewTransition>Navigate</Link>
```

## Active States

It's common to set an active state for navigation links based on the current page. This can be accomplished when using Inertia by inspecting the `page` object and doing string comparisons against the `page.url` and `page.component` properties.

```vue Vue icon="vuejs" theme={null}
import { Link } from '@inertiajs/vue3' // URL exact match...
<Link href="/users" :class="{ active: $page.url === '/users' }">Users</Link>

// Component exact match...
<Link
  href="/users"
  :class="{ active: $page.component === 'Users/Index' }"
>Users</Link>

// URL starts with (/users, /users/create, /users/1, etc.)...
<Link
  href="/users"
  :class="{ active: $page.url.startsWith('/users') }"
>Users</Link>

// Component starts with (Users/Index, Users/Create, Users/Show, etc.)...
<Link
  href="/users"
  :class="{ active: $page.component.startsWith('Users') }"
>Users</Link>
```

```jsx React icon="react" theme={null}
import { usePage } from '@inertiajs/react'

const { url, component } = usePage()

// URL exact match...
<Link href="/users" className={url === '/users' ? 'active' : ''}>Users</Link>

// Component exact match...
<Link href="/users" className={component === 'Users/Index' ? 'active' : ''}>Users</Link>

// URL starts with (/users, /users/create, /users/1, etc.)...
<Link href="/users" className={url.startsWith('/users') ? 'active' : ''}>Users</Link>

// Component starts with (Users/Index, Users/Create, Users/Show, etc.)...
<Link href="/users" className={component.startsWith('Users') ? 'active' : ''}>Users</Link>
```

```svelte Svelte icon="s" theme={null}
import { inertia, Link, page } from '@inertiajs/svelte'

// URL exact match...
<a href="/users" use:inertia class:active={page.url === '/users'}>Users</a>

// Component exact match...
<a href="/users" use:inertia class:active={page.component === 'Users/Index'}>Users</a>

// URL starts with (/users, /users/create, /users/1, etc.)...
<Link href="/users" class={page.url.startsWith('/users') ? 'active' : ''}>Users</Link>

// Component starts with (Users/Index, Users/Create, Users/Show, etc.)...
<Link href="/users" class={page.component.startsWith('Users') ? 'active' : ''}>Users</Link>
```

You can perform exact match comparisons (`===`), `startsWith()` comparisons (useful for matching a subset of pages), or even more complex comparisons using regular expressions.

Using this approach, you're not limited to just setting class names. You can use this technique to conditionally render any markup on active state, such as different link text or even an SVG icon that indicates the link is active.

## Data Loading Attribute

While a link is making an active request, a `data-loading` attribute is added to the link element. This allows you to style the link while it's in a loading state. The attribute is removed once the request is complete.
