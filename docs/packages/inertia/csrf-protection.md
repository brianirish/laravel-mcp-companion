# Inertia - Csrf Protection

Source: https://inertiajs.com/csrf-protection

# CSRF protection

## Making requests

## Handling mismatches

If your server-side framework includes cross-site request forgery (CSRF) protection, you'll need to ensure that each Inertia request includes the necessary CSRF token for POST, PUT, PATCH, and DELETE requests.

Of course, as already discussed, some server-side frameworks such as Laravel automatically handle the inclusion of the CSRF token when making requests. Therefore, no additional configuration is required when using one of these frameworks.

However, if you need to handle CSRF protection manually, one approach is to include the CSRF token as a prop on every response. You can then use the token when making Inertia requests.

You can even use Inertia's shared data functionality to automatically include the csrf_token with each response.

However, a better approach is to use the CSRF functionality already built into axios for this. Axios is the HTTP library that Inertia uses under the hood.

Axios automatically checks for the existence of an XSRF-TOKEN cookie. If it's present, it will then include the token in an X-XSRF-TOKEN header for any requests it makes.

The easiest way to implement this is using server-side middleware. Simply include the XSRF-TOKEN cookie on each response, and then verify the token using the X-XSRF-TOKEN header sent in the requests from axios.

When a CSRF token mismatch occurs, your server-side framework will likely throw an exception that results in an error response. For example, when using Laravel, a TokenMismatchException is thrown which results in a 419 error page. Since that isn't a valid Inertia response, the error is shown in a modal.

Obviously, this isn't a great user experience. A better way to handle these errors is to return a redirect back to the previous page, along with a flash message that the page expired. This will result in a valid Inertia response with the flash message available as a prop which you can then display to the user. Of course, you'll need to share your flash messages with Inertia for this to work.

When using Laravel, you may modify your application's exception handler to automatically redirect the user back to the page they were previously on while flashing a message to the session. To accomplish this, you may use the respond exception method in your application's bootstrap/app.php file.

The end result is a much better experience for your users. Instead of seeing the error modal, the user is instead presented with a message that the page "expired" and are asked to try again.

`csrf-token`
`POST`
`PUT`
`PATCH`
`DELETE`
`csrf_token`
`XSRF-TOKEN`
`X-XSRF-TOKEN`
`TokenMismatchException`
`419`
`respond`
`bootstrap/app.php`
**Therefore, no additional configuration is required when using one of these frameworks.**
[shared data](/shared-data)
[axios](https://github.com/axios/axios)
[flash messages](/shared-data#flash-messages)
The page expired, please try again.
