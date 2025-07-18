# Livewire - Teleport

Source: https://livewire.laravel.com/docs/teleport

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

Teleport
========

Are you a visual learner?

Master Livewire with our in-depth screencasts

Watch now

Livewire allows you to *teleport* part of your template to another part of the DOM on the page entirely.

This is useful for things like nested dialogs. When nesting one dialog inside of another, the z-index of the parent modal is applied to the nested modal. This can cause problems with styling backdrops and overlays. To avoid this problem, you can use Livewire's `@teleport` directive to render each nested modal as siblings in the rendered DOM.

This functionality is powered by Alpine's `x-teleport` directive.

#Basic usage
------------

To *teleport* a portion of your template to another part of the DOM, you can wrap it in Livewire's `@teleport` directive.

Below is an example of using `@teleport` to render a modal dialog's contents at the end of the `<body>` element on the page:

```php

<div>

<!-- Modal -->

<div x-data="{ open: false }">

<button @click="open = ! open">Toggle Modal</button>

@teleport('body')

<div x-show="open">

Modal contents...

</div>

@endteleport

</div>

</div>

```
The `@teleport` selector can be any string you would normally pass into something like `document.querySelector()`.

You can learn more about `document.querySelector()` by consulting its MDN documentation.

Now, when the above Livewire template is rendered on the page, the *contents* portion of the modal will be rendered at the end of `<body>`:

```php

<body>

<!-- ... -->

<div x-show="open">

Modal contents...

</div>

</body>

```
You must teleport outside the component

Livewire only supports teleporting HTML outside your components. For example, teleporting a modal to the `<body>` tag is fine, but teleporting it to another element within your component will not work.

Teleporting only works with a single root element

Make sure you only include a single root element inside your `@teleport` statement.

On this page

* Basic usage

![Flux Ad](/images/flux_ad.jpg)

Pro UI Components

Flux · The official Livewire component library

Built by the folks behind Livewire and Alpine.