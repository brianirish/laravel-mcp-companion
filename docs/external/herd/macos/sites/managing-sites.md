Source: https://herd.laravel.com/docs/macos/sites/managing-sites.md

# Managing Sites

# Manage Sites in Herd

If you've read the [Applications](https://herd.laravel.com/docs/macos/getting-started/applications.md) introduction of the [Getting Started](https://herd.laravel.com/docs/macos/getting-started/installation.md) section, you are already familiar with the concept of parked paths and linked directories – but how do you use them if you have many sites and use different technologies for them?

## Folder structure

We recommend to put all PHP based sites in your Herd directory until you reach a point where it makes sense to split them into a folder structure that makes sense for you. This could be sites per client, or if you run different technologies like Next.js, you can serve them from a different folder via `npm run dev`.

This setup keeps the Applications window clean and easy to use because you can simply unpark a directory in case that you don't work on these sites for a few weeks.

If you don't mind a long list of sites, you can also [mark your most important sites as favorites](#favorites-and-groups) to display them at the top.

## The Applications window

You can manage your sites via the CLI or in the Applications window. Open it by selecting "Applications" from the Herd menu bar icon, by clicking the Herd icon in the Dock, or with the global "Open Sites List" shortcut that you can set up in the [shortcut settings](https://herd.laravel.com/docs/macos/advanced-usage/shortcuts.md).


By default, Herd opens the Applications window when it starts and keeps its icon in the Dock. If you prefer Herd to only live in the menu bar, turn off "Always Show Dock Icon" in the general settings. Herd then only shows the Dock icon while one of its windows is open.

### Dashboard

The Applications window opens with a dashboard. At the top, you can describe a new application and [build it with AI](https://herd.laravel.com/docs/macos/herd-studio/build-with-ai.md). Below, the dashboard shows your favorite applications and your most recent applications with a preview of each site.


Click an application to show its details in the inspector on the right side. Double-click an application or click "Open" to open it in your browser. If [Herd Studio](https://herd.laravel.com/docs/macos/herd-studio/overview.md) is enabled, Herd opens the site in Herd Studio.

Click "See All" to see all your applications.

### All Applications

The list of all applications shows every site that Herd serves. You can switch between a grid and a list view in the toolbar and search for applications with `⌘F`.


The "View Options" menu in the toolbar – also available via right-click on the list – lets you sort applications by name, PHP version, Node version, path, modification date or creation date.

If you [link a site with multiple domains](https://herd.laravel.com/docs/macos/getting-started/applications.md#linking-an-existing-application), Herd groups these domains under their application. Enable "Show Linked Applications" in the list view to display every linked domain as its own row, or click the link badge of an application to see its domains.

Use the refresh button in the toolbar if you made changes to your parked or linked directories via the CLI while the Applications window is open.

The toolbar also has buttons to open [Insights](https://herd.laravel.com/docs/macos/debugging/insights.md), [Mail](https://herd.laravel.com/docs/macos/herd-pro-services/mail.md) and the settings.

### Favorites and groups

You can mark an application as favorite with the star icon in the inspector. Favorites appear at the top of the dashboard and the list of all applications.

If you are working with many sites at the same time and don't want to use multiple parked directories that you add and remove when you need them, you can group sites. Right-click an application, select "Add Site To" and choose an existing group or "Create New Group…". You can collapse groups, and Herd remembers which groups are collapsed.

Right-click an application and select "Add Alias" to serve it on an additional domain.

## The inspector

The inspector on the right side of the Applications window shows everything about the selected application and lets you change its configuration.


### Overview

The top of the inspector shows a preview of the site, its URL and its path. Click the URL to open the site, or the path to reveal the project in Finder. The share button next to the URL [shares the site via Expose](https://herd.laravel.com/docs/macos/sites/sharing-sites.md#sharing-from-the-applications-window).

The "Deploy to Laravel Cloud" button ships your application to production. Learn more in the [Laravel Cloud](https://herd.laravel.com/docs/macos/integrations/laravel-cloud.md) docs.

### Build with AI

If [Herd Studio](https://herd.laravel.com/docs/macos/herd-studio/overview.md) is enabled, you can describe a change or a feature and send it to a coding agent right from the inspector. See [Build with AI](https://herd.laravel.com/docs/macos/herd-studio/build-with-ai.md#changing-an-existing-application).

The "Workspaces" section below lists all [workspaces](https://herd.laravel.com/docs/macos/sites/workspaces.md) of the site.

### Quick Actions

Quick Actions open the site in your browser, the project in your editor, a terminal in the project directory, or the project folder in Finder.

### Services

[Herd Pro](https://herd.laravel.com/checkout) users can switch the database, queue, cache and broadcasting services of a Laravel application with a single click. Learn more in [Per-Site Services](https://herd.laravel.com/docs/macos/herd-pro-services/per-site-services.md).


### Environment

The environment section lets you choose the PHP version and the Node.js version of the site, and serve it via HTTPS.

Selecting a PHP version isolates the site to this version. This tells Herd to serve this site with a specific PHP version and not to use the [global configuration](https://herd.laravel.com/docs/macos/technology/php-versions.md#using-different-php-versions-via-the-gui) that you apply in the settings.

If you select a specific Node.js version, Herd creates an `.nvmrc` file in your project directory. This tells your terminal to switch to the selected Node and NPM version automatically.

The HTTPS toggle [secures the site](https://herd.laravel.com/docs/macos/sites/securing-sites.md) with a local TLS certificate.

### Deleting sites

The button at the bottom of the inspector deletes a parked application and moves its folder to the Trash. For linked applications, the button unlinks the application from Herd and keeps its files.

## Best Practices

It's a good practice to name your local sites like your domains and subdomains to easily access them in your browser. As an example, the Herd website usually lives in the directory `~/Code/herd.laravel.com` so that it's accessible via `http://herd.laravel.com.test`. The Laravel website is in the directory `~/Code/laravel.com`, etc.

> [!NOTE]
>
> Directory names must not start with `www.`. Herd strips this part to allow you to access your local site via `www.laravel.com` and `laravel.com`.
