Source: https://inertiajs.com/docs/v3/data-props/infinite-scroll.md

# Infinite Scroll

Inertia's infinite scroll feature loads additional pages of content as users scroll, replacing traditional pagination controls. This is great for applications like chat interfaces, social feeds, photo grids, and product listings.

## Server-Side

To configure your paginated data for infinite scrolling, you should use the `Inertia::scroll()` method when returning your response. This method automatically configures the proper merge behavior and normalizes pagination metadata for the front-end component.

```php theme={null}
Route::get('/users', function () {
    return Inertia::render('Users/Index', [
        'users' => Inertia::scroll(fn () => User::paginate())
    ]);
});
```

The `Inertia::scroll()` method works with Laravel's `paginate()`, `simplePaginate()`, and `cursorPaginate()` methods, as well as pagination data wrapped in [Eloquent API resources](https://laravel.com/docs/eloquent-resources). For more details, check out the [Inertia::scroll() method](#inertia-scroll-method) documentation.

## Client-Side

On the client side, Inertia provides the `<InfiniteScroll>` component to automatically load additional pages of content. The component accepts a `data` prop that specifies the key of the prop containing your paginated data. The `<InfiniteScroll>` component should wrap the content that depends on the paginated data.

```vue Vue icon="vuejs" theme={null}
<script setup>
import { InfiniteScroll } from "@inertiajs/vue3";

defineProps(["users"]);
</script>

<template>
  <InfiniteScroll data="users">
    <div v-for="user in users.data" :key="user.id">
      {{ user.name }}
    </div>
  </InfiniteScroll>
</template>
```

```jsx React icon="react" theme={null}
import { InfiniteScroll } from "@inertiajs/react";

export default function Users({ users }) {
  return (
    <InfiniteScroll data="users">
      {users.data.map((user) => (
        <div key={user.id}>{user.name}</div>
      ))}
    </InfiniteScroll>
  );
}
```

```svelte Svelte icon="s" theme={null}
<script>
    import { InfiniteScroll } from '@inertiajs/svelte'
    let { users } = $props()
</script>

<InfiniteScroll data="users">
    {#each users.data as user (user.id)}
        <div>{user.name}</div>
    {/each}
</InfiniteScroll>
```

