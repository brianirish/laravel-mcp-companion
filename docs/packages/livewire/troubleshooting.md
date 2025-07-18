# Livewire - Troubleshooting

Source: https://livewire.laravel.com/docs/troubleshooting

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

Troubleshooting
===============

Are you a visual learner?

Master Livewire with our in-depth screencasts

Watch now

Here at Livewire HQ, we try to remove problems from your pathway before you hit them. However, sometimes, there are some problems that we can't solve without introducing new ones, and other times, there are problems we can't anticipate.

Here are some common errors and scenarios you may encounter in your Livewire apps.

#Component mismatches
---------------------

When interacting with Livewire components on your page, you may encounter odd behavior or error messages like the following:

```php

Error: Component already initialized

```
```php

Error: Snapshot missing on Livewire component with id: ...

```
There are lots of reasons why you may encounter these messages, but the most common one is forgetting to add `wire:key` to elements and components inside a `@foreach` loop.

### #Adding `wire:key`

Any time you have a loop in your Blade templates using something like `@foreach`, you need to add `wire:key` to the opening tag of the first element within the loop:

```php

@foreach($posts as $post)

<div wire:key="{{ $post->id }}">

...

</div>

@endforeach

```
This ensures that Livewire can keep track of different elements in the loop when the loop changes.

The same applies to Livewire components within a loop:

```php

@foreach($posts as $post)

<livewire:show-post :$post :key="$post->id" />

@endforeach

```
However, here's a tricky scenario you might not have assumed:

When you have a Livewire component deeply nested inside a `@foreach` loop, you STILL need to add a key to it. For example:

```php

@foreach($posts as $post)

<div wire:key="{{ $post->id }}">

...

<livewire:show-post :$post :key="$post->id" />

...

</div>

@endforeach

```
Without the key on the nested Livewire component, Livewire will be unable to match the looped components up between network requests.

#### #Prefixing keys

Another tricky scenario you may run into is having duplicate keys within the same component. This often results from using model IDs as keys, which can sometimes collide.

Here's an example where we need to add a `post-` and an `author-` prefix to designate each set of keys as unique. Otherwise, if you have a `$post` and `$author` model with the same ID, you would have an ID collision:

```php

<div>

@foreach($posts as $post)

<div wire:key="post-{{ $post->id }}">...</div>

@endforeach

@foreach($authors as $author)

<div wire:key="author-{{ $author->id }}">...</div>

@endforeach

</div>

```
#Multiple instances of Alpine
-----------------------------

When installing Livewire, you may run into error messages like the following:

```php

Error: Detected multiple instances of Alpine running

```
```php

Alpine Expression Error: $wire is not defined

```
If this is the case, you likely have two versions of Alpine running on the same page. Livewire includes its own bundle of Alpine under the hood, so you must remove any other versions of Alpine on Livewire pages in your application.

One common scenario in which this happens is adding Livewire to an existing application that already includes Alpine. For example, if you installed the Laravel Breeze starter kit and then added Livewire later, you would run into this.

The fix for this is simple: remove the extra Alpine instance.

### #Removing Laravel Breeze's Alpine

If you are installing Livewire inside an existing Laravel Breeze (Blade + Alpine version), you need to remove the following lines from `resources/js/app.js`:

```php

import './bootstrap';

-import Alpine from 'alpinejs';

-

-window.Alpine = Alpine;

-

-Alpine.start();

```
### #Removing a CDN version of Alpine

Because Livewire version 2 and below didn't include Alpine by default, you may have included an Alpine CDN as a script tag in the head of your layout. In Livewire v3, you can remove this CDN altogether, and Livewire will automatically provide Alpine for you:

```php

...

-    <script defer src="https://cdn.jsdelivr.net/npm/[email protected]/dist/cdn.min.js"></script>

</head>

```
Note: you can also remove any additional Alpine plugins, as Livewire includes all Alpine plugins except `@alpinejs/ui`.

#Missing `@alpinejs/ui`
-----------------------

Livewire's bundled version of Alpine includes all Alpine plugins EXCEPT `@alpinejs/ui`. If you are using headless components from Alpine Components, which relies on this plugin, you may encounter errors like the following:

```php

Uncaught Alpine: no element provided to x-anchor

```
To fix this, you can simply include the `@alpinejs/ui` plugin as a CDN in your layout file like so:

```php

...

+    <script defer src="https://unpkg.com/@alpinejs/[email protected]/dist/cdn.min.js"></script>

</head>

```
Note: be sure to include the latest version of this plugin, which you can find on any component's documentation page.

On this page

* Component mismatches
  + Adding wire:key
* Multiple instances of Alpine
  + Removing Laravel Breeze's Alpine
  + Removing a CDN version of Alpine
* Missing @alpinejs/ui

![Flux Ad](/images/flux_ad.jpg)

Pro UI Components

Flux · The official Livewire component library

Built by the folks behind Livewire and Alpine.