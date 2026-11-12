Source: https://inertiajs.com/docs/v3/security/authentication.md

# Authentication

One benefit of using Inertia is that you don't need a special authentication system, such as OAuth, to connect to your API. Since your data is provided through your controllers and served from the same domain as your JavaScript components, you don't need to set up CORS.

Instead, you can use whatever authentication system your server-side framework provides. Typically, this is a session-based system, such as Laravel's.

> [card] [Laravel Starter Kits](https://laravel.com/docs/starter-kits)
>
> Laravel's starter kits provide out-of-the-box scaffolding for new Inertia applications, including authentication.
