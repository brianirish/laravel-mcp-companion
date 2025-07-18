# Inertia - Partial Reloads

Source: https://inertiajs.com/partial-reloads

# Partial reloads

## Only certain props

## Except certain props

## Router shorthand

## Using links

## Lazy data evaluation

When making visits to the same page you are already on, it's not always necessary to re-fetch all of the page's data from the server. In fact, selecting only a subset of the data can be a helpful performance optimization if it's acceptable that some page data becomes stale. Inertia makes this possible via its "partial reload" feature.

As an example, consider a "user index" page that includes a list of users, as well as an option to filter the users by their company. On the first request to the page, both the users and companies props are passed to the page component. However, on subsequent visits to the same page (maybe to filter the users), you can request only the users data from the server without requesting the companies data. Inertia will then automatically merge the partial data returned from the server with the data it already has in memory client-side.

To perform a partial reload, use the only visit option to specify which data the server should return. This option should be an array of keys which correspond to the keys of the props.

In addition to the only visit option you can also use the except option to specify which data the server should exclude. This option should also be an array of keys which correspond to the keys of the props.

Since partial reloads can only be made to the same page component the user is already on, it almost always makes sense to just use the router.reload() method, which automatically uses the current URL.

It's also possible to perform partial reloads with Inertia links using the only property.

For partial reloads to be most effective, be sure to also use lazy data evaluation when returning props from your server-side routes or controllers. This can be accomplished by wrapping all optional page data in a closure.

When Inertia performs a request, it will determine which data is required and only then will it evaluate the closure. This can significantly increase the performance of pages that contain a lot of optional data.

Additionally, Inertia provides an Inertia::optional() method to specify that a prop should never be included unless explicitly requested using the only option:

On the inverse, you can use the Inertia::always() method to specify that a prop should always be included, even if it has not been explicitly required in a partial reload.

Here's a summary of each approach:

`users`
`companies`
`only`
`except`
`router.reload()`
`Inertia::optional()`
`Inertia::always()`
[Show active](/users?active=true)
, [
                  // ALWAYS included on standard visits
                  // OPTIONALLY included on partial reloads
                  // ALWAYS evaluated
