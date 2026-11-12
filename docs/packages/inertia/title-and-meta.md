Source: https://inertiajs.com/docs/v3/the-basics/title-and-meta.md

# Title & Meta

Since Inertia-powered JavaScript apps are rendered within the document `<body>`, they are unable to render markup to the document `<head>`, as it's outside of their scope. To help with this, Inertia ships with a `<Head>` component which can be used to set the page `<title>`, `<meta>` tags, and other `<head>` elements.

The `<Head>` component will only replace `<head>` elements that are not in your server-side root template.

The `<Head>` component is not available in the Svelte adapter, as Svelte already ships with its own `<svelte:head>` component.

## Head Component

To add `<head>` elements to your page, use the `<Head>` component. Within this component, you can include the elements that you wish to add to the document `<head>`.

```vue Vue icon="vuejs" theme={null}
import { Head } from '@inertiajs/vue3'

<Head>
    <title>Your page title</title>
    <meta name="description" content="Your page description">
</Head>
```

```jsx React icon="react" theme={null}
import { Head } from "@inertiajs/react";

<Head>
  <title>Your page title</title>
  <meta name="description" content="Your page description" />
</Head>;
```

```svelte Svelte icon="s" theme={null}
<svelte:head>
    <title>Your page title</title>
    <meta name="description" content="Your page description" />
</svelte:head>
```

## Title Shorthand

If you only need to add a `<title>` to the document `<head>`, you may simply pass the title as a prop to the `<Head>` component.

```vue Vue icon="vuejs" theme={null}
import { Head } from '@inertiajs/vue3'

<Head title="Your page title" />
```

```jsx React icon="react" theme={null}
import { Head } from "@inertiajs/react";

<Head title="Your page title" />;
```

```js Svelte icon="s" theme={null}
// Not supported
```

## Title Callback

You can globally modify the page `<title>` using the `title` callback in the `createInertiaApp` setup method. Typically, this method is invoked in your application's main JavaScript file. A common use case for the title callback is automatically adding an app name before or after each page title.

```js theme={null}
createInertiaApp({
  title: (title) => `${title} - My App`,
  // ...
});
```

