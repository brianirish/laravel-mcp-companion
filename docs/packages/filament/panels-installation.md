# Filament - Panels/Installation

Source: https://filamentphp.com/docs/3.x/panels/installation

#Requirements
-------------

Filament requires the following to run:

* PHP 8.1+
* Laravel v10.0+
* Livewire v3.0+

#Installation
-------------

> If you are upgrading from Filament v2, please review the upgrade guide.

Install the Filament Panel Builder by running the following commands in your Laravel project directory:

```php
composer require filament/filament:"^3.3" -W

php artisan filament:install --panels

```
This will create and register a new Laravel service provider called `app/Providers/Filament/AdminPanelProvider.php`.

> If you get an error when accessing your panel, check that the service provider was registered in `bootstrap/providers.php` (Laravel 11 and above) or `config/app.php` (Laravel 10 and below). If not, you should manually add it.

#Create a user
--------------

You can create a new user account with the following command:

```php
php artisan make:filament-user

```
Open `/admin` in your web browser, sign in, and start building your app!

Not sure where to start? Review the Getting Started guide to learn how to build a complete Filament admin panel.

#Using other Filament packages
------------------------------

The Filament Panel Builder pre-installs the Form Builder, Table Builder, Notifications, Actions, Infolists, and Widgets packages. No other installation steps are required to use these packages within a panel.

#Improving Filament panel performance
-------------------------------------

### #Optimizing Filament for production

To optimize Filament for production, you should run the following command in your deployment script:

```php
php artisan filament:optimize

```
This command will cache the Filament components and additionally the Blade icons, which can significantly improve the performance of your Filament panels. This command is a shorthand for the commands `php artisan filament:cache-components` and `php artisan icons:cache`.

To clear the caches at once, you can run:

```php
php artisan filament:optimize-clear

```
#### #Caching Filament components

If you’re not using the `filament:optimize` command, you may wish to consider running `php artisan filament:cache-components` in your deployment script, especially if you have large numbers of components (resources, pages, widgets, relation managers, custom Livewire components, etc.). This will create cache files in the `bootstrap/cache/filament` directory of your application, which contain indexes for each type of component. This can significantly improve the performance of Filament in some apps, as it reduces the number of files that need to be scanned and auto-discovered for components.

However, if you are actively developing your app locally, you should avoid using this command, as it will prevent any new components from being discovered until the cache is cleared or rebuilt.

You can clear the cache at any time without rebuilding it by running `php artisan filament:clear-cached-components`.

#### #Caching Blade Icons

If you’re not using the `filament:optimize` command, you may wish to consider running `php artisan icons:cache` locally, and also in your deployment script. This is because Filament uses the Blade Icons package, which can be much more performant when cached.

### #Enabling OPcache on your server

From the Laravel Forge documentation:

> Optimizing the PHP OPcache for production will configure OPcache to store your compiled PHP code in memory to greatly improve performance.

Please use a search engine to find the relevant OPcache setup instructions for your environment.

### #Optimizing your Laravel app

You should also consider optimizing your Laravel app for production by running `php artisan optimize` in your deployment script. This will cache the configuration files and routes.

#Deploying to production
------------------------

### #Allowing users to access a panel

By default, all `User` models can access Filament locally. However, when deploying to production or running unit tests, you must update your `App\Models\User.php` to implement the `FilamentUser` contract — ensuring that only the correct users can access your panel:

```php
<?php

namespace App\Models;

use Filament\Models\Contracts\FilamentUser;
use Filament\Panel;
use Illuminate\Foundation\Auth\User as Authenticatable;

class User extends Authenticatable implements FilamentUser
{
    // ...

    public function canAccessPanel(Panel $panel): bool
    {
        return str_ends_with($this->email, '@yourdomain.com') && $this->hasVerifiedEmail();
    }
}

```
> If you don’t complete these steps, a 403 Forbidden error will be returned when accessing the app in production.

Learn more about users.

### #Using a production-ready storage disk

Filament has a storage disk defined in the configuration, which by default is set to `public`. You can set the `FILAMENT_FILESYSTEM_DISK` environment variable to change this.

The `public` disk, while great for easy local development, is not suitable for production. It does not support file visibility, so features of Filament such as file uploads will create public files. In production, you need to use a production-ready disk such as `s3` with a private access policy, to prevent unauthorized access to the uploaded files.

#Publishing configuration
-------------------------

You can publish the Filament package configuration (if needed) using the following command:

```php
php artisan vendor:publish --tag=filament-config

```
#Publishing translations
------------------------

You can publish the language files for translations (if needed) with the following command:

```php
php artisan vendor:publish --tag=filament-panels-translations

```
Since this package depends on other Filament packages, you can publish the language files for those packages with the following commands:

```php
php artisan vendor:publish --tag=filament-actions-translations

php artisan vendor:publish --tag=filament-forms-translations

php artisan vendor:publish --tag=filament-infolists-translations

php artisan vendor:publish --tag=filament-notifications-translations

php artisan vendor:publish --tag=filament-tables-translations

php artisan vendor:publish --tag=filament-translations

```
#Upgrading
----------

> Upgrading from Filament v2? Please review the upgrade guide.

Filament automatically upgrades to the latest non-breaking version when you run `composer update`. After any updates, all Laravel caches need to be cleared, and frontend assets need to be republished. You can do this all at once using the `filament:upgrade` command, which should have been added to your `composer.json` file when you ran `filament:install` the first time:

```php
"post-autoload-dump": [
    // ...
    "@php artisan filament:upgrade"
],

```
Please note that `filament:upgrade` does not actually handle the update process, as Composer does that already. If you’re upgrading manually without a `post-autoload-dump` hook, you can run the command yourself:

```php
composer update

php artisan filament:upgrade

```
Edit on GitHub

Still need help? Join our Discord community or open a GitHub discussion