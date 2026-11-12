Source: https://inertiajs.com/docs/v3/core-concepts/the-protocol.md

# The Protocol

This page specifies the Inertia protocol, which defines the requests and responses exchanged between the Inertia client and your server. The [how it works](https://inertiajs.com/docs/v3/core-concepts/how-it-works.md) page gives a high-level overview.

The protocol is framework-agnostic, so any backend that speaks HTTP may implement it. The official Laravel adapter is the reference implementation, and the requests and responses on this page show its output. Placeholders such as `...` and comments shorten the longer examples. The [building an adapter](https://inertiajs.com/docs/v3/advanced/building-an-adapter.md) guide explains how to structure an implementation around this specification.

## Request Lifecycle Diagram

The following diagram shows the request lifecycle of an Inertia application. The first visit is a standard request, and the server returns an HTML document with a root element and a script element that holds the page object. With SSR enabled, the root element also contains server-rendered markup, which the client hydrates. Later visits are XHR requests that return JSON, and Inertia swaps the page component without a full-page reload.

```mermaid theme={null}
sequenceDiagram
    participant Client
    participant Server

    Client->>Server: First Visit
    Server-->>Client: Returns HTML Skeleton

    Note over Client: Inertia.js is loaded

    Client->>Server: Inertia Request (X-Inertia: true)
    Server-->>Client: Returns the page object as JSON

    Note over Client: Inertia.js swaps components
```

## HTML Responses

The first request to an Inertia app is a regular full-page browser request, with no Inertia headers. The server answers it with a complete HTML document.

The document loads the site's CSS and JavaScript and contains a root `<div>`, where the client-side app mounts. A `<script type="application/json">` element holds the JSON-encoded [page object](#the-page-object) for the initial page. The script's `data-page` attribute matches the root element's `id`. Inertia reads the page object from this script, boots your client-side framework, and renders the initial page component. Earlier Inertia versions stored the page object in a `data-page` attribute on the root `<div>`. The current client does not read that attribute.

```http theme={null}
REQUEST
GET: https://example.com/events/80
Accept: text/html, application/xhtml+xml

RESPONSE
HTTP/1.1 200 OK
Content-Type: text/html; charset=utf-8

<html>
    <head>
        <title>My app</title>
        <link href="/css/app.css" rel="stylesheet">
        <script src="/js/app.js" defer></script>
    </head>
    <body>
        <script data-page="app" type="application/json">{"component":"Event","props":{"errors":{},"event":{"id":80,"title":"Birthday party","start_date":"2019-06-02","description":"Come out and celebrate Jonathan's 36th birthday party!"}},"url":"\/events\/80","version":"c32b8e4965f418ad16eaebba1d4e960f"}</script>
        <div id="app"></div>
    </body>
</html>
```

> [!WARNING]
>
> The serialized page object must not contain a literal `</script>` sequence, since it closes the script element early and breaks the page. Escaping forward slashes (`/` becomes `\/`) or the `<` character (`<` becomes `\u003C`) prevents this. The Laravel adapter escapes both, so the example above contains `"\/events\/80"`. The server must not use HTML-entity encoding here either, because the browser does not decode entities inside a script element and JSON parsing fails.

## Inertia Responses

After the app boots, Inertia makes every later request with XHR and sets the `X-Inertia` header to `true`. The header marks the request as an Inertia visit rather than a full-page visit.

The server detects the `X-Inertia` header and returns the [page object](#the-page-object) as JSON instead of an HTML document.

```http theme={null}
REQUEST
GET: https://example.com/events/80
Accept: text/html, application/xhtml+xml
X-Requested-With: XMLHttpRequest
X-Inertia: true
X-Inertia-Version: 6b16b94d7c51cbe5b1fa42aac98241d5

RESPONSE
HTTP/1.1 200 OK
Content-Type: application/json
Vary: X-Inertia
X-Inertia: true

{
    "component": "Event",
    "props": {
        "errors": {},
        "event": {
            "id": 80,
            "title": "Birthday party",
            "start_date": "2019-06-02",
            "description": "Come out and celebrate Jonathan's 36th birthday party!"
        }
    },
    "url": "/events/80",
    "version": "6b16b94d7c51cbe5b1fa42aac98241d5",
    "encryptHistory": true
}
```

## How the Client Handles Responses

The client inspects each response before it changes the page, and handles it as follows:

* **An Inertia response (`X-Inertia: true`)**: the client applies the page object and swaps the component.
* **A `409 Conflict` with `X-Inertia-Location`**: the client makes a full `window.location` visit to that URL, which loads fresh assets. A background request skips this visit when the asset version changed, because a reload the user did not start would discard unsaved state.
* **A `409 Conflict` with `X-Inertia-Redirect`**: the client makes a new Inertia `GET` visit to that URL.
* **Any other response**, such as an HTML document, plain JSON, or an error page: the client treats it as an exception. It fires a cancelable HTTP exception event and shows an error modal unless a listener cancels the event.

Standard `3xx` redirects never reach these rules. The browser follows them and sends the same request headers to the new location. `X-Inertia` therefore reaches the redirect target, and the client inspects only the final response in the chain. The [redirects](#redirects) section lists the statuses a server returns to control this.

An Inertia response with a status of `400` or greater fires the same cancelable HTTP exception event before the client renders it. Canceling the event stops the render, so the application may handle the failure itself.

## Request Headers

The Inertia client sends the following request headers.

**X-Inertia** `boolean`

Set to `true` on every Inertia request.

**X-Requested-With** `string`

Set to `XMLHttpRequest` on all Inertia requests.

**Accept** `string`

Set to `text/html, application/xhtml+xml`.

**Content-Type** `string`

Set to `application/json` for requests with a JSON body. Requests without a
body, such as `GET` requests, omit it.

**X-Inertia-Version** `string`

The asset version of the current page. The client omits the header when the
version is an empty string.

**X-XSRF-TOKEN** `string`

The CSRF token read from the `XSRF-TOKEN` cookie. The cookie and header names
are configurable.

**Purpose** `string`

Set to `prefetch` on [prefetch](https://inertiajs.com/docs/v3/data-props/prefetching.md) requests.

**X-Inertia-Partial-Component** `string`

The component name for [partial reloads](https://inertiajs.com/docs/v3/data-props/partial-reloads.md).

**X-Inertia-Partial-Data** `string`

Comma-separated list of props to include in a partial reload.

**X-Inertia-Partial-Except** `string`

Comma-separated list of props to exclude from a partial reload.

**X-Inertia-Reset** `string`

Comma-separated list of props to [reset](#resetting-props).

**Cache-Control** `string`

Set to `no-cache` on reload requests, so caches do not serve stale content.

**X-Inertia-Error-Bag** `string`

The name of the error bag for [validation errors](#validation-errors).

**X-Inertia-Infinite-Scroll-Merge-Intent** `string`

Whether the client appends or prepends the requested page of an
[infinite scroll](https://inertiajs.com/docs/v3/data-props/infinite-scroll.md) prop.

**X-Socket-Id** `string`

The broadcaster's connection id, sent on same-origin requests once the
application configures [live props](#live-props) or a [custom socket
ID](https://inertiajs.com/docs/v3/data-props/live-props.md#skipping-the-current-connection) resolver. The server may use it to
skip broadcasting back to the connection that caused the change.

**X-Inertia-Except-Once-Props** `string`

Comma-separated list of the [once prop](#once-props) keys that the client
has loaded and that have not expired. The server skips these props unless a
partial reload requests them or the server refreshes them.

[Precognition](https://inertiajs.com/docs/v3/the-basics/forms.md#precognition) validation requests use the following headers.

**Precognition** `boolean`

Set to `true` on a Precognition validation request.

**Precognition-Validate-Only** `string`

Comma-separated list of field names to validate.

## Response Headers

The server sets the following headers on an Inertia JSON response.

**X-Inertia** `boolean`

Set to `true` on an Inertia response.

**Vary** `string`

Set to `X-Inertia`, so browsers and caches keep the HTML response and the
JSON response for one URL apart.

The following headers appear on `409 Conflict` control responses. A `409` response tells the client to navigate rather than render a page, so it carries no `X-Inertia` header.

**X-Inertia-Location** `string`

The destination URL for a full `window.location` visit. Set on an external
redirect and on an asset version mismatch.

**X-Inertia-Redirect** `string`

The full redirect URL, including its fragment, for a redirect whose target
contains a URL fragment. The client makes a new Inertia `GET` visit instead of
a full-page reload.

**X-Inertia-Version** `string`

The server's current asset version, set on a version mismatch `409`.

[Precognition](https://inertiajs.com/docs/v3/the-basics/forms.md#precognition) validation responses use the following headers.

**Precognition** `string`

Set to `true` on a Precognition validation response.

**Precognition-Success** `string`

Set to `true`, with a `204 No Content` status, when validation passes.

**Vary** `string`

Set to `Precognition` on every response that passes through the Precognition
middleware.

## The Page Object

The server and the client exchange data through the page object. The page object holds what the client needs to render the page component, update the browser's history state, and track the site's asset version. It may contain the following properties.

**component** `string`

The name of the JavaScript page component.

**props** `object`

The page props. Usually includes an [`errors`](#validation-errors) object.

**url** `string`

The page URL.

**version** `string`

The current [asset version](https://inertiajs.com/docs/v3/advanced/asset-versioning.md).

**encryptHistory** `boolean`

Whether the client [encrypts the page's history
state](https://inertiajs.com/docs/v3/security/history-encryption.md). Included only when `true`.

**clearHistory** `boolean`

Whether the client [clears encrypted history
state](https://inertiajs.com/docs/v3/security/history-encryption.md#clearing-history). Included only when `true`.

**preserveBigIntegers** `boolean`

Whether the props wrap integers outside JavaScript's safe range as `{"$bigint": "<digits>"}` markers. The client turns each marker into a [`BigInt` value](https://inertiajs.com/docs/v3/advanced/big-integers). Included only when `true`.

**preserveFragment** `boolean`

Whether the client [keeps the URL fragment](https://inertiajs.com/docs/v3/the-basics/redirects.md#preserving-fragments) of the original request after a redirect. Included only when `true`.

**mergeProps** `array`

Prop keys whose new values the client [appends](https://inertiajs.com/docs/v3/data-props/merging-props.md)
to the existing values.

**prependProps** `array`

Prop keys whose new values the client [prepends](https://inertiajs.com/docs/v3/data-props/merging-props.md)
to the existing values.

**deepMergeProps** `array`

Prop keys whose new values the client [deep
merges](https://inertiajs.com/docs/v3/data-props/merging-props.md#deep-merge) into the existing values.

**matchPropsOn** `array`

The fields that identify items when the client [merges
props](#matching-items).

**scrollProps** `object`

The pagination state of each [infinite scroll](#infinite-scroll) prop.

**deferredProps** `object`

The [deferred props](#deferred-and-optional-props) that the client loads in
follow-up requests, grouped by request group.

**rescuedProps** `array`

The keys of [deferred props](#rescued-deferred-props) that threw and that
the server rescued. The client renders the `rescue` slot of the `<Deferred>`
component for these props.

**sharedProps** `array`

The top-level keys of the [shared props](https://inertiajs.com/docs/v3/data-props/shared-data.md). The
client carries these props over during [instant
visits](https://inertiajs.com/docs/v3/the-basics/instant-visits.md).

**onceProps** `object`

The [once props](#once-props) of the page. Each entry maps a key to an object
with the `prop` name and an `expiresAt` timestamp in milliseconds, or `null`
for no expiry.

**liveProps** `object`

The [live props](#live-props) of the page. Each entry maps a prop path to the
channels and events that refresh it, and an optional `throttle` in
milliseconds.

**flash** `object`

The flash data for the current request. Included only when flash data
exists. The client exposes it through the `inertia:flash` event and leaves it
out of the saved history state.

Every page object contains `component`, `props`, `url`, and `version`. A minimal page object looks like this.

```json theme={null}
{
  "component": "User/Edit",
  "props": {
    "errors": {},
    "user": {
      "name": "Jonathan"
    }
  },
  "url": "/user/123",
  "version": "6b16b94d7c51cbe5b1fa42aac98241d5"
}
```

The server emits the other fields only when they apply. The client reads a missing field as an empty array, an empty object, or `false`. A server may therefore omit an empty field or send it, with the same result.

## Prop Evaluation Model

Every prop belongs to one or more categories. The category decides whether the server resolves the prop for a request, and which metadata fields describe it. These rules apply only on the server. The client applies whatever metadata it receives.

Resolution differs between the two request modes. A full visit resolves every eligible prop. A partial reload resolves only the props that the client requests for the same page component.

**Full visit**

| Prop category | Resolved? | Metadata emitted |
| :- | :- | :- |
| Regular | Yes | none |
| Always | Yes, ignoring `only` and `except` | none |
| Optional | No, and not announced | none |
| Deferred | No, but announced | `deferredProps` |
| Merge, deep merge, prepend | Yes | `mergeProps`, `deepMergeProps`, `prependProps`, `matchPropsOn` |
| Once | Yes, unless already remembered by client | `onceProps` |
| Scroll | Yes | `scrollProps`, `mergeProps` |
| Live | Yes | `liveProps` |

**Partial reload**

| Prop category | Resolved? | Metadata emitted |
| :- | :- | :- |
| Regular | Only when `only` or `except` selects it | none |
| Always | Yes, ignoring `only` and `except` | none |
| Optional | Only when `only` or `except` selects it | none |
| Deferred | Only when `only` or `except` selects it | `rescuedProps`, when rescued |
| Merge, deep merge, prepend | When resolved | `mergeProps`, `deepMergeProps`, `prependProps`, `matchPropsOn` |
| Once | When requested, ignoring except-once | `onceProps` |
| Scroll | When resolved | `scrollProps`, `mergeProps` |
| Live | When resolved | `liveProps` |

Some metadata fields depend on the mode:

* `deferredProps` appears only on full visits. Deferred props resolve in the follow-up partial reload, so `deferredProps` is empty or absent there.
* `rescuedProps` appears only on partial reloads. It lists the deferred props that failed to resolve.
* Merge, scroll, once, and live metadata appears on each response that contains props with those behaviors, so a partial reload keeps the live listeners of the props it refreshes up to date.

### Always Props

The server resolves always props on every response in both modes. Always props ignore the partial reload filters, so the server sends an always prop even when the request lists it in `except`. Always props carry no metadata. The Laravel adapter's middleware shares `errors` as an always prop, so its page objects include an `errors` object unless a page prop overrides it.

### Composing Categories

A prop may belong to several categories, such as deferred and mergeable, once and deferred, or scroll and deferred. The metadata fields are independent. The page object carries every label that applies, subject to the mode, the partial reload filters, and the reset rules.

## Partial Reloads

A partial reload requests a subset of the props on a later visit to the same page component. The [partial reloads](https://inertiajs.com/docs/v3/data-props/partial-reloads.md) page covers the client-side API.

A partial reload request carries the `X-Inertia-Partial-Component` header. It may also carry `X-Inertia-Partial-Data`, `X-Inertia-Partial-Except`, or both.

* `X-Inertia-Partial-Data` lists the prop keys to return.
* `X-Inertia-Partial-Except` lists the prop keys to leave out. Sent alone, it returns every prop except the listed ones.
* With both headers, the server first narrows the response to the `X-Inertia-Partial-Data` list, then removes the `X-Inertia-Partial-Except` list. A prop named in both headers is left out.

Entries in both headers may be dot-notated paths, such as `auth.user`, which select or exclude a nested prop. The Laravel adapter applies nested paths only inside plain arrays, and returns a prop that a closure resolves in full.

`X-Inertia-Partial-Component` holds the name of the page component being reloaded. Partial reloads apply only to the same page component. The server resolves a request that ends on a different component as a full visit. A login page after the session expired is a common example.

```http theme={null}
REQUEST
GET: https://example.com/events
Accept: text/html, application/xhtml+xml
X-Requested-With: XMLHttpRequest
X-Inertia: true
X-Inertia-Version: 6b16b94d7c51cbe5b1fa42aac98241d5
X-Inertia-Partial-Data: events
X-Inertia-Partial-Component: Events

RESPONSE
HTTP/1.1 200 OK
Content-Type: application/json

{
    "component": "Events",
    "props": {
        "events": [...], // the requested prop
        "errors": {}     // always included
    },
    "url": "/events",
    "version": "6b16b94d7c51cbe5b1fa42aac98241d5"
}
```

### Resetting Props

The `X-Inertia-Reset` header lists the prop paths that the client resets before it applies new data. The client sends each reset path in both `X-Inertia-Reset` and `X-Inertia-Partial-Data`. The server resolves a reset prop again and returns it in `props` without a merge label, so the client replaces the value instead of merging it. For a scroll prop, the server also sets `scrollProps[path].reset`. The [infinite scroll](https://inertiajs.com/docs/v3/data-props/infinite-scroll.md) component then resets its pagination state to the returned page. The [resetting props](https://inertiajs.com/docs/v3/data-props/merging-props.md#resetting-props) section covers the client-side API.

## Deferred and Optional Props

A deferred prop is data that the client loads in a follow-up request. On a full visit, the server skips the prop and lists its key under `deferredProps`, grouped by request group. Group names are arbitrary, and the client sends one partial reload per group. See the [deferred props](https://inertiajs.com/docs/v3/data-props/deferred-props.md) documentation for the server and client APIs.

```json theme={null}
{
  "component": "Posts/Index",
  "props": {
    "errors": {},
    "user": {
      "name": "Jonathan"
    }
  },
  "url": "/posts",
  "version": "6b16b94d7c51cbe5b1fa42aac98241d5",
  "deferredProps": {
    "default": ["comments", "analytics"],
    "sidebar": ["relatedPosts"]
  }
}
```

Optional props are never announced. The server skips them on full visits and resolves them only when a partial reload selects them with `only` or `except`.

### Rescued Deferred Props

A rescued deferred prop that throws does not fail the response, which is still a `200` with every other prop. The server reports the exception through the framework's error handling and leaves the prop out of `props` entirely, rather than sending it as `null`. Instead, it adds the key to the top-level `rescuedProps` array, and the client renders the `rescue` slot of the `<Deferred>` component for it. The deferred props [error handling](https://inertiajs.com/docs/v3/data-props/deferred-props.md#error-handling) documentation covers the server and client APIs.

```json theme={null}
{
  "component": "Users/Index",
  "props": {
    "errors": {}
  },
  "url": "/users",
  "version": "6b16b94d7c51cbe5b1fa42aac98241d5",
  "rescuedProps": ["permissions"]
}
```

## Merging Props

A merge prop tells the client to combine new data with the data already on the page instead of replacing it. The client appends or prepends arrays and merges objects, either shallowly or deeply. The page object labels each merge prop under `mergeProps` to append, `prependProps` to prepend, or `deepMergeProps` to deep merge. The client merges only on partial reloads, so a full visit replaces the prop even when it carries a merge label. See the [merging props](https://inertiajs.com/docs/v3/data-props/merging-props.md) documentation for more details.

```json theme={null}
{
  "component": "Feed/Index",
  "props": {
    "errors": {},
    "user": {
      "name": "Jonathan"
    },
    "posts": [
      {
        "id": 1,
        "title": "First Post"
      }
    ],
    "notifications": [
      {
        "id": 2,
        "message": "New comment"
      }
    ],
    "conversations": {
      "data": [
        {
          "id": 1,
          "title": "Support Chat",
          "participants": ["John", "Jane"]
        }
      ]
    }
  },
  "url": "/feed",
  "version": "6b16b94d7c51cbe5b1fa42aac98241d5",
  "mergeProps": ["posts"],
  "prependProps": ["notifications"],
  "deepMergeProps": ["conversations"],
  "matchPropsOn": ["posts.id", "notifications.id", "conversations.data.id"]
}
```

### Matching Items

The `matchPropsOn` array names the field that identifies each item. The client uses that field to update an existing item in place instead of adding a duplicate. Each entry has the form `"<propPath>.<keyField>"`, and the client splits it at the last dot. The text before the last dot is the prop path, and the final segment is the key field. For example, `conversations.data.id` matches items of the array at `conversations.data` by their `id` field. The [matching items](https://inertiajs.com/docs/v3/data-props/merging-props.md#matching-items) section covers the server-side API.

## Once Props

The server resolves a once prop on its first use. The client remembers the value and reuses it on later pages that include the same prop, until the value expires or the server refreshes it. The page object carries an `onceProps` object. Each entry maps a key to the prop name and an expiration timestamp in milliseconds, or `null` for no expiry. The [once props](https://inertiajs.com/docs/v3/data-props/once-props.md) page covers the server and client APIs.

```json theme={null}
{
  "component": "Billing/Plans",
  "props": {
    "errors": {},
    "plans": [
      {
        "id": 1,
        "name": "Basic"
      },
      {
        "id": 2,
        "name": "Pro"
      }
    ]
  },
  "url": "/billing/plans",
  "version": "6b16b94d7c51cbe5b1fa42aac98241d5",
  "onceProps": {
    "plans": {
      "prop": "plans",
      "expiresAt": null
    }
  }
}
```

On later Inertia requests, the client sends the keys of loaded once props that have not expired in the `X-Inertia-Except-Once-Props` header. The server skips those props and leaves them out of the response, except in the cases that [force-fresh and partial reloads](#force-fresh-and-partial-reloads) describes. The client reuses the values it already has.

```http theme={null}
REQUEST
GET: https://example.com/billing/upgrade
Accept: text/html, application/xhtml+xml
X-Requested-With: XMLHttpRequest
X-Inertia: true
X-Inertia-Version: 6b16b94d7c51cbe5b1fa42aac98241d5
X-Inertia-Except-Once-Props: plans

RESPONSE
HTTP/1.1 200 OK
Content-Type: application/json

{
    "component": "Billing/Upgrade",
    "props": {
        "errors": {},
        "currentPlan": {
            "id": 1,
            "name": "Basic"
        }
    },
    "url": "/billing/upgrade",
    "version": "6b16b94d7c51cbe5b1fa42aac98241d5",
    "onceProps": {
        "plans": {
            "prop": "plans",
            "expiresAt": null
        }
    }
}
```

The response lists `plans` in `onceProps` but not in `props`, because the client already has the value. The `onceProps` key identifies the once prop across pages, and `prop` holds the prop name. The two differ when the application uses [custom keys](https://inertiajs.com/docs/v3/data-props/once-props.md#custom-keys).

### Force-Fresh and Partial Reloads

The server may send a new value for a once prop even when `X-Inertia-Except-Once-Props` lists its key, for example after the underlying data changes. The new value and its `expiresAt` replace the client's copy. The server ignores the except-once header on a partial reload, so it always resolves a requested once prop.

## Live Props

A live prop refreshes itself whenever a broadcast event arrives. The page object carries a `liveProps` entry for each live prop, listing the channels it listens on, the events broadcast on each channel, and an optional `throttle` in milliseconds. Channel names are unprefixed and carry their type separately, so the client applies whichever prefix its broadcaster expects. The [live props](https://inertiajs.com/docs/v3/data-props/live-props.md) page covers the server and client APIs.

```json theme={null}
{
  "component": "Orders/Show",
  "props": {
    "errors": {},
    "order": {
      "id": 1,
      "status": "shipped"
    }
  },
  "url": "/orders/1",
  "version": "6b16b94d7c51cbe5b1fa42aac98241d5",
  "liveProps": {
    "order": {
      "listeners": [
        {
          "channel": { "name": "orders.1", "type": "private" },
          "events": ["App\\Events\\OrderUpdated"]
        }
      ],
      "throttle": 5000
    }
  }
}
```

An incoming event refreshes the props that listen for it with a regular partial reload, so the client receives whatever the server resolves at that moment. An event may instead carry new values under an `__inertia.props` key in its payload, keyed by prop path, and the client writes them into the page without a request. The client ignores values for props that don't listen for the event. It also sends the broadcaster's connection id in the `X-Socket-Id` header, so the server may exclude the connection that caused the change.

## Infinite Scroll

Infinite scroll builds on merge props. The server labels the prop's inner array for merging, usually at `<path>.data`, and the page object carries a `scrollProps` entry that describes the pagination state. See the [infinite scroll](https://inertiajs.com/docs/v3/data-props/infinite-scroll.md) documentation for the server and client APIs.

```json theme={null}
{
  "component": "Posts/Index",
  "props": {
    "errors": {},
    "posts": {
      "data": [
        {
          "id": 1,
          "title": "First Post"
        },
        {
          "id": 2,
          "title": "Second Post"
        }
      ]
    }
  },
  "url": "/posts?page=1",
  "version": "6b16b94d7c51cbe5b1fa42aac98241d5",
  "mergeProps": ["posts.data"],
  "scrollProps": {
    "posts": {
      "pageName": "page",
      "previousPage": null,
      "nextPage": 2,
      "currentPage": 1,
      "reset": false
    }
  }
}
```

Every scroll response repeats the merge label and sends the current pagination state. On a reset request, the server also sets `scrollProps[path].reset` to `true`, and the client resets its pagination state to the returned page. A deferred scroll prop emits no `scrollProps` on the full visit, because it resolves in the follow-up request.

## Asset Versioning

The `version` field of the page object identifies the current version of the site's assets. It may be any string that changes when the assets change, such as a file hash. A server that does not track asset versions sends an empty string. The client sends a non-empty version back in the `X-Inertia-Version` header. The server compares the two values, usually in middleware, and treats a missing header as an empty string.

Matching versions let the request continue. On a `GET` request with a mismatch, the server returns a `409 Conflict`. The `X-Inertia-Location` header holds the full URL of the request, and `X-Inertia-Version` holds the server's current version. For a visit the user started, the client then makes a full-page visit to that URL, which follows any server-side redirect to the final page. For a background request, the client keeps the current page, as described in [how the client handles responses](#how-the-client-handles-responses). A non-`GET` request never receives a mismatch `409`, but the `GET` redirect that follows it may. On a version mismatch, the server also keeps the session's flash data for the next request.

```http theme={null}
REQUEST
GET: https://example.com/events/80
Accept: text/html, application/xhtml+xml
X-Requested-With: XMLHttpRequest
X-Inertia: true
X-Inertia-Version: 6b16b94d7c51cbe5b1fa42aac98241d5

RESPONSE
409: Conflict
X-Inertia-Location: https://example.com/events/80
X-Inertia-Version: 2f8a1c9e4b7d0a3f6c5e8b1d4a7f0c2e
```

The [asset versioning](https://inertiajs.com/docs/v3/advanced/asset-versioning.md) page covers how to configure the version and how the client handles background requests.

## Redirects

Inertia uses standard HTTP redirects for navigation after a server-side action. The server converts a `302 Found` after a `PUT`, `PATCH`, `DELETE`, or `QUERY` request into a `303 See Other`. The browser then requests the redirect target with `GET` instead of repeating the original method.

An external redirect points outside the Inertia app, where the Inertia request headers do not carry over, so an XHR visit may not follow it. The server returns a `409 Conflict` with an `X-Inertia-Location` header instead, and the client makes a full `window.location` visit.

For a redirect whose target contains a URL fragment, the server returns a `409 Conflict` with the full URL in an `X-Inertia-Redirect` header, and the client makes a new Inertia `GET` visit to that URL. Prefetch requests are the exception and receive the redirect unchanged. This is separate from the `preserveFragment` page object field, which keeps the fragment of the original request after an ordinary redirect. The [redirects](https://inertiajs.com/docs/v3/the-basics/redirects.md) page covers the server-side API.

## Validation Errors

The server sends validation errors in the `errors` prop. The Laravel adapter's middleware registers `errors` as an always prop. Every page object rendered through the middleware therefore contains `errors`, unless a page prop overrides it. The value is `{}` when there are no errors. The client treats a missing `errors` prop as an empty object.

Each key maps to either a single message or an array of messages, and the client renders the shape it receives. The Laravel adapter sends the first message per field by default and may be [configured](https://inertiajs.com/docs/v3/the-basics/validation.md#multiple-errors-per-field) to send all messages.

A request may name an error bag in the `X-Inertia-Error-Bag` header, so multiple forms on one page keep their errors apart. The Laravel adapter handles error bags by these rules:

* A request with the `X-Inertia-Error-Bag` header receives the default bag's errors under the requested name.
* A request without the header receives the default bag unwrapped.
* Named bags appear under their own names only when no default bag exists, with or without the header.

The [validation](https://inertiajs.com/docs/v3/the-basics/validation.md) page covers the client-side API.

## HTTP Status Codes

Inertia uses the following HTTP status codes.

| Status Code | Description |
| :- | :- |
| **200 OK** | The successful response, for both HTML and Inertia JSON responses. |
| **302 Found** | The standard redirect response. |
| **303 See Other** | Replaces a `302` redirect after a `PUT`, `PATCH`, `DELETE`, or `QUERY` request. The browser follows it with a `GET`. See [redirects](#redirects). |
| **409 Conflict** | A control response instead of a page, for an [asset version mismatch](#asset-versioning), an external redirect, or a fragment redirect. See [redirects](#redirects). |

[Precognition](https://inertiajs.com/docs/v3/the-basics/forms.md#precognition) validation requests use the following status codes.

| Status Code | Description |
| :- | :- |
| **204 No Content** | The validation passed. |
| **422 Unprocessable Entity** | The validation failed. The response body contains the errors. |

## Server-Side Rendering

Inertia does not render page components on the server by default. [SSR](https://inertiajs.com/docs/v3/advanced/server-side-rendering.md) adds a second contract, between the server-side adapter and Inertia's Node SSR server. The adapter sends the page object to the SSR server in a `POST` request, and the SSR server returns the rendered markup for the HTML document.

```http theme={null}
REQUEST
POST: http://127.0.0.1:13714/render
Content-Type: application/json

{"component":"Event","props":{"errors":{},"event":{"id":80,"title":"Birthday party"}},"url":"/events/80","version":"c32b8e4965f418ad16eaebba1d4e960f"}

RESPONSE
HTTP/1.1 200 OK
Content-Type: application/json
Server: Inertia.js SSR

{"head":["<title>Birthday party</title>"],"body":"<script data-page=\"app\" type=\"application/json\">{\"component\":\"Event\",...}</script><div data-server-rendered=\"true\" id=\"app\"><h1>Birthday party</h1></div>"}
```

The response fills the two slots of the root template. The Laravel adapter provides these slots as the `<x-inertia::head>` and `<x-inertia::app>` Blade components. The `head` array holds the elements for the document's `<head>`, such as the title and meta tags. The `body` string replaces the page object script and the root `<div>` of a document rendered without SSR, because the SSR markup already contains both. Its root element carries `data-server-rendered="true"`, so the client hydrates the existing DOM instead of mounting a new app. The SSR server escapes the embedded page object, so the adapter prints the `body` markup unchanged.

During development, the [Vite plugin](https://inertiajs.com/docs/v3/advanced/server-side-rendering.md#development-mode) accepts the same render request at a `/__inertia_ssr` endpoint on the Vite dev server, so no separate Node process runs. The plugin registers the endpoint only when it finds an SSR entry point. The Laravel adapter sends its render requests there while Vite runs in hot mode.

The SSR server has two more endpoints. A `GET` request to `/health` returns `{"status":"OK","timestamp":...}`. An adapter may call it to check that the process runs before it sends a render. A request to `/shutdown` stops the process. The Laravel adapter's `inertia:stop-ssr` command uses this endpoint.

Error formatting is enabled by default. With it enabled, a failed render returns a `500` response with a JSON body that classifies the error.

```json theme={null}
{
  "error": "window is not defined",
  "type": "browser-api",
  "component": "Events/Show",
  "url": "/events/80",
  "browserApi": "window",
  "hint": "The global window object doesn't exist in Node.js. Wrap browser-specific code in a lifecycle hook...",
  "stack": "ReferenceError: window is not defined\n    at ...",
  "sourceLocation": "resources/js/Pages/Events/Show.vue:14:3",
  "timestamp": "2026-03-14T09:21:44.512Z"
}
```

The response always contains `error`, `hint`, and `timestamp`. It contains `component`, `url`, `stack`, and `sourceLocation` when the SSR server can determine them. The `type` field names the cause:

* `browser-api`: the render used a browser global. `browserApi` names the global.
* `component-resolution`: the SSR server could not resolve the page component.
* `render`: a component threw any other error.

A failed render is not fatal to the request. The adapter reports the error through the application's error handling and returns the document without SSR markup. A broken SSR build therefore does not take the site down. The Laravel adapter throws an exception instead when its `inertia.ssr.throw_on_error` option is enabled, which is useful in end-to-end tests. The Laravel adapter dispatches an [`SsrRenderFailed` event](https://inertiajs.com/docs/v3/advanced/server-side-rendering#error-handling). It also reports a `connection` type when it cannot reach the SSR server.
