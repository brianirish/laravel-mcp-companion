# Inertia - Validation

Source: https://inertiajs.com/validation

# Validation

## How it works

## Sharing errors

## Displaying errors

## Repopulating input

## Error bags

Handling server-side validation errors in Inertia works differently than a classic XHR-driven form that requires you to catch the validation errors from 422 responses and manually update the form's error state - because Inertia never receives 422 responses. Instead, Inertia operates much more like a standard full page form submission. Here's how:

First, you submit your form using Inertia. If there are server-side validation errors, you don't return those errors as a 422 JSON response. Instead, you redirect (server-side) the user back to the form page they were previously on, flashing the validation errors in the session. Some frameworks, such as Laravel, do this automatically.

Next, any time these validation errors are present in the session, they automatically get shared with Inertia, making them available client-side as page props which you can display in your form. Since props are reactive, they are automatically shown when the form submission completes.

Finally, since Inertia apps never generate 422 responses, Inertia needs another way to determine if a response includes validation errors. To do this, Inertia checks the page.props.errors object for the existence of any errors. In the event that errors are present, the request's onError() callback will be called instead of the onSuccess() callback.

In order for your server-side validation errors to be available client-side, your server-side framework must share them via the errors prop. Inertia's first-party adapters, such as the Laravel adapter, do this automatically. For other frameworks, you may need to do this manually. Please refer to your specific server-side adapter documentation for more information.

Since validation errors are made available client-side as page component props, you can conditionally display them based on their existence. Remember, when using our first-party server adapters (such as the Laravel adapter), the errors prop will automatically be available to your page.

While handling errors in Inertia is similar to full page form submissions, Inertia offers even more benefits. In fact, you don't even need to manually repopulate old form input data.

When validation errors occur, the user is typically redirected back to the form page they were previously on. And, by default, Inertia automatically preserves the component state for post, put, patch, and delete requests. Therefore, all the old form input data remains exactly as it was when the user submitted the form.

So, the only work remaining is to display any validation errors using the errors prop.

For pages that have more than one form, it's possible to encounter conflicts when displaying validation errors if two forms share the same field names. For example, imagine a "create company" form and a "create user" form that both have a name field. Since both forms will be displaying the page.props.errors.name validation error, generating a validation error for the name field in either form will cause the error to appear in both forms.

To solve this issue, you can use "error bags". Error bags scope the validation errors returned from the server within a unique key specific to that form. Continuing with our example above, you might have a createCompany error bag for the first form and a createUser error bag for the second form.

Specifying an error bag will cause the validation errors to come back from the server within page.props.errors.createCompany and page.props.errors.createUser.

`422`
`page.props.errors`
`onError()`
`onSuccess()`
`errors`
`$page.props.errors`
`post`
`put`
`patch`
`delete`
`name`
`page.props.errors.name`
`createCompany`
`createUser`
`page.props.errors.createCompany`
`page.props.errors.createUser`
[submit your form using Inertia](/forms)
[component state](/manual-visits#state-preservation)
[form helper](/forms#form-helper)