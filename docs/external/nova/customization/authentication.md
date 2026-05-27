# Nova - Customization/Authentication

*Source: https://nova.laravel.com/docs/v5/customization/authentication*

---

## On this page
- [Using Nova as Your Application’s Default Login](#using-nova-as-your-application%E2%80%99s-default-login)
- [Using Custom Authentication Routes](#using-custom-authentication-routes)
- [Enabling Two Factor Authentication](#enabling-two-factor-authentication)
- [Enabling Email Verification](#enabling-email-verification)
Digging Deeper
# Authentication
Learn how to customize the Nova authentication logic.
> ## Documentation Index
>
> Fetch the complete documentation index at: <https://nova.laravel.com/docs/llms.txt>
>
> Use this file to discover all available pages before exploring further.
Nova utilizes [Laravel Fortify](https://laravel.com/docs/fortify) and offers two-factor authentication, email address verification, and password confirmation. By default, these features are not enabled but can be enabled with just a few changes to your application’s `app/Providers/NovaServiceProvider.php` file.
### [​](#using-nova-as-your-application’s-default-login) Using Nova as Your Application’s Default Login
Sometimes you might want to use Nova as the default authentication UI for your application. To accomplish this, you should enable Nova’s authentication and password reset routes within the `routes` method of your application’s `App\Providers\NovaServiceProvider` class:
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
```
php artisan nova:publish

php artisan migrate
```
Once completed, Nova users will be able to access a new **User Security** page from the User Menu. Please refer to Fortify’s [two-factor authentication documentation](https://laravel.com/docs/fortify#two-factor-authentication) for more information.
### [​](#enabling-email-verification) Enabling Email Verification
Nova also includes support for requiring email verification for newly registered users. To enable this feature, you should uncomment the relevant entry in the `features` configuration item in the `fortify` method of your application’s `App\Provider\NovaServiceProvider` class:
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