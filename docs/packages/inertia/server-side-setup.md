Source: https://inertiajs.com/docs/v3/installation/server-side-setup.md

# Server-Side Setup

The first step when installing Inertia is to configure your server-side framework. Inertia maintains an official server-side adapter for [Laravel](https://laravel.com/), and the community maintains [adapters](#other-frameworks) for Rails, Django, Phoenix, and many other frameworks.

Inertia is fine-tuned for Laravel, so the documentation examples on this website utilize Laravel. For examples of using Inertia with other server-side frameworks, please refer to the framework-specific documentation maintained by the relevant adapter.

> [card] [Laravel Starter Kits](https://laravel.com/docs/starter-kits)
>
> Laravel's starter kits provide out-of-the-box scaffolding for new Inertia applications.
>
> These starter kits are the absolute fastest way to start building a new Inertia project using Laravel and Vue or React. However, if you would like to manually install Inertia into your application, please consult the documentation below.

## Installation

**1. Install dependencies**

First, install the Inertia server-side adapter using the Composer package manager.

```bash theme={null}
composer require inertiajs/inertia-laravel
```

**2. Setup root template**

Next, create a `resources/views/app.blade.php` file. This root template will be loaded on the first page visit to your application. Inertia provides Blade components for rendering the head and body content.

```blade resources/views/app.blade.php theme={null}
<html>
    <head>
        <meta charset="utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1">
        @vite('resources/js/app.js')
        <x-inertia::head />
    </head>
    <body>
        <x-inertia::app />
    </body>
</html>
```

For React applications, it's recommended to include the `@viteReactRefresh` directive before the `@vite` directive to enable Fast Refresh in development. You may also pass the current page component to the `@vite` directive to [preload the initial page](https://inertiajs.com/docs/v3/advanced/code-splitting.md#preloading-the-initial-page).

The `<x-inertia::app>` component renders a `<div>` element with an `id` of `app`. This element serves as the mounting point for your JavaScript application. You may customize the `id` by passing a different value to the component.

```blade theme={null}
<x-inertia::app id="custom-app-id" />
```

If you change the `id` of the root element, be sure to update it [client-side](https://inertiajs.com/docs/v3/installation/client-side-setup.md#defining-a-root-element) as well.

The `<x-inertia::head>` component also accepts [fallback content](https://inertiajs.com/docs/v3/the-basics/title-and-meta.md#ssr-fallback) via its slot for managing head elements when [SSR](https://inertiajs.com/docs/v3/advanced/server-side-rendering.md) is not active.

By default, Inertia's Laravel adapter will assume your root template is named `app.blade.php`. You may change this using the `Inertia::setRootView()` method.

**3. Register middleware**

Next, set up the Inertia middleware by publishing the `HandleInertiaRequests` middleware to your application with the following Artisan command.

```sh theme={null}
php artisan inertia:middleware
```

Once the middleware has been published, append the `HandleInertiaRequests` middleware to the `web` middleware group in your application's `bootstrap/app.php` file.

```php theme={null}
use App\Http\Middleware\HandleInertiaRequests;

->withMiddleware(function (Middleware $middleware) {
    $middleware->web(append: [
        HandleInertiaRequests::class,
    ]);
})
```

This middleware provides a `version()` method for setting your [asset version](https://inertiajs.com/docs/v3/advanced/asset-versioning.md), as well as a `share()` method for defining [shared data](https://inertiajs.com/docs/v3/data-props/shared-data.md).

**4. Create your first response**

That's it, you're ready to start creating Inertia [pages](https://inertiajs.com/docs/v3/the-basics/pages.md) and rendering them via [responses](https://inertiajs.com/docs/v3/the-basics/responses.md).

```php theme={null}
use Inertia\Inertia;

class EventsController extends Controller
{
    public function show(Event $event)
    {
        return Inertia::render('Event/Show', [
            'event' => $event->only(
                'id',
                'title',
                'start_date',
                'description',
            ),
        ]);
    }
}
```

## Blade Directives

Prior to v3, Inertia used `@inertiaHead` and `@inertia` Blade directives to render head and body content. These directives are still supported but do not offer SSR head [fallback content](https://inertiajs.com/docs/v3/the-basics/title-and-meta.md#ssr-fallback). The Blade components above are recommended for new applications.

```blade resources/views/app.blade.php theme={null}
<html>
    <head>
        @vite('resources/js/app.js')
        @inertiaHead
    </head>
    <body>
        @inertia
    </body>
</html>
```

You may customize the root element `id` by passing a value to the directive: `@inertia('custom-app-id')`.

## Other Frameworks

Inertia works with any server-side framework that implements the [Inertia protocol](https://inertiajs.com/docs/v3/core-concepts/the-protocol.md). You may use one of the community adapters or build your own.

> [card] [Community Adapters](https://inertiajs.com/docs/v3/installation/community-adapters.md)
>
> Adapters for Rails, Django, Phoenix, Symfony, and more.

> [card] [Building an Adapter](https://inertiajs.com/docs/v3/advanced/building-an-adapter.md)
>
> Bring Inertia to a framework that doesn't have an adapter yet.
