# Nova - Customization/Impersonation

*Source: https://nova.laravel.com/docs/v5/customization/impersonation*

---

- [Community](https://discord.com/invite/laravel)
- [Blog](https://blog.laravel.com)

##### Get Started

- [Installation](/docs/v5/installation)
- [Release Notes](/docs/v5/releases)
- [Upgrade Guide](/docs/v5/upgrade)

##### Resources

- [The Basics](/docs/v5/resources/the-basics)
- [Fields](/docs/v5/resources/fields)
- [Dependent Fields](/docs/v5/resources/dependent-fields)
- [Date Fields](/docs/v5/resources/date-fields)
- [File Fields](/docs/v5/resources/file-fields)
- [Repeater Fields](/docs/v5/resources/repeater-fields)
- [Field Panels](/docs/v5/resources/panels)
- [Relationships](/docs/v5/resources/relationships)
- [Validation](/docs/v5/resources/validation)
- [Authorization](/docs/v5/resources/authorization)

##### Search

- [The Basics](/docs/v5/search/the-basics)
- [Global Search](/docs/v5/search/global-search)
- [Scout Integration](/docs/v5/search/scout-integration)

##### Filters

- [Defining Filters](/docs/v5/filters/defining-filters)
- [Registering Filters](/docs/v5/filters/registering-filters)

##### Lenses

- [Defining Lenses](/docs/v5/lenses/defining-lenses)
- [Registering Lenses](/docs/v5/lenses/registering-lenses)

##### Actions

- [Defining Actions](/docs/v5/actions/defining-actions)
- [Registering Actions](/docs/v5/actions/registering-actions)

##### Metrics

- [Defining Metrics](/docs/v5/metrics/defining-metrics)
- [Registering Metrics](/docs/v5/metrics/registering-metrics)

##### Digging Deeper

- [Dashboards](/docs/v5/customization/dashboards)
- [Menus](/docs/v5/customization/menus)
- [Notifications](/docs/v5/customization/notifications)
- [Authentication](/docs/v5/customization/authentication)
- [Impersonation](/docs/v5/customization/impersonation)
- [Tools](/docs/v5/customization/tools)
- [Resource Tools](/docs/v5/customization/resource-tools)
- [Cards](/docs/v5/customization/cards)
- [Fields](/docs/v5/customization/fields)
- [Filters](/docs/v5/customization/filters)
- [CSS / JavaScript](/docs/v5/customization/frontend)
- [Assets](/docs/v5/customization/assets)
- [Localization](/docs/v5/customization/localization)
- [Stubs](/docs/v5/customization/stubs)

On this page

- [Overview](#overview)
- [Enabling Impersonation](#enabling-impersonation)
- [Customizing Impersonation Authorization](#customizing-impersonation-authorization)
- [Inspecting Impersonation State](#inspecting-impersonation-state)
- [Impersonation Events](#impersonation-events)

Digging Deeper

# Impersonation

Learn how to impersonate other users in your application.

## [​](#overview) Overview

After deploying your application to production, you may occasionally need to “impersonate” another user of your application in order to debug problems your customers are reporting. Thankfully, Nova includes built-in functionality to handle this exact scenario.

## [​](#enabling-impersonation) Enabling Impersonation

To enable user impersonation, add the `Laravel\Nova\Auth\Impersonatable` trait to your application’s `User` model:

app/Models/User.php

Copy

Ask AI

```
namespace App\Models;

use Illuminate\Contracts\Auth\MustVerifyEmail;
use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Foundation\Auth\User as Authenticatable;
use Illuminate\Notifications\Notifiable;
use Laravel\Nova\Auth\Impersonatable;
use Laravel\Sanctum\HasApiTokens;

class User extends Authenticatable
{
    use HasApiTokens, HasFactory, Impersonatable, Notifiable;

    // ...
}
```

Once the `Impersonatable` trait has been added to your application’s `User` model, an “Impersonate” action will be available via the inline action menu for the corresponding resource:

![Impersonation](https://mintcdn.com/nova-laravel/ISBJ63muGLVA9l3K/images/impersonate.png?fit=max&auto=format&n=ISBJ63muGLVA9l3K&q=85&s=2998c68c60ae0a5a1e344a425f4ddf11)

### [​](#customizing-impersonation-authorization) Customizing Impersonation Authorization

By default, any user that has permission to view the Nova dashboard can impersonate any other user. However, you may customize who can impersonate other users and what users can be impersonated by defining `canImpersonate` and `canBeImpersonated` methods on your application’s `Impersonatable` model:

app/Models/User.php

Copy

Ask AI

```
use Illuminate\Support\Facades\Gate;

// ...

/**
 * Determine if the user can impersonate another user.
 *
 * @return bool
 */
public function canImpersonate()
{
    return Gate::forUser($this)->check('viewNova');
}

/**
 * Determine if the user can be impersonated.
 *
 * @return bool
 */
public function canBeImpersonated()
{
    return true;
}
```

## [​](#inspecting-impersonation-state) Inspecting Impersonation State

By resolving an implementation of the `Laravel\Nova\Contracts\ImpersonatesUsers` interface via Laravel’s service container, you can inspect the current impersonation state of the application:

routes/web.php

Copy

Ask AI

```
use App\Models\User;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Route;
use Laravel\Nova\Contracts\ImpersonatesUsers;

Route::get('/impersonation', function (Request $request, ImpersonatesUsers $impersonator) {
    if ($impersonator->impersonating($request)) {
        $impersonator->stopImpersonating($request, Auth::guard(), User::class);
    }
});
```

## [​](#impersonation-events) Impersonation Events

By default, you add additional customisation by using available events for Impersonations:

- `Laravel\Nova\Events\StartedImpersonating`
- `Laravel\Nova\Events\StoppedImpersonating`

For example, you may want to log impersonation events, which you can register listeners for in the `boot` method of your application’s `AppServiceProvider` or `EventServiceProvider`:

app/Providers/EventServiceProvider.php

Copy

Ask AI

```
use Illuminate\Support\Facades\Event;
use Laravel\Nova\Events\StartedImpersonating;
use Laravel\Nova\Events\StoppedImpersonating;

// ...

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    parent::boot();

    Event::listen(StartedImpersonating::class, function ($event) {
        logger("User {$event->impersonator->name} started impersonating {$event->impersonated->name}");
    });

    Event::listen(StoppedImpersonating::class, function ($event) {
        logger("User {$event->impersonator->name} stopped impersonating {$event->impersonated->name}");
    });
}
```

Was this page helpful?

YesNo

[Authentication](/docs/v5/customization/authentication)[Tools](/docs/v5/customization/tools)

⌘I