# Livewire - Installation

Source: https://livewire.laravel.com/docs/installation

Version 3.x

Version 3.x
Version 2.x
Version 1.x

* ##### Getting Started

  + Quickstart
  + Installation
  + Upgrade Guide

UI Components →

* ##### Essentials

  + Components
  + Properties
  + Actions
  + Forms
  + Events
  + Lifecycle Hooks
  + Nesting Components
  + Testing
* ##### Features

  + Alpine
  + Navigate
  + Lazy Loading
  + Validation
  + File Uploads
  + Pagination
  + URL Query Parameters
  + Computed Properties
  + Session Properties
  + Redirecting
  + File Downloads
  + Locked Properties
  + Request Bundling
  + Offline States
  + Teleport
* ##### HTML Directives

  + wire:click
  + wire:submit
  + wire:model
  + wire:loading
  + wire:navigate
  + wire:current
  + wire:cloak
  + wire:dirty
  + wire:confirm
  + wire:transition
  + wire:init
  + wire:poll
  + wire:offline
  + wire:ignore
  + wire:replace
  + wire:show
  + wire:stream
  + wire:text
* ##### Concepts

  + Morphing
  + Hydration
  + Nesting
* ##### Advanced

  + Troubleshooting
  + Security
  + JavaScript
  + Synthesizers
  + Contribution Guide
* ##### Packages

  + Volt

Installation
============

Are you a visual learner?

Master Livewire with our in-depth screencasts

Watch now

Livewire is a Laravel package, so you will need to have a Laravel application up and running before you can install and use Livewire. If you need help setting up a new Laravel application, please see the official Laravel documentation.

To install Livewire, open your terminal and navigate to your Laravel application directory, then run the following command:

```php

composer require livewire/livewire

```
That's it — really. If you want more customization options, keep reading. Otherwise, you can jump right into using Livewire.

`/livewire/livewire.js` returning a 404 status code

By default, Livewire exposes a route in your application to serve its JavaScript assets from: `/livewire/livewire.js`. This is fine for most applications, however, if you are using Nginx with a custom configuration, you may receive a 404 from this endpoint. To fix this issue, you can either compile Livewire's JavaScript assets yourself, or configure Nginx to allow for this.

#Publishing the configuration file
----------------------------------

Livewire is "zero-config", meaning you can use it by following conventions, without any additional configuration. However, if needed, you can publish and customize Livewire's configuration file by running the following Artisan command:

```php

php artisan livewire:publish --config

```
This will create a new `livewire.php` file in your Laravel application's `config` directory.

#Manually including Livewire's frontend assets
----------------------------------------------

By default, Livewire injects the JavaScript and CSS assets it needs into each page that includes a Livewire component.

If you want more control over this behavior, you can manually include the assets on a page using the following Blade directives:

```php

<html>

<head>

...

@livewireStyles

</head>

<body>

...

@livewireScripts

</body>

</html>

```
By including these assets manually on a page, Livewire knows not to inject the assets automatically.

AlpineJS is bundled with Livewire

Because Alpine is bundled with Livewire's JavaScript assets, you must include `@livewireScripts` on every page you wish to use Alpine. Even if you're not using Livewire on that page.

Though rarely required, you may disable Livewire's auto-injecting asset behavior by updating the `inject_assets` configuration option in your application's `config/livewire.php` file:

```php

'inject_assets' => false,

```
If you'd rather force Livewire to inject its assets on a single page or multiple pages, you can call the following global method from the current route or from a service provider.

```php

\Livewire\Livewire::forceAssetInjection();

```
#Configuring Livewire's update endpoint
---------------------------------------

Every update in a Livewire component sends a network request to the server at the following endpoint: `https://example.com/livewire/update`

This can be a problem for some applications that use localization or multi-tenancy.

In those cases, you can register your own endpoint however you like, and as long as you do it inside `Livewire::setUpdateRoute()`, Livewire will know to use this endpoint for all component updates:

```php

Livewire::setUpdateRoute(function ($handle) {

return Route::post('/custom/livewire/update', $handle);

});

```
Now, instead of using `/livewire/update`, Livewire will send component updates to `/custom/livewire/update`.

