# Inertia - Client Side Setup

Source: https://inertiajs.com/client-side-setup

# Client-side setup

## Laravel starter kits

## Install dependencies

## Initialize the Inertia app

## Resolving components

## Defining a root element

Once you have your server-side framework configured, you then need to setup your client-side framework. Inertia currently provides support for React, Vue, and Svelte.

Laravel's starter kits provide out-of-the-box scaffolding for new Inertia applications. These starter kits are the absolute fastest way to start building a new Inertia project using Laravel and Vue or React. However, if you would like to manually install Inertia into your application, please consult the documentation below.

First, install the Inertia client-side adapter corresponding to your framework of choice.

Next, update your main JavaScript file to boot your Inertia app. To accomplish this, we'll initialize the client-side framework with the base Inertia component.

The setup callback receives everything necessary to initialize the client-side framework, including the root Inertia App component.

The resolve callback tells Inertia how to load a page component. It receives a page name (string), and returns a page component module. How you implement this callback depends on which bundler (Vite or Webpack) you're using.

By default we recommend eager loading your components, which will result in a single JavaScript bundle. However, if you'd like to lazy-load your components, see our code splitting documentation.

By default, Inertia assumes that your application's root template has a root element with an id of app. If your application's root element has a different id, you can provide it using the id property.

If you change the id of the root element, be sure to update it server-side as well.

`setup`
`App`
`resolve`
`id`
`app`
`If you change the id`
[server-side framework configured](/server-side-setup)
[starter kits](https://laravel.com/starter-kits)
[code splitting](/code-splitting)
[server-side](/server-side-setup#root-template)