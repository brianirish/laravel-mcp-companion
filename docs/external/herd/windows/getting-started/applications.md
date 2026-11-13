Source: https://herd.laravel.com/docs/windows/getting-started/applications.md

# Applications

# Applications

Herd uses the concept of *parked* paths and *linked* directories for serving applications. You can access every application in a parked path via `http://<directory-name>.test`. By default, Herd will automatically park the `%USERPROFILE%\Herd` directory for you. Any PHP application in this directory is automatically available via its `.test` domain. If you have other locations for your projects, you can add them as parked paths in the general settings or link individual projects as a linked directory.


Aside from Laravel, Herd [supports many frameworks](https://herd.laravel.com/docs/windows/extending-herd/supported-frameworks.md) and applications out-of-the-box. If your framework is not in the list, you can create a [custom driver](https://herd.laravel.com/docs/windows/extending-herd/custom-drivers.md) to run it with Herd.

## Creating your first application

The fastest way to manage your applications and to create new ones is the command line.

#### Command Prompt (CMD)

```
cd %USERPROFILE%\Herd
laravel new my-project
cd my-project
herd open
herd edit
```

#### Powershell

```
Set-Location -Path "$env:USERPROFILE\Herd"
laravel new my-project
cd my-project
herd open
herd edit
```

These commands go into your Herd directory, create a brand-new Laravel application and open it in your browser. The `herd edit` command even opens your favorite IDE if you've set up [the protocols](https://herd.laravel.com/docs/windows/sites/managing-sites.md#open-in-ide).

## Linking an existing application

You can link an existing application with a specific domain via the `link` command from any directory on your machine. The `link` command uses the directory name as domain name if you don't set additional parameters.

#### Command Prompt (CMD)

```
cd %USERPROFILE%\Herd\your-project
herd link
herd link custom-domain
```

#### Powershell

```
Set-Location -Path "$env:USERPROFILE\Herd\your-project"
herd link
herd link custom-domain
```

These commands create Herd configurations, add the domains to your hosts file, and you can now access the application via `your-project.test` and `custom-domain.test`. This is useful if you want to use an application from multiple domains, for example in multi-tenancy environments or if you store all your projects across multiple directories.

## Via the GUI

If you prefer creating and linking applications via a graphical user interface, use the composer at the top of the [Applications window](https://herd.laravel.com/docs/windows/sites/managing-sites.md). Select "New Application" from the menu of the Herd system tray icon, click "New" in the toolbar of the Applications window or press `Ctrl+N` there – all of them take you to the composer.

Enter a name for your application. Herd shows whether the `.test` domain for this name is still available. Then select a starter kit – No Starter Kit, React, Vue, Svelte or Livewire – and click "Create App" or press `Ctrl+Enter`. Herd creates a fresh Laravel application with this starter kit in your Herd directory. You don't need AI for this: as long as the prompt field stays empty, Herd only runs the Laravel installer.


Click "Options" to configure the Laravel installer:

| Section | Options |
| - | - |
| Location | The directory that Herd creates the application in. |
| Starter Kit | Authentication, team support, the testing framework and whether Herd installs [Laravel Boost](https://boost.laravel.com). The options depend on the selected starter kit. |
| Project | Whether Herd initializes a Git repository, and the database of the application. |


To use a community starter kit, select "Custom…" in the starter kit menu and enter its Composer package in the options, for example `vendor/package-name`.

If you describe your application in the prompt field, the button changes to "Build" and a coding agent [builds the application for you](https://herd.laravel.com/docs/windows/herd-studio/build-with-ai.md).

Click "Link Existing App" to add an existing project from any directory on your machine to Herd.

## Unlinking an existing application

You may remove a previously created link, by using the `unlink` command from any directory on your machine. The `unlink` command uses the directory name as domain name if you don't set additional parameters.

#### Command Prompt (CMD)

```
cd %USERPROFILE%\Herd\your-project
herd unlink
herd unlink custom-domain
```

#### Powershell

```
Set-Location -Path "$env:USERPROFILE\Herd\your-project"
herd unlink
herd unlink custom-domain
```

These commands remove any previously created links to your application.

## Integrations

Herd allows linking your local applications with first-party Laravel cloud services and makes triggering common tasks like deployments super easy. Herd supports deploying applications to [Laravel Cloud](https://herd.laravel.com/docs/windows/integrations/laravel-cloud.md) and connecting them to sites on Laravel Forge with the [Forge integration](https://herd.laravel.com/docs/windows/integrations/laravel-forge.md).
