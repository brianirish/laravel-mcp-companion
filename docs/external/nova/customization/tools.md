# Nova - Customization/Tools

*Source: https://nova.laravel.com/docs/v5/customization/tools*

---

- [Community](https://discord.com/invite/laravel)
- [Blog](https://blog.laravel.com)

##### Get Started

- [Installation](/docs/v5/installation)
- [Release Notes](/docs/v5/releases)
- [Upgrade Guide](/docs/v5/upgrade)

##### Resources

- [The Basics](/docs/v5/resources/the-basics)
- [Fields](/docs/v5/resources/fields)
- [Dependent Fields](/docs/v5/resources/dependent-fields)
- [Date Fields](/docs/v5/resources/date-fields)
- [File Fields](/docs/v5/resources/file-fields)
- [Repeater Fields](/docs/v5/resources/repeater-fields)
- [Field Panels](/docs/v5/resources/panels)
- [Relationships](/docs/v5/resources/relationships)
- [Validation](/docs/v5/resources/validation)
- [Authorization](/docs/v5/resources/authorization)

##### Search

- [The Basics](/docs/v5/search/the-basics)
- [Global Search](/docs/v5/search/global-search)
- [Scout Integration](/docs/v5/search/scout-integration)

##### Filters

- [Defining Filters](/docs/v5/filters/defining-filters)
- [Registering Filters](/docs/v5/filters/registering-filters)

##### Lenses

- [Defining Lenses](/docs/v5/lenses/defining-lenses)
- [Registering Lenses](/docs/v5/lenses/registering-lenses)

##### Actions

- [Defining Actions](/docs/v5/actions/defining-actions)
- [Registering Actions](/docs/v5/actions/registering-actions)

##### Metrics

- [Defining Metrics](/docs/v5/metrics/defining-metrics)
- [Registering Metrics](/docs/v5/metrics/registering-metrics)

##### Digging Deeper

- [Dashboards](/docs/v5/customization/dashboards)
- [Menus](/docs/v5/customization/menus)
- [Notifications](/docs/v5/customization/notifications)
- [Authentication](/docs/v5/customization/authentication)
- [Impersonation](/docs/v5/customization/impersonation)
- [Tools](/docs/v5/customization/tools)
- [Resource Tools](/docs/v5/customization/resource-tools)
- [Cards](/docs/v5/customization/cards)
- [Fields](/docs/v5/customization/fields)
- [Filters](/docs/v5/customization/filters)
- [CSS / JavaScript](/docs/v5/customization/frontend)
- [Assets](/docs/v5/customization/assets)
- [Localization](/docs/v5/customization/localization)
- [Stubs](/docs/v5/customization/stubs)

On this page

- [Overview](#overview)
- [Defining Tools](#defining-tools)
- [Registering Tools](#registering-tools)
- [Authorization](#authorization)
- [Building Tools](#building-tools)
- [Routing](#routing)
- [Routing Authorization](#routing-authorization)
- [Navigation](#navigation)
- [Sidebar Icons](#sidebar-icons)
- [Assets](#assets)
- [Registering Assets](#registering-assets)
- [JavaScript Bootstrap & Components](#javascript-bootstrap-%26-components)
- [Compiling Assets](#compiling-assets)
- [Vue Page Components & Nova Plugins](#vue-page-components-%26-nova-plugins)

Digging Deeper

# Tools

Learn how to build custom tools for your Nova application.

## [​](#overview) Overview

Sometimes, your business may need additional functionality that isn’t provided by Nova. For this reason, Nova allows you to build custom tools and add them to the Nova sidebar. Nova tools are incredibly customizable, as they primarily consist of a single-file Vue component that is totally under your control. Within your Vue component, you are free to make HTTP requests to any controller within your application.

## [​](#defining-tools) Defining Tools

Custom tools may be generated using the `nova:tool` Artisan command. By default, all new tools will be placed in the `nova-components` directory of your application. When generating a tool using the `nova:tool` command, the tool name you pass to the command should follow the Composer `vendor/package` format. So, if we were building a price tracker tool, we might run the following command to generate our tool:

Copy

Ask AI

```
php artisan nova:tool acme/price-tracker
```

When generating a tool, Nova will prompt you to install the tool’s NPM dependencies, compile its assets, and update your application’s `composer.json` file. All custom tools are registered with your application as a Composer [“path” repository](https://getcomposer.org/doc/05-repositories#path).
Nova tools include all of the scaffolding necessary to build your tool. Each tool even contains its own `composer.json` file and is ready to be shared with the world on GitHub or the source control provider of your choice.

## [​](#registering-tools) Registering Tools

Nova tools may be registered in your application’s `App/Providers/NovaServiceProvider` class. Your service provider contains a `tools` method, which returns an array of tools. To register your tool, simply add it to the list of tools returned by this method. For example, if you created a Nova tool named `acme/price-tracker`, you may register the tool like so:

app/Nova/NovaServiceProvider.php

Copy

Ask AI

```
use Acme\PriceTracker\PriceTracker;

// ..

/**
 * Get the tools that should be listed in the Nova sidebar.
 */
public function tools(): array
{
    return [
        new PriceTracker,
    ];
}
```

### [​](#authorization) Authorization

If you would like to only expose a given tool to certain users, you may chain the `canSee` method onto your tool’s registration. The `canSee` method accepts a Closure which should return `true` or `false`. The Closure will receive the incoming HTTP request:

app/Providers/NovaServiceProvider.php

Copy

Ask AI

```
use Acme\PriceTracker\PriceTracker;

// ...

/**
 * Get the tools that should be listed in the Nova sidebar.
 */
public function tools(): array
{
    return [
        (new PriceTracker)->canSee(function ($request) {
            return false;
        }),
    ];
}
```

## [​](#building-tools) Building Tools

Each tool generated by Nova includes its own service provider and “tool” class. Using the `price-tracker` tool as an example, the tool class will be located at `src/PriceTracker.php`. The tool class must be registered with your application’s `NovaServiceProvider` as previously noted.
The tool’s service provider is also located within the `src` directory of the tool, and is registered within the `extra` section of your tool’s `composer.json` file so that it will be auto-loaded by Laravel.

### [​](#routing) Routing

Often, you will need to define Laravel routes that are called by your tool. When Nova generates your tool, it creates `routes/inertia.php` and `routes/api.php` route files.
The `routes/inertia.php` file is tasked with rendering your tool via [Inertia](https://legacy.inertiajs.com), while the `routes/api.php` file may be used to define any routes that your Inertia based tool will be making requests to in order to gather additional data or perform additional tasks.
All routes within the `routes/api.php` file are automatically defined inside a route group by your tool’s `ToolServiceProvider`. The route group specifies that all “API routes”, which will typically be invoked from the client via [Nova.request](./frontend#nova-requests), should receive a `/nova-vendor/tool-name` URL prefix, where `tool-name` is the “kebab-case” name of your tool.
Similarly, routes within the `routes/inertia.php` file are also placed within a route group that prefixes all of the routes within the file with the name of your tool.
You are free to modify this route group definition, but you should ensure your Nova tool will easily co-exist with other Nova packages.

#### [​](#routing-authorization) Routing Authorization

Your Nova tool is generated with an `Authorize` middleware. You should not typically need to modify this middleware, as it automatically determines whether the authenticated user can “see” the tool before it processes any requests to routes within your tool’s route group; however, you are free to modify this middleware if needed.

### [​](#navigation) Navigation

Your Nova tool class contains a `menu` method. This method should return a [custom menu](./menus) that renders your tool’s left-side navigation links. You are free to customize this method as needed:

nova-components/PriceTracker/src/PriceTracker.php

Copy

Ask AI

```
use Illuminate\Http\Request;
use Laravel\Nova\Menu\MenuSection;

// ...

/**
 * Build the menu that renders the navigation links for the tool.
 *
 * @param  \Illuminate\Http\Request  $request
 * @return mixed
 */
public function menu(Request $request)
{
    return MenuSection::make('Price Tracker')
        ->path('/price-tracker')
        ->icon('server');
}
```

If you have [customized Nova’s main sidebar menu](./menus#customizing-the-main-menu), a link to your tool will not automatically display in Nova’s sidebar. You will need to manually define your tool’s menu inside your custom `Nova::mainMenu` callback.

#### [​](#sidebar-icons) Sidebar Icons

Nova utilizes the free [Heroicons](https://heroicons.com/) icon set by [Steve Schoger](https://twitter.com/steveschoger). Therefore, you may simply specify the name of one of these icons when providing the icon name to the `icon` method.

## [​](#assets) Assets

When Nova generates your tool, `resources/js` and `resources/css` directories are generated for you. These directories contain your tool’s JavaScript and CSS. The primary files of interest in these directories are: `resources/js/components/Tool.vue` and `resources/css/tool.css`.
The `Tool.vue` file is a single-file Vue component that contains your tool’s front-end. From this file, you are free to build your tool however you want. Your tool can make HTTP requests using Axios via [Nova.request](./frontend#nova-requests).

### [​](#registering-assets) Registering Assets

Your Nova tool class contains a `boot` method. This method is executed when the tool is registered and available. By default, this method registers your tool’s compiled assets so that they will be available to the Nova front-end:

nova-components/PriceTracker/src/ToolServiceProvider.php

Copy

Ask AI

```
use Laravel\Nova\Nova;
use Laravel\Nova\Events\ServingNova;

// ...

/**
 * Perform any tasks that need to happen on tool registration.
 */
public function boot(): void
{
    parent::boot();

    Nova::serving(function () {
        Nova::mix('p

*[Content truncated for length]*