Source: https://inertiajs.com/docs/v3/advanced/events.md

# Events

Inertia provides an event system that allows you to "hook into" the various lifecycle events of the library.

## Registering Listeners

To register an event listener, use the `router.on()` method.

```js Vue icon="vuejs" theme={null}
import { router } from "@inertiajs/vue3";

router.on("start", (event) => {
  console.log(`Starting a visit to ${event.detail.visit.url}`);
});
```

```jsx React icon="react" theme={null}
import { router } from "@inertiajs/react";

router.on("start", (event) => {
  console.log(`Starting a visit to ${event.detail.visit.url}`);
});
```

```js Svelte icon="s" theme={null}
import { router } from "@inertiajs/svelte";

router.on("start", (event) => {
  console.log(`Starting a visit to ${event.detail.visit.url}`);
});
```

Under the hood, Inertia uses native browser events, so you can also interact with Inertia events using the typical event methods you may already be familiar with. Just be sure to prepend `inertia:` to the event name.

```js Vue icon="vuejs" theme={null}
import { router } from "@inertiajs/vue3";

document.addEventListener("inertia:start", (event) => {
  console.log(`Starting a visit to ${event.detail.visit.url}`);
});
```

```jsx React icon="react" theme={null}
import { router } from "@inertiajs/react";

document.addEventListener("inertia:start", (event) => {
  console.log(`Starting a visit to ${event.detail.visit.url}`);
});
```

```js Svelte icon="s" theme={null}
import { router } from "@inertiajs/svelte";

document.addEventListener("inertia:start", (event) => {
  console.log(`Starting a visit to ${event.detail.visit.url}`);
});
```

## Removing Listeners

When you register an event listener, Inertia automatically returns a callback that can be invoked to remove the event listener.

```js Vue icon="vuejs" theme={null}
import { router } from "@inertiajs/vue3";

let removeStartEventListener = router.on("start", (event) => {
  console.log(`Starting a visit to ${event.detail.visit.url}`);
});

// Remove the listener...
removeStartEventListener();
```

```jsx React icon="react" theme={null}
import { router } from "@inertiajs/react";

let removeStartEventListener = router.on("start", (event) => {
  console.log(`Starting a visit to ${event.detail.visit.url}`);
});

// Remove the listener...
removeStartEventListener();
```

```js Svelte icon="s" theme={null}
import { router } from "@inertiajs/svelte";

let removeStartEventListener = router.on("start", (event) => {
  console.log(`Starting a visit to ${event.detail.visit.url}`);
});

// Remove the listener...
removeStartEventListener();
```

Combined with hooks, you can automatically remove the event listener when components unmount.

```vue Vue icon="vuejs" theme={null}
<script setup>
import { router } from '@inertiajs/vue3'
import { onUnmounted } from 'vue'

onUnmounted(
  router.on('start', (event) => {
    console.log(`Starting a visit to ${event.detail.visit.url}`)
  })
)
</script>
```

```jsx React icon="react" theme={null}
import { useEffect } from "react";
import { router } from "@inertiajs/react";

useEffect(() => {
  return router.on("start", (event) => {
    console.log(`Starting a visit to ${event.detail.visit.url}`);
  });
}, []);
```

```js Svelte icon="s" theme={null}
import { router } from "@inertiajs/svelte";

$effect(() => {
  return router.on("start", (event) => {
    console.log(`Starting a visit to ${event.detail.visit.url}`);
  });
});
```

Alternatively, if you're using native browser events, you can remove the event listener using `removeEventListener()`.

```js Vue icon="vuejs" theme={null}
import { router } from "@inertiajs/vue3";

let startEventListener = (event) => {
  console.log(`Starting a visit to ${event.detail.visit.url}`);
};

document.addEventListener("inertia:start", startEventListener);

// Remove the listener...
document.removeEventListener("inertia:start", startEventListener);
```

```jsx React icon="react" theme={null}
import { router } from "@inertiajs/react";

let startEventListener = (event) => {
  console.log(`Starting a visit to ${event.detail.visit.url}`);
};

document.addEventListener("inertia:start", startEventListener);

// Remove the listener...
document.removeEventListener("inertia:start", startEventListener);
```

```js Svelte icon="s" theme={null}
import { router } from "@inertiajs/svelte";

let startEventListener = (event) => {
  console.log(`Starting a visit to ${event.detail.visit.url}`);
};

document.addEventListener("inertia:start", startEventListener);

// Remove the listener...
document.removeEventListener("inertia:start", startEventListener);
```

