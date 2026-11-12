Source: https://inertiajs.com/docs/v3/the-basics/manual-visits.md

# Manual Visits

In addition to [creating links](https://inertiajs.com/docs/v3/the-basics/links.md), it's also possible to manually make Inertia visits or requests programmatically via JavaScript. This is accomplished via the `router.visit()` method.

```js Vue icon="vuejs" theme={null}
import { router } from "@inertiajs/vue3";

router.visit(url, {
  method: "get",
  data: {},
  replace: false,
  preserveState: false,
  preserveScroll: false,
  only: [],
  except: [],
  headers: {},
  errorBag: null,
  forceFormData: false,
  queryStringArrayFormat: "brackets",
  async: false,
  showProgress: true,
  fresh: false,
  reset: [],
  preserveUrl: false,
  prefetch: false,
  preserveErrors: false,
  viewTransition: false,
  component: null,
  pageProps: null,
  onCancelToken: (cancelToken) => {},
  onCancel: () => {},
  onBefore: (visit) => {},
  onStart: (visit) => {},
  onProgress: (progress) => {},
  onSuccess: (page) => {},
  onError: (errors) => {},
  onHttpException: (response) => {},
  onNetworkError: (error) => {},
  onFinish: (visit) => {},
  onPrefetching: () => {},
  onPrefetched: () => {},
});
```

```js React icon="react" theme={null}
import { router } from "@inertiajs/react";

router.visit(url, {
  method: "get",
  data: {},
  replace: false,
  preserveState: false,
  preserveScroll: false,
  only: [],
  except: [],
  headers: {},
  errorBag: null,
  forceFormData: false,
  queryStringArrayFormat: "brackets",
  async: false,
  showProgress: true,
  fresh: false,
  reset: [],
  preserveUrl: false,
  prefetch: false,
  preserveErrors: false,
  viewTransition: false,
  component: null,
  pageProps: null,
  onCancelToken: (cancelToken) => {},
  onCancel: () => {},
  onBefore: (visit) => {},
  onStart: (visit) => {},
  onProgress: (progress) => {},
  onSuccess: (page) => {},
  onError: (errors) => {},
  onHttpException: (response) => {},
  onNetworkError: (error) => {},
  onFinish: (visit) => {},
  onPrefetching: () => {},
  onPrefetched: () => {},
});
```

```js Svelte icon="s" theme={null}
import { router } from "@inertiajs/svelte";

router.visit(url, {
  method: "get",
  data: {},
  replace: false,
  preserveState: false,
  preserveScroll: false,
  only: [],
  except: [],
  headers: {},
  errorBag: null,
  forceFormData: false,
  queryStringArrayFormat: "brackets",
  async: false,
  showProgress: true,
  fresh: false,
  reset: [],
  preserveUrl: false,
  prefetch: false,
  preserveErrors: false,
  viewTransition: false,
  component: null,
  pageProps: null,
  onCancelToken: (cancelToken) => {},
  onCancel: () => {},
  onBefore: (visit) => {},
  onStart: (visit) => {},
  onProgress: (progress) => {},
  onSuccess: (page) => {},
  onError: (errors) => {},
  onHttpException: (response) => {},
  onNetworkError: (error) => {},
  onFinish: (visit) => {},
  onPrefetching: () => {},
  onPrefetched: () => {},
});
```

However, it's generally more convenient to use one of Inertia's shortcut request methods. These methods share all the same options as `router.visit()`.

```js Vue icon="vuejs" theme={null}
import { router } from "@inertiajs/vue3";

router.get(url, data, options);
router.post(url, data, options);
router.put(url, data, options);
router.patch(url, data, options);
router.delete(url, options);
router.query(url, data, options);
router.reload(options); // Uses the current URL
```

```js React icon="react" theme={null}
import { router } from "@inertiajs/react";

router.get(url, data, options);
router.post(url, data, options);
router.put(url, data, options);
router.patch(url, data, options);
router.delete(url, options);
router.query(url, data, options);
router.reload(options); // Uses the current URL
```

```js Svelte icon="s" theme={null}
import { router } from "@inertiajs/svelte";

router.get(url, data, options);
router.post(url, data, options);
router.put(url, data, options);
router.patch(url, data, options);
router.delete(url, options);
router.query(url, data, options);
router.reload(options); // Uses the current URL
```

The `reload()` method is a convenient, shorthand method that automatically visits the current page with `preserveState` and `preserveScroll` both set to `true`, making it the perfect method to invoke when you just want to reload the current page's data.

## Method

You may use the `method` option to set the request's HTTP method to `get`, `post`, `put`, `patch`, `delete`, or `query`. The default method is `get`.

```js Vue icon="vuejs" theme={null}
import { router } from "@inertiajs/vue3";

router.visit(url, { method: "post" });
```

```js React icon="react" theme={null}
import { router } from "@inertiajs/react";

router.visit(url, { method: "post" });
```

```js Svelte icon="s" theme={null}
import { router } from "@inertiajs/svelte";

router.visit(url, { method: "post" });
```

Uploading files via `put` or `patch` is not supported in Laravel. Instead, make the request via `post`, including a `_method` field set to `put` or `patch`. This is called [form method spoofing](https://laravel.com/docs/routing#form-method-spoofing).

## QUERY Method

v3.10.0+Laravel Adapter v3.6.0+

Sometimes you may wish to send search filters that are too large or too deeply nested for a query string. Like `GET`, the `QUERY` HTTP method is safe and idempotent, but it sends its data in the request body instead of the URL. You may make a `QUERY` visit using the `router.query()` method.

```js Vue icon="vuejs" theme={null}
import { router } from "@inertiajs/vue3";

router.query("/products", {
  categories: ["Keyboards", "Monitors"],
  price: { min: 100, max: 500 },
});
```

```js React icon="react" theme={null}
import { router } from "@inertiajs/react";

router.query("/products", {
  categories: ["Keyboards", "Monitors"],
  price: { min: 100, max: 500 },
});
```

```js Svelte icon="s" theme={null}
import { router } from "@inertiajs/svelte";

router.query("/products", {
  categories: ["Keyboards", "Monitors"],
  price: { min: 100, max: 500 },
});
```

As with other non-`GET` visits, `QUERY` visits [preserve component state](#state-preservation) by default. The data isn't part of the URL, so refreshing the page or sharing its link loses the filters. `GET` remains the better choice for filters that users should be able to bookmark or share.

Inertia remembers the request body of a page rendered by a `QUERY` visit and resends it on reloads, [partial reloads](https://inertiajs.com/docs/v3/data-props/partial-reloads.md), [polling](https://inertiajs.com/docs/v3/data-props/polling.md), [deferred props](https://inertiajs.com/docs/v3/data-props/deferred-props.md), and [infinite scroll](https://inertiajs.com/docs/v3/data-props/infinite-scroll.md) requests, so these keep returning the filtered results. Any `data` passed to `router.reload()` is merged into the remembered body.

## Wayfinder

When using [Wayfinder](https://github.com/laravel/wayfinder), you can pass the resulting object directly to any router method. The router will infer the HTTP method and URL from the Wayfinder object.

```js Vue icon="vuejs" theme={null}
import { router } from "@inertiajs/vue3";
import { show } from "App/Http/Controllers/UserController";

router.visit(show(1));
router.post(store());
router.delete(destroy(1));
```

```js React icon="react" theme={null}
import { router } from "@inertiajs/react";
import { show } from "App/Http/Controllers/UserController";

router.visit(show(1));
router.post(store());
router.delete(destroy(1));
```

```js Svelte icon="s" theme={null}
import { router } from "@inertiajs/svelte";
import { show } from "App/Http/Controllers/UserController";

router.visit(show(1));
router.post(store());
router.delete(destroy(1));
```

If you provide both a Wayfinder object and specify the `method` option, the `method` option will take precedence.

```js Vue icon="vuejs" theme={null}
import { router } from "@inertiajs/vue3";
import { update } from "App/Http/Controllers/UserController";

router.visit(update(1), { method: "patch" });
```

```js React icon="react" theme={null}
import { router } from "@inertiajs/react";
import { update } from "App/Http/Controllers/UserController";

router.visit(update(1), { method: "patch" });
```

```js Svelte icon="s" theme={null}
import { router } from "@inertiajs/svelte";
import { update } from "App/Http/Controllers/UserController";

router.visit(update(1), { method: "patch" });
```

## Data

You may use the `data` option to add data to the request.

```js Vue icon="vuejs" theme={null}
import { router } from "@inertiajs/vue3";

router.visit("/users", {
  method: "post",
  data: {
    name: "John Doe",
    email: "john.doe@example.com",
  },
});
```

```js React icon="react" theme={null}
import { router } from "@inertiajs/react";

router.visit("/users", {
  method: "post",
  data: {
    name: "John Doe",
    email: "john.doe@example.com",
  },
});
```

```js Svelte icon="s" theme={null}
import { router } from "@inertiajs/svelte";

router.visit("/users", {
  method: "post",
  data: {
    name: "John Doe",
    email: "john.doe@example.com",
  },
});
```

For convenience, the `get()`, `post()`, `put()`, `patch()`, and `query()` methods all accept `data` as their second argument.

```js Vue icon="vuejs" theme={null}
import { router } from "@inertiajs/vue3";

router.post("/users", {
  name: "John Doe",
  email: "john.doe@example.com",
});
```

```js React icon="react" theme={null}
import { router } from "@inertiajs/react";

router.post("/users", {
  name: "John Doe",
  email: "john.doe@example.com",
});
```

```js Svelte icon="s" theme={null}
import { router } from "@inertiajs/svelte";

router.post("/users", {
  name: "John Doe",
  email: "john.doe@example.com",
});
```

## Custom Headers

The `headers` option allows you to add custom headers to a request.

```js Vue icon="vuejs" theme={null}
import { router } from "@inertiajs/vue3";

router.post("/users", data, {
  headers: {
    "Custom-Header": "value",
  },
});
```

```js React icon="react" theme={null}
import { router } from "@inertiajs/react";

router.post("/users", data, {
  headers: {
    "Custom-Header": "value",
  },
});
```

```js Svelte icon="s" theme={null}
import { router } from "@inertiajs/svelte";

router.post("/users", data, {
  headers: {
    "Custom-Header": "value",
  },
});
```

The headers Inertia uses internally to communicate its state to the server take priority and therefore cannot be overwritten.

## Global Visit Options

You may configure a `visitOptions` callback when [initializing your Inertia app](https://inertiajs.com/docs/v3/installation/client-side-setup.md#configuring-defaults) to modify visit options globally for every request. The callback receives the target URL and the current visit options, and should return an object with any options you want to override.

```js Vue icon="vuejs" theme={null}
import { createApp, h } from "vue";
import { createInertiaApp } from "@inertiajs/vue3";

createInertiaApp({
  // ...
  defaults: {
    visitOptions: (href, options) => {
      return {
        headers: {
          ...options.headers,
          "X-Custom-Header": "value",
        },
      };
    },
  },
});
```

```jsx React icon="react" theme={null}
import { createInertiaApp } from "@inertiajs/react";
import { createRoot } from "react-dom/client";

createInertiaApp({
  // ...
  defaults: {
    visitOptions: (href, options) => {
      return {
        headers: {
          ...options.headers,
          "X-Custom-Header": "value",
        },
      };
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
      return {
        headers: {
          ...options.headers,
          "X-Custom-Header": "value",
        },
      };
    },
  },
});
```

## File Uploads

When making visits / requests that include files, Inertia will automatically convert the request data into a `FormData` object. If you would like the request to always use a `FormData` object, you may use the `forceFormData` option.

```js Vue icon="vuejs" theme={null}
import { router } from "@inertiajs/vue3";

router.post("/companies", data, {
  forceFormData: true,
});
```

```js React icon="react" theme={null}
import { router } from "@inertiajs/react";

router.post("/companies", data, {
  forceFormData: true,
});
```

```js Svelte icon="s" theme={null}
import { router } from "@inertiajs/svelte";

router.post("/companies", data, {
  forceFormData: true,
});
```

For more information on uploading files, check out the dedicated [file uploads](https://inertiajs.com/docs/v3/the-basics/file-uploads.md) documentation.

## Browser History

When making visits, Inertia automatically adds a new entry into the browser history. However, it's also possible to replace the current history entry by setting the `replace` option to `true`.

```js Vue icon="vuejs" theme={null}
import { router } from "@inertiajs/vue3";

router.get("/users", { search: "John" }, { replace: true });
```

```js React icon="react" theme={null}
import { router } from "@inertiajs/react";

router.get("/users", { search: "John" }, { replace: true });
```

```js Svelte icon="s" theme={null}
import { router } from "@inertiajs/svelte";

router.get("/users", { search: "John" }, { replace: true });
```

Visits made to the same URL automatically set `replace` to `true`.

## Client-Side Visits

You can use the `router.push` and `router.replace` methods to make client-side visits. These methods are useful when you want to update the browser's history without making a server request.

```js Vue icon="vuejs" theme={null}
import { router } from "@inertiajs/vue3";

router.push({
  url: "/users",
  component: "Users",
  props: { search: "John" },
  clearHistory: false,
  encryptHistory: false,
  preserveScroll: false,
  preserveState: false,
  errorBag: null,
  onSuccess: (page) => {},
  onError: (errors) => {},
  onFinish: (visit) => {},
});
```

```js React icon="react" theme={null}
import { router } from "@inertiajs/react";

router.push({
  url: "/users",
  component: "Users",
  props: { search: "John" },
  clearHistory: false,
  encryptHistory: false,
  preserveScroll: false,
  preserveState: false,
  errorBag: null,
  onSuccess: (page) => {},
  onError: (errors) => {},
  onFinish: (visit) => {},
});
```

```js Svelte icon="s" theme={null}
import { router } from "@inertiajs/svelte";

router.push({
  url: "/users",
  component: "Users",
  props: { search: "John" },
  clearHistory: false,
  encryptHistory: false,
  preserveScroll: false,
  preserveState: false,
  errorBag: null,
  onSuccess: (page) => {},
  onError: (errors) => {},
  onFinish: (visit) => {},
});
```

All of the parameters are optional. By default, all passed parameters (except `errorBag`) will be merged with the current page. This means you are responsible for overriding the current page's URL, component, and props.

If you need access to the current page's props, you may pass a function to the `props` option. This function receives the current props (including any [once props](https://inertiajs.com/docs/v3/data-props/once-props.md)) and should return the new props.

```js Vue icon="vuejs" theme={null}
import { router } from "@inertiajs/vue3";

router.push({ url: "/users", component: "Users" });

router.replace({
  props: (currentProps) => ({ ...currentProps, search: "John" }),
});
```

```js React icon="react" theme={null}
import { router } from "@inertiajs/react";

router.push({ url: "/users", component: "Users" });

router.replace({
  props: (currentProps) => ({ ...currentProps, search: "John" }),
});
```

```js Svelte icon="s" theme={null}
import { router } from "@inertiajs/svelte";

router.push({ url: "/users", component: "Users" });

router.replace({
  props: (currentProps) => ({ ...currentProps, search: "John" }),
});
```

The function also receives [once props](https://inertiajs.com/docs/v3/data-props/once-props.md) as a second argument. This is useful when you want to replace all regular props while still preserving once props.

```js Vue icon="vuejs" theme={null}
import { router } from "@inertiajs/vue3";

router.replace({
  props: (currentProps, onceProps) => ({ ...onceProps, search: "John" }),
});
```

```js React icon="react" theme={null}
import { router } from "@inertiajs/react";

router.replace({
  props: (currentProps, onceProps) => ({ ...onceProps, search: "John" }),
});
```

```js Svelte icon="s" theme={null}
import { router } from "@inertiajs/svelte";

router.replace({
  props: (currentProps, onceProps) => ({ ...onceProps, search: "John" }),
});
```

The `errorBag` option allows you to specify which error bag to use when handling validation errors in the `onError` callback.

Make sure that any route you push on the client side is also defined on the server side. If the user refreshes the page, the server will need to know how to render the page.

> [!WARNING]
>
> Some browsers limit the number of `history.pushState()` and
> `history.replaceState()` calls allowed within a short time period. Inertia
> catches this error and logs it to the console, but the state update will be
> lost. Avoid calling `router.push()` or `router.replace()` too frequently, and
> consider debouncing or batching updates in high-frequency scenarios.

### Prop Helpers

Inertia provides three helper methods for updating page props without making server requests. These methods are shortcuts to `router.replace()` and automatically set `preserveScroll` and `preserveState` to `true`.

```js Vue icon="vuejs" theme={null}
import { router } from "@inertiajs/vue3";

// Replace a prop value...
router.replaceProp("user.name", "Jane Smith");

// Append to an array prop...
router.appendToProp("messages", { id: 4, text: "New message" });

// Prepend to an array prop...
router.prependToProp("tags", "urgent");
```

```js React icon="react" theme={null}
import { router } from "@inertiajs/react";

// Replace a prop value...
router.replaceProp("user.name", "Jane Smith");

// Append to an array prop...
router.appendToProp("messages", { id: 4, text: "New message" });

// Prepend to an array prop...
router.prependToProp("tags", "urgent");
```

```js Svelte icon="s" theme={null}
import { router } from "@inertiajs/svelte";

// Replace a prop value...
router.replaceProp("user.name", "Jane Smith");

// Append to an array prop...
router.appendToProp("messages", { id: 4, text: "New message" });

// Prepend to an array prop...
router.prependToProp("tags", "urgent");
```

All three methods support dot notation for nested props and can accept a callback function that receives the current value as the first argument and the current page props as the second argument.

```js Vue icon="vuejs" theme={null}
import { router } from '@inertiajs/vue3'

router.prependToProp('notifications', (current, props) => {
    return {
        id: Date.now(),
        message: `Hello ${props.user.name}`,
    }
})
```

```js React icon="react" theme={null}
import { router } from '@inertiajs/react'

router.prependToProp('notifications', (current, props) => {
    return {
        id: Date.now(),
        message: `Hello ${props.user.name}`,
    }
})
```

```js Svelte icon="s" theme={null}
import { router } from '@inertiajs/svelte'

router.prependToProp('notifications', (current, props) => {
    return {
        id: Date.now(),
        message: `Hello ${props.user.name}`,
    }
})
```

## State Preservation

By default, page visits to the same page create a fresh page component instance. This causes any local state, such as form inputs, scroll positions, and focus states to be lost.

However, in some situations, it's necessary to preserve the page component state. For example, when submitting a form, you need to preserve your form data in the event that form validation fails on the server.

For this reason, the `post`, `put`, `patch`, `delete`, `query`, and `reload` methods all set the `preserveState` option to `true` by default.

You can instruct Inertia to preserve the component's state when using the `get` method by setting the `preserveState` option to `true`.

```js Vue icon="vuejs" theme={null}
import { router } from "@inertiajs/vue3";

router.get("/users", { search: "John" }, { preserveState: true });
```

```js React icon="react" theme={null}
import { router } from "@inertiajs/react";

router.get("/users", { search: "John" }, { preserveState: true });
```

```js Svelte icon="s" theme={null}
import { router } from "@inertiajs/svelte";

router.get("/users", { search: "John" }, { preserveState: true });
```

If you'd like to only preserve state if the response includes validation errors, set the `preserveState` option to "errors".

```js Vue icon="vuejs" theme={null}
import { router } from "@inertiajs/vue3";

router.get("/users", { search: "John" }, { preserveState: "errors" });
```

```js React icon="react" theme={null}
import { router } from "@inertiajs/react";

router.get("/users", { search: "John" }, { preserveState: "errors" });
```

```js Svelte icon="s" theme={null}
import { router } from "@inertiajs/svelte";

router.get("/users", { search: "John" }, { preserveState: "errors" });
```

You can also lazily evaluate the `preserveState` option based on the response by providing a callback.

```js Vue icon="vuejs" theme={null}
import { router } from "@inertiajs/vue3";

router.post("/users", data, {
  preserveState: (page) => page.props.someProp === "value",
});
```

```js React icon="react" theme={null}
import { router } from "@inertiajs/react";

router.post("/users", data, {
  preserveState: (page) => page.props.someProp === "value",
});
```

```js Svelte icon="s" theme={null}
import { router } from "@inertiajs/svelte";

router.post("/users", data, {
  preserveState: (page) => page.props.someProp === "value",
});
```

## Scroll Preservation

When navigating between pages, Inertia mimics default browser behavior by automatically resetting the scroll position of the document body (as well as any [scroll regions](https://inertiajs.com/docs/v3/advanced/scroll-management.md#scroll-regions) you've defined) back to the top of the page.

You can disable this behavior by setting the `preserveScroll` option to `true`.

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

For more information regarding this feature, please consult the [scroll management](https://inertiajs.com/docs/v3/advanced/scroll-management.md) documentation.

## Partial Reloads

The `only` option allows you to request a subset of the props (data) from the server on subsequent visits to the same page, thus making your application more efficient since it does not need to retrieve data that the page is not interested in refreshing.

```js Vue icon="vuejs" theme={null}
import { router } from "@inertiajs/vue3";

router.get("/users", { search: "John" }, { only: ["users"] });
```

```js React icon="react" theme={null}
import { router } from "@inertiajs/react";

router.get("/users", { search: "John" }, { only: ["users"] });
```

```js Svelte icon="s" theme={null}
import { router } from "@inertiajs/svelte";

router.get("/users", { search: "John" }, { only: ["users"] });
```

For more information on this feature, please consult the [partial reloads](https://inertiajs.com/docs/v3/data-props/partial-reloads.md) documentation.

## View Transitions

You may enable [View transitions](https://inertiajs.com/docs/v3/the-basics/view-transitions.md) for a visit by setting the `viewTransition` option to `true`. This will use the browser's View Transitions API to animate the page transition.

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

## Visit Cancellation

You may cancel all in-flight visits using the `router.cancelAll()` method. By default, this cancels all synchronous, asynchronous, and prefetch requests.

```js Vue icon="vuejs" theme={null}
import { router } from "@inertiajs/vue3";

// Cancel all in-flight requests...
router.cancelAll();
```

```js React icon="react" theme={null}
import { router } from "@inertiajs/react";

// Cancel all in-flight requests...
router.cancelAll();
```

```js Svelte icon="s" theme={null}
import { router } from "@inertiajs/svelte";

// Cancel all in-flight requests...
router.cancelAll();
```

You may selectively cancel specific request types by passing an options object.

```js theme={null}
// Cancel only async requests (leaving sync and prefetch active)...
router.cancelAll({ sync: false, prefetch: false });

// Cancel only sync requests...
router.cancelAll({ async: false, prefetch: false });

// Cancel everything except prefetch requests...
router.cancelAll({ prefetch: false });
```

### Cancel Tokens

For more granular control, you may cancel individual visits using a cancel token. Inertia automatically generates a cancel token and provides it via the `onCancelToken()` callback prior to making the visit.

```js Vue icon="vuejs" theme={null}
import { router } from "@inertiajs/vue3";

router.post("/users", data, {
  onCancelToken: (cancelToken) => (this.cancelToken = cancelToken),
});

// Cancel the visit...
this.cancelToken.cancel();
```

```js React icon="react" theme={null}
import { router } from "@inertiajs/react";

router.post("/users", data, {
  onCancelToken: (cancelToken) => (this.cancelToken = cancelToken),
});

// Cancel the visit...
this.cancelToken.cancel();
```

```js Svelte icon="s" theme={null}
import { router } from "@inertiajs/svelte";

router.post("/users", data, {
  onCancelToken: (cancelToken) => (this.cancelToken = cancelToken),
});

// Cancel the visit...
this.cancelToken.cancel();
```

The `onCancel()` and `onFinish()` event callbacks will be executed when a visit is canceled.

## Event Callbacks

In addition to Inertia's [global events](https://inertiajs.com/docs/v3/advanced/events.md), Inertia also provides a number of per-visit event callbacks.

```js Vue icon="vuejs" theme={null}
import { router } from "@inertiajs/vue3";

router.post("/users", data, {
  onBefore: (visit) => {},
  onStart: (visit) => {},
  onProgress: (progress) => {},
  onSuccess: (page) => {},
  onError: (errors) => {},
  onHttpException: (response) => {},
  onNetworkError: (error) => {},
  onCancel: () => {},
  onFinish: (visit) => {},
  onPrefetching: () => {},
  onPrefetched: () => {},
});
```

```js React icon="react" theme={null}
import { router } from "@inertiajs/react";

router.post("/users", data, {
  onBefore: (visit) => {},
  onStart: (visit) => {},
  onProgress: (progress) => {},
  onSuccess: (page) => {},
  onError: (errors) => {},
  onHttpException: (response) => {},
  onNetworkError: (error) => {},
  onCancel: () => {},
  onFinish: (visit) => {},
  onPrefetching: () => {},
  onPrefetched: () => {},
});
```

```js Svelte icon="s" theme={null}
import { router } from "@inertiajs/svelte";

router.post("/users", data, {
  onBefore: (visit) => {},
  onStart: (visit) => {},
  onProgress: (progress) => {},
  onSuccess: (page) => {},
  onError: (errors) => {},
  onHttpException: (response) => {},
  onNetworkError: (error) => {},
  onCancel: () => {},
  onFinish: (visit) => {},
  onPrefetching: () => {},
  onPrefetched: () => {},
});
```

Returning `false` from the `onBefore()` callback will cause the visit to be canceled. Returning `false` from `onHttpException()` or `onNetworkError()` will prevent the corresponding [global event](https://inertiajs.com/docs/v3/advanced/events.md) from being fired and its default behavior.

```js Vue icon="vuejs" theme={null}
import { router } from '@inertiajs/vue3'

router.delete(`/users/${user.id}`, {
    onBefore: () => confirm('Are you sure you want to delete this user?'),
})
```

```js React icon="react" theme={null}
import { router } from '@inertiajs/react'

router.delete(`/users/${user.id}`, {
    onBefore: () => confirm('Are you sure you want to delete this user?'),
})
```

```js Svelte icon="s" theme={null}
import { router } from '@inertiajs/svelte'

router.delete(`/users/${user.id}`, {
    onBefore: () => confirm('Are you sure you want to delete this user?'),
})
```

It's also possible to return a promise from the `onSuccess()` and `onError()` callbacks. When doing so, the "finish" event will be delayed until the promise has resolved.

```js Vue icon="vuejs" theme={null}
import { router } from '@inertiajs/vue3'

router.post(url, {
    onSuccess: () => {
        return Promise.all([
            this.firstTask(),
            this.secondTask()
        ])
    },
    onFinish: visit => {
        // Not called until firstTask() and secondTask() have finished
    },
})
```

```js React icon="react" theme={null}
import { router } from '@inertiajs/react'

router.post(url, {
    onSuccess: () => {
        return Promise.all([
            this.firstTask(),
            this.secondTask()
        ])
    },
    onFinish: visit => {
        // Not called until firstTask() and secondTask() have finished
    },
})
```

```js Svelte icon="s" theme={null}
import { router } from '@inertiajs/svelte'

router.post(url, {
    onSuccess: () => {
        return Promise.all([
            this.firstTask(),
            this.secondTask()
        ])
    },
    onFinish: visit => {
        // Not called until firstTask() and secondTask() have finished
    },
})
```
