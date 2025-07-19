# Inertia - Server Side Rendering

Source: https://inertiajs.com/server-side-rendering

# Server-side Rendering (SSR)

## Laravel starter kits

## Install dependencies

## Add server entry-point

### Clustering

## Setup Vite

## Update npm script

## Running the SSR server

## Client side hydration

## Deployment

### Laravel Forge

### Heroku

Server-side rendering pre-renders your JavaScript pages on the server, allowing your visitors to receive fully rendered HTML when they visit your application. Since fully rendered HTML is served by your application, it's also easier for search engines to index your site.

If you are using Laravel Starter Kits, Inertia SSR is supported through a build command:

If you are not using a Laravel starter kit and would like to manually configure SSR, we'll first install the additional dependencies required for server-side rendering. This is only necessary for the Vue adapters, so you can skip this step if you're using React or Svelte.

Next, we'll create a resources/js/ssr.js file within our Laravel project that will serve as our SSR entry point.

This file is going to look very similar to your resources/js/app.js file, except it's not going to run in the browser, but rather in Node.js. Here's a complete example.

When creating this file, be sure to add anything that's missing from your app.js file that makes sense to run in SSR mode, such as plugins or custom mixins.

By default, the SSR server will run on a single thread. Clustering starts multiple Node servers on the same port, requests are then handled by each thread in a round-robin way.

You can enable clustering by passing a second argument to createServer:

Next, we need to update our Vite configuration to build our new ssr.js file. We can do this by adding a ssr property to Laravel's Vite plugin configuration in our vite.config.js file.

Next, let's update the build script in our package.json file to also build our new ssr.js file.

Now you can build both your client-side and server-side bundles.

Now that you have built both your client-side and server-side bundles, you should be able run the Node-based Inertia SSR server using the following command.

You may use the --runtime option to specify which runtime you want to use. This allows you to switch from the default Node.js runtime to Bun.

With the server running, you should be able to access your app within the browser with server-side rendering enabled. In fact, you should be able to disable JavaScript entirely and still navigate around your application.

Since your website is now being server-side rendered, you can instruct Vue React Svelte to "hydrate" the static markup and make it interactive instead of re-rendering all the HTML that we just generated.

To enable client-side hydration in a Vue app, update your ssr.js file to use createSSRApp instead of createApp:

To enable client-side hydration in a React app, update your ssr.js file to use hydrateRoot instead of createRoot:

To enable client-side hydration in a Svelte 4 app, set the hydrate option to true in your ssr.js file:

To enable client-side hydration in a Svelte 5 app, update your ssr.js file to use hydrate instead of mount when server rendering:

You will also need to set the hydratable compiler option to true in your vite.config.js file:

When deploying your SSR enabled app to production, you'll need to build both the client-side ( app.js) and server-side bundles (ssr.js), and then run the SSR server as a background process, typically using a process monitoring tool such as Supervisor.

To stop the SSR server, for instance when you deploy a new version of your website, you may utilize the inertia:stop-ssr Artisan command. Your process monitor (such as Supervisor) should be responsible for automatically restarting the SSR server after it has stopped.

You may use the inertia:check-ssr Artisan command to verify that the SSR server is running. This can be helpful after deployment and works well as a Docker health check to ensure the server is responding as expected.

By default, a check is performed to ensure the server-side bundle exists before dispatching a request to the SSR server. In some cases, such as when your app runs on multiple servers or is containerized, the web server may not have access to the SSR bundle. To disable this check, you may set the inertia.ssr.ensure_bundle_exists configuration value to false.

To run the SSR server on Forge, you should create a new daemon that runs php artisan inertia:start-ssr from the root of your app. Or, you may utilize the built-in Inertia integration from your Forge application's management dashboard.

Next, whenever you deploy your application, you can automatically restart the SSR server by calling the php artisan inertia:stop-ssr command. This will stop the existing SSR server, forcing a new one to be started by your process monitor.

To run the SSR server on Heroku, update the web configuration in your Procfile to run the SSR server before starting your web server.

Note, you must have the heroku/nodejs buildpack installed in addition to the heroku/php buildback for the SSR server to run.

`resources/js/ssr.js`
`This file is going to look very similar to your resources/js/app.js`
`app.js`
`createServer`
`ssr.js`
`ssr`
`vite.config.js`
`Update npm script Next, let's update the build`
`package.json`
`Now you can build both your client-side and server-side bundles. Running the SSR server Now that you have built both your client-side and server-side bundles, you should be able run the Node-based Inertia SSR server using the following command. You may use the --runtime`
`With the server running, you should be able to access your app within the browser with server-side rendering enabled. In fact, you should be able to disable JavaScript entirely and still navigate around your application. Client side hydration Since your website is now being server-side rendered, you can instruct Vue React Svelte to "hydrate" the static markup and make it interactive instead of re-rendering all the HTML that we just generated. To enable client-side hydration in a Vue app, update your ssr.js`
`createSSRApp`
`createApp`
`hydrateRoot`
`createRoot`
`hydrate`
`true`
`mount`
`hydratable`
`To stop the SSR server, for instance when you deploy a new version of your website, you may utilize the inertia:stop-ssr`
`You may use the inertia:check-ssr`
`By default, a check is performed to ensure the server-side bundle exists before dispatching a request to the SSR server. In some cases, such as when your app runs on multiple servers or is containerized, the web server may not have access to the SSR bundle. To disable this check, you may set the inertia.ssr.ensure_bundle_exists`
`false`
`php artisan inertia:start-ssr`
`php artisan inertia:stop-ssr`
`web`
`Procfile`
`Note, you must have the heroku/nodejs`
`heroku/php`
[Laravel Starter Kits](https://laravel.com/docs/starter-kits)
[supported](https://laravel.com/docs/starter-kits#inertia-ssr)
s not going to
        run in the browser, but rather in Node.js. Here

vite build && vite build --ssr

web: php artisan inertia:start-ssr & vendor/bin/heroku-php-apache2 public/
