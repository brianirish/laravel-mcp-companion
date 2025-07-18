# Livewire - Wire Offline

Source: https://livewire.laravel.com/docs/wire-offline

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

wire:offline
============

Are you a visual learner?

Master Livewire with our in-depth screencasts

Watch now

In certain circumstances it can be helpful for your users to know if they are currently connected to the internet.

If for example, you have built a blogging platform on Livewire, you may want to notify your users in some way if they are offline so that they don't draft an entire blog post without the ability for Livewire to save it to the database.

Livewire make this trivial by providing the `wire:offline` directive. By attaching `wire:offline` to an element in your Livewire component, it will be hidden by default and only be displayed when Livewire detects the network connection has been interrupted and is unavailable. It will then disappear again when the network has regained connection.

For example:

```php

<p class="alert alert-warning" wire:offline>

Whoops, your device has lost connection. The web page you are viewing is offline.

</p>

```
On this page

![Flux Ad](/images/flux_ad.jpg)

Pro UI Components

Flux · The official Livewire component library

Built by the folks behind Livewire and Alpine.