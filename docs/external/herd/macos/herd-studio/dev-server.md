Source: https://herd.laravel.com/docs/macos/herd-studio/dev-server.md

# Dev Server

# Automatic Dev Server

Modern Laravel applications need a running Vite dev server – or the full `php artisan dev` stack – before their pages render correctly. With [Herd Studio](https://herd.laravel.com/docs/macos/herd-studio/overview.md) enabled, Herd starts the dev server for you as soon as you open a site in the browser, so you never see a missing Vite manifest error again.

## How it works

When you open a page of a site, Herd checks whether the site's dev server is running. If it isn't, and the site has a `vite.config.js` (or `.ts`, `.mjs`, `.mts`) or supports `php artisan dev`, Herd starts it in the background.

If the site has no production build in `public/build` yet, Herd holds the first page request for up to 15 seconds until Vite is ready. This way, the first page renders with all assets instead of showing an error.

Herd picks the command based on your application:

* **`php artisan dev`**: for Laravel 13.25 or later, Herd runs the complete dev stack of your application. This includes the web server, queue worker, Pail, Vite and any additional processes that you configured. Herd Studio shows the output of every process separately.
* **Vite**: for all other applications, Herd runs the `dev` script of your `package.json` with the package manager of the project, for example `npm run dev`.

## Stopping the dev server

Herd stops the dev server when you no longer use the site. This happens one minute after you close the last Herd Studio tab for the site, and only when the site hasn't received any requests for five minutes.

You can also stop the dev server manually in Herd Studio. Herd doesn't restart a dev server that you stopped yourself, and it doesn't retry automatically after a failed start. If you don't want Herd to start the dev server for a specific site at all, you can turn off the automatic start for that site in Herd Studio.

> [!NOTE]
>
> The automatic dev server requires Herd Studio. If you disable Herd Studio in the settings, Herd no longer starts dev servers and you need to run `npm run dev` or `composer run dev` yourself.
