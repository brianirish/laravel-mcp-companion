Source: https://inertiajs.com/docs/v3/security/csrf-protection.md

# CSRF Protection

## Making Requests

Laravel automatically includes the proper CSRF token when making requests via Inertia or Axios. However, if you're using Laravel, be sure to omit the `csrf-token` meta tag from your project, as this will prevent the CSRF token from refreshing properly.

Server-side frameworks with cross-site request forgery (CSRF) protection require each Inertia `POST`, `PUT`, `PATCH`, `DELETE`, and `QUERY` request to include a CSRF token.

Some server-side frameworks, such as Laravel, automatically include the CSRF token when making requests. No additional configuration is required when using these frameworks.

However, if you need to handle CSRF protection manually, one approach is to include the CSRF token as a prop on every response. You can then use the token when making Inertia requests.

```js Vue icon="vuejs" theme={null}
import { router, usePage } from "@inertiajs/vue3";

const page = usePage();

router.post("/users", {
  _token: page.props.csrf_token,
  name: "John Doe",
  email: "john.doe@example.com",
});
```

```js React icon="react" theme={null}
import { router, usePage } from "@inertiajs/react";

const props = usePage().props;

router.post("/users", {
  _token: props.csrf_token,
  name: "John Doe",
  email: "john.doe@example.com",
});
```

```js Svelte icon="s" theme={null}
import { page, router } from "@inertiajs/svelte";

router.post("/users", {
  _token: page.props.csrf_token,
  name: "John Doe",
  email: "john.doe@example.com",
});
```

You can even use Inertia's [shared data](https://inertiajs.com/docs/v3/data-props/shared-data.md) functionality to automatically include the `csrf_token` with each response.

A better approach is to use Inertia's built-in XSRF token handling. Inertia's HTTP client automatically checks for the existence of an `XSRF-TOKEN` cookie and, when present, includes the token in an `X-XSRF-TOKEN` header for every request it makes.

The easiest way to implement this is using server-side middleware. Simply include the `XSRF-TOKEN` cookie on each response, and then verify the token using the `X-XSRF-TOKEN` header sent in the requests from Inertia.

You may customize the cookie and header names via the `http` option in `createInertiaApp`.

```js theme={null}
createInertiaApp({
  http: {
    xsrfCookieName: 'MY-XSRF-TOKEN',
    xsrfHeaderName: 'X-MY-XSRF-TOKEN',
  },
  // ...
})
```

## Handling Mismatches

When a CSRF token mismatch occurs, your server-side framework will likely throw an exception that results in an error response. For example, Laravel throws a `TokenMismatchException`, which results in a `419` error page. Since that isn't a valid Inertia response, the error is shown in a modal.

<video controls src="https://mintcdn.com/inertiajs/X4AKX_y_0pX0Y95-/mp4/csrf-mismatch-modal.mp4?fit=max&auto=format&n=X4AKX_y_0pX0Y95-&q=85&s=25545a6fdb2bc79216314e656dddcad6" />

Obviously, this isn't a great user experience. A better way to handle these errors is to return a redirect back to the previous page, along with a flash message that the page expired. This will result in a valid Inertia response with the flash message available as a prop which you can then display to the user. Of course, you'll need to share your [flash messages](https://inertiajs.com/docs/shared-data.md#flash-messages) with Inertia for this to work.

When using Laravel, you may modify your application's exception handler to automatically redirect the user back to the page they were previously on while flashing a message to the session. To accomplish this, you may use the `respond` exception method in your application's `bootstrap/app.php` file.

```php theme={null}
use Symfony\Component\HttpFoundation\Response;

->withExceptions(function (Exceptions $exceptions) {
    $exceptions->respond(function (Response $response) {
        if ($response->getStatusCode() === 419) {
            return back()->with([
                'message' => 'The page expired, please try again.',
            ]);
        }

        return $response;
    });
});
```

The result is a much better experience: instead of seeing the error modal, users see a message that the page has expired and are asked to try again.

<video controls src="https://mintcdn.com/inertiajs/X4AKX_y_0pX0Y95-/mp4/csrf-mismatch-warning.mp4?fit=max&auto=format&n=X4AKX_y_0pX0Y95-&q=85&s=75f0899947cae6f9ce9125edc45891ab" />
