# Livewire - Offline

Source: https://livewire.laravel.com/docs/offline

wire:offline
============

The official Livewire UI kit

Build polished Livewire apps faster.

Explore Flux Pro
→


In real-time applications, it can be helpful to provide a visual indication that the user's device is no longer connected to the internet.

For example, if you have built a blogging platform on Livewire, you may want to notify your users if they are offline so that they don't draft an entire blog post without the ability for Livewire to save it to the database.

Livewire provides the `wire:offline` directive for such cases. By adding `wire:offline` to an element inside a Livewire component, it will be hidden by default and become visible when the user loses connection:

```php
<div wire:offline>

This device is currently offline.

</div>
```
The element will disappear again when the network connection is restored.

Toggling classes¶
-----------------

Adding the `class` modifier allows you to add a class to an element when the user loses their connection. The class will be removed again, once the user is back online:

```php
<div wire:offline.class="bg-red-300">
```
Or, using the `.remove` modifier, you can remove a class when a user loses their connection. In this example, the `bg-green-300` class will be removed from the `<div>` while the user has lost their connection:

```php
<div class="bg-green-300" wire:offline.class.remove="bg-green-300">
```
Toggling attributes¶
--------------------

The `.attr` modifier allows you to add an attribute to an element when the user loses their connection. In this example, the "Save" button will be disabled while the user has lost their connection:

```php
<button wire:offline.attr="disabled">Save</button>
```
Reference¶
----------

```php
wire:offline
```
### Modifiers¶

| Modifier | Description |
| --- | --- |
| `.class="class-name"` | Add a CSS class when offline |
| `.class.remove="class-name"` | Remove a CSS class when offline |
| `.attr="attribute"` | Add an HTML attribute when offline |

Ecosystem sponsor


Neon is a complete backend built around Lakebase Postgres, for developers, startups, and agent platforms, by Databricks.
neon.com ↗

Return to

wire:poll

Continue to

wire:ignore