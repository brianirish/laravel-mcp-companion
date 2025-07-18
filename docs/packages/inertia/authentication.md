# Inertia - Authentication

Source: https://inertiajs.com/authentication

# Authentication

One of the benefits of using Inertia is that you don't need a special authentication system such as OAuth to connect to your data provider (API). Also, since your data is provided via your controllers, and housed on the same domain as your JavaScript components, you don't have to worry about setting up CORS.

Rather, when using Inertia, you can simply use whatever authentication system your server-side framework ships with. Typically, this will be a session based authentication system such as the authentication system included with Laravel.

Laravel's starter kits provide out-of-the-box scaffolding for new Inertia applications, including authentication.

[starter kits](https://laravel.com/docs/starter-kits)