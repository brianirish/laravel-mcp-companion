# Spatie - Basic Usage/Artisan

Source: https://spatie.be/docs/laravel-permission/v6/basic-usage/artisan

Docs

Laravel-permission

Basic-usage

Artisan Commands

Artisan Commands
================

### On this page

1. Creating roles and permissions with Artisan Commands
2. Displaying roles and permissions in the console
3. Resetting the Cache

##Creating roles and permissions with Artisan Commands
------------------------------------------------------

You can create a role or permission from the console with artisan commands.

```php
php artisan permission:create-role writer

```
```php
php artisan permission:create-permission "edit articles"

```
When creating permissions/roles for specific guards you can specify the guard names as a second argument:

```php
php artisan permission:create-role writer web

```
```php
php artisan permission:create-permission "edit articles" web

```
When creating roles you can also create and link permissions at the same time:

```php
php artisan permission:create-role writer web "create articles|edit articles"

```
When creating roles with teams enabled you can set the team id by adding the `--team-id` parameter:

```php
php artisan permission:create-role --team-id=1 writer
php artisan permission:create-role writer api --team-id=1

```
##Displaying roles and permissions in the console
-------------------------------------------------

There is also a `show` command to show a table of roles and permissions per guard:

```php
php artisan permission:show

```
##Resetting the Cache
---------------------

When you use the built-in functions for manipulating roles and permissions, the cache is automatically reset for you, and relations are automatically reloaded for the current model record.

See the Advanced-Usage/Cache section of these docs for detailed specifics.

If you need to manually reset the cache for this package, you may use the following artisan command:

```php
php artisan permission:cache-reset

```
Again, it is more efficient to use the API provided by this package, instead of manually clearing the cache.

Using multiple guards

Middleware

Help us improve this page