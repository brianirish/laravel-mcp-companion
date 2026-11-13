Source: https://nightwatch.laravel.com/docs/user.md

# Users

> Monitor your users and their activity

Nightwatch automatically captures details about the authenticated user when any event occurs. By default, it captures the user's `id`, `name`, and `email` attributes.

## Customizing User Fields

Sometimes you may need to adjust what is captured. For example:

* Your app uses `first_name` and `last_name` instead of a single `name` field.
* You run a multi-tenant app where the user IDs are not unique across tenants.
* You prefer not to store certain user details at all.

Nightwatch makes this easy with the `Nightwatch::user` method, which you can call inside your `AppServiceProvider`.

Here's an example of how you can combine `first_name` and `last_name` as the name field:

```php theme={null}
use Illuminate\Contracts\Auth\Authenticatable;
use Laravel\Nightwatch\Facades\Nightwatch;

Nightwatch::user(fn (Authenticatable $user) => [
    'name' => "{$user->first_name} {$user->last_name}",
    'username' => $user->email,
]);
```

## Customizing User IDs

In systems where user IDs may not be unique, such as multi-tenant apps with auto-incrementing IDs, you can customize the ID to include the tenant identifier so Nightwatch can tell them apart.

```php theme={null}
Nightwatch::user(fn (Authenticatable $user) => [
    'id' => "{$user->tenant_id}-{$user->id}",
    'name' => $user->name,
    'username' => $user->email,
]);
```

## Omitting User Fields

If you don't want Nightwatch to capture certain fields, you can simply leave them out of the returned array. Note that the `id` will always be captured.

```php theme={null}
// Exclude both fields...
Nightwatch::user(fn (Authenticatable $user) => []);

// Only include the name field...
Nightwatch::user(fn (Authenticatable $user) => [
    'name' => $user->name,
]);
```