## One-time Listeners

You may register a listener that fires only once using the `router.once()` method. The listener is automatically removed after the first invocation.

```js Vue icon="vuejs" theme={null}
import { router } from "@inertiajs/vue3";

router.once("start", (event) => {
  console.log(`Starting a visit to ${event.detail.visit.url}`);
});
```

```jsx React icon="react" theme={null}
import { router } from "@inertiajs/react";

router.once("start", (event) => {
  console.log(`Starting a visit to ${event.detail.visit.url}`);
});
```

```js Svelte icon="s" theme={null}
import { router } from "@inertiajs/svelte";

router.once("start", (event) => {
  console.log(`Starting a visit to ${event.detail.visit.url}`);
});
```

Like `router.on()`, this method returns a callback you may invoke to remove the listener before it fires.

```js Vue icon="vuejs" theme={null}
import { router } from "@inertiajs/vue3";

let removeStartEventListener = router.once("start", (event) => {
  console.log(`Starting a visit to ${event.detail.visit.url}`);
});

// Remove the listener before it fires...
removeStartEventListener();
```

```jsx React icon="react" theme={null}
import { router } from "@inertiajs/react";

let removeStartEventListener = router.once("start", (event) => {
  console.log(`Starting a visit to ${event.detail.visit.url}`);
});

// Remove the listener before it fires...
removeStartEventListener();
```

```js Svelte icon="s" theme={null}
import { router } from "@inertiajs/svelte";

let removeStartEventListener = router.once("start", (event) => {
  console.log(`Starting a visit to ${event.detail.visit.url}`);
});

// Remove the listener before it fires...
removeStartEventListener();
```

## Canceling Events

Some events, such as `before`, `networkError`, `httpException`, `location`, and `live`, support cancellation, allowing you to prevent Inertia's default behavior. Just like native events, the event will be canceled if only one event listener calls `event.preventDefault()`.

```js Vue icon="vuejs" theme={null}
import { router } from "@inertiajs/vue3";

router.on("before", (event) => {
  if (!confirm("Are you sure you want to navigate away?")) {
    event.preventDefault();
  }
});
```

```jsx React icon="react" theme={null}
import { router } from "@inertiajs/react";

router.on("before", (event) => {
  if (!confirm("Are you sure you want to navigate away?")) {
    event.preventDefault();
  }
});
```

```js Svelte icon="s" theme={null}
import { router } from "@inertiajs/svelte";

router.on("before", (event) => {
  if (!confirm("Are you sure you want to navigate away?")) {
    event.preventDefault();
  }
});
```

For convenience, if you register your event listener using `router.on()`, you can cancel the event by returning `false` from the listener.

```js Vue icon="vuejs" theme={null}
import { router } from "@inertiajs/vue3";

router.on("before", (event) => {
  return confirm("Are you sure you want to navigate away?");
});
```

```jsx React icon="react" theme={null}
import { router } from "@inertiajs/react";

router.on("before", (event) => {
  return confirm("Are you sure you want to navigate away?");
});
```

```js Svelte icon="s" theme={null}
import { router } from "@inertiajs/svelte";

router.on("before", (event) => {
  return confirm("Are you sure you want to navigate away?");
});
```

Note that browsers do not allow canceling the native `popstate` event, so preventing forward and back history visits with Inertia is not possible.

## Before

The `before` event fires when a request is about to be made to the server. This is useful for intercepting visits.

```js Vue icon="vuejs" theme={null}
import { router } from "@inertiajs/vue3";

router.on("before", (event) => {
  console.log(`About to make a visit to ${event.detail.visit.url}`);
});
```

```jsx React icon="react" theme={null}
import { router } from "@inertiajs/react";

router.on("before", (event) => {
  console.log(`About to make a visit to ${event.detail.visit.url}`);
});
```

```js Svelte icon="s" theme={null}
import { router } from "@inertiajs/svelte";

router.on("before", (event) => {
  console.log(`About to make a visit to ${event.detail.visit.url}`);
});
```

The primary purpose of this event is to allow you to prevent a visit from happening.

```js Vue icon="vuejs" theme={null}
import { router } from "@inertiajs/vue3";

router.on("before", (event) => {
  return confirm("Are you sure you want to navigate away?");
});
```