The callback also receives the current [page object](https://inertiajs.com/docs/v3/the-basics/pages.md) as its second argument, which you may use to build titles from the page's props.

```js theme={null}
createInertiaApp({
  title: (title, page) => `${title} - ${page.props.appName}`,
  // ...
});
```

After defining the `title` callback, the callback will automatically be invoked when you set a title using the `<Head>` component.

```vue Vue icon="vuejs" theme={null}
import { Head } from '@inertiajs/vue3'

<Head title="Home">
```

```jsx React icon="react" theme={null}
import { Head } from '@inertiajs/react'

<Head title="Home">
```

```js Svelte icon="s" theme={null}
// Not supported
```

In this example, this results in the following `<title>` tag.

```html theme={null}
<title>Home - My App</title>
```

The `title` callback will also be invoked when you set the title using a `<title>` tag within your `<Head>` component.

```vue Vue icon="vuejs" theme={null}
import { Head } from '@inertiajs/vue3'

<Head>
    <title>Home</title>
</Head>
```

```jsx React icon="react" theme={null}
import { Head } from "@inertiajs/react";

<Head>
  <title>Home</title>
</Head>;
```

```js Svelte icon="s" theme={null}
// Not supported
```

## Multiple Head Instances

It's possible to have multiple instances of the `<Head>` component throughout your application. For example, your layout can set some default `<Head>` elements, and then your individual pages can override those defaults.

```vue Vue icon="vuejs" theme={null}
// Layout.vue import { Head } from '@inertiajs/vue3'

<Head>
    <title>My app</title>
    <meta head-key="description" name="description" content="This is the default description" />
    <link rel="icon" type="image/svg+xml" href="/favicon.svg" />
</Head>

// About.vue import { Head } from '@inertiajs/vue3'

<Head>
    <title>About - My app</title>
    <meta head-key="description" name="description" content="This is a page specific description" />
</Head>
```

```jsx React icon="react" theme={null}
// Layout.js

import { Head } from "@inertiajs/react";

<Head>
  <title>My app</title>
  <meta
    head-key="description"
    name="description"
    content="This is the default description"
  />
  <link rel="icon" type="image/svg+xml" href="/favicon.svg" />
</Head>;

// About.js

import { Head } from "@inertiajs/react";

<Head>
  <title>About - My app</title>
  <meta
    head-key="description"
    name="description"
    content="This is a page specific description"
  />
</Head>;
```

```js Svelte icon="s" theme={null}
// Not supported
```

Inertia will only ever render one `<title>` tag; however, all other tags will be stacked since it's valid to have multiple instances of them. To avoid duplicate tags in your `<head>`, you can use the `head-key` property, which will make sure the tag is only rendered once. This is illustrated in the example above for the `<meta name="description">` tag.

The code example above will render the following HTML.

```html theme={null}
<head>
  <link rel="icon" type="image/svg+xml" href="/favicon.svg" />
  <title>About - My app</title>
  <meta name="description" content="This is a page specific description" />
</head>
```

## Head Extension

When building a real application, it can sometimes be helpful to create a custom head component that extends Inertia's `<Head>` component. This gives you a place to set app-wide defaults, such as appending the app name to the page title.

```vue Vue icon="vuejs" theme={null}
<!-- AppHead.vue -->

<script setup>
import { Head } from "@inertiajs/vue3";

defineProps({ title: String });
</script>

<template>
  <Head :title="title ? `${title} - My App` : 'My App'">
    <slot />
  </Head>
</template>
```

```jsx React icon="react" theme={null}
// AppHead.js

import { Head } from "@inertiajs/react";

const Site = ({ title, children }) => {
  return (
    <Head>
      <title>{title ? `${title} - My App` : "My App"}</title>
      {children}
    </Head>
  );
};

export default Site;
```

```js Svelte icon="s" theme={null}
// Not supported
```

Once you have created the custom component, you can just start using it in your pages.

```vue Vue icon="vuejs" theme={null}
import AppHead from './AppHead'

<AppHead title="About" />
```

```jsx React icon="react" theme={null}
import AppHead from './AppHead'

<AppHead title="About">
```

```js Svelte icon="s" theme={null}
// Not supported
```

## Server-Side Head Elements

You may wish to include default head elements like `<title>` or `<meta>` tags in your root Blade template. This creates two challenges: preventing duplicates when [SSR](https://inertiajs.com/docs/v3/advanced/server-side-rendering.md) is active, and ensuring the client-side `<Head>` component may replace them during navigation.

### SSR Fallback

The `<x-inertia::head>` Blade component accepts fallback content via its slot. This content is only rendered in the initial HTML when [SSR](https://inertiajs.com/docs/v3/advanced/server-side-rendering.md) is not active. When SSR is active, the `<Head>` component already provides these elements as part of the server-rendered response, so the fallback is skipped.

```blade resources/views/app.blade.php theme={null}
<head>
    @vite('resources/js/app.js')
    <x-inertia::head>
        <title>{{ config('app.name') }}</title>
        <meta name="description" content="My application description">
    </x-inertia::head>
</head>
```

### The `data-inertia` Attribute

The client-side `<Head>` component tracks the elements it manages by marking them with a `data-inertia` attribute. By default, it leaves any other tags in your Blade template untouched. Since there may only be one `<title>` tag, the `<Head>` component will always replace it. Other elements like `<meta>` and `<link>` may have multiple instances, so the component needs a way to identify which ones it should manage.

You may add the `data-inertia` attribute to elements in your Blade template to have the `<Head>` component adopt them. On the first client-side navigation, it will match these elements by key and replace or remove them as needed.

```blade resources/views/app.blade.php theme={null}
<head>
    @vite('resources/js/app.js')
    <title>{{ config('app.name') }}</title>
    <meta data-inertia="description" name="description" content="My application description">
</head>
```

The `data-inertia` value corresponds to the `head-key` property on your client-side `<Head>` elements.