Because Livewire allows you to register your own update route, you can declare any additional middleware you want Livewire to use directly inside `setUpdateRoute()`:

```php

Livewire::setUpdateRoute(function ($handle) {

return Route::post('/custom/livewire/update', $handle)

->middleware([...]);

});

```
#Customizing the asset URL
--------------------------

By default, Livewire will serve its JavaScript assets from the following URL: `https://example.com/livewire/livewire.js`. Additionally, Livewire will reference this asset from a script tag like so:

```php

<script src="/livewire/livewire.js" ...

```
If your application has global route prefixes due to localization or multi-tenancy, you can register your own endpoint that Livewire should use internally when fetching its JavaScript.

To use a custom JavaScript asset endpoint, you can register your own route inside `Livewire::setScriptRoute()`:

```php

Livewire::setScriptRoute(function ($handle) {

return Route::get('/custom/livewire/livewire.js', $handle);

});

```
Now, Livewire will load its JavaScript like so:

```php

<script src="/custom/livewire/livewire.js" ...

```
#Manually bundling Livewire and Alpine
--------------------------------------

By default, Alpine and Livewire are loaded using the `<script src="livewire.js">` tag, which means you have no control over the order in which these libraries are loaded. Consequently, importing and registering Alpine plugins, as shown in the example below, will no longer function:

```php

// Warning: This snippet demonstrates what NOT to do...

import Alpine from 'alpinejs'

import Clipboard from '@ryangjchandler/alpine-clipboard'

Alpine.plugin(Clipboard)

Alpine.start()

```
To address this issue, we need to inform Livewire that we want to use the ESM (ECMAScript module) version ourselves and prevent the injection of the `livewire.js` script tag. To achieve this, we must add the `@livewireScriptConfig` directive to our layout file (`resources/views/components/layouts/app.blade.php`):

```php

<html>

<head>

<!-- ... -->

@livewireStyles

@vite(['resources/js/app.js'])

</head>

<body>

{{ $slot }}

@livewireScriptConfig

</body>

</html>

```
When Livewire detects the `@livewireScriptConfig` directive, it will refrain from injecting the Livewire and Alpine scripts. If you are using the `@livewireScripts` directive to manually load Livewire, be sure to remove it. Make sure to add the `@livewireStyles` directive if it is not already present.

The final step is importing Alpine and Livewire in our `app.js` file, allowing us to register any custom resources, and ultimately starting Livewire and Alpine:

```php

import { Livewire, Alpine } from '../../vendor/livewire/livewire/dist/livewire.esm';

import Clipboard from '@ryangjchandler/alpine-clipboard'

Alpine.plugin(Clipboard)

Livewire.start()

```
Rebuild your assets after composer update

Make sure that if you are manually bundling Livewire and Alpine, that you rebuild your assets whenever you run `composer update`.

Not compatible with Laravel Mix

Laravel Mix will not work if you are manually bundling Livewire and AlpineJS. Instead, we recommend that you switch to Vite.

#Publishing Livewire's frontend assets
--------------------------------------

Publishing assets isn't necessary

Publishing Livewire's assets isn't necessary for Livewire to run. Only do this if you have a specific need for it.

If you prefer the JavaScript assets to be served by your web server not through Laravel, use the `livewire:publish` command:

```php

php artisan livewire:publish --assets

```
To keep assets up-to-date and avoid issues in future updates, we strongly recommend that you add the following command to your composer.json file:

```php

{

"scripts": {

"post-update-cmd": [

// Other scripts

"@php artisan vendor:publish --tag=livewire:assets --ansi --force"

]

}

}

```
On this page

* Publishing the configuration file
* Manually including Livewire's frontend assets
* Configuring Livewire's update endpoint
* Customizing the asset URL
* Manually bundling Livewire and Alpine
* Publishing Livewire's frontend assets

![Flux Ad](/images/flux_ad.jpg)

Pro UI Components

Flux · The official Livewire component library

Built by the folks behind Livewire and Alpine.