```jsx React icon="react" theme={null}
import { router } from "@inertiajs/react";

router.on("before", (event) => {
  return confirm("Are you sure you want to navigate away?");
});
```

```js Svelte icon="s" theme={null}
import { router } from "@inertiajs/svelte";

router.on("before", (event) => {
  return confirm("Are you sure you want to navigate away?");
});
```

## Start

The `start` event fires when a request to the server has started. This is useful for displaying loading indicators.

```js Vue icon="vuejs" theme={null}
import { router } from "@inertiajs/vue3";

router.on("start", (event) => {
  console.log(`Starting a visit to ${event.detail.visit.url}`);
});
```

```jsx React icon="react" theme={null}
import { router } from "@inertiajs/react";

router.on("start", (event) => {
  console.log(`Starting a visit to ${event.detail.visit.url}`);
});
```

```js Svelte icon="s" theme={null}
import { router } from "@inertiajs/svelte";

router.on("start", (event) => {
  console.log(`Starting a visit to ${event.detail.visit.url}`);
});
```

The `start` event is not cancelable.

## Progress

The `progress` event fires as progress increments during file uploads.

```js Vue icon="vuejs" theme={null}
import { router } from "@inertiajs/vue3";

router.on("progress", (event) => {
  this.form.progress = event.detail.progress.percentage;
});
```

```jsx React icon="react" theme={null}
import { router } from "@inertiajs/react";

router.on("progress", (event) => {
  this.form.progress = event.detail.progress.percentage;
});
```

```js Svelte icon="s" theme={null}
import { router } from "@inertiajs/svelte";

router.on("progress", (event) => {
  this.form.progress = event.detail.progress.percentage;
});
```

The `progress` event is not cancelable.

## Success

The `success` event fires on successful page visits, unless validation errors are present. However, this does *not* include history visits.

```js Vue icon="vuejs" theme={null}
import { router } from "@inertiajs/vue3";

router.on("success", (event) => {
  console.log(`Successfully made a visit to ${event.detail.page.url}`);
});
```

```jsx React icon="react" theme={null}
import { router } from "@inertiajs/react";

router.on("success", (event) => {
  console.log(`Successfully made a visit to ${event.detail.page.url}`);
});
```

```js Svelte icon="s" theme={null}
import { router } from "@inertiajs/svelte";

router.on("success", (event) => {
  console.log(`Successfully made a visit to ${event.detail.page.url}`);
});
```

The `success` event is not cancelable.

## Flash

