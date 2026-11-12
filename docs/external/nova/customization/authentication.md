Source: https://nova.laravel.com/docs/v5/customization/authentication.md

# Authentication

> Learn how to customize the Nova authentication logic.

Nova utilizes [Laravel Fortify](https://laravel.com/docs/fortify) and offers two-factor authentication, email address verification, and password confirmation. By default, these features are not enabled but can be enabled with just a few changes to your application's `app/Providers/NovaServiceProvider.php` file.

### Using Nova as Your Application's Default Login

Sometimes you might want to use Nova as the default authentication UI for your application. To accomplish this, you should enable Nova's authentication and password reset routes within the `routes` method of your application's `App\Providers\NovaServiceProvider` class:

```php {7} theme={null}
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

### Using Custom Authentication Routes

Alternatively, you can disable Nova's authentication and password reset routes and instead provide Nova with your application's own authentication route paths. This will instruct Nova where to redirect unauthenticated users:

```php theme={null}
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

### Enabling Passkey Authentication

To allow your users to authenticate with passkey authentication, you will need to update your application's `User` model and `App\Providers\NovaServiceProvider` service provider.

First, add the `Laravel\Fortify\PasskeyAuthenticatable` trait and `Laravel\Fortify\Contracts\PasskeyUser` interface to your application's `User` model:

```php {7-8,12} theme={null}
<?php

namespace App\Models;

use Illuminate\Foundation\Auth\User as Authenticatable;
use Illuminate\Notifications\Notifiable;
use Laravel\Fortify\Contracts\PasskeyUser;
use Laravel\Fortify\PasskeyAuthenticatable;
 
class User extends Authenticatable implements PasskeyUser
{
    use Notifiable, PasskeyAuthenticatable;

    // ...
}
```

Next, update the `features` method in your application's `App\Providers\NovaServiceProvider` class to enable passkey authentication:

```php {15-18} theme={null}
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
            Features::passkeys(),
        ])
        ->register();
}
```

Finally, run the `nova:publish` Artisan command to publish the required Fortify migrations. Then, run the `migrate` command:

```shell theme={null}
php artisan nova:publish

php artisan migrate
```

Once completed, Nova users will be able to access a new **User Security** page from the User Menu. Please refer to Fortify's [passkey authentication documentation](https://laravel.com/docs/fortify#passkeys) for more information.

### Enabling Two Factor Authentication

To allow your users to authenticate with two-factor authentication, you will need to update your application's `User` model and `App\Providers\NovaServiceProvider` service provider.

First, add the `Laravel\Fortify\TwoFactorAuthenticatable` trait to your application's `User` model:

```php {7,11} theme={null}
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

Next, update the `features` method in your application's `App\Providers\NovaServiceProvider` class to enable two-factor authentication:

```php {15-18} theme={null}
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

```shell theme={null}
php artisan nova:publish

php artisan migrate
```

Once completed, Nova users will be able to access a new **User Security** page from the User Menu. Please refer to Fortify's [two-factor authentication documentation](https://laravel.com/docs/fortify#two-factor-authentication) for more information.

### Enabling Email Verification

Nova also includes support for requiring email verification for newly registered users. To enable this feature, you should uncomment the relevant entry in the `features` configuration item in the `fortify` method of your application's `App\Provider\NovaServiceProvider` class:

```php {14} theme={null}
use Laravel\Fortify\Features;
use Laravel\Nova\Nova;

// ...

/**
 * Register the configurations for Laravel Fortify.
 */
protected function fortify(): void # [!code focus:11]
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

```php {5,9} theme={null}
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

Finally, to secure the Nova page from being used by unverified users, you can add the `Laravel\Nova\Http\Middleware\EnsureEmailIsVerified` middleware to the `api_middleware` configuration key in your application's `config/nova.php` configuration file:

```php {4} theme={null}
'api_middleware' => [
    'nova',
    \Laravel\Nova\Http\Middleware\Authenticate::class,
    \Laravel\Nova\Http\Middleware\EnsureEmailIsVerified::class,
    \Laravel\Nova\Http\Middleware\Authorize::class,
],
```
