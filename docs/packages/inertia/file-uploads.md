# Inertia - File Uploads

Source: https://inertiajs.com/file-uploads

# File uploads

## FormData conversion

## File upload example

## Multipart limitations

When making Inertia requests that include files (even nested files), Inertia will automatically convert the request data into a FormData object. This conversion is necessary in order to submit a multipart/form-data request via XHR.

If you would like the request to always use a FormData object regardless of whether a file is present in the data, you may provide the forceFormData option when making the request.

You can learn more about the FormData interface via its MDN documentation.

Let's examine a complete file upload example using Inertia. This example includes both a name text input and an avatar file input.

Uploading files using a multipart/form-data request is not natively supported in some server-side frameworks when using the PUT,PATCH, or DELETE HTTP methods. The simplest workaround for this limitation is to simply upload files using a POST request instead.

However, some frameworks, such as Laravel and Rails , support form method spoofing, which allows you to upload the files using POST, but have the framework handle the request as a PUT or PATCH request. This is done by including a _method attribute in the data of your request.

This example uses the Inertia form helper for convenience, since the form helper provides easy access to the current upload progress. However, you are free to submit your forms using manual Inertia visits as well.

`FormData`
`multipart/form-data`
`forceFormData`
`name`
`avatar`
`PUT`
`PATCH`
`DELETE`
`POST`
`_method`
[Laravel](https://laravel.com/docs/routing#form-method-spoofing)
[Rails](https://guides.rubyonrails.org/form_helpers.html#how-do-forms-with-patch-put-or-delete-methods-work-questionmark)
[MDN documentation](https://developer.mozilla.org/en-US/docs/Web/API/FormData)
[Inertia form helper](/forms#form-helper)
[manual Inertia visits](/manual-visits)