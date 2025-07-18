# Inertia - Shared Data

Source: https://inertiajs.com/shared-data

# Shared data

## Sharing data

## Accessing shared data

## Flash messages

Sometimes you need to access specific pieces of data on numerous pages within your application. For example, you may need to display the current user in the site header. Passing this data manually in each response across your entire application is cumbersome. Thankfully, there is a better option: shared data.

Inertia's server-side adapters all provide a method of making shared data available for every request. This is typically done outside of your controllers. Shared data will be automatically merged with the page props provided in your controller.

In Laravel applications, this is typically handled by the HandleInertiaRequests middleware that is automatically installed when installing the server-side adapter.

Alternatively, you can manually share data using the Inertia::share method.

Once you have shared the data server-side, you will be able to access it within any of your pages or components. Here's an example of how to access shared data in a layout component.

Another great use-case for shared data is flash messages. These are messages stored in the session only for the next request. For example, it's common to set a flash message after completing a task and before redirecting to a different page.

Here's a simple way to implement flash messages in your Inertia applications. First, share the flash message on each request.

Next, display the flash message in a frontend component, such as the site layout.

`HandleInertiaRequests`
`Inertia::share`
[server-side adapter](/server-side-setup#middleware)
method where you can define the data that is automatically shared with each Inertia response.
