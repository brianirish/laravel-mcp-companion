Source: https://herd.laravel.com/docs/macos/getting-started/applications.md

# Applications

# Applications

Herd uses the concept of *parked* paths and *linked* directories for serving applications. You can access every application in a parked path via `<directory-name>.test`. By default, Herd parks the `~/Herd` directory for you. Any PHP application in this directory is available via its `.test` domain automatically. If you have other locations for your projects, you can add them as parked paths in the general settings or link individual projects as a linked directory.


Aside from Laravel, Herd [supports many frameworks](https://herd.laravel.com/docs/macos/extending-herd/supported-frameworks.md) and applications out-of-the-box. If your framework is not in the list, you can create a [custom driver](https://herd.laravel.com/docs/macos/extending-herd/custom-drivers.md) to run it with Herd.

## Creating your first application

The fastest way to manage your applications and to create new ones is the command line.

```shell theme={null}
cd ~/Herd
laravel new my-new-application
cd my-new-application
herd open
herd edit
```

These commands go into your Herd directory, create a brand new Laravel application and open it in your browser. The `herd edit` command even opens your favorite IDE.

## Linking an existing application

You can link an existing application with a specific domain via the `link` command from any directory on your machine. The `link` command uses the directory name as domain name if you don't set additional parameters.

```shell theme={null}
cd ~/Code/your-project
herd link
herd link custom-domain
```

These commands create Herd configurations, and you can now access the application via `your-project.test` and `custom-domain.test`. This is useful if you want to use an application from multiple domains, for example in multi-tenancy environments or if you don't store all your projects in a single code directory.

## Via the GUI

If you prefer creating and linking applications via a graphical user interface, you can use the new application window of Herd. Select "New Application" from the Herd menu bar icon or press `⌘N` in the [Applications window](https://herd.laravel.com/docs/macos/sites/managing-sites.md).

You can describe your application in a prompt and let a coding agent [build it for you](https://herd.laravel.com/docs/macos/herd-studio/build-with-ai.md). If you leave the prompt empty, Herd creates a fresh Laravel application with the selected starter kit.


Click "Advanced" to configure all options of the Laravel installer, like the starter kit, authentication, testing framework and the database. Herd Pro users can install MySQL, MariaDB or PostgreSQL right from this form if the database isn't installed yet.


Click "Link Existing App" to add an existing project from any directory on your machine to Herd.

## Unlinking an existing application

You may remove a previously created link, by using the `unlink` command from any directory on your machine. The `unlink` command uses the directory name as domain name if you don't set additional parameters.

```shell theme={null}
cd ~/Code/your-project
herd unlink
herd unlink custom-domain
```

These commands remove any previously created links to your application.

## Integrations

Herd allows linking your local applications with first-party Laravel cloud services and makes triggering common tasks like deployments super easy. Herd supports deploying applications to [Laravel Cloud](https://herd.laravel.com/docs/macos/integrations/laravel-cloud.md) and connecting them to sites on Laravel Forge with the [Forge integration](https://herd.laravel.com/docs/macos/integrations/laravel-forge.md).
