# Livewire - Wire Bind

Source: https://livewire.laravel.com/docs/4.x/wire-bind

wire:bind
=========


`wire:bind` is a directive that dynamically binds HTML attributes to component properties or expressions. Unlike using Blade's attribute syntax, `wire:bind` updates the attribute reactively on the client without requiring a full re-render.

If you are familiar with Alpine's `x-bind` directive, the two are essentially the same.

Basic usage¶
------------

```php
<input wire:model="message" wire:bind:class="message.length > 240 && 'text-red-500'">
```
As the user types, `wire:bind:class` reacts to the message length and applies the class instantly on the client.

Common use cases¶
-----------------

### Binding styles¶

```php
<div wire:bind:style="{ 'color': textColor, 'font-size': fontSize + 'px' }">

Styled text

</div>
```
### Binding href¶

```php
<a wire:bind:href="url">Dynamic link</a>
```
### Binding disabled state¶

```php
<button wire:bind:disabled="isArchived">Delete</button>
```
### Binding data attributes¶

```php
<div wire:bind:data-count="count">...</div>
```
Reference¶
----------

```php
wire:bind:{attribute}="expression"
```
Replace `{attribute}` with any valid HTML attribute name (e.g., `class`, `style`, `href`, `disabled`, `data-*`).

This directive has no modifiers.

Ecosystem sponsor


Postmark delivers your app's transactional and broadcast email fast, with industry-leading deliverability and the tools developers need to see exactly what happened to every message.
postmarkapp.com ↗

Return to

Teleport

Continue to

wire:click