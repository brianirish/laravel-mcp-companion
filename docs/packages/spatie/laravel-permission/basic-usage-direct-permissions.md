# Spatie - Basic Usage/Direct Permissions

Source: https://spatie.be/docs/laravel-permission/v6/basic-usage/direct-permissions

Docs

Laravel-permission

Basic-usage

Direct Permissions

Direct Permissions
==================

### On this page

1. Best Practice
2. Direct Permissions to Users
3. Checking Direct Permissions

##Best Practice
---------------

INSTEAD OF DIRECT PERMISSIONS, it is better to assign permissions to Roles, and then assign Roles to Users.

See the Roles vs Permissions section of the docs for a deeper explanation.

HOWEVER, If you have reason to directly assign individual permissions to specific users (instead of to roles which are assigned to those users), you can do that as well:

##Direct Permissions to Users
-----------------------------

### ##Giving/Revoking direct permissions

A permission can be given to any user:

```php
$user->givePermissionTo('edit articles');

// You can also give multiple permission at once
$user->givePermissionTo('edit articles', 'delete articles');

// You may also pass an array
$user->givePermissionTo(['edit articles', 'delete articles']);

```
A permission can be revoked from a user:

```php
$user->revokePermissionTo('edit articles');

```
Or revoke & add new permissions in one go:

```php
$user->syncPermissions(['edit articles', 'delete articles']);

```
##Checking Direct Permissions
-----------------------------

Like all permissions assigned via roles, you can check if a user has a permission by using Laravel's default `can` function. This will also allow you to use Super-Admin features provided by Laravel's Gate:

```php
$user->can('edit articles');

```
> NOTE: The following `hasPermissionTo`, `hasAnyPermission`, `hasAllPermissions` functions do not support Super-Admin functionality. Use `can`, `canAny` instead.

You can check if a user has a permission:

```php
$user->hasPermissionTo('edit articles');

```
Or you may pass an integer representing the permission id

```php
$user->hasPermissionTo('1');
$user->hasPermissionTo(Permission::find(1)->id);
$user->hasPermissionTo($somePermission->id);

```
You can check if a user has Any of an array of permissions:

```php
$user->hasAnyPermission(['edit articles', 'publish articles', 'unpublish articles']);

```
...or if a user has All of an array of permissions:

```php
$user->hasAllPermissions(['edit articles', 'publish articles', 'unpublish articles']);

```
You may also pass integers to lookup by permission id

```php
$user->hasAnyPermission(['edit articles', 1, 5]);

```
Basic Usage

Using Permissions via Roles

Help us improve this page