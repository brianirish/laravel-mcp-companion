# Inertia - Manual Visits

Source: https://inertiajs.com/manual-visits

# Manual visits

## Method

## Data

## Custom headers

## File uploads

## Browser history

## Client side visits

## State preservation

## Scroll preservation

## Partial reloads

## Visit cancellation

## Event callbacks

In addition to creating links, it's also possible to manually make Inertia visits / requests programmatically via JavaScript. This is accomplished via the router.visit() method.

However, it's generally more convenient to use one of Inertia's shortcut request methods. These methods share all the same options as router.visit().

The reload() method is a convenient, shorthand method that automatically visits the current page with preserveState and preserveScroll both set to true, making it the perfect method to invoke when you just want to reload the current page's data.

When making manual visits, you may use the method option to set the request's HTTP method to get, post, put, patch or delete. The default method is get.

You may use the data option to add data to the request.

For convenience, the get(), post(), put(), and patch() methods all accept data as their second argument.

The headers option allows you to add custom headers to a request.

When making visits / requests that include files, Inertia will automatically convert the request data into a FormData object. If you would like the request to always use a FormData object, you may use the forceFormData option.

For more information on uploading files, please consult the dedicated file uploads documentation.

When making visits, Inertia automatically adds a new entry into the browser history. However, it's also possible to replace the current history entry by setting the replace option to true.

You can use the router.push and router.replace method to make client-side visits. This method is useful when you want to update the browser's history without making a server request.

All of the parameters are optional. By default, all passed paramaters will be merged with the current page. This means you are responsible for overriding the current page's URL, component, and props.

If you need access to the current page's props you can pass a function to the props option. This function will receive the current page's props as an argument and should return the new props.

By default, page visits to the same page create a fresh page component instance. This causes any local state, such as form inputs, scroll positions, and focus states to be lost.

However, in some situations, it's necessary to preserve the page component state. For example, when submitting a form, you need to preserve your form data in the event that form validation fails on the server.

For this reason, the post, put, patch, delete, and reload methods all set the preserveState option to true by default.

You can instruct Inertia to preserve the component's state when using the get method by setting the preserveState option to true.

If you'd like to only preserve state if the response includes validation errors, set the preserveState option to "errors".

You can also lazily evaluate the preserveState option based on the response by providing a callback.

When navigating between pages, Inertia mimics default browser behavior by automatically resetting the scroll position of the document body (as well as any scroll regions you've defined) back to the top of the page.

You can disable this behavior by setting the preserveScroll option to false.

If you'd like to only preserve the scroll position if the response includes validation errors, set the preserveScroll option to "errors".

You can also lazily evaluate the preserveScroll option based on the response by providing a callback.

For more information regarding this feature, please consult the scroll management documentation.

The only option allows you to request a subset of the props (data) from the server on subsequent visits to the same page, thus making your application more efficient since it does not need to retrieve data that the page is not interested in refreshing.

For more information on this feature, please consult the partial reloads documentation.

You can cancel a visit using a cancel token, which Inertia automatically generates and provides via the onCancelToken() callback prior to making the visit.

The onCancel() and onFinish() event callbacks will be executed when a visit is cancelled.

In addition to Inertia's global events, Inertia also provides a number of per-visit event callbacks.

Returning false from the onBefore() callback will cause the visit to be cancelled.

It's also possible to return a promise from the onSuccess() and onError() callbacks. When doing so, the "finish" event will be delayed until the promise has resolved.

`router.visit()`
`reload()`
`preserveState`
`preserveScroll`
`true`
`method`
`get`
`post`
`put`
`patch`
`delete`
`_method`
`data`
`get()`
`post()`
`put()`
`patch()`
`headers`
`FormData`
`forceFormData`
`replace`
`router.push`
`router.replace`
`reload`
`false`
`only`
`onCancelToken()`
`onCancel()`
`onFinish()`
`onBefore()`
`onSuccess()`
`onError()`
[creating links](/links)
[form method spoofing](https://laravel.com/docs/routing#form-method-spoofing)
[file uploads](/file-uploads)
[scroll regions](/scroll-management#scroll-regions)
[scroll management](/scroll-management)
[partial reloads](/partial-reloads)
[global events](/events)