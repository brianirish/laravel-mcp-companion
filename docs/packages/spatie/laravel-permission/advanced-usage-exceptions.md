# Spatie - Advanced Usage/Exceptions

Source: https://spatie.be/docs/laravel-permission/v6/advanced-usage/exceptions

Docs

Laravel-permission

Advanced-usage

Exceptions

Exceptions
==========

If you need to override exceptions thrown by this package, you can simply use normal Laravel practices for handling exceptions.

An example is shown below for your convenience, but nothing here is specific to this package other than the name of the exception.

You can find all the exceptions added by this package in the code here: https://github.com/spatie/laravel-permission/tree/main/src/Exceptions

**Laravel 10: app/Exceptions/Handler.php**

```php

public function register()
{
    $this->renderable(function (\Spatie\Permission\Exceptions\UnauthorizedException $e, $request) {
        return response()->json([
            'responseMessage' => 'You do not have the required authorization.',
            'responseStatus'  => 403,
        ]);
    });
}

```
**Laravel 11: bootstrap/app.php**

```php

->withExceptions(function (Exceptions $exceptions) {
    $exceptions->render(function (\Spatie\Permission\Exceptions\UnauthorizedException $e, $request) {
        return response()->json([
            'responseMessage' => 'You do not have the required authorization.',
            'responseStatus'  => 403,
        ]);
    });
}

```
Database Seeding

Extending

Help us improve this page