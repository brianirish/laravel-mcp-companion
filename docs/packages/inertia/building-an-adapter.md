Source: https://inertiajs.com/docs/v3/advanced/building-an-adapter.md

# Building an Adapter

Inertia speaks plain HTTP and JSON, so you may bring it to any server-side framework by writing an adapter that implements the [Inertia protocol](https://inertiajs.com/docs/v3/core-concepts/the-protocol.md). Before you start, check the [community adapters](https://inertiajs.com/docs/v3/installation/community-adapters.md) to see whether your framework already has one.

This page outlines how an adapter is structured and which practices to follow, while the protocol specifies every header and field mentioned here.

## The Reference Implementation

The official [Laravel adapter](https://github.com/inertiajs/inertia-laravel) is the reference implementation of the protocol, and every example in this documentation uses it. Where the protocol leaves a choice to the server, follow the Laravel adapter unless your framework has a strong reason to differ.

| Concern | Laravel Source |
| :- | :- |
| Rendering responses | [`Response.php`](https://github.com/inertiajs/inertia-laravel/blob/3.x/src/Response.php), [`ResponseFactory.php`](https://github.com/inertiajs/inertia-laravel/blob/3.x/src/ResponseFactory.php) |
| Resolving props | [`PropsResolver.php`](https://github.com/inertiajs/inertia-laravel/blob/3.x/src/PropsResolver.php) |
| Middleware | [`Middleware.php`](https://github.com/inertiajs/inertia-laravel/blob/3.x/src/Middleware.php) |
| Root template | [`View/Components/App.php`](https://github.com/inertiajs/inertia-laravel/blob/3.x/src/View/Components/App.php), [`View/Components/Head.php`](https://github.com/inertiajs/inertia-laravel/blob/3.x/src/View/Components/Head.php) |
| Server-side rendering | [`Ssr/HttpGateway.php`](https://github.com/inertiajs/inertia-laravel/blob/3.x/src/Ssr/HttpGateway.php) |
| Testing helpers | [`Testing/AssertableInertia.php`](https://github.com/inertiajs/inertia-laravel/blob/3.x/src/Testing/AssertableInertia.php) |

The adapter's [test suite](https://github.com/inertiajs/inertia-laravel/tree/3.x/tests) covers edge cases that the protocol describes only briefly, so porting the relevant tests is a quick way to confirm that your adapter behaves the same way.

## The Basics

A basic Inertia application needs a render function, a root template helper, and a middleware from your adapter.

The render function accepts a component name and props, builds the [page object](https://inertiajs.com/docs/v3/core-concepts/the-protocol.md#the-page-object), and returns either an [HTML response](https://inertiajs.com/docs/v3/core-concepts/the-protocol.md#html-responses) or an [Inertia response](https://inertiajs.com/docs/v3/core-concepts/the-protocol.md#inertia-responses). A minimal version looks like this.

```php theme={null}
public function toResponse($request)
{
    $page = [
        'component' => $this->component,
        'props' => array_merge($this->sharedProps, $this->props),
        'url' => $request->getRequestUri(),
        'version' => $this->version,
    ];

    if ($request->header('X-Inertia')) {
        return new JsonResponse($page, 200, ['X-Inertia' => 'true']);
    }

    return view($this->rootView, ['page' => $page]);
}
```

Prop types such as deferred and merge props add their own metadata fields to the page object. You may add those [later](#additional-features).

The root template helper renders the page object script and the root element into the application's layout, like the Laravel adapter's `<x-inertia::app>` and `<x-inertia::head>` Blade components. These helpers also print the output of [server-side rendering](https://inertiajs.com/docs/v3/core-concepts/the-protocol.md#server-side-rendering).

The middleware handles most cross-cutting protocol behavior. The Laravel adapter's [`Middleware::handle()`](https://github.com/inertiajs/inertia-laravel/blob/3.x/src/Middleware.php) method does the following:

* Sets the `Vary: X-Inertia` header on every response.
* Returns a `409` on an [asset version](https://inertiajs.com/docs/v3/core-concepts/the-protocol.md#asset-versioning) mismatch for Inertia `GET` requests.
* Converts a `302` [redirect](https://inertiajs.com/docs/v3/core-concepts/the-protocol.md#redirects) after a `PUT`, `PATCH`, `DELETE`, or `QUERY` request into a `303`.
* Converts a redirect to a URL fragment into an `X-Inertia-Redirect` response.
* Redirects back when a controller returns an empty `200 OK` response.
* Reflashes the session's flash data on redirects and version mismatches.
* Registers [shared data](https://inertiajs.com/docs/v3/data-props/shared-data.md), including the [validation errors](https://inertiajs.com/docs/v3/core-concepts/the-protocol.md#validation-errors) from the session.

Your adapter also needs to handle [partial reloads](https://inertiajs.com/docs/v3/core-concepts/the-protocol.md#partial-reloads). Apply the partial reload filters before invoking any prop closures, so excluded props never run their queries.

### Verifying Your Adapter

Unit tests confirm that your adapter emits the right headers and page objects, but not that the official client accepts them. Build a small application with one of the official client-side adapters and check the following:

1. The first page load renders the page component.
2. Clicking a [`<Link>`](https://inertiajs.com/docs/v3/the-basics/links) swaps the component without a full page reload.
3. Submitting a form with invalid data redirects back and shows the validation errors.
4. A [partial reload](https://inertiajs.com/docs/v3/data-props/partial-reloads.md) returns only the requested props and the `errors` prop.
5. Changing the asset version makes the next visit reload the full page.

For broader coverage, you may port the controllers of the [demo application](https://inertiajs.com/docs/v3/getting-started/demo-application.md) to your framework and run its Vue frontend against your adapter. Its pages cover most of the features in this documentation, including forms, prefetching, deferred props, and error handling.

## Additional Features

Once the basics work, you may add any of the following features.

| Feature | Laravel API | Specification |
| :- | :- | :- |
| Optional and deferred props | `Inertia::optional()`, `Inertia::defer()` | [Deferred and optional props](https://inertiajs.com/docs/v3/core-concepts/the-protocol.md#deferred-and-optional-props) |
| Always props | `Inertia::always()` | [Always props](https://inertiajs.com/docs/v3/core-concepts/the-protocol.md#always-props) |
| Rescued deferred props | `Inertia::defer(..., rescue: true)` | [Rescued deferred props](https://inertiajs.com/docs/v3/core-concepts/the-protocol.md#rescued-deferred-props) |
| Merge props | `Inertia::merge()`, `Inertia::deepMerge()` | [Merging props](https://inertiajs.com/docs/v3/core-concepts/the-protocol.md#merging-props) |
| Once props | `Inertia::once()` | [Once props](https://inertiajs.com/docs/v3/core-concepts/the-protocol.md#once-props) |
| Infinite scroll | `Inertia::scroll()` | [Infinite scroll](https://inertiajs.com/docs/v3/core-concepts/the-protocol.md#infinite-scroll) |
| Live props | `Inertia::live()` | [Live props](https://inertiajs.com/docs/v3/core-concepts/the-protocol.md#live-props) |
| External redirects | `Inertia::location()` | [Redirects](https://inertiajs.com/docs/v3/core-concepts/the-protocol.md#redirects) |
| Flash data | `Inertia::flash()` | [The page object](https://inertiajs.com/docs/v3/core-concepts/the-protocol.md#the-page-object) |
| History encryption | `Inertia::encryptHistory()` | [The page object](https://inertiajs.com/docs/v3/core-concepts/the-protocol.md#the-page-object) |
| Server-side rendering | | [Server-side rendering](https://inertiajs.com/docs/v3/core-concepts/the-protocol.md#server-side-rendering) |
| Big integers | `preserveBigIntegers()` | [The page object](https://inertiajs.com/docs/v3/core-concepts/the-protocol.md#the-page-object) |
| Precognition | | [Request headers](https://inertiajs.com/docs/v3/core-concepts/the-protocol.md#request-headers) |
| Testing helpers | `assertInertia()` | [Testing](https://inertiajs.com/docs/v3/advanced/testing.md#endpoint-tests) |
| DevTools | | [DevTools protocol](https://inertiajs.com/docs/v3/advanced/devtools-protocol.md) |

## Best Practices

### Follow Your Framework's Conventions

Follow your framework's naming, configuration style, and extension points, so a Rails adapter reads like Rails and a Django adapter reads like Django. Keep the concepts close to the Laravel adapter's, such as `render`, `share`, `defer`, and `merge`, so this documentation stays useful to your users.

### Build Both Responses From One Code Path

Build the page object for the HTML document and for the JSON response in one code path. Any difference between the two causes bugs that appear only on the first visit or only after navigation.

### Compose Prop Types

A single prop may be both deferred and mergeable, or once and deferred. Modeling each behavior as an independent flag or trait, rather than as one class per combination, keeps these combinations simple.

### Encode Empty Errors as Objects

Encode the `errors` prop and each error bag as JSON objects, even when they are empty. Languages that use one type for lists and maps, such as PHP, encode an empty one as `[]` by default, but the protocol expects `{}`.

### Render Error Pages Through Inertia

Exceptions such as `404` and `500` errors are often rendered outside your middleware, so they lose shared data. Provide a way to render them as Inertia responses with the middleware's shared data, like the Laravel adapter's [`Inertia::handleExceptionsUsing()`](https://inertiajs.com/docs/v3/advanced/error-handling) method.

### Run Post-Response Work for Client Redirects

A `409` for an external redirect or a fragment redirect is a successful request, because the client completes the navigation. Some frameworks skip post-response work, such as after-response callbacks, for `4xx` statuses, so make sure your adapter still runs it for these responses.

### Document Your Coverage

Users assume that every feature in this documentation works with your adapter. State which Inertia version your adapter targets and which protocol features it implements, and review the [Laravel adapter's releases](https://github.com/inertiajs/inertia-laravel/releases) to keep it current. Once your adapter is ready, you may [list it](https://inertiajs.com/docs/v3/installation/community-adapters.md#listing-your-adapter) on the community adapters page.
