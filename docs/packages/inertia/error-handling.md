# Inertia - Error Handling

Source: https://inertiajs.com/error-handling

# Error handling

## Development

## Production

One of the advantages to working with a robust server-side framework is the built-in exception handling you get for free. For example, Laravel ships with a beautiful error reporting tool which displays a nicely formatted stack trace in local development.

The challenge is, if you're making an XHR request (which Inertia does) and you hit a server-side error, you're typically left digging through the network tab in your browser's devtools to diagnose the problem.

Inertia solves this issue by showing all non-Inertia responses in a modal. This means you get the same beautiful error-reporting you're accustomed to, even though you've made that request over XHR.

In production you will want to return a proper Inertia error response instead of relying on the modal-driven error reporting that is present during development. To accomplish this, you'll need to update your framework's default exception handler to return a custom error page.

When building Laravel applications, you can accomplish this by using the respond exception method in your application's bootstrap/app.php file.

You may have noticed we're returning an ErrorPage page component in the example above. You'll need to actually create this component, which will serve as the generic error page for your application. Here's an example error component you can use as a starting point.

`respond`
`bootstrap/app.php`
`ErrorPage`
re
        typically left digging through the network tab in your browser

absolute inset-0 flex h-full w-full items-center justify-center text-sm

The page expired, please try again.

Whoops, something went wrong on our servers.

Sorry, the page you are looking for could not be found.
