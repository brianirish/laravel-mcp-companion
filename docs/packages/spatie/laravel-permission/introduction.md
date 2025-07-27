# Spatie - Introduction

Source: https://spatie.be/docs/laravel-permission/v6/introduction

Docs

Laravel-permission

Introduction

Laravel Permission
==================

Associate users with roles and permissions
------------------------------------------

Use this package to easily add permissions or roles to users in your Laravel app.

Repository

Open Issues

68,977,504

12,584

Introduction
------------

This package allows you to manage user permissions and roles in a database.

Once installed you can do stuff like this:

```php
// Adding permissions to a user
$user->givePermissionTo('edit articles');

// Adding permissions via a role
$user->assignRole('writer');

$role->givePermissionTo('edit articles');

```
If you're using multiple guards we've got you covered as well. Every guard will have its own set of permissions and roles that can be assigned to the guard's users. Read about it in the using multiple guards section.

Because all permissions will be registered on Laravel's gate, you can check if a user has a permission with Laravel's default `can` function:

```php
$user->can('edit articles');

```
and Blade directives:

```php
@can('edit articles')
...
@endcan

```
About us

Support us

Help us improve this page