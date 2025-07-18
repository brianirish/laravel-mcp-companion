# Livewire - Wire Click

Source: https://livewire.laravel.com/docs/wire-click

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

wire:click
==========

Are you a visual learner?

Master Livewire with our in-depth screencasts

Watch now

Livewire provides a simple `wire:click` directive for calling component methods (aka actions) when a user clicks a specific element on the page.

For example, given the `ShowInvoice` component below:

```php

<?php

namespace App\Livewire;

use Livewire\Component;

use App\Models\Invoice;

class ShowInvoice extends Component

{

public Invoice $invoice;

public function download()

{

return response()->download(

$this->invoice->file_path, 'invoice.pdf'

);

}

}

```
You can trigger the `download()` method from the class above when a user clicks a "Download Invoice" button by adding `wire:click="download"`:

```php

<button type="button" wire:click="download">

Download Invoice

</button>

```
#Using `wire:click` on links
----------------------------

When using `wire:click` on `<a>` tags, you must append `.prevent` to prevent the default handling of a link in the browser. Otherwise, the browser will visit the provided link and update the page's URL.

```php

<a href="#" wire:click.prevent="...">

```
#Going deeper
-------------

The `wire:click` directive is just one of many different available event listeners in Livewire. For full documentation on its (and other event listeners) capabilities, visit the Livewire actions documentation page.

On this page

* Using wire:click on links
* Going deeper

![Flux Ad](/images/flux_ad.jpg)

Pro UI Components

Flux · The official Livewire component library

Built by the folks behind Livewire and Alpine.