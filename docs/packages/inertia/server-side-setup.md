# Inertia - Server Side Setup

Source: https://inertiajs.com/server-side-setup

# Server-side setup

## Laravel starter kits

## Install dependencies

## Root template

## Middleware

## Creating responses

The first step when installing Inertia is to configure your server-side framework. Inertia maintains an official server-side adapter for Laravel. For other frameworks, please see the community adapters.

Inertia is fine-tuned for Laravel, so the documentation examples on this website utilize Laravel. For examples of using Inertia with other server-side frameworks, please refer to the framework specific documentation maintained by that adapter.

Laravel's starter kits, Breeze and Jetstream, provide out-of-the-box scaffolding for new Inertia applications. These starter kits are the absolute fastest way to start building a new Inertia project using Laravel and Vue or React. However, if you would like to manually install Inertia into your application, please consult the documentation below.

First, install the Inertia server-side adapter using the Composer package manager.

Next, setup the root template that will be loaded on the first page visit to your application. This template should include your site's CSS and JavaScript assets, along with the @inertia and @inertiaHead directives.

The @inertia directive renders a element with an id of app. This element serves as the mounting point for your JavaScript application. You may customize the id by passing a different value to the directive.

If you change the id of the root element, be sure to update it client-side as well.

By default, Inertia's Laravel adapter will assume your root template is named app.blade.php. If you would like to use a different root view, you can change it using the Inertia::setRootView() method.

Next we need to setup the Inertia middleware. You can accomplish this by publishing the HandleInertiaRequests middleware to your application, which can be done using the following Artisan command.

Once the middleware has been published, append the HandleInertiaRequests middleware to the web middleware group in your application's bootstrap/app.php file.

This middleware provides a version() method for setting your asset version, as well as a share() method for defining shared data.

That's it, you're all ready to go server-side! Now you're ready to start creating Inertia pages and rendering them via responses.

`@inertia`
`@inertiaHead`
`@viteReactRefresh`
`@vite`
`id`
`app`
`app.blade.php`
`Inertia::setRootView()`
`HandleInertiaRequests`
`Once the middleware has been published, append the HandleInertiaRequests`
`web`
`bootstrap/app.php`
`share()`
[Laravel](https://laravel.com/)
[community adapters](/community-adapters)
[starter kits](https://laravel.com/docs/starter-kits)
[client-side](/client-side-setup#defining-a-root-element)
[asset version](/asset-versioning)
[shared data](/shared-data)
[pages](/pages)
[responses](/responses)