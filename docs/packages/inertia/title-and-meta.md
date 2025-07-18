# Inertia - Title And Meta

Source: https://inertiajs.com/title-and-meta

# Title & meta

## Head component

## Title shorthand

## Title callback

## Multiple Head instances

## Head extension

Since Inertia powered JavaScript apps are rendered within the document , they are unable to render markup to the document , as it's outside of their scope. To help with this, Inertia ships with a component which can be used to set the page , tags, and other elements.

To add elements to your page, use the component. Within this component, you can include the elements that you wish to add to the document .

If you only need to add a to the document , you may simply pass the title as a prop to the component.

You can globally modify the page using the title callback in the createInertiaApp setup method. Typically, this method is invoked in your application's main JavaScript file. A common use case for the title callback is automatically adding an app name before or after each page title.

After defining the title callback, the callback will automatically be invoked when you set a title using the component.

Which, in this example, will result in the following tag.

The title callback will also be invoked when you set the title using a tag within your component.

It's possible to have multiple instances of the component throughout your application. For example, your layout can set some default elements, and then your individual pages can override those defaults.

Inertia will only ever render one tag; however, all other tags will be stacked since it's valid to have multiple instances of them. To avoid duplicate tags in your , you can use the head-key property, which will make sure the tag is only rendered once. This is illustrated in the example above for the tag.

The code example above will render the following HTML.

When building a real application, it can sometimes be helpful to create a custom head component that extends Inertia's component. This gives you a place to set app-wide defaults, such as appending the app name to the page title.

Once you have created the custom component, you may simply start using the custom component in your pages.

`title`
`createInertiaApp`
`head-key`
This is a page specific description
