# Livewire - Downloads

Source: https://livewire.laravel.com/docs/downloads

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

File Downloads
==============

Are you a visual learner?

Master Livewire with our in-depth screencasts

Watch now

File downloads in Livewire work much the same as in Laravel itself. Typically, you can use any Laravel download utility inside a Livewire component, and it should work as expected.

However, behind the scenes, file downloads are handled differently than in a standard Laravel application. When using Livewire, the file's contents are Base64 encoded, sent to the frontend, and decoded back into binary to be downloaded directly from the client.

#Basic usage
------------

Triggering a file download in Livewire is as simple as returning a standard Laravel download response.

Below is an example of a `ShowInvoice` component that contains a "Download" button to download the invoice PDF:

```php

<?php

namespace App\Livewire;

use Livewire\Component;

use App\Models\Invoice;

class ShowInvoice extends Component

{

public Invoice $invoice;

public function mount(Invoice $invoice)

{

$this->invoice = $invoice;

}

public function download()

{

return response()->download(

$this->invoice->file_path, 'invoice.pdf'

);

}

public function render()

{

return view('livewire.show-invoice');

}

}

```
```php

<div>

<h1>{{ $invoice->title }}</h1>

<span>{{ $invoice->date }}</span>

<span>{{ $invoice->amount }}</span>

<button type="button" wire:click="download">Download</button>

</div>

```
Just like in a Laravel controller, you can also use the `Storage` facade to initiate downloads:

```php

public function download()

{

return Storage::disk('invoices')->download('invoice.csv');

}

```
#Streaming downloads
--------------------

Livewire can also stream downloads; however, they aren't truly streamed. The download isn't triggered until the file's contents are collected and delivered to the browser:

```php

public function download()

{

return response()->streamDownload(function () {

echo '...'; // Echo download contents directly...

}, 'invoice.pdf');

}

```
#Testing file downloads
-----------------------

Livewire also provides a `->assertFileDownloaded()` method to easily test that a file was downloaded with a given name:

```php

use App\Models\Invoice;

/** @test */

public function can_download_invoice()

{

$invoice = Invoice::factory();

Livewire::test(ShowInvoice::class)

->call('download')

->assertFileDownloaded('invoice.pdf');

}

```
You can also test to ensure a file was not downloaded using the `->assertNoFileDownloaded()` method:

```php

use App\Models\Invoice;

/** @test */

public function does_not_download_invoice_if_unauthorised()

{

$invoice = Invoice::factory();

Livewire::test(ShowInvoice::class)

->call('download')

->assertNoFileDownloaded();

}

```
On this page

* Basic usage
* Streaming downloads
* Testing file downloads

![Flux Ad](/images/flux_ad.jpg)

Pro UI Components

Flux · The official Livewire component library

Built by the folks behind Livewire and Alpine.