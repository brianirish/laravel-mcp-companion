# Inertia - Routing

Source: https://inertiajs.com/routing

# Routing

## Defining routes

## Shorthand routes

## Generating URLs

## Customizing the Page URL

When using Inertia, all of your application's routes are defined server-side. This means that you don't need Vue Router or React Router. Instead, you can simply define Laravel routes and return Inertia responses from those routes.

If you have a page that doesn't need a corresponding controller method, like an "FAQ" or "about" page, you can route directly to a component via the Route::inertia() method.

Some server-side frameworks allow you to generate URLs from named routes. However, you will not have access to those helpers client-side. Here are a couple ways to still use named routes with Inertia.

The first option is to generate URLs server-side and include them as props. Notice in this example how we're passing the edit_url and create_url to the Users/Index component.

However, when using Laravel, the Ziggy library can make your named, server-side routes available to you via a global route() function. In fact, if you are developing an application using one of Laravel's starter kits, Ziggy is already configured for you.

If you're using the Vue plugin included with Ziggy, you may use the route() function directly in your templates.

When server-side rendering is enabled, you may pass an options object to the Ziggy plugin in your ssr.js file. This should include the route definitions and current location.

The page object includes a url that represents the current page's URL. By default, the Laravel adapter resolves this using the fullUrl() method on the Request instance, but strips the scheme and host so the result is a relative URL.

If you need to customize how the URL is resolved, you may provide a resolver within the urlResolver method of the Inertia HandleInertiaRequests middleware.

Alternatively, you may define the resolver using the Inertia::resolveUrlUsing() method.

`Route::inertia()`
`edit_url`
`create_url`
`Users/Index`
`route()`
`Customizing the Page URL The page object includes a url`
`fullUrl()`
`Request`
`urlResolver`
`HandleInertiaRequests`
`Alternatively, you may define the resolver using the Inertia::resolveUrlUsing()`
[Inertia responses](/responses)
[page](/pages)
[Ziggy](https://github.com/tighten/ziggy)
[starter kits](https://laravel.com/docs/starter-kits)
[server-side rendering](/server-side-rendering)
[page object](/the-protocol#the-page-object)