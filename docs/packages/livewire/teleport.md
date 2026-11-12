# Livewire - Teleport

Source: https://livewire.laravel.com/docs/teleport

Teleport
========

The official Livewire UI kit

Build polished Livewire apps faster.

Explore Flux Pro
→


Livewire allows you to *teleport* part of your template to another part of the DOM on the page entirely.

This is useful for things like nested dialogs. When nesting one dialog inside of another, the z-index of the parent modal is applied to the nested modal. This can cause problems with styling backdrops and overlays. To avoid this problem, you can use Livewire's `@teleport` directive to render each nested modal as siblings in the rendered DOM.

This functionality is powered by Alpine's `x-teleport` directive.

Basic usage¶
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
info

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

Ecosystem sponsor


Postmark delivers your app's transactional and broadcast email fast, with industry-leading deliverability and the tools developers need to see exactly what happened to every message.
postmarkapp.com ↗

Return to

File Downloads

Continue to

wire:bind