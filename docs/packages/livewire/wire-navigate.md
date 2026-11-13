# Livewire - Wire Navigate

Source: https://livewire.laravel.com/docs/4.x/wire-navigate

wire:navigate
=============


Livewire's `wire:navigate` feature makes page navigation much faster, providing an SPA-like experience for your users.

This page is a simple reference for the `wire:navigate` directive. Be sure to read the page on Livewire's Navigate feature for more complete documentation.

Below is a simple example of adding `wire:navigate` to links in a nav bar:

```php
<nav>

<a href="/" wire:navigate>Dashboard</a>

<a href="/posts" wire:navigate>Posts</a>

<a href="/users" wire:navigate>Users</a>

</nav>
```
When any of these links are clicked, Livewire will intercept the click and, instead of allowing the browser to perform a full page visit, Livewire will fetch the page in the background and swap it with the current page (resulting in much faster and smoother page navigation).

`wire:navigate` only intercepts same-origin page visits. External links, links with a non-`_self` target, download links, and URLs such as `mailto:` or `tel:` automatically fall back to the browser's default behavior.

Styling active links with data-current¶
---------------------------------------

Livewire automatically adds a `data-current` attribute to any `wire:navigate` link that matches the current page URL. This allows you to style active navigation links using CSS or Tailwind without any additional directives:

```php
<nav>

<a href="/" wire:navigate class="data-current:font-bold">Dashboard</a>

<a href="/posts" wire:navigate class="data-current:font-bold">Posts</a>

<a href="/users" wire:navigate class="data-current:font-bold">Users</a>

</nav>
```
The `data-current` attribute is added and removed automatically as users navigate between pages. Read more about highlighting active links in the Navigate documentation.

Prefetching pages on hover¶
---------------------------

By adding the `.hover` modifier, Livewire will pre-fetch a page after a user hovers over or focuses a link for 60 milliseconds. This gives both mouse and keyboard users a head start before following the link.

```php
<a href="/" wire:navigate.hover>Dashboard</a>
```
Going deeper¶
-------------

For more complete documentation on this feature, visit Livewire's navigate documentation page.

See also¶
---------

* **Navigate** — Complete guide to SPA navigation
* **Pages** — Create routable page components
* **@persist** — Persist elements during navigation

Reference¶
----------

```php
wire:navigate
```
### Modifiers¶

| Modifier | Description |
| --- | --- |
| `.hover` | Prefetches the page when the user hovers over or focuses the link |

Ecosystem sponsor


Postmark delivers your app's transactional and broadcast email fast, with industry-leading deliverability and the tools developers need to see exactly what happened to every message.
postmarkapp.com ↗

Return to

wire:loading

Continue to

wire:current