> ## Documentation Index
> Fetch the complete documentation index at: https://inertiajs.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Routing

## Defining Routes

When using Inertia, all of your application's routes are defined server-side. This means that you don't need Vue Router or React Router. Instead, you can simply define Laravel routes and return [Inertia responses](/docs/v3/the-basics/responses) from those routes.

## Shorthand Routes

If you have a [page](/docs/v3/the-basics/pages) that doesn't need a corresponding controller method, like an "FAQ" or "about" page, you can route directly to a component via the `Route::inertia()` method.

```php theme={null}
Route::inertia('/about', 'About');
```

## Generating URLs

Some server-side frameworks allow you to generate URLs from named routes. However, you will not have access to those helpers client-side. Here are a couple ways to still use named routes with Inertia.

The first option is to generate URLs server-side and include them as props. Notice in this example how we're passing the `edit_url` and `create_url` to the `Users/Index` component.

```php theme={null}
class UsersController extends Controller
{
    public function index()
    {
        return Inertia::render('Users/Index', [
            'users' => User::all()->map(fn ($user) => [
                'id' => $user->id,
                'name' => $user->name,
                'email' => $user->email,
                'edit_url' => route('users.edit', $user),
            ]),
            'create_url' => route('users.create'),
        ]);
    }
}
```

When using Laravel, you have several options to make your server-side routes available to your client-side code:

### Wayfinder

When using [Wayfinder](https://github.com/laravel/wayfinder), you can pass the generated TypeScript method directly to the [Link component](/docs/v3/the-basics/links#wayfinder), [form helpers](/docs/v3/the-basics/forms#wayfinder), or [router methods](/docs/v3/the-basics/manual-visits#wayfinder) and Inertia understand how to handle it. In fact, if you are developing an application using one of Laravel's [starter kits](https://laravel.com/docs/starter-kits), Wayfinder is already configured for you.

### Ziggy

The [Ziggy](https://github.com/tighten/ziggy) library can make your named, server-side routes available to you via a global `route()` function. If you're using the Vue plugin included with Ziggy, you may use the `route()` function directly in your templates.

```vue theme={null}
<Link :href="route('users.create')">Create User</Link>
```

When [server-side rendering](/docs/v3/advanced/server-side-rendering) is enabled, you may pass an options object to the Ziggy plugin in your `ssr.js` file. This should include the route definitions and current location.

```js theme={null}
.use(ZiggyVue, {
    ...page.props.ziggy,
    location: new URL(page.props.ziggy.location),
});
```

## Customizing the Page URL

The [page object](/docs/v3/core-concepts/the-protocol#the-page-object) includes a `url` that represents the current page's URL. By default, the Laravel adapter resolves this using the `fullUrl()` method on the `Request` instance, but strips the scheme and host so the result is a relative URL.

If you need to customize how the URL is resolved, you may provide a resolver within the `urlResolver` method of the Inertia `HandleInertiaRequests` middleware.

```php theme={null}
class HandleInertiaRequests extends Middleware
{
    public function urlResolver()
    {
        return function (Request $request) {
            // Return the URL for the request...
        };
    }
}
```

Alternatively, you may define the resolver using the `Inertia::resolveUrlUsing()` method.

```php theme={null}
Inertia::resolveUrlUsing(function (Request $request) {
    // Return the URL for the request...
});
```
