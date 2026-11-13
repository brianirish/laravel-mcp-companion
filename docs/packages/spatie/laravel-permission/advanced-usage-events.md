# Spatie - Advanced Usage/Events

Source: https://spatie.be/docs/laravel-permission/v8/advanced-usage/events

SPATIE

Laravel Permission
==================

spatie.be/open-source

Docs

Laravel-permission

Advanced-usage

Events

Events
======

### On this page

1. Available Events

By default Events are not enabled, because not all apps need to fire events related to roles and permissions.

However, you may enable events by setting the `events_enabled => true` in `config/permission.php`

Note that the events can receive the role or permission details as a model ID or as an Eloquent record, or as an array or collection of ids or records. Be sure to inspect the parameter before acting on it.

##Available Events
------------------

The following events are available since `v7.0.0`:

```php
\Spatie\Permission\Events\RoleAttachedEvent::class
\Spatie\Permission\Events\RoleDetachedEvent::class
\Spatie\Permission\Events\PermissionAttachedEvent::class
\Spatie\Permission\Events\PermissionDetachedEvent::class
```
Between `v6.15.0` and `v7.0.0` the events did not have "Event" as a suffix, so they were:

```php
\Spatie\Permission\Events\RoleAttached::class
\Spatie\Permission\Events\RoleDetached::class
\Spatie\Permission\Events\PermissionAttached::class
\Spatie\Permission\Events\PermissionDetached::class
```
Cache

Custom Permission Check

Help us improve this page