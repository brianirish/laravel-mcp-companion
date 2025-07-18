# Inertia - Links

Source: https://inertiajs.com/links

# Links

## Creating links

## Method

## Wayfinder

## Data

## Custom headers

## Browser history

## State preservation

## Scroll preservation

## Partial reloads

## Active states

## Data loading attribute

To create links to other pages within an Inertia app, you will typically use the Inertia component. This component is a light wrapper around a standard anchor link that intercepts click events and prevents full page reloads. This is how Inertia provides a single-page app experience once your application has been loaded.

To create an Inertia link, use the Inertia component. Any attributes you provide to this component will be proxied to the underlying HTML tag.

By default, Inertia renders links as anchor elements. However, you can change the tag using the as prop.

You can specify the HTTP request method for an Inertia link request using the method prop. The default method used by links is GET, but you can use the method prop to make POST, PUT, PATCH, and DELETE requests via links.

When using Wayfinder in conjunction with the Link component, you can simply pass the resulting object directly to the href prop. The Link will infer the HTTP method and URL directly from the Wayfinder object:

When making POST or PUT requests, you may wish to add additional data to the request. You can accomplish this using the data prop. The provided data can be an object or FormData instance.

The headers prop allows you to add custom headers to an Inertia link. However, the headers Inertia uses internally to communicate its state to the server take priority and therefore cannot be overwritten.

The replace prop allows you to specify the browser's history behavior. By default, page visits push (new) state (window.history.pushState) into the history; however, it's also possible to replace state (window.history.replaceState) by setting the replace prop to true. This will cause the visit to replace the current history state instead of adding a new history state to the stack.

You can preserve a page component's local state using the preserve-state prop. This will prevent a page component from fully re-rendering. The preserve-state prop is especially helpful on pages that contain forms, since you can avoid manually repopulating input fields and can also maintain a focused input.

You can use the preserveScroll prop to prevent Inertia from automatically resetting the scroll position when making a page visit.

For more information on managing scroll position, please consult the documentation on scroll management.

The only prop allows you to specify that only a subset of a page's props (data) should be retrieved from the server on subsequent visits to that page.

For more information on this topic, please consult the complete documentation on partial reloads.

It's often desirable to set an active state for navigation links based on the current page. This can be accomplished when using Inertia by inspecting the page object and doing string comparisons against the page.url and page.component properties.

You can perform exact match comparisons (===), startsWith() comparisons (useful for matching a subset of pages), or even more complex comparisons using regular expressions.

Using this approach, you're not limited to just setting class names. You can use this technique to conditionally render any markup on active state, such as different link text or even an SVG icon that represents the link is active.

While a link is making an active request, a data-loading attribute is added to the link element. This allows you to style the link while it's in a loading state. The attribute is removed once the request is complete.

`as`
`POST`
`PUT`
`PATCH`
`DELETE`
`method`
`GET`
`Link`
`href`
`data`
`object`
`FormData`
`headers`
`replace`
`window.history.pushState`
`window.history.replaceState`
`true`
`preserve-state`
`preserveScroll`
`only`
`page`
`page.url`
`page.component`
`===`
`startsWith()`
`data-loading`
[Home](/)
[Show active](/users?active=true)
[Users](/users)
[how Inertia provides a single-page app experience](/how-it-works)
[Wayfinder](https://github.com/laravel/wayfinder)
[scroll management](/scroll-management)
[partial reloads](/partial-reloads)
The use:inertia action can be applied to any HTML element.
