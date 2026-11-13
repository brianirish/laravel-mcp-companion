Source: https://nightwatch.laravel.com/docs/context.md

# Context

> Add additional metadata to your events to make them easier to debug


Nightwatch integrates with [**Laravel Context**](https://laravel.com/docs/context), enabling you to attach metadata to your requests, jobs, and commands. Context is available in the framework from **Laravel 11.x** onwards.

## Examples

### Augment user details

Add additional user context to help identify user types that are experiencing issues:

```php theme={null}
use Illuminate\Support\Facades\Context;

Context::add('locale', App::currentLocale());

Context::add('user', [
    'role' => Auth::user()->role,
    'subscription_tier' => Auth::user()->subscription_tier,
]);
```

### Track feature flags

Track which feature flags were active during a request:

```php theme={null}
use Illuminate\Support\Facades\Context;
use Laravel\Pennant\Feature;

Context::add('feature_flags', [
    'new_dashboard' => Feature::active('new_dashboard'),
    'enhanced_search' => Feature::active('enhanced_search'),
    'beta_checkout' => Feature::active('beta_checkout'),
]);
```

### Debug multi-tenant issues

Add tenant context to help debug tenant-specific issues:

```php theme={null}
use Illuminate\Support\Facades\Context;

Context::add('tenant', [
    'id' => $tenant->id,
    'name' => $tenant->name,
    'plan' => $tenant->subscription_plan,
    'region' => $tenant->region,
]);
```

> [!NOTE]
>
> **Size limits**\ Up to 65 KB of context data is supported per execution; data
> beyond this limit will be truncated.
