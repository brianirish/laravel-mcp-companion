Source: https://inertiajs.com/docs/v3/advanced/error-handling.md

# Error Handling

## Development

One of the advantages to working with a robust server-side framework is the built-in exception handling you get for free. For example, Laravel ships with a beautiful error reporting tool which displays a nicely formatted stack trace in local development.

The challenge is, if you're making an XHR request (which Inertia does) and you hit a server-side error, you're typically left digging through the network tab in your browser's devtools to diagnose the problem.

Inertia solves this issue by showing all non-Inertia responses in a modal. This means you get the same beautiful error-reporting you're accustomed to, even though you've made that request over XHR.

For applications using a [Content Security Policy](https://developer.mozilla.org/en-US/docs/Web/HTTP/CSP) that restricts inline styles, you may pass a `nonce` to `createInertiaApp()` to permit the inline styles the error modal injects. See [Content Security Policy](https://inertiajs.com/docs/v3/installation/client-side-setup.md#content-security-policy) for details.

## Production

In production you will want to return a proper Inertia error response instead of relying on the modal-driven error reporting that is present during development. To accomplish this, you may use the `Inertia::handleExceptionsUsing()` method in your application's service provider.

```php theme={null}
// app/Providers/AppServiceProvider.php
use Inertia\Inertia;
use Inertia\ExceptionResponse;

public function boot(): void
{
    Inertia::handleExceptionsUsing(function (ExceptionResponse $response) {
        if (in_array($response->statusCode(), [403, 404, 500, 503])) {
            return $response->render('ErrorPage', [
                'status' => $response->statusCode(),
            ])->withSharedData();
        }
    });
}
```

Since exceptions like 404s occur outside of the Inertia middleware (the request never reaches your routes), the error response won't have access to shared data or the root view by default. Calling `withSharedData()` explicitly resolves the Inertia middleware and includes your shared props in the error page.

The `ExceptionResponse` instance provides the `exception`, `request`, and `response` as public readonly properties, along with the following methods:

* `render($component, $props)` - Render an Inertia page component with the given props
* `withSharedData()` - Include shared data from the Inertia middleware
* `usingMiddleware($class)` - Specify which Inertia middleware to use for shared data and root view resolution
* `rootView($view)` - Set a custom root view for the error response
* `statusCode()` - Get the HTTP status code of the original response

The Inertia middleware is auto-resolved from the matched route or the kernel's middleware groups, so `withSharedData()` typically works without specifying a middleware class. Returning `null` from the callback falls through to Laravel's default exception rendering.

### Error Page Example

You'll need to create the error page components referenced above. Here's an example you may use as a starting point.

```vue Vue icon="vuejs" theme={null}
<script setup>
import { computed } from "vue";

const props = defineProps({ status: Number });

const title = computed(() => {
  return {
    503: "503: Service Unavailable",
    500: "500: Server Error",
    404: "404: Page Not Found",
    403: "403: Forbidden",
  }[props.status];
});

const description = computed(() => {
  return {
    503: "Sorry, we are doing some maintenance. Please check back soon.",
    500: "Whoops, something went wrong on our servers.",
    404: "Sorry, the page you are looking for could not be found.",
    403: "Sorry, you are forbidden from accessing this page.",
  }[props.status];
});
</script>

<template>
  <div>
    <h1>{{ title }}</h1>
    <div>{{ description }}</div>
  </div>
</template>
```

```jsx React icon="react" theme={null}
export default function ErrorPage({ status }) {
  const title = {
    503: "503: Service Unavailable",
    500: "500: Server Error",
    404: "404: Page Not Found",
    403: "403: Forbidden",
  }[status];

  const description = {
    503: "Sorry, we are doing some maintenance. Please check back soon.",
    500: "Whoops, something went wrong on our servers.",
    404: "Sorry, the page you are looking for could not be found.",
    403: "Sorry, you are forbidden from accessing this page.",
  }[status];

  return (
    <div>
      <h1>{title}</h1>
      <div>{description}</div>
    </div>
  );
}
```

```svelte Svelte icon="s" theme={null}
<script>
    let { status } = $props()

    const title = {
        503: '503: Service Unavailable',
        500: '500: Server Error',
        404: '404: Page Not Found',
        403: '403: Forbidden',
    }

    const description = {
        503: 'Sorry, we are doing some maintenance. Please check back soon.',
        500: 'Whoops, something went wrong on our servers.',
        404: 'Sorry, the page you are looking for could not be found.',
        403: 'Sorry, you are forbidden from accessing this page.',
    }
</script>

<div>
    <h1>{title[status]}</h1>
    <div>{description[status]}</div>
</div>
```

### Manual Exception Handling

Under the hood, `handleExceptionsUsing()` registers a `$exceptions->respond()` callback in your application's `bootstrap/app.php` file. You may register this callback manually if you prefer.

```php theme={null}
use Illuminate\Http\Request;
use Symfony\Component\HttpFoundation\Response;
use Inertia\Inertia;

->withExceptions(function (Exceptions $exceptions) {
    $exceptions->respond(function (Response $response, Throwable $exception, Request $request) {
        if (! app()->environment(['local', 'testing']) && in_array($response->getStatusCode(), [500, 503, 404, 403])) {
            return Inertia::render('ErrorPage', ['status' => $response->getStatusCode()])
                ->toResponse($request)
                ->setStatusCode($response->getStatusCode());
        }

        return $response;
    });
})
```
