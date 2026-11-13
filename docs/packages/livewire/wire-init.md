# Livewire - Wire Init

Source: https://livewire.laravel.com/docs/4.x/wire-init

wire:init
=========


Livewire offers a `wire:init` directive to run an action as soon as the component is rendered. This can be helpful in cases where you don't want to hold up the entire page load, but want to load some data immediately after the page load.

```php
<div wire:init="loadPosts">

<!-- ... -->

</div>
```
The `loadPosts` action will be run immediately after the Livewire component renders on the page.

In most cases however, Livewire's lazy loading feature is preferable to using `wire:init`.

Reference¶
----------

```php
wire:init="action"
```
This directive has no modifiers.

Ecosystem sponsor


Neon is a complete backend built around Lakebase Postgres, for developers, startups, and agent platforms, by Databricks.
neon.com ↗

Return to

wire:transition

Continue to

wire:intersect