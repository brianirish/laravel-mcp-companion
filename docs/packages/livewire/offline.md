# Livewire - Offline

Source: https://livewire.laravel.com/docs/offline

Version 3.x

Version 3.x
Version 2.x
Version 1.x

* ##### Getting Started

  + Quickstart
  + Installation
  + Upgrade Guide

UI Components →

* ##### Essentials

  + Components
  + Properties
  + Actions
  + Forms
  + Events
  + Lifecycle Hooks
  + Nesting Components
  + Testing
* ##### Features

  + Alpine
  + Navigate
  + Lazy Loading
  + Validation
  + File Uploads
  + Pagination
  + URL Query Parameters
  + Computed Properties
  + Session Properties
  + Redirecting
  + File Downloads
  + Locked Properties
  + Request Bundling
  + Offline States
  + Teleport
* ##### HTML Directives

  + wire:click
  + wire:submit
  + wire:model
  + wire:loading
  + wire:navigate
  + wire:current
  + wire:cloak
  + wire:dirty
  + wire:confirm
  + wire:transition
  + wire:init
  + wire:poll
  + wire:offline
  + wire:ignore
  + wire:replace
  + wire:show
  + wire:stream
  + wire:text
* ##### Concepts

  + Morphing
  + Hydration
  + Nesting
* ##### Advanced

  + Troubleshooting
  + Security
  + JavaScript
  + Synthesizers
  + Contribution Guide
* ##### Packages

  + Volt

Offline States
==============

Are you a visual learner?

Master Livewire with our in-depth screencasts

Watch now

In real-time applications, it can be helpful to provide a visual indication that the user's device is no longer connected to the internet.

Livewire provides the `wire:offline` directive for such cases.

By adding `wire:offline` to an element inside a Livewire component, it will be hidden by default and become visible when the user loses connection:

```php

<div wire:offline>

This device is currently offline.

</div>

```
#Toggling classes
-----------------

Adding the `class` modifier allows you to add a class to an element when the user loses their connection. The class will be removed again, once the user is back online:

```php

<div wire:offline.class="bg-red-300">

```
Or, using the `.remove` modifier, you can remove a class when a user loses their connection. In this example, the `bg-green-300` class will be removed from the `<div>` while the user has lost their connection:

```php

<div class="bg-green-300" wire:offline.class.remove="bg-green-300">

```
#Toggling attributes
--------------------

The `.attr` modifier allows you to add an attribute to an element when the user loses their connection. In this example, the "Save" button will be disabled while the user has lost their connection:

```php

<button wire:offline.attr="disabled">Save</button>

```
On this page

* Toggling classes
* Toggling attributes

![Flux Ad](/images/flux_ad.jpg)

Pro UI Components

Flux · The official Livewire component library

Built by the folks behind Livewire and Alpine.