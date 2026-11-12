Source: https://inertiajs.com/docs/v3/the-basics/redirects.md

# Redirects

When making a non-GET Inertia request manually or via a `<Link>` element, you should ensure that you always respond with a proper Inertia redirect response.

For example, if your controller is creating a new user, your "store" endpoint should return a redirect back to a standard `GET` endpoint, such as your user "index" page. Inertia will automatically follow this redirect and update the page accordingly.

```php theme={null}
class UsersController extends Controller
{
    public function index()
    {
        return Inertia::render('Users/Index', [
            'users' => User::all(),
        ]);
    }

    public function store(Request $request)
    {
        User::create(
            $request->validate([
                'name' => ['required', 'max:50'],
                'email' => ['required', 'max:50', 'email'],
            ])
        );

        return to_route('users.index');
    }
}
```

## 303 Response Code

You must use a `303` response code when redirecting after a `PUT`, `PATCH`, `DELETE`, or `QUERY` request. Otherwise, the browser will not issue the subsequent request as a `GET` request. A `303` redirect is very similar to a `302` redirect; however, the follow-up request is explicitly changed to a `GET` request.

If you're using one of our official server-side adapters, all redirects will automatically be converted to `303` redirects.

## Preserving Fragments

Sometimes a user may visit a URL with a fragment, such as `/article/old-slug#section`, and the server needs to redirect to a different URL. The fragment from the original request is normally lost during the redirect.

```vue Vue icon="vuejs" theme={null}
import { Link } from '@inertiajs/vue3'

<Link href="/article/old-slug#section">View section</Link>
```

```jsx React icon="react" theme={null}
import { Link } from "@inertiajs/react";

<Link href="/article/old-slug#section">View section</Link>
```

```svelte Svelte icon="s" theme={null}
import { Link } from '@inertiajs/svelte'

<Link href="/article/old-slug#section">View section</Link>
```

You may preserve the fragment by chaining the `preserveFragment` method on the redirect response. The client will carry over the `#section` fragment to the redirect target, resulting in `/article/new-slug#section`.

```php theme={null}
return redirect('/article/new-slug')->preserveFragment();
```

## External Redirects

Sometimes it's necessary to redirect to an external website, or even another non-Inertia endpoint in your app while handling an Inertia request. This can be accomplished using a server-side initiated `window.location` visit via the `Inertia::location()` method.

```php theme={null}
return Inertia::location($url);
```

The `Inertia::location()` method will generate a `409 Conflict` response and include the destination URL in the `X-Inertia-Location` header. When this response is received client-side, Inertia will automatically perform a `window.location = url` visit.

## Previous URL

Laravel Adapter v3.4.0+

Sometimes you may wish to know which page the user navigated from. Laravel's session middleware doesn't store the previous URL and route for Inertia visits, since they are sent as AJAX requests, so `session()->previousUrl()`, `session()->previousUri()`, and `session()->previousRoute()` return the last full page load. The `back()` helper is unaffected, as it resolves the previous location from the request's `Referer` header. You may enable the `store_previous_url` option in your `config/inertia.php` configuration file to store the previous location for Inertia visits as well.

```php config/inertia.php theme={null}
return [
    'store_previous_url' => true,
];
```

Prefetch requests and [partial reloads](https://inertiajs.com/docs/v3/data-props/partial-reloads.md) are excluded, since deferred props, polling, and infinite scroll requests aren't navigations the user came from. Overriding the `shouldStoreCurrentUrl()` method in your `HandleInertiaRequests` middleware allows you to customize which visits are stored.

```php theme={null}
use Illuminate\Http\Request;
use Inertia\Middleware;
use Symfony\Component\HttpFoundation\Response;

class HandleInertiaRequests extends Middleware
{
    public function shouldStoreCurrentUrl(Request $request, Response $response): bool
    {
        return parent::shouldStoreCurrentUrl($request, $response)
            && ! $request->routeIs('admin.*');
    }
}
```
