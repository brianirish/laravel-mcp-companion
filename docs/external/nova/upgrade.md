# Nova - Upgrade

*Source: https://nova.laravel.com/docs/v5/upgrade*

---

[Laravel Nova home page![light logo](https://mintcdn.com/nova-laravel/bY_66OSFONsRO54M/logo/light.svg?fit=max&auto=format&n=bY_66OSFONsRO54M&q=85&s=d7b82e399050ba766ad412155b0dbc7a)![dark logo](https://mintcdn.com/nova-laravel/bY_66OSFONsRO54M/logo/dark.svg?fit=max&auto=format&n=bY_66OSFONsRO54M&q=85&s=a81b28aeb4ce32b7a8afd9ed1f9ce58b)](https://nova.laravel.com)

v5

Search...

⌘KAsk AI

- Support
- [Platform Status](https://status.laravel.com/)
- [Dashboard](https://nova.laravel.com)
- [Dashboard](https://nova.laravel.com)

Search...

Navigation

Get Started

Upgrade Guide

[Documentation](/docs/v5/installation)[Knowledge Base](/docs/kb/support)

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

- [Dependency Upgrades](#dependency-upgrades)
- [Server](#server)
- [Client](#client)
- [Updating Composer Dependencies](#updating-composer-dependencies)
- [Updating Assets and Translations](#updating-assets-and-translations)
- [Updating Third-Party Nova Packages ​](#updating-third-party-nova-packages-%E2%80%8B)
- [Upgrading Authentication Features](#upgrading-authentication-features)
- [Updating Nova Components (Custom Tool, Cards, Fields, Filters)](#updating-nova-components-custom-tool%2C-cards%2C-fields%2C-filters)
- [Inertia 2 Compatibility](#inertia-2-compatibility)
- [Replacing form-backend-validation](#replacing-form-backend-validation)
- [Medium Impact Changes](#medium-impact-changes)
- [Form Abandonment (Using Browser Navigation)](#form-abandonment-using-browser-navigation)
- [Algolia Place Field Removed](#algolia-place-field-removed)
- [Low Impact Changes](#low-impact-changes)
- [Update Published Stubs](#update-published-stubs)

Get Started

# Upgrade Guide

Learn how to upgrade your Laravel Nova installation to the latest version.

## [​](#dependency-upgrades) Dependency Upgrades

Nova’s upstream dependencies have been upgraded. You will find a complete list of our dependency upgrades below:

#### [​](#server) Server

- PHP 8.1+
- Laravel Framework 10.34+ and 11.0+
- Inertia Laravel 1.3+ and 2.0+
- Replaced `laravel/ui` with `laravel/fortify` v1.21+
- Removed `doctrine/dbal`

#### [​](#client) Client

- Update to `@inertiajs/vue3` v2
- Update to Heroicons v2
- Update to `trix` v2
- Remove deprecated `form-backend-validation`
- Remove deprecated `places.js`

### [​](#updating-composer-dependencies) Updating Composer Dependencies

You should update your `laravel/nova` dependency to `^5.0` in your application’s `composer.json` file:

composer.json

Copy

Ask AI

```
    "require": {
-       "laravel/nova": "^4.0",
+       "laravel/nova": "^5.0",
    }
```

Next, install your updated Composer dependencies:

Copy

Ask AI

```
composer update mirrors

composer update
```

### [​](#updating-assets-and-translations) Updating Assets and Translations

Next, you should update your application’s Nova assets and translation files. To get started, you may run the following commands to update your assets and translations.
**You may wish to store a copy of your current translation file before running this command so you can easily port any custom translations back into the new file after running these commands.**:

Copy

Ask AI

```
php artisan vendor:publish --tag=nova-assets --force
php artisan vendor:publish --tag=nova-lang --force
```

### [​](#updating-third-party-nova-packages-​) Updating Third-Party Nova Packages ​

If your application relies on Nova tools or packages developed by third-parties, it is possible that these packages are not yet compatible with Nova 5.0 and will require an update from their maintainers.

## [​](#upgrading-authentication-features) Upgrading Authentication Features

Next, you will need to update your Nova configuration file. Ensure that the `api_middleware` configuration option within your application’s `nova` configuration file appears as follows:

config/nova.php

Copy

Ask AI

```
return [

    // ...

    'api_middleware' => [
        'nova',
        \Laravel\Nova\Http\Middleware\Authenticate::class,
        // \Laravel\Nova\Http\Middleware\EnsureEmailIsVerified::class,
        \Laravel\Nova\Http\Middleware\Authorize::class,
    ],

];
```

Next, update the `register` method in your application’s `App\Providers\NovaServiceProvider` class to call the parent’s `register` method. The `parent::register()` method should be invoked before any other code in the method:

app/Nova/NovaServiceProvider.php

Copy

Ask AI

```
/**
 * Register any application services.
 */
public function register(): void 
{
    parent::register();

    //
}
```

## [​](#updating-nova-components-custom-tool,-cards,-fields,-filters) Updating Nova Components (Custom Tool, Cards, Fields, Filters)

### [​](#inertia-2-compatibility) Inertia 2 Compatibility

In Nova 5, Nova’s frontend JavaScript now utilizes Inertia.js 2.x, which will affect any projects that directly import from `@inertiajs/inertia` or `@inertiajs/inertia-vue3`. You should inspect your custom components and packages to ensure all references have been updated as suggested in [Inertia’s upgrade guide](https://inertiajs.com/upgrade-guide).

Copy

Ask AI

```
<script>
-import { usePage } from '@inertiajs/inertia-vue3'
-import { Inertia } from '@inertiajs/inertia'
+import { router as Inertia, usePage } from '@inertiajs/vue3'

// ...

</script>
```

### [​](#replacing-form-backend-validation) Replacing `form-backend-validation`

The `form-backend-validation` repository has been archived and should no longer be used by third-party packages or components. Instead, you may simply import `Errors` from `laravel-nova`:

Copy

Ask AI

```
<script>
-import { Errors } from 'form-backend-validation'
+import { Errors } from 'laravel-nova'

// ...

</script>
```

Then, you may remove `form-backend-validation` from your component’s `package.json`:

Copy

Ask AI

```
npm remove form-backend-validation
```

## [​](#medium-impact-changes) Medium Impact Changes

### [​](#form-abandonment-using-browser-navigation) Form Abandonment (Using Browser Navigation)

With the introduction of Inertia.js 2.x, we are no longer able to provide form abandonment warnings when using the browser’s back button.

### [​](#algolia-place-field-removed) Algolia Place Field Removed

Algolia [retired their “Places” API](https://www.algolia.com/blog/product/sunsetting-our-places-feature/) on May 31, 2022; therefore, the `Place` field was deprecated on Nova 4 and is now removed in Nova 5.

## [​](#low-impact-changes) Low Impact Changes

### [​](#update-published-stubs) Update Published Stubs

Due to various changes in Nova 5.x, you should re-publish the Nova “stubs” if you have previously published them. You can accomplish this by executing the `nova:stubs` Artisan command with the `--force` option:

Copy

Ask AI

```
php artisan nova:stubs --force
```

Was this page helpful?

YesNo

[Release Notes](/docs/v5/releases)[The Basics](/docs/v5/resources/the-basics)

⌘I

[Laravel Nova home page![light logo](https://mintcdn.com/nova-laravel/bY_66OSFONsRO54M/logo/light.svg?fit=max&auto=format&n=bY_66OSFONsRO54M&q=85&s=d7b82e399050ba766ad412155b0dbc7a)![dark logo](https://mintcdn.com/nova-laravel/bY_66OSFONsRO54M/logo/dark.svg?fit=max&auto=format&n=bY_66OSFONsRO54M&q=85&s=a81b28aeb4ce32b7a8afd9ed1f9ce58b)](https://nova.laravel.com)

[x](https://x.com/laravelphp)[github](https://github.com/laravel)[discord](https://discord.com/invite/laravel)[linkedin](https://linkedin.com/company/laravel)

Platform

[Dashboard](https://nova.laravel.com/)[Status](https://status.laravel.com/)

Legal and Compliance

[Term of Service](https://nova.laravel.com/terms)[Privacy Policy](https://nova.laravel.com/privacy)

[x](https://x.com/laravelphp)[github](https://github.com/laravel)[discord](https://discord.com/invite/laravel)[linkedin](https://linkedin.com/company/laravel)