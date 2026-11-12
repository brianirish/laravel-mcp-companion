Source: https://inertiajs.com/docs/v3/data-props/once-props.md

# Once Props

Some data rarely changes, is expensive to compute, or is simply large. Rather than including this data in every response, you may use once props. These props are remembered by the client and reused on subsequent pages that include the same prop. This makes them ideal for [shared data](https://inertiajs.com/docs/v3/data-props/shared-data.md).

## Creating Once Props

To create a once prop, use the `Inertia::once()` method when returning your response. This method receives a callback that returns the prop data.

```php theme={null}
return Inertia::render('Billing', [
    'plans' => Inertia::once(fn () => Plan::all()),
]);
```

After the client has received this prop, subsequent requests will skip resolving the callback and exclude the prop from the response. The client only remembers once props while navigating between pages that include them.

Navigating to a page without the once prop will forget the remembered value, and it will be resolved again on the next page that has it. In practice, this is rarely an issue since once props are typically used as shared data or within a specific section of your application.

## Forcing a Refresh

You may force a once prop to be refreshed using the `fresh()` method.

```php theme={null}
return Inertia::render('Billing', [
    'plans' => Inertia::once(fn () => Plan::all())->fresh(),
]);
```

This method also accepts a boolean, allowing you to conditionally refresh the prop.

```php theme={null}
return Inertia::render('Billing', [
    'plans' => Inertia::once(fn () => Plan::all())->fresh($condition),
]);
```

## Refreshing from the Client

You may refresh a once prop from the client-side using a [partial reload](https://inertiajs.com/docs/v3/data-props/partial-reloads.md). The server will always resolve a once prop when explicitly requested.

```js Vue icon="vuejs" theme={null}
import { router } from "@inertiajs/vue3";

router.reload({ only: ["plans"] });
```

```js React icon="react" theme={null}
import { router } from "@inertiajs/react";

router.reload({ only: ["plans"] });
```

```js Svelte icon="s" theme={null}
import { router } from "@inertiajs/svelte";

router.reload({ only: ["plans"] });
```

## Expiration

You may set an expiration time using the `until()` method. This method accepts a `DateTimeInterface`, `DateInterval`, or an integer (seconds). The prop will be refreshed on a subsequent visit after the expiration time has passed.

```php theme={null}
return Inertia::render('Dashboard', [
    'rates' => Inertia::once(fn () => ExchangeRate::all())->until(now()->addDay()),
]);
```

## Custom Keys

You may assign a custom key to the prop using the `as()` method. This is useful when you want to share data across multiple pages while using different prop names.

```php theme={null}
// Team member list...
return Inertia::render('Team/Index', [
    'memberRoles' => Inertia::once(fn () => Role::all())->as('roles'),
]);

// Invite form...
return Inertia::render('Team/Invite', [
    'availableRoles' => Inertia::once(fn () => Role::all())->as('roles'),
]);
```

Both pages share the same underlying data because they use the same custom key, so the prop is only resolved for whichever page you visit first.

## Sharing Once Props

You may share once props globally using the `Inertia::share()` method.

```php theme={null}
Inertia::share('countries', Inertia::once(fn () => Country::all()));
```

Or, for convenience, you may use the `shareOnce()` method.

```php theme={null}
Inertia::shareOnce('countries', fn () => Country::all());
```

You may also chain `as()`, `fresh()`, and `until()` onto the `shareOnce` method.

```php theme={null}
Inertia::shareOnce('countries', fn () => Country::all())->until(now()->addDay());
```

Additionally, you may define a dedicated `shareOnce()` method in your middleware. The middleware will evaluate both `share()` and `shareOnce()`, merging the results.

```php theme={null}
class HandleInertiaRequests extends Middleware
{
    public function shareOnce(Request $request): array
    {
        return array_merge(parent::shareOnce($request), [
            'countries' => fn () => Country::all(),
        ]);
    }
}
```

## Conditional Once Props

Some shared data is mostly stable but changes at specific moments, like the authenticated user. You may return a once prop while a user is authenticated, and `null` otherwise. Sign in and sign out usually end with a redirect to a page that does not explicitly request the `auth` prop, so a remembered once value would go stale.

Returning `null` on signed-out requests overwrites the remembered user on every response, while returning a once prop when authenticated lets the client remember the user across visits.

```php theme={null}
class HandleInertiaRequests extends Middleware
{
    public function share(Request $request): array
    {
        return [
            ...parent::share($request),
            'auth' => $request->user()
                ? Inertia::once(fn () => $request->user())
                : null,
        ];
    }
}
```

## Prefetching

Once props are compatible with [prefetching](https://inertiajs.com/docs/v3/data-props/prefetching.md). The client automatically includes any remembered once props in prefetched responses, so navigating to a prefetched page will already have the once props available.

Prefetched pages containing an expired once prop will be invalidated from the cache.

## Combining with Other Prop Types

The `once()` modifier may be chained onto [deferred](https://inertiajs.com/docs/v3/data-props/deferred-props.md), [merge](https://inertiajs.com/docs/v3/data-props/merging-props.md), and [optional](https://inertiajs.com/docs/v3/data-props/partial-reloads.md#lazy-data-evaluation) props.

```php theme={null}
return Inertia::render('Dashboard', [
    'permissions' => Inertia::defer(fn () => Permission::all())->once(),
    'activity' => Inertia::merge(fn () => $user->recentActivity())->once(),
    'categories' => Inertia::optional(fn () => Category::all())->once(),
]);
```
