# Livewire - Morphing

Source: https://livewire.laravel.com/docs/morphing

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

Morphing
========

Are you a visual learner?

Master Livewire with our in-depth screencasts

Watch now

When a Livewire component updates the browser's DOM, it does so in an intelligent way we call "morphing". The term *morph* is in contrast with a word like *replace*.

Instead of *replacing* a component's HTML with newly rendered HTML every time a component is updated, Livewire dynamically compares the current HTML with the new HTML, identifies differences, and makes surgical changes to the HTML only in the places where changes are needed.

This has the benefit of preserving existing, un-changed elements on a component. For example, event listeners, focus state, and form input values are all preserved between Livewire updates. Of course, morphing also offers increased performance compared to wiping and re-rending new DOM on every update.

#How morphing works
-------------------

To understand how Livewire determines which elements to update between Livewire requests, consider this simple `Todos` component:

```php

class Todos extends Component

{

public $todo = '';

public $todos = [

'first',

'second',

];

public function add()

{

$this->todos[] = $this->todo;

}

}

```
```php

<form wire:submit="add">

<ul>

@foreach ($todos as $item)

<li>{{ $item }}</li>

@endforeach

</ul>

<input wire:model="todo">

</form>

```
The initial render of this component will output the following HTML:

```php

<form wire:submit="add">

<ul>

<li>first</li>

<li>second</li>

</ul>

<input wire:model="todo">

</form>

```
Now, imagine you typed "third" into the input field and pressed the `[Enter]` key. The newly rendered HTML would be:

```php

<form wire:submit="add">

<ul>

<li>first</li>

<li>second</li>

+        <li>third</li>

</ul>

<input wire:model="todo">

</form>

```
When Livewire processes the component update, it *morphs* the original DOM into the newly rendered HTML. The following visualization should intuitively give you an understanding of how it works:

As you can see, Livewire walks both HTML trees simultaneously. As it encounters each element in both trees, it compares them for changes, additions, and removals. If it detects one, it surgically makes the appropriate change.

#Morphing shortcomings
----------------------

The following are scenarios where morphing algorithms fail to correctly identify the change in HTML trees and therefore cause problems in your application.

### #Inserting intermediate elements

Consider the following Livewire Blade template for a fictitious `CreatePost` component:

```php

<form wire:submit="save">

<div>

<input wire:model="title">

</div>

@if ($errors->has('title'))

<div>{{ $errors->first('title') }}</div>

@endif

<div>

<button>Save</button>

</div>

</form>

```
If a user tries submitting the form, but encounters a validation error, the following problem occurs:

As you can see, when Livewire encounters the new `<div>` for the error message, it doesn't know whether to change the existing `<div>` in-place, or insert the new `<div>` in the middle.

To re-iterate what's happening more explicitly:

* Livewire encounters the first `<div>` in both trees. They are the same, so it continues.
* Livewire encounters the second `<div>` in both trees and thinks they are the same `<div>`, just one has changed contents. So instead of inserting the error message as a new element, it changes the `<button>` into an error message.
* Livewire then, after mistakenly modifying the previous element, notices an additional element at the end of the comparison. It then creates and appends the element after the previous one.
* Therefore, destroying, then re-creating an element that otherwise should have been simply moved.

This scenario is at the root of almost all morph-related bugs.

Here are a few specific problematic impacts of these bugs:

* Event listeners and element state are lost between updates
* Event listeners and state are misplaced across the wrong elements
* Entire Livewire components can be reset or duplicated as Livewire components are also simply elements in the DOM tree
* Alpine components and state can be lost or misplaced

Fortunately, Livewire has worked hard to mitigate these problems using the following approaches:

### #Internal look-ahead

Livewire has an additional step in its morphing algorithm that checks subsequent elements and their contents before changing an element.

This prevents the above scenario from happening in many cases.

Here is a visualization of the "look-ahead" algorithm in action:

### #Injecting morph markers

On the backend, Livewire automatically detects conditionals inside Blade templates and wraps them in HTML comment markers that Livewire's JavaScript can use as a guide when morphing.

Here's an example of the previous Blade template but with Livewire's injected markers:

```php

<form wire:submit="save">

<div>

<input wire:model="title">

</div>

<!--[if BLOCK]><![endif]-->

@if ($errors->has('title'))

<div>Error: {{ $errors->first('title') }}</div>

@endif

<!--[if ENDBLOCK]><![endif]-->

<div>

<button>Save</button>

</div>

</form>

```
With these markers injected into the template, Livewire can now more easily detect the difference between a change and an addition.

This feature is extremely beneficial to Livewire applications, but because it requires parsing templates via regex, it can sometimes fail to properly detect conditionals. If this feature is more of a hindrance than a help to your application, you can disable it with the following configuration in your application's `config/livewire.php` file:

```php

'inject_morph_markers' => false,

```
#### #Wrapping conditionals

If the above two solutions don't cover your situation, the most reliable way to avoid morphing problems is to wrap conditionals and loops in their own elements that are always present.

For example, here's the above Blade template rewritten with wrapping `<div>` elements:

```php

<form wire:submit="save">

<div>

<input wire:model="title">

</div>

<div>

@if ($errors->has('title'))

<div>{{ $errors->first('title') }}</div>

@endif

</div>

<div>

<button>Save</button>

</div>

</form>

```
Now that the conditional has been wrapped in a persistent element, Livewire will morph the two different HTML trees properly.

#### #Bypassing morphing

If you need to bypass morphing entirely for an element, you can use wire:replace to instruct livewire to replace all children of an element instead of attempting to morph the existing elements.

On this page

* How morphing works
* Morphing shortcomings
  + Inserting intermediate elements
  + Internal look-ahead
  + Injecting morph markers

![Flux Ad](/images/flux_ad.jpg)

Pro UI Components

Flux · The official Livewire component library

Built by the folks behind Livewire and Alpine.