The `flash` event fires when [flash data](https://inertiajs.com/docs/v3/data-props/flash-data.md) is received from the server. This is useful for displaying toast notifications or handling temporary data in a central location.

```js Vue icon="vuejs" theme={null}
import { router } from "@inertiajs/vue3";

router.on("flash", (event) => {
  if (event.detail.flash.toast) {
    showToast(event.detail.flash.toast);
  }
});
```

```jsx React icon="react" theme={null}
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

The `flash` event is not cancelable and fires on every response that carries flash data.

## Error

The `error` event fires when validation errors are present on "successful" page visits.

```js Vue icon="vuejs" theme={null}
import { router } from "@inertiajs/vue3";

router.on("error", (event) => {
  console.log(event.detail.errors);
});
```

```jsx React icon="react" theme={null}
import { router } from "@inertiajs/react";

router.on("error", (event) => {
  console.log(event.detail.errors);
});
```

```js Svelte icon="s" theme={null}
import { router } from "@inertiajs/svelte";

router.on("error", (event) => {
  console.log(event.detail.errors);
});
```

The `error` event is not cancelable.

## HTTP Exception

The `httpException` event fires when a non-Inertia response is received from the server, such as an HTML or JSON response. A valid Inertia response has the `X-Inertia` header set to `true` and a JSON payload containing [the page object](https://inertiajs.com/docs/v3/core-concepts/the-protocol.md#the-page-object).

This event is fired for all response types, including `200`, `400`, and `500` response codes.

```js Vue icon="vuejs" theme={null}
import { router } from "@inertiajs/vue3";

router.on("httpException", (event) => {
  console.log(`An invalid Inertia response was received.`);
  console.log(event.detail.response);
});
```

```jsx React icon="react" theme={null}
import { router } from "@inertiajs/react";

router.on("httpException", (event) => {
  console.log(`An invalid Inertia response was received.`);
  console.log(event.detail.response);
});
```

```js Svelte icon="s" theme={null}
import { router } from "@inertiajs/svelte";

router.on("httpException", (event) => {
  console.log(`An invalid Inertia response was received.`);
  console.log(event.detail.response);
});
```

You may cancel the `httpException` event to prevent Inertia from showing the non-Inertia response modal.

```js Vue icon="vuejs" theme={null}
import { router } from "@inertiajs/vue3";

router.on("httpException", (event) => {
  event.preventDefault();

  // Handle the invalid response yourself...
});
```

```jsx React icon="react" theme={null}
import { router } from "@inertiajs/react";

router.on("httpException", (event) => {
  event.preventDefault();

  // Handle the invalid response yourself...
});
```

```js Svelte icon="s" theme={null}
import { router } from "@inertiajs/svelte";

router.on("httpException", (event) => {
  event.preventDefault();

  // Handle the invalid response yourself...
});
```

## Network Error

The `networkError` event fires on unexpected XHR errors such as network interruptions. In addition, this event fires for errors generated when resolving page components.

```js Vue icon="vuejs" theme={null}
import { router } from "@inertiajs/vue3";

router.on("networkError", (event) => {
  console.log(`An unexpected error occurred during an Inertia visit.`);
  console.log(event.detail.error);
});
```

```jsx React icon="react" theme={null}
import { router } from "@inertiajs/react";

router.on("networkError", (event) => {
  console.log(`An unexpected error occurred during an Inertia visit.`);
  console.log(event.detail.error);
});
```

```js Svelte icon="s" theme={null}
import { router } from "@inertiajs/svelte";

router.on("networkError", (event) => {
  console.log(`An unexpected error occurred during an Inertia visit.`);
  console.log(event.detail.error);
});
```

You may cancel the `networkError` event to prevent the error from being thrown.

```js Vue icon="vuejs" theme={null}
import { router } from "@inertiajs/vue3";

router.on("networkError", (event) => {
  event.preventDefault();
  // Handle the error yourself
});
```

```jsx React icon="react" theme={null}
import { router } from "@inertiajs/react";

router.on("networkError", (event) => {
  event.preventDefault();
  // Handle the error yourself
});
```

```js Svelte icon="s" theme={null}
import { router } from "@inertiajs/svelte";

router.on("networkError", (event) => {
  event.preventDefault();
  // Handle the error yourself
});
```

This event will *not* fire for XHR requests that receive `400`- and `500`-level responses or for non-Inertia responses, as these situations are handled in other ways by Inertia. Please consult the [error handling documentation](https://inertiajs.com/docs/v3/advanced/error-handling.md) for more information.

## Finish

The `finish` event fires after an XHR request has completed for both "successful" and "unsuccessful" responses. This event is useful for hiding loading indicators.

```js Vue icon="vuejs" theme={null}
import { router } from "@inertiajs/vue3";

router.on("finish", (event) => {
  NProgress.done();
});
```

```jsx React icon="react" theme={null}
import { router } from "@inertiajs/react";

router.on("finish", (event) => {
  NProgress.done();
});
```

```js Svelte icon="s" theme={null}
import { router } from "@inertiajs/svelte";

router.on("finish", (event) => {
  NProgress.done();
});
```

The `finish` event is not cancelable.

## Navigate

The `navigate` event fires on successful page visits, as well as when navigating through history.

v3.9.0+

The event detail includes a `type` value describing how the navigation happened: `initial` for the first page load, `visit` for Inertia visits, and `history` for back and forward navigation.

```js Vue icon="vuejs" theme={null}
import { router } from "@inertiajs/vue3";

router.on("navigate", (event) => {
  console.log(`Navigated to ${event.detail.page.url}`);
  console.log(`Navigation type: ${event.detail.type}`);
});
```

```jsx React icon="react" theme={null}
import { router } from "@inertiajs/react";

router.on("navigate", (event) => {
  console.log(`Navigated to ${event.detail.page.url}`);
  console.log(`Navigation type: ${event.detail.type}`);
});
```

```js Svelte icon="s" theme={null}
import { router } from "@inertiajs/svelte";

router.on("navigate", (event) => {
  console.log(`Navigated to ${event.detail.page.url}`);
  console.log(`Navigation type: ${event.detail.type}`);
});
```

The `navigate` event is not cancelable.

## Location

v3.6.0+

The `location` event fires whenever Inertia is about to force a full-page navigation, either because the [asset version](https://inertiajs.com/docs/v3/advanced/asset-versioning.md) changed or because the server returned an `Inertia::location()` redirect. The event detail includes a `versionChange` boolean so you may tell an automatic asset version change apart from a manual redirect.

```js Vue icon="vuejs" theme={null}
import { router } from "@inertiajs/vue3";

router.on("location", (event) => {
  console.log(`Navigating to ${event.detail.url}`);
  console.log(`Triggered by a version change: ${event.detail.versionChange}`);
});
```

```jsx React icon="react" theme={null}
import { router } from "@inertiajs/react";

router.on("location", (event) => {
  console.log(`Navigating to ${event.detail.url}`);
  console.log(`Triggered by a version change: ${event.detail.versionChange}`);
});
```

```js Svelte icon="s" theme={null}
import { router } from "@inertiajs/svelte";

router.on("location", (event) => {
  console.log(`Navigating to ${event.detail.url}`);
  console.log(`Triggered by a version change: ${event.detail.versionChange}`);
});
```

You may cancel the `location` event to take over the navigation yourself, for example to show a "new version available" banner instead of reloading.

```js Vue icon="vuejs" theme={null}
import { router } from "@inertiajs/vue3";

router.on("location", (event) => {
  if (event.detail.versionChange) {
    event.preventDefault();
    showBanner("A new version is available.");
  }
});
```

```jsx React icon="react" theme={null}
import { router } from "@inertiajs/react";

router.on("location", (event) => {
  if (event.detail.versionChange) {
    event.preventDefault();
    showBanner("A new version is available.");
  }
});
```

```js Svelte icon="s" theme={null}
import { router } from "@inertiajs/svelte";

router.on("location", (event) => {
  if (event.detail.versionChange) {
    event.preventDefault();
    showBanner("A new version is available.");
  }
});
```

## Prefetching

The `prefetching` event fires when the router starts prefetching a page.

```js Vue icon="vuejs" theme={null}
import { router } from "@inertiajs/vue3";

router.on("prefetching", (event) => {
  console.log(`Prefetching ${event.detail.visit.url}`);
});
```

```jsx React icon="react" theme={null}
import { router } from "@inertiajs/react";

router.on("prefetching", (event) => {
  console.log(`Prefetching ${event.detail.visit.url}`);
});
```

```js Svelte icon="s" theme={null}
import { router } from "@inertiajs/svelte";

router.on("prefetching", (event) => {
  console.log(`Prefetching ${event.detail.visit.url}`);
});
```

The `prefetching` event is not cancelable.

## Prefetched

The `prefetched` event fires when the router has successfully prefetched a page.

```js Vue icon="vuejs" theme={null}
import { router } from "@inertiajs/vue3";

router.on("prefetched", (event) => {
  console.log(`Prefetched ${event.detail.visit.url}`);
});
```

```jsx React icon="react" theme={null}
import { router } from "@inertiajs/react";

router.on("prefetched", (event) => {
  console.log(`Prefetched ${event.detail.visit.url}`);
});
```

```js Svelte icon="s" theme={null}
import { router } from "@inertiajs/svelte";

router.on("prefetched", (event) => {
  console.log(`Prefetched ${event.detail.visit.url}`);
});
```

The `prefetched` event is not cancelable.

## Live

The `live` event fires whenever a broadcast event is about to refresh a [live prop](https://inertiajs.com/docs/v3/data-props/live-props.md). The event detail includes the props that are about to be refreshed, the channel the broadcast arrived on, the broadcast event name, and its payload.

```js Vue icon="vuejs" theme={null}
import { router } from "@inertiajs/vue3";

router.on("live", (event) => {
  console.log(`Refreshing ${event.detail.props.join(", ")}`);
});
```

```js React icon="react" theme={null}
import { router } from "@inertiajs/react";

router.on("live", (event) => {
  console.log(`Refreshing ${event.detail.props.join(", ")}`);
});
```

```js Svelte icon="s" theme={null}
import { router } from "@inertiajs/svelte";

router.on("live", (event) => {
  console.log(`Refreshing ${event.detail.props.join(", ")}`);
});
```

The `live` event is cancelable, allowing you to hold back the update and let the user decide when to see the new data.

## Event Callbacks

In addition to the global events described throughout this page, Inertia also provides a number of [event callbacks](https://inertiajs.com/docs/v3/the-basics/manual-visits.md#event-callbacks) that fire when you manually make Inertia visits.
