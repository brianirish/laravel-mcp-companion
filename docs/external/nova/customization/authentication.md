# Nova - Customization/Authentication

*Source: https://nova.laravel.com/docs/v5/customization/authentication*

---

[Laravel Nova home page](https://nova.laravel.com)
v5
Search...
⌘KAsk AI
- [email protected]
- [Platform Status](https://status.laravel.com/)
- [Dashboard](https://nova.laravel.com)
- [Dashboard](https://nova.laravel.com)
Search...
Navigation
Digging Deeper
Authentication
[Documentation](/docs/v5/installation)[Knowledge Base](/docs/kb/support)
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
- [Using Nova as Your Application’s Default Login](#using-nova-as-your-application%E2%80%99s-default-login)
- [Using Custom Authentication Routes](#using-custom-authentication-routes)
- [Enabling Two Factor Authentication](#enabling-two-factor-authentication)
- [Enabling Email Verification](#enabling-email-verification)
Digging Deeper
# Authentication
Learn how to customize the Nova authentication logic.
Nova utilizes [Laravel Fortify](https://laravel.com/docs/fortify) and offers two-factor authentication, email address verification, and password confirmation. By default, these features are not enabled but can be enabled with just a few changes to your application’s `app/Providers/NovaServiceProvider.php` file.
### [​](#using-nova-as-your-application’s-default-login) Using Nova as Your Application’s Default Login
Sometimes you might want to use Nova as the default authentication UI for your application. To accomplish this, you should enable Nova’s authentication and password reset routes within the `routes` method of your application’s `App\Providers\NovaServiceProvider` class:
Copy
Ask AI
```
/**
 * Register the Nova routes.
 */
protected function routes(): void
{
    Nova::routes()
        ->withAuthenticationRoutes(default: true)
        ->withPasswordResetRoutes()
        ->register();
}
```
### [​](#using-custom-authentication-routes) Using Custom Authentication Routes
Alternatively, you can disable Nova’s authentication and password reset routes and instead provide Nova with your application’s own authentication route paths. This will instruct Nova where to redirect unauthenticated users:
Copy
Ask AI
```
/**
 * Register the Nova routes.
 */
protected function routes(): void
{
    Nova::routes()
        ->withoutAuthenticationRoutes(
            login: '/login', 
            logout: '/logout',
        )
        ->withoutPasswordResetRoutes(
            forgotPassword: '/forgot-password', 
            resetPassword: '/reset-password',
        )
        ->register();
}
```
### [​](#enabling-two-factor-authentication) Enabling Two Factor Authentication
To allow your users to authenticate with two-factor authentication, you will need to update your application’s `User` model and `App\Providers\NovaServiceProvider` service provider.
First, add the `Laravel\Fortify\TwoFactorAuthenticatable` trait to your application’s `User` model:
Copy
Ask AI
```
<?php

namespace App\Models;

use Illuminate\Foundation\Auth\User as Authenticatable;
use Illuminate\Notifications\Notifiable;
use Laravel\Fortify\TwoFactorAuthenticatable;
 
class User extends Authenticatable
{
    use Notifiable, TwoFactorAuthenticatable;

    // ...
}
```
Next, update the `routes` method in your application’s `App\Providers\NovaServiceProvider` class to enable two-factor authentication:
Copy
Ask AI
```
use Laravel\Fortify\Features;
use Laravel\Nova\Nova;

// ...

/**
 * Register the configurations for Laravel Fortify.
 */
protected function fortify(): void
{
    Nova::fortify()
        ->features([
            Features::updatePasswords(),
            // Features::emailVerification(),
            Features::twoFactorAuthentication([
                'confirm' => true,
                'confirmPassword' => true
            ]),
        ])
        ->register();
}
```
Finally, run the `nova:publish` Artisan command to publish the required Fortify migrations. Then, run the `migrate` command:
Copy
Ask AI
```
php artisan nova:publish

php artisan migrate
```
Once completed, Nova users will be able to access a new **User Security** page from the User Menu. Please refer to Fortify’s [two-factor authentication documentation](https://laravel.com/docs/fortify#two-factor-authentication) for more information.
### [​](#enabling-email-verification) Enabling Email Verification
Nova also includes support for requiring email verification for newly registered users. To enable this feature, you should uncomment the relevant entry in the `features` configuration item in the `fortify` method of your application’s `App\Provider\NovaServiceProvider` class:
Copy
Ask AI
```
use Laravel\Fortify\Features;
use Laravel\Nova\Nova;

// ...

/**
 * Register the configurations for Laravel Fortify.
 */
protected function fortify(): void
{
    Nova::fortify()
        ->features([
            Features::updatePasswords(),
            Features::emailVerification(),
            // Features::twoFactorAuthentication(['confirm' => true, 'confirmPassword' => true]),
        ])
        ->register();
}
```
Next, you should ensure that your `User` model implements the `Illuminate\Contracts\Auth\MustVerifyEmail` interface:
Copy
Ask AI
```
<?php

namespace App\Models;

use Illuminate\Contracts\Auth\MustVerifyEmail;
use Illuminate\Foundation\Auth\User as Authenticatable;
use Illuminate\Notifications\Notifiable;

class User extends Authenticatable implements MustVerifyEmail
{
    use Notifiable;

    // ...
}
```
Finally, to secure the Nova page from being used by unverified users, you can add the `Laravel\Nova\Http\Middleware\EnsureEmailIsVerified` middleware to the `api_middleware` configuration key in your application’s `config/nova.php` configuration file:
Copy
Ask AI
```
'api_middleware' => [
    'nova',
    \Laravel\Nova\Http\Middleware\Authenticate::class,
    \Laravel\Nova\Http\Middleware\EnsureEmailIsVerified::class,
    \Laravel\Nova\Http\Middleware\Authorize::class,
],
```
Was this page helpful?
YesNo
[Notifications](/docs/v5/customization/notifications)[Impersonation](/docs/v5/customization/impersonation)
⌘I
[Laravel Nova home page](https://nova.laravel.com)
Platform
[Dashboard](https://nova.laravel.com/)[Status](https://status.laravel.com/)
Legal and Compliance
[Term of Service](https://nova.laravel.com/terms)[Privacy Policy](https://nova.laravel.com/privacy)