The component uses [intersection observers](https://developer.mozilla.org/en-US/docs/Web/API/Intersection_Observer_API) to detect when users scroll near the end of the content and automatically triggers requests to load the next page. New data is merged with existing content rather than replacing it.

## Loading Buffer

You can control how early content begins loading by setting a buffer distance. The buffer specifies how many pixels before the end of the content loading should begin.

```vue Vue icon="vuejs" theme={null}
<InfiniteScroll data="users" :buffer="500">
    <!-- ... -->
</InfiniteScroll>
```

```jsx React icon="react" theme={null}
<InfiniteScroll data="users" buffer={500}>
  {/* ... */}
</InfiniteScroll>
```

```svelte Svelte icon="s" theme={null}
<InfiniteScroll data="users" buffer={500}>
    <!-- ... -->
</InfiniteScroll>
```

In the example above, content will start loading 500 pixels before reaching the end of the current content. A larger buffer loads content earlier but potentially loads content that users may never see.

## URL Synchronization

The infinite scroll component updates the browser URL's query string (`?page=...`) as users scroll through content. The URL reflects which page has the most visible items on screen, updating in both directions as users scroll up or down. This allows users to bookmark or share links to specific pages. You can disable this behavior to maintain the original page URL.

```vue Vue icon="vuejs" theme={null}
<InfiniteScroll data="users" preserve-url>
    <!-- ... -->
</InfiniteScroll>
```

```jsx React icon="react" theme={null}
<InfiniteScroll data="users" preserveUrl>
  {/* ... */}
</InfiniteScroll>
```

```svelte Svelte icon="s" theme={null}
<InfiniteScroll data="users" preserve-url>
    <!-- ... -->
</InfiniteScroll>
```

This is useful when infinite scroll is used for secondary content that shouldn't affect the main page URL, such as comments on a blog post or related products on a product page.

## Resetting

When filters or other parameters change, you may need to reset the infinite scroll data to start from the beginning. Without resetting, new results will merge with existing content instead of replacing it.

You can reset data using the `reset` visit option.

```vue Vue icon="vuejs" theme={null}
<script setup>
import { router } from "@inertiajs/vue3";

const show = (role) => {
  router.visit(route("users"), {
    data: { filter: { role } },
    only: ["users"],
    reset: ["users"],
  });
};
</script>

<template>
  <button @click="show('admin')">Show admins</button>
  <button @click="show('customer')">Show customers</button>

  <InfiniteScroll data="users">
    <div v-for="user in users.data" :key="user.id">
      {{ user.name }}
    </div>
  </InfiniteScroll>
</template>
```

```jsx React icon="react" theme={null}
import { InfiniteScroll, router } from '@inertiajs/react'

export default function Users({ users }) {
    const show = (role) => {
        router.visit(route('users'), {
            data: { filter: { role } },
            only: ['users'],
            reset: ['users'],
        })
    }

    return (

            <button onClick={() => show('admin')}>Show admins</button>
            <button onClick={() => show('customer')}>Show customers</button>

            <InfiniteScroll data="users">
                {users.data.map(user => (
                    <div key={user.id}>
                        {user.name}
                    </div>
                ))}
            </InfiniteScroll>

    )
}
```

```svelte Svelte icon="s" theme={null}
<script>
    import { InfiniteScroll, router } from '@inertiajs/svelte'
    let { users } = $props()

    const show = (role) => {
        router.visit(route('users'), {
            data: { filter: { role } },
            only: ['users'],
            reset: ['users'],
        })
    }
</script>

<button onclick={() => show('admin')}>Show admins</button>
<button onclick={() => show('customer')}>Show customers</button>

<InfiniteScroll data="users">
    {#each users.data as user (user.id)}
        <div>{user.name}</div>
    {/each}
</InfiniteScroll>
```

For more information about the reset option, see the [Resetting props](https://inertiajs.com/docs/v3/data-props/merging-props.md#resetting-props) documentation.

## Loading Direction

The infinite scroll component loads content in both directions when you scroll near the start or end. You can control this behavior using the `only-next` and `only-previous` props.

```vue Vue icon="vuejs" theme={null}
<!-- Only load the next page -->
<InfiniteScroll data="users" only-next>
    <!-- ... -->
</InfiniteScroll>

<!-- Only load the previous page -->
<InfiniteScroll data="messages" only-previous>
    <!-- ... -->
</InfiniteScroll>

<!-- Load in both directions (default) -->
<InfiniteScroll data="posts">
    <!-- ... -->
</InfiniteScroll>
```

```jsx React icon="react" theme={null}
{
  /* Only load the next page */
}
<InfiniteScroll data="users" onlyNext>
  {/* ... */}
</InfiniteScroll>;

{
  /* Only load the previous page */
}
<InfiniteScroll data="messages" onlyPrevious>
  {/* ... */}
</InfiniteScroll>;

{
  /* Load in both directions (default) */
}
<InfiniteScroll data="posts">{/* ... */}</InfiniteScroll>;
```

```svelte Svelte icon="s" theme={null}
<!-- Only load the next page -->
<InfiniteScroll data="users" only-next>
    <!-- ... -->
</InfiniteScroll>

<!-- Only load the previous page -->
<InfiniteScroll data="messages" only-previous>
    <!-- ... -->
</InfiniteScroll>

<!-- Load in both directions (default) -->
<InfiniteScroll data="posts">
    <!-- ... -->
</InfiniteScroll>
```

The default option is particularly useful when users start on a middle page and need to scroll in both directions to access all content.

## Reverse Mode

For chat applications, timelines, or interfaces where content is sorted descendingly (newest items at the bottom), you can enable reverse mode. This configures the component to load older content when scrolling upward.

```vue Vue icon="vuejs" theme={null}
<InfiniteScroll data="messages" reverse>
    <!-- ... -->
</InfiniteScroll>
```

```jsx React icon="react" theme={null}
<InfiniteScroll data="messages" reverse>
  {/* ... */}
</InfiniteScroll>
```

```svelte Svelte icon="s" theme={null}
<InfiniteScroll data="messages" reverse>
    <!-- ... -->
</InfiniteScroll>
```

In reverse mode, the component flips the loading directions so that scrolling up loads the next page (older content) and scrolling down loads the previous page (newer content). The component handles the loading positioning, but you are responsible for reversing your content to display in the correct order.

Reverse mode also enables automatic scrolling to the bottom on initial load, which you can disable with `:auto-scroll="false"`.

```vue Vue icon="vuejs" theme={null}
<InfiniteScroll data="messages" reverse :auto-scroll="false">
    <!-- ... -->
</InfiniteScroll>
```

```jsx React icon="react" theme={null}
<InfiniteScroll data="messages" reverse autoScroll={false}>
  {/* ... */}
</InfiniteScroll>
```

```svelte Svelte icon="s" theme={null}
<InfiniteScroll data="messages" reverse auto-scroll={false}>
    <!-- ... -->
</InfiniteScroll>
```

## Manual Mode

Manual mode disables automatic loading when scrolling and allows you to control when content loads through the `next` and `previous` slots. For more details about available slot properties and customization options, see the [Slots](#slots) documentation.

```vue Vue icon="vuejs" theme={null}
<template>
  <InfiniteScroll data="users" manual>
    <template #previous="{ loading, fetch, hasMore }">
      <button v-if="hasMore" @click="fetch" :disabled="loading">
        {{ loading ? "Loading..." : "Load previous" }}
      </button>
    </template>

    <!-- Your content -->

    <template #next="{ loading, fetch, hasMore }">
      <button v-if="hasMore" @click="fetch" :disabled="loading">
        {{ loading ? "Loading..." : "Load more" }}
      </button>
    </template>
  </InfiniteScroll>
</template>
```

```jsx React icon="react" theme={null}
import { InfiniteScroll } from "@inertiajs/react";

export default ({ users }) => (
  <InfiniteScroll
    data="users"
    manual
    previous={({ loading, fetch, hasMore }) =>
      hasMore && (
        <button onClick={fetch} disabled={loading}>
          {loading ? "Loading..." : "Load previous"}
        </button>
      )
    }
    next={({ loading, fetch, hasMore }) =>
      hasMore && (
        <button onClick={fetch} disabled={loading}>
          {loading ? "Loading..." : "Load more"}
        </button>
      )
    }
  >
    {users.data.map((user) => (
      <div key={user.id}>{user.name}</div>
    ))}
  </InfiniteScroll>
);
```

```svelte Svelte icon="s" theme={null}
<script>
    import { InfiniteScroll } from '@inertiajs/svelte'
    let { users } = $props()
</script>

<InfiniteScroll data="users" manual>
    {#snippet previous({ hasMore, fetch, loading })}
        {#if hasMore}
            <button onclick={fetch} disabled={loading}>
                {loading ? 'Loading...' : 'Load previous'}
            </button>
        {/if}
    {/snippet}

    {#each users.data as user (user.id)}
        <div>{user.name}</div>
    {/each}

    {#snippet next({ hasMore, fetch, loading })}
        {#if hasMore}
            <button onclick={fetch} disabled={loading}>
                {loading ? 'Loading...' : 'Load more'}
            </button>
        {/if}
    {/snippet}
</InfiniteScroll>
```

You can also configure the component to automatically switch to manual mode after a certain number of pages using the `manualAfter` prop.

```vue Vue icon="vuejs" theme={null}
<InfiniteScroll data="users" :manual-after="3">
    <!-- ... -->
</InfiniteScroll>
```

```jsx React icon="react" theme={null}
<InfiniteScroll data="users" manualAfter={3}>
  {/* ... */}
</InfiniteScroll>
```

```svelte Svelte icon="s" theme={null}
<InfiniteScroll data="users" manual-after={3}>
    <!-- ... -->
</InfiniteScroll>
```

## Slots

The infinite scroll component provides several slots to customize the loading experience. These slots allow you to display custom loading indicators and create manual load controls. Each slot receives properties that provide loading state information and functions to trigger content loading.

### Default Slot

The main content area where you render your data items. This slot receives loading state information.

```vue Vue icon="vuejs" theme={null}
<InfiniteScroll
  data="users"
  #default="{ loading, loadingPrevious, loadingNext }"
>
    <!-- Your content with access to loading states -->
</InfiniteScroll>
```

```jsx React icon="react" theme={null}
<InfiniteScroll data="users">
  {({ loading, loadingPrevious, loadingNext }) => (
    <div>{/* Your content with access to loading states */}</div>
  )}
</InfiniteScroll>
```

```svelte Svelte icon="s" theme={null}
<InfiniteScroll data="users">
    {#snippet children({ loading, loadingPrevious, loadingNext })}
        <!-- Your content with access to loading states -->
    {/snippet}
</InfiniteScroll>
```

### Loading Slot

The loading slot is used as a fallback when loading content and no custom `before` or `after` slots are provided. This creates a default loading indicator.

```vue Vue icon="vuejs" theme={null}
<template>
  <InfiniteScroll data="users">
    <!-- Your content -->

    <template #loading> Loading more users... </template>
  </InfiniteScroll>
</template>
```

```jsx React icon="react" theme={null}
<InfiniteScroll data="users" loading={() => "Loading more users..."}>
  {/* Your content */}
</InfiniteScroll>
```

```svelte Svelte icon="s" theme={null}
<InfiniteScroll data="users">
    <!-- Your content -->

    {#snippet loading()}
        Loading more users...
    {/snippet}
</InfiniteScroll>
```

### Previous and Next Slots

The `previous` and `next` slots are rendered above and below the main content, typically used for manual load controls. These slots receive several properties including loading states, fetch functions, and mode indicators.

```vue theme={null}
<template>
  <InfiniteScroll data="users" :manual-after="3">
    <template #previous="{ loading, fetch, hasMore, manualMode }">
      <button v-if="manualMode && hasMore" @click="fetch" :disabled="loading">
        {{ loading ? "Loading..." : "Load previous" }}
      </button>
    </template>

    <!-- Your content -->

    <template #next="{ loading, fetch, hasMore, manualMode }">
      <button v-if="manualMode && hasMore" @click="fetch" :disabled="loading">
        {{ loading ? "Loading..." : "Load more" }}
      </button>
    </template>
  </InfiniteScroll>
</template>
```

The `loading`, `previous`, and `next` slots receive the following properties:

| Property | Description |
| :- | :- |
| `loading` | Whether the slot is currently loading content |
| `loadingPrevious` | Whether previous content is loading |
| `loadingNext` | Whether next content is loading |
| `fetch` | Function to trigger loading for the slot |
| `hasMore` | Whether more content is available for the slot |
| `hasPrevious` | Whether more previous content is available |
| `hasNext` | Whether more next content is available |
| `manualMode` | Whether manual mode is active |
| `autoMode` | Whether automatic loading is active |

## Custom Element

The `InfiniteScroll` component renders as a `<div>` element. You may customize this to use any HTML element using the `as` prop.

```vue Vue icon="vuejs" theme={null}
<template>
  <InfiniteScroll data="products" as="ul">
    <li v-for="product in products.data" :key="product.id">
      {{ product.name }}
    </li>
  </InfiniteScroll>
</template>
```

```jsx React icon="react" theme={null}
<InfiniteScroll data="products" as="ul">
  {products.data.map((product) => (
    <li key={product.id}>{product.name}</li>
  ))}
</InfiniteScroll>
```

```svelte Svelte icon="s" theme={null}
<InfiniteScroll data="products" as="ul">
    {#each products.data as product (product.id)}
        <li>{product.name}</li>
    {/each}
</InfiniteScroll>
```

## Element Targeting

The infinite scroll component automatically tracks content and assigns page numbers to elements for [URL synchronization](#url-synchronization). When your data items are not direct children of the component's root element, you need to specify which element contains the actual data items using the `itemsElement` prop.

```vue Vue icon="vuejs" theme={null}
<template>
  <InfiniteScroll data="users" items-element="#table-body">
    <table>
      <thead>
        <tr>
          <th>Name</th>
        </tr>
      </thead>
      <tbody id="table-body">
        <tr v-for="user in users.data" :key="user.id">
          <td>{{ user.name }}</td>
        </tr>
      </tbody>
    </table>
  </InfiniteScroll>
</template>
```

```jsx React icon="react" theme={null}
<InfiniteScroll data="users" itemsElement="#table-body">
  <table>
    <thead>
      <tr>
        <th>Name</th>
      </tr>
    </thead>
    <tbody id="table-body">
      {users.data.map((user) => (
        <tr key="{user.id}">
          <td>{user.name}</td>
        </tr>
      ))}
    </tbody>
  </table>
</InfiniteScroll>
```

```svelte Svelte icon="s" theme={null}
<InfiniteScroll data="users" items-element="#table-body">
    <table>
        <thead>
            <tr><th>Name</th></tr>
        </thead>
        <tbody id="table-body">
            {#each users.data as user (user.id)}
            <tr>
                <td>{user.name}</td>
            </tr>
            {/each}
        </tbody>
    </table>
</InfiniteScroll>
```

In this example, the component monitors the `#table-body` element and automatically tags each `<tr>` with a page number as new content loads. This enables proper URL updates based on which page's content is most visible in the viewport.

You can also specify custom trigger elements for loading more content using CSS selectors. This prevents the default trigger elements from being rendered and uses intersection observers on your custom elements instead.

```vue Vue icon="vuejs" theme={null}
<template>
  <InfiniteScroll
    data="users"
    items-element="#table-body"
    start-element="#table-header"
    end-element="#table-footer"
  >
    <table>
      <thead id="table-header">
        <tr>
          <th>Name</th>
        </tr>
      </thead>
      <tbody id="table-body">
        <tr v-for="user in users.data" :key="user.id">
          <td>{{ user.name }}</td>
        </tr>
      </tbody>
      <tfoot id="table-footer">
        <tr>
          <td>Footer</td>
        </tr>
      </tfoot>
    </table>
  </InfiniteScroll>
</template>
```

```jsx React icon="react" theme={null}
<InfiniteScroll
  data="users"
  itemsElement="#table-body"
  startElement="#table-header"
  endElement="#table-footer"
>
  <table>
    <thead id="table-header">
      <tr>
        <th>Name</th>
      </tr>
    </thead>
    <tbody id="table-body">
      {users.data.map((user) => (
        <tr key={user.id}>
          <td>{user.name}</td>
        </tr>
      ))}
    </tbody>
    <tfoot id="table-footer">
      <tr>
        <td>Footer</td>
      </tr>
    </tfoot>
  </table>
</InfiniteScroll>
```

```svelte Svelte icon="s" theme={null}
<InfiniteScroll
    data="users"
    items-element="#table-body"
    start-element="#table-header"
    end-element="#table-footer"
>
    <table>
        <thead id="table-header">
            <tr><th>Name</th></tr>
        </thead>
        <tbody id="table-body">
            {#each users.data as user (user.id)}
                <tr>
                    <td>{user.name}</td>
                </tr>
            {/each}
        </tbody>
        <tfoot id="table-footer">
            <tr><td>Footer</td></tr>
        </tfoot>
    </table>
</InfiniteScroll>
```

Alternatively, you can use template refs instead of CSS selectors. This avoids adding HTML attributes and provides direct element references.

```vue Vue icon="vuejs" theme={null}
<script setup>
import { ref } from "vue";
const tableHeader = ref();
const tableFooter = ref();
const tableBody = ref();
</script>

<template>
  <InfiniteScroll
    data="users"
    :items-element="() => tableBody"
    :start-element="() => tableHeader"
    :end-element="() => tableFooter"
  >
    <table>
      <thead ref="tableHeader">
        <tr>
          <th>Name</th>
        </tr>
      </thead>
      <tbody ref="tableBody">
        <tr v-for="user in users.data" :key="user.id">
          <td>{{ user.name }}</td>
        </tr>
      </tbody>
      <tfoot ref="tableFooter">
        <tr>
          <td>Footer</td>
        </tr>
      </tfoot>
    </table>
  </InfiniteScroll>
</template>
```

```jsx React icon="react" theme={null}
import { useRef } from "react";

export default ({ users }) => {
  const tableHeader = useRef();
  const tableFooter = useRef();
  const tableBody = useRef();

  return (
    <InfiniteScroll
      data="users"
      itemsElement={tableBody}
      startElement={tableHeader}
      endElement={tableFooter}
    >
      <table>
        <thead ref={tableHeader}>
          <tr>
            <th>Name</th>
          </tr>
        </thead>
        <tbody ref={tableBody}>
          {users.data.map((user) => (
            <tr key={user.id}>
              <td>{user.name}</td>
            </tr>
          ))}
        </tbody>
        <tfoot ref={tableFooter}>
          <tr>
            <td>Footer</td>
          </tr>
        </tfoot>
      </table>
    </InfiniteScroll>
  );
};
```

```svelte Svelte icon="s" theme={null}
<script>
    import { InfiniteScroll } from '@inertiajs/svelte'
    let { users } = $props()

    let tableHeader
    let tableFooter
    let tableBody
</script>

<InfiniteScroll
    data="users"
    items-element={() => tableBody}
    start-element={() => tableHeader}
    end-element={() => tableFooter}
>
    <table>
        <thead bind:this={tableHeader}>
            <tr><th>Name</th></tr>
        </thead>
        <tbody bind:this={tableBody}>
            {#each users.data as user (user.id)}
                <tr>
                    <td>{user.name}</td>
                </tr>
            {/each}
        </tbody>
        <tfoot bind:this={tableFooter}>
            <tr><td>Footer</td></tr>
        </tfoot>
    </table>
</InfiniteScroll>
```

## Scroll Containers

The infinite scroll component works within any scrollable container, not just the main document. The component automatically adapts to use the custom scroll container for trigger detection and calculations instead of the main document scroll.

```vue Vue icon="vuejs" theme={null}
<template>
  <div style="height: 400px; overflow-y: auto;">
    <InfiniteScroll data="users">
      <div v-for="user in users.data" :key="user.id">
        {{ user.name }}
      </div>
    </InfiniteScroll>
  </div>
</template>
```

```jsx React icon="react" theme={null}
<div style={{ height: "400px", overflowY: "auto" }}>
  <InfiniteScroll data="users">
    {users.data.map((user) => (
      <div key={user.id}>{user.name}</div>
    ))}
  </InfiniteScroll>
</div>
```

```svelte Svelte icon="s" theme={null}
<div style="height: 400px; overflow-y: auto;">
    <InfiniteScroll data="users">
        {#each users.data as user (user.id)}
            <div>{user.name}</div>
        {/each}
    </InfiniteScroll>
</div>
```

### Multiple Scroll Containers

Sometimes you may need to render multiple infinite scroll components on a single page. However, if both components use the default `page` query parameter for [URL synchronization](#url-synchronization), they will conflict with each other. To resolve this, instruct each paginator to use a custom `pageName`.

```php theme={null}
Route::get('/dashboard', function () {
    return Inertia::render('Dashboard', [
        'users' => Inertia::scroll(
            fn() => User::paginate(pageName: 'users')
        ),
        'orders' => Inertia::scroll(
            fn() => Order::paginate(pageName: 'orders')
        ),
    ]);
});
```

The `Inertia::scroll()` method automatically detects the `pageName` from each paginator, allowing both scroll containers to maintain independent pagination state. This results in URLs like `?users=2&orders=3` instead of conflicting `?page=` parameters.

For more information about pagination page names, see [Laravel's documentation](https://laravel.com/docs/pagination#multiple-paginator-instances-per-page).

## Programmatic Access

When you need to trigger loading actions programmatically, you may use a template ref.

```vue Vue icon="vuejs" theme={null}
<script setup>
import { ref } from "vue";
const infiniteScrollRef = ref(null);

const fetchNext = () => {
  infiniteScrollRef.value?.fetchNext();
};
</script>

<template>
  <button @click="fetchNext">Load More</button>

  <InfiniteScroll ref="infiniteScrollRef" data="users" manual>
    <!-- Your content -->
  </InfiniteScroll>
</template>
```

```jsx React icon="react" theme={null}
import { InfiniteScroll } from '@inertiajs/react'
import { useRef } from 'react'

export default ({ users }) => {
    const infiniteScrollRef = useRef(null)

    const fetchNext = () => {
        infiniteScrollRef.current?.fetchNext()
    }

    return (

            <button onClick={fetchNext}>Load More</button>

            <InfiniteScroll ref={infiniteScrollRef} data="users" manual>
                {users.data.map(user => (
                    <div key={user.id}>{user.name}</div>
                ))}
            </InfiniteScroll>

    )
}
```

```svelte Svelte icon="s" theme={null}
<script>
    import { InfiniteScroll } from '@inertiajs/svelte'
    let { users } = $props()

    let infiniteScrollRef

    const fetchNext = () => {
        infiniteScrollRef?.fetchNext()
    }
</script>

<button onclick={fetchNext}>Load More</button>

<InfiniteScroll bind:this={infiniteScrollRef} data="users" manual>
    {#each users.data as user (user.id)}
        <div>{user.name}</div>
    {/each}
</InfiniteScroll>
```

The component exposes the following methods:

* `fetchNext()` - Manually fetch the next page
* `fetchPrevious()` - Manually fetch the previous page
* `hasNext()` - Whether there is a next page
* `hasPrevious()` - Whether there is a previous page

## Inertia::scroll() Method

The `Inertia::scroll()` method provides server-side configuration for infinite scrolling. It automatically configures the proper merge behavior so that new data is appended or prepended to existing content instead of replacing it, and normalizes pagination metadata for the front-end component.

```php theme={null}
// Works with all Laravel pagination methods...
Inertia::scroll(User::paginate(20));
Inertia::scroll(User::simplePaginate(20));
Inertia::scroll(User::cursorPaginate(20));

// Works with API resources...
Inertia::scroll(UserResource::collection(User::paginate(20)));
```

If you don't use Laravel's paginator or use a different transformation layer, you may use the additional arguments that `scroll()` accepts.

```php theme={null}
// Customize the data wrapper key (defaults to 'data')...
Inertia::scroll($customPaginatedData, wrapper: 'items');

// Provide custom metadata resolution...
Inertia::scroll($data, metadata: $metadataProvider);
```

The metadata parameter accepts an instance of `ProvidesScrollMetadata` or a callback that returns such an instance. The callback receives the `$data` parameter. This is useful when integrating with third-party pagination libraries like Fractal.

```php theme={null}
use League\Fractal\Resource\Collection;

class FractalScrollMetadata implements ProvidesScrollMetadata
{
    public function __construct(protected Collection $resource) {}
    public function getPageName(): string {}
    public function getPreviousPage(): int|string|null {}
    public function getNextPage(): int|string|null {}
    public function getCurrentPage(): int|string|null {}
}
```

You may then use this custom metadata provider in your scroll function.

```php theme={null}
// Using an instance directly
Inertia::scroll($data, metadata: new FractalScrollMetadata($data));

// Using a callback
Inertia::scroll(
    fn() => $this->transformData($data),
    metadata: fn($data) => new FractalScrollMetadata($data)
);
```

To avoid repeating this setup in multiple controllers, you may define a macro.

```php theme={null}
// In your AppServiceProvider's boot method
Inertia::macro('fractalScroll', function (Collection $data) {
    return Inertia::scroll(
        $data,
        metadata: fn(Collection $data) => new FractalScrollMetadata($data)
    );
});

// Then use it in your controllers
return Inertia::render('Users/Index', [
    'users' => Inertia::fractalScroll($fractalCollection)
]);
```
