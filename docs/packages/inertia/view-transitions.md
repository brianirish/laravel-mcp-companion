Source: https://inertiajs.com/docs/v3/the-basics/view-transitions.md

# View Transitions

Inertia supports the [View Transitions API](https://developer.chrome.com/docs/web-platform/view-transitions), allowing you to animate page transitions.

The View Transitions API is a [relatively new browser feature](https://caniuse.com/view-transitions). Inertia gracefully falls back to standard page transitions in browsers that don't support the API.

## Enabling Transitions

You may enable view transitions for a visit by setting the `viewTransition` option to `true`. By default, this will apply a cross-fade transition between pages.

```js Vue icon="vuejs" theme={null}
import { router } from "@inertiajs/vue3";

router.visit("/another-page", { viewTransition: true });
```

```js React icon="react" theme={null}
import { router } from "@inertiajs/react";

router.visit("/another-page", { viewTransition: true });
```

```js Svelte icon="s" theme={null}
import { router } from "@inertiajs/svelte";

router.visit("/another-page", { viewTransition: true });
```

## Transition Callbacks

You may also pass a callback to the `viewTransition` option, which will receive the standard [`ViewTransition`](https://developer.mozilla.org/en-US/docs/Web/API/ViewTransition) instance provided by the browser. This allows you to hook into the various promises provided by the API.

```js Vue icon="vuejs" theme={null}
import { router } from "@inertiajs/vue3";

router.visit("/another-page", {
  viewTransition: (transition) => {
    transition.ready.then(() => console.log("Transition ready"));
    transition.updateCallbackDone.then(() => console.log("DOM updated"));
    transition.finished.then(() => console.log("Transition finished"));
  },
});
```

```js React icon="react" theme={null}
import { router } from "@inertiajs/react";

router.visit("/another-page", {
  viewTransition: (transition) => {
    transition.ready.then(() => console.log("Transition ready"));
    transition.updateCallbackDone.then(() => console.log("DOM updated"));
    transition.finished.then(() => console.log("Transition finished"));
  },
});
```

```js Svelte icon="s" theme={null}
import { router } from "@inertiajs/svelte";

router.visit("/another-page", {
  viewTransition: (transition) => {
    transition.ready.then(() => console.log("Transition ready"));
    transition.updateCallbackDone.then(() => console.log("DOM updated"));
    transition.finished.then(() => console.log("Transition finished"));
  },
});
```

## Links

The `viewTransition` option is also available on the `Link` component.

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

You may also pass a callback to access the `ViewTransition` instance.

```vue Vue icon="vuejs" theme={null}
import { Link } from '@inertiajs/vue3'

<Link
  href="/another-page"
  :view-transition="
    (transition) => transition.finished.then(() => console.log('Done'))
  "
>
    Navigate
</Link>
```

```jsx React icon="react" theme={null}
import { Link } from "@inertiajs/react";

<Link
  href="/another-page"
  viewTransition={(transition) =>
    transition.finished.then(() => console.log("Done"))
  }
>
  Navigate
</Link>;
```

```svelte Svelte icon="s" theme={null}
import { Link } from '@inertiajs/svelte'

<Link
    href="/another-page"
    viewTransition={(transition) => transition.finished.then(() => console.log('Done'))}
>
    Navigate
</Link>
```

## Global Configuration

You may enable view transitions globally for all visits by configuring the `visitOptions` callback when [initializing your Inertia app](https://inertiajs.com/docs/v3/installation/client-side-setup.md#configuring-defaults).

```js Vue icon="vuejs" theme={null}
import { createInertiaApp } from "@inertiajs/vue3";

createInertiaApp({
  // ...
  defaults: {
    visitOptions: (href, options) => {
      return { viewTransition: true };
    },
  },
});
```

```jsx React icon="react" theme={null}
import { createInertiaApp } from "@inertiajs/react";

createInertiaApp({
  // ...
  defaults: {
    visitOptions: (href, options) => {
      return { viewTransition: true };
    },
  },
});
```

```js Svelte icon="s" theme={null}
import { createInertiaApp } from "@inertiajs/svelte";

createInertiaApp({
  // ...
  defaults: {
    visitOptions: (href, options) => {
      return { viewTransition: true };
    },
  },
});
```

## Customizing Transitions

You may customize the transition animations using CSS. The View Transitions API uses several pseudo-elements that you can target with CSS to create custom animations. The following examples are taken from the [Chrome documentation](https://developer.chrome.com/docs/web-platform/view-transitions/same-document#customize_the_transition).

```css theme={null}
@keyframes fade-in {
  from {
    opacity: 0;
  }
}
@keyframes fade-out {
  to {
    opacity: 0;
  }
}
@keyframes slide-from-right {
  from {
    transform: translateX(30px);
  }
}
@keyframes slide-to-left {
  to {
    transform: translateX(-30px);
  }
}
::view-transition-old(root) {
  animation:
    90ms cubic-bezier(0.4, 0, 1, 1) both fade-out,
    300ms cubic-bezier(0.4, 0, 0.2, 1) both slide-to-left;
}
::view-transition-new(root) {
  animation:
    210ms cubic-bezier(0, 0, 0.2, 1) 90ms both fade-in,
    300ms cubic-bezier(0.4, 0, 0.2, 1) both slide-from-right;
}
```

You may also animate individual elements between pages by assigning them a unique `view-transition-name`. For example, you may animate an avatar from a large size on a profile page to a small size on a dashboard.

```vue Vue icon="vuejs" theme={null}
<!-- Profile.vue -->
<template>
  <img src="/avatar.jpg" alt="User" class="avatar-large" />
</template>

<style>
.avatar-large {
  view-transition-name: user-avatar;
  width: auto;
  height: 200px;
}
</style>

<!-- Dashboard.vue -->
<template>
  <img src="/avatar.jpg" alt="User" class="avatar-small" />
</template>

<style>
.avatar-small {
  view-transition-name: user-avatar;
  width: auto;
  height: 40px;
}
</style>
```

```jsx React icon="react" theme={null}
// Profile.jsx
export default function Profile() {
    return <img src="/avatar.jpg" alt="User" className="avatar-large" />
}

// CSS
.avatar-large {
    view-transition-name: user-avatar;
    width: auto;
    height: 200px;
}

// Dashboard.jsx
export default function Dashboard() {
    return <img src="/avatar.jpg" alt="User" className="avatar-small" />
}

// CSS
.avatar-small {
    view-transition-name: user-avatar;
    width: auto;
    height: 40px;
}
```

```svelte Svelte icon="s" theme={null}
<!-- Profile.svelte -->
<img src="/avatar.jpg" alt="User" class="avatar-large" />

<style>
.avatar-large {
    view-transition-name: user-avatar;
    width: auto;
    height: 200px;
}
</style>

<!-- Dashboard.svelte -->
<img src="/avatar.jpg" alt="User" class="avatar-small" />

<style>
.avatar-small {
    view-transition-name: user-avatar;
    width: auto;
    height: 40px;
}
</style>
```

You may customize view transitions to your liking using any CSS animations you wish. For more information, please consult the [View Transitions API documentation](https://developer.chrome.com/docs/web-platform/view-transitions/same-document#customize_the_transition).
