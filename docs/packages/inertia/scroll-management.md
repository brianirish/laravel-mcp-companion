# Inertia - Scroll Management

Source: https://inertiajs.com/scroll-management

# Scroll management

## Scroll resetting

## Scroll preservation

## Scroll regions

When navigating between pages, Inertia mimics default browser behavior by automatically resetting the scroll position of the document body (as well as any scroll regions you've defined) back to the top.

In addition, Inertia keeps track of the scroll position of each page and automatically restores that scroll position as you navigate forward and back in history.

Sometimes it's desirable to prevent the default scroll resetting when making visits. You can disable this behavior by setting the preserveScroll option to false.

If you'd like to only preserve the scroll position if the response includes validation errors, set the preserveScroll option to "errors".

You can also lazily evaluate the preserveScroll option based on the response by providing a callback.

When using an Inertia link, you can preserve the scroll position using the preserveScroll prop.

If your app doesn't use document body scrolling, but instead has scrollable elements (using the overflow CSS property), scroll resetting will not work.

In these situations, you must tell Inertia which scrollable elements to manage by adding the scroll-region attribute to the element.

`preserveScroll`
`false`
`overflow`
`scroll-region`
[Home](/)
[scroll regions](#scroll-regions)
[Inertia link](/links)