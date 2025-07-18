# Livewire - Wire Submit

Source: https://livewire.laravel.com/docs/wire-submit

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

wire:submit
===========

Are you a visual learner?

Master Livewire with our in-depth screencasts

Watch now

Livewire makes it easy to handle form submissions via the `wire:submit` directive. By adding `wire:submit` to a `<form>` element, Livewire will intercept the form submission, prevent the default browser handling, and call any Livewire component method.

Here's a basic example of using `wire:submit` to handle a "Create Post" form submission:

```php

<?php

namespace App\Livewire;

use Livewire\Component;

use App\Models\Post;

class CreatePost extends Component

{

public $title = '';

public $content = '';

public function save()

{

Post::create([

'title' => $this->title,

'content' => $this->content,

]);

$this->redirect('/posts');

}

public function render()

{

return view('livewire.create-post');

}

}

```
```php

<form wire:submit="save">

<input type="text" wire:model="title">

<textarea wire:model="content"></textarea>

<button type="submit">Save</button>

</form>

```
In the above example, when a user submits the form by clicking "Save", `wire:submit` intercepts the `submit` event and calls the `save()` action on the server.

Livewire automatically calls`preventDefault()`

`wire:submit` is different than other Livewire event handlers in that it internally calls `event.preventDefault()` without the need for the `.prevent` modifier. This is because there are very few instances you would be listening for the `submit` event and NOT want to prevent it's default browser handling (performing a full form submission to an endpoint).

Livewire automatically disables forms while submitting

By default, when Livewire is sending a form submission to the server, it will disable form submit buttons and mark all form inputs as `readonly`. This way a user cannot submit the same form again until the initial submission is complete.

#Going deeper
-------------

`wire:submit` is just one of many event listeners that Livewire provides. The following two pages provide much more complete documentation on using `wire:submit` in your application:

* Responding to browser events with Livewire
* Creating forms in Livewire

On this page

* Going deeper

![Flux Ad](/images/flux_ad.jpg)

Pro UI Components

Flux · The official Livewire component library

Built by the folks behind Livewire and Alpine.