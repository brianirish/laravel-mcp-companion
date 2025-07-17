# Nova - Customization/Frontend

*Source: https://nova.laravel.com/docs/v5/customization/frontend*

---

[Laravel Nova home page![light logo](https://mintlify.s3.us-west-1.amazonaws.com/nova-laravel/logo/light.svg)![dark logo](https://mintlify.s3.us-west-1.amazonaws.com/nova-laravel/logo/dark.svg)](https://nova.laravel.com)

v5

Search...

⌘KAsk AI

- Support
- [Platform Status](https://status.laravel.com/)
- [Dashboard](https://nova.laravel.com)
- [Dashboard](https://nova.laravel.com)

Search...

Navigation

Digging Deeper

CSS / JavaScript

[Documentation](/docs/v5/installation)[Knowledge Base](/docs/kb/support)

- [Community](https://discord.com/invite/laravel)
- [Blog](https://blog.laravel.com/nova)

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

Digging Deeper

# CSS / JavaScript

Learn how to customize the CSS and JavaScript of your Nova application.

When building custom Nova tools, resource tools, cards, and fields, you may use a variety of helpers that are globally available to your JavaScript components.

### [​](#nova-requests) Nova Requests

You may use the `Nova.request()` method to make XHR requests to backend routes provided by your application or custom tools, cards, and fields. The `Nova.request()` method is powered by [Axios](https://github.com/axios/axios) and offers the same API. However, the `Nova.request()` method configures its own instance of Axios that has pre-configured interceptors to properly handle and redirect on `401`, `403`, and `500` level HTTP server responses:

Copy

Ask AI

```
Nova.request().get('/nova-vendor/stripe-inspector/endpoint').then(response => {
    // ...
})

```

### [​](#manual-navigation) Manual Navigation

The global `Nova` JavaScript object offers a `visit` method that may be invoked to navigate to other URLs within your Nova dashboard:

Copy

Ask AI

```
// Navigate to User's detail page...
Nova.visit(`/resources/users/${userId}`)

// Navigate to remote URL...
Nova.visit({ url: 'https://nova.laravel.com', remote: true })

```

The `visit` method accepts an array of navigation options as its second argument. As the `visit` method uses Inertia’s own `visit` method behind the scenes, all of [Inertia’s `visit` options](https://legacy.inertiajs.com/manual-visits) are supported by Nova’s `visit` method:

Copy

Ask AI

```
Nova.visit(`/resources/users/${userId}`, {
  onFinish: () => Nova.success(`User ${userId} detail page.`)
})

```

### [​](#event-bus) Event Bus

The global `Nova` JavaScript object may be used as an event bus by your custom components. The bus provides the following methods, which correspond to and have the same behavior as the event methods provided by [tiny-emitter](https://www.npmjs.com/package/tiny-emitter):

Copy

Ask AI

```
Nova.$on(event, callback)
Nova.$once(event, callback)
Nova.$off(event, callback)
Nova.$emit(event, [...args])

```

### [​](#notifications) Notifications

You may display toast notification to users of your custom frontend components by calling the `success`, `error`, `info`, or `warning` methods on the global `Nova` object:

Copy

Ask AI

```
Nova.success('It worked!')
Nova.error('It failed!')

```

### [​](#shortcuts) Shortcuts

Nova provides two convenience methods for managing keyboard shortcuts, powered by [Mousetrap](https://craig.is/killing/mice). You may use these methods within your custom components to register and unregister shortcuts:

Copy

Ask AI

```
// Add a single keyboard shortcut...
Nova.addShortcut('ctrl+k', event => {
    // Callback...
})

// Add multiple keyboard shortcuts...
Nova.addShortcut(['ctrl+k', 'command+k'], event => {
    // Callback...
})

// Add a sequence shortcut...
Nova.addShortcut('* a', event => {
    // Callback...
})

// Remove a shortcut...
Nova.disableShortcut('ctrl+k')

// Remove multiple shortcuts...
Nova.disableShortcut(['ctrl+k', 'command+k'])

```

### [​](#global-variables) Global Variables

The global `Nova` JavaScript object’s `config` method allows you to get the current Nova `base` path and `userId` configuration values:

Copy

Ask AI

```
const userId = Nova.config('userId');
const basePath = Nova.config('base');

```

However, you are free to add additional values to this object using the `Nova::provideToScript` method. You may call this method within a `Nova::serving` listener, which should typically be registered in the `boot` method of your application or custom component’s service provider:

app/Providers/NovaServiceProvider.php

Copy

Ask AI

```
use Laravel\Nova\Nova;
use Laravel\Nova\Events\ServingNova;

// ...

/**
 * Bootstrap any application services.
 *
 * @return void
 */
public function boot()
{
    parent::boot();

    Nova::serving(function (ServingNova $event) {
        Nova::provideToScript([
            'mail_driver' => config('mail.default'),
        ]);
    });
}

```

Once the variable has been provided to Nova via the `provideToScript` method, you may access it using the global `Nova` JavaScript object’s `config` method:

Copy

Ask AI

```
const driver = Nova.config('mail_driver');

```

### [​](#localizations) Localizations

Localization strings can be passed to the frontend via your `NovaServiceProvider`. To learn more, please consult the [full custom localization documentation](./localization#frontend).

### [​](#using-nova-mixins) Using Nova Mixins

Custom Nova tools, resource tools, cards, and other custom packages that are being developed within a `nova-components` directory of a Laravel application can utilize `laravel-nova` mixins by importing `nova.mix.js` Mix Extension from the Nova Devtool installation that is located within your root application’s `vendor` directory. This extension should be placed in your package’s `webpack.mix.js`:

webpack.mix.js

Copy

Ask AI

```
let mix = require('laravel-mix')
mix.extend('nova', new require('laravel-nova-devtool'))

mix
  .setPublicPath('dist')
  .js('resources/js/card.js', 'js')
  .vue({ version: 3 })
  .css('resources/css/card.css', 'css')
  .nova('acme/analytics')

```

Laravel Nova’s assets are built using **lockfile** version `3` and require NPM 9+.

### [​](#vue-devtools) Vue DevTools

The following feature require the `laravel/nova-devtool` Composer package to be installed:

Copy

Ask AI

```
composer require --dev "laravel/nova-devtool"

```

By default, Nova’s JavaScript is compiled for production. As such, you will not be able to access the Vue DevTools out of the box without compiling Nova’s JavaScript for development. To accomplish this, you may issue the following terminal commands from the root of your Nova project:

Application

Package

Copy

Ask AI

```
php artisan nova:enable-vue-devtool

```

Was this page helpful?

YesNo

[Filters](/docs/v5/customization/filters)[Assets](/docs/v5/customization/assets)

On this page

- [Nova Requests](#nova-requests)
- [Manual Navigation](#manual-navigation)
- [Event Bus](#event-bus)
- [Notifications](#notifications)
- [Shortcuts](#shortcuts)
- [Global Variables](#global-variables)
- [Localizations](#localizations)
- [Using Nova Mixins](#using-nova-mixins)
- [Vue DevTools](#vue-devtools)

[Laravel Nova home page![light logo](https://mintlify.s3.us-west-1.amazonaws.com/nova-laravel/logo/light.svg)![dark logo](https://mintlify.s3.us-west-1.amazonaws.com/nova-laravel/logo/dark.svg)](https://nova.laravel.com)

[x](https://x.com/laravelphp)[github](https://github.com/laravel)[discord](https://discord.com/invite/laravel)[linkedin](https://linkedin.com/company/laravel)

Platform

[Dashboard](https://nova.laravel.com/)[Status](https://status.laravel.com/)

Legal and Compliance

[Term of Service](https://nova.laravel.com/terms)[Privacy Policy](https://nova.laravel.com/privacy)

[x](https://x.com/laravelphp)[github](https://github.com/laravel)[discord](https://discord.com/invite/laravel)[linkedin](https://linkedin.com/company/laravel)

Assistant

Responses are generated using AI and may contain mistakes.