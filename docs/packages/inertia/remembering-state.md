# Inertia - Remembering State

Source: https://inertiajs.com/remembering-state

# Remembering state

## Saving local state

## Multiple components

## Form helper

## Manually saving state

When navigating browser history, Inertia restores pages using prop data cached in history state. However, Inertia does not restore local page component state since this is beyond its reach. This can lead to outdated pages in your browser history.

For example, if a user partially completes a form, then navigates away, and then returns back, the form will be reset and their work will be lost.

To mitigate this issue, you can tell Inertia which local component state to save in the browser history.

To save local component state to the history state, use the remember feature to tell Inertia which data it should remember.

Now, whenever your local form state changes, Inertia will automatically save this data to the history state and will also restore it on history navigation.

If your page contains multiple components that use the remember functionality provided by Inertia, you need to provide a unique key for each component so that Inertia knows which data to restore to each component.

If you have multiple instances of the same component on the page using the remember functionality, be sure to also include a unique key for each component instance, such as a model identifier.

If you're using the Inertia form helper, you can pass a unique form key as the first argument when instantiating your form. This will cause the form data and errors to automatically be remembered.

The useRemember hook watch for data changes and automatically save those changes to the history state. Then, Inertia will restore the data on page load.

However, it's also possible to manage this manually using the underlying remember() and restore() methods in Inertia.

`remember`
`form`
`useRemember`
`remember()`
`restore()`
[Inertia form helper](/forms#form-helper)
hook to tell Inertia which data it should remember.

store to tell Inertia which data it should remember.

Set a key as the second argument of useRemember().

Set a dynamic key as the second argument of useRemember().
