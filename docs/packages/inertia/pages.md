# Inertia - Pages

Source: https://inertiajs.com/pages

# Pages

## Creating pages

# Welcome

## Creating layouts

## Persistent layouts

## Default layouts

When building applications using Inertia, each page in your application typically has its own controller / route and a corresponding JavaScript component. This allows you to retrieve just the data necessary for that page - no API required.

In addition, all of the data needed for the page can be retrieved before the page is ever rendered by the browser, eliminating the need for displaying "loading" states when users visit your application.

Inertia pages are simply JavaScript components. If you have ever written a Vue, React, or Svelte component, you will feel right at home. As you can see in the example below, pages receive data from your application's controllers as props.

Hello , welcome to your first Inertia app!

Given the page above, you can render the page by returning an Inertia response from a controller or route. In this example, let's assume this page is stored at resources/js/Pages/User/Show.vue resources/js/Pages/User/Show.jsx resources/js/Pages/User/Show.svelte within a Laravel application.

While not required, for most projects it makes sense to create a site layout that all of your pages can extend. You may have noticed in our page example above that we're wrapping the page content within a component. Here's an example of such a component:

As you can see, there is nothing Inertia specific within this template. This is just a typical Vue React Svelte component.

While it's simple to implement layouts as children of page components, it forces the layout instance to be destroyed and recreated between visits. This means you cannot have persistent layout state when navigating between pages.

For example, maybe you have an audio player on a podcast website that you want to continue playing as users navigate the site. Or, maybe you simply want to maintain the scroll position in your sidebar navigation between page visits. In these situations, the solution is to leverage Inertia's persistent layouts.

You can also create more complex layout arrangements using nested layouts.

If you're using Vue 3.3+, you can alternatively use defineOptions to define a layout within . Older versions of Vue can use the defineOptions plugin:

If you're using persistent layouts, you may find it convenient to define the default page layout in the resolve() callback of your application's main JavaScript file.

This will automatically set the page layout to Layout if a layout has not already been set for that page.

You can even go a step further and conditionally set the default page layout based on the page name , which is available to the resolve() callback. For example, maybe you don't want the default layout to be applied to your public pages.

`resources/js/Pages/User/Show.vue`
`resources/js/Pages/User/Show.jsx`
`resources/js/Pages/User/Show.svelte`
`Layout`
`name`
`resolve()`
[Home](/)
[About](/about)
[Contact](/contact)
[Inertia response](/responses)
[defineOptions](https://vuejs.org/api/sfc-script-setup.html#defineoptions)
[defineOptions plugin](https://vue-macros.sxzz.moe/macros/define-options.html)