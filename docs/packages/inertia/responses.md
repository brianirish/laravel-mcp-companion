# Inertia - Responses

Source: https://inertiajs.com/responses

# Responses

## Creating responses

## Root template data

## Maximum response size

Creating an Inertia response is simple. To get started, invoke the Inertia::render() method within your controller or route, providing both the name of the JavaScript page component that you wish to render, as well as any props (data) for the page.

In the example below, we will pass a single prop (event) which contains four attributes ( id, title, start_date and description) to the Event/Show page component.

There are situations where you may want to access your prop data in your application's root Blade template. For example, you may want to add a meta description tag, Twitter card meta tags, or Facebook Open Graph meta tags. You can access this data via the $page variable.

Sometimes you may even want to provide data to the root template that will not be sent to your JavaScript page / component. This can be accomplished by invoking the withViewData method.

After invoking the withViewData method, you can access the defined data as you would typically access a Blade template variable.

To enable client-side history navigation, all Inertia server responses are stored in the browser's history state. However, keep in mind that some browsers impose a size limit on how much data can be saved within the history state.

For example, Firefox has a size limit of 16 MiB and throws a NS_ERROR_ILLEGAL_VALUE error if you exceed this limit. Typically, this is much more data than you'll ever practically need when building applications.

`Inertia::render()`
`event`
`id`
`title`
`start_date`
`description`
`Event/Show`
`$page`
`withViewData`
`NS_ERROR_ILLEGAL_VALUE`
[JavaScript page component](/pages)
[Firefox](https://developer.mozilla.org/en-US/docs/Web/API/History/pushState)
Within Laravel applications, the Event/Show page would typically correspond to the file located at resources/js/Pages/Event/Show.(js|vue|svelte).
