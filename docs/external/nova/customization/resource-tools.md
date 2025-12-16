# Nova - Customization/Resource-Tools

*Source: https://nova.laravel.com/docs/v5/customization/resource-tools*

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
- [Tool Options](#tool-options)
- [Accessing Tool Options](#accessing-tool-options)
- [Dynamic Options](#dynamic-options)
- [Building Tools](#building-tools)
- [Routing](#routing)
- [Assets](#assets)
- [Registering Assets](#registering-assets)
- [Compiling Assets](#compiling-assets)

Digging Deeper

# Resource Tools

Learn how to build custom tools for your Nova resources.

## [​](#overview) Overview

Resource tools are very similar to [custom tools](./tools); however, instead of being listed in the Nova sidebar, resource tools are displayed on a particular resource’s detail page. Like Nova tools, resource tools are incredibly customizable, and primarily consist of a single-file Vue component that is totally under your control.

## [​](#defining-tools) Defining Tools

Resource tools may be generated using the `nova:resource-tool` Artisan command. By default, all new tools will be placed in the `nova-components` directory of your application. When generating a tool using the `nova:resource-tool` command, the tool name you pass to the command should follow the Composer `vendor/package` format. So, if we were building a Stripe inspector tool, we might run the following command:

Copy

Ask AI

```
php artisan nova:resource-tool acme/stripe-inspector
```

When generating a tool, Nova will prompt you to install the tool’s NPM dependencies, compile its assets, and update your application’s `composer.json` file. All custom tools are registered with your application as a Composer [“path” repository](https://getcomposer.org/doc/05-repositories#path).
Nova resource tools include all of the scaffolding necessary to build your tool. Each tool even contains its own `composer.json` file and is ready to be shared with the world on GitHub or the source control provider of your choice.

## [​](#registering-tools) Registering Tools

Nova resource tools may be registered in your resource’s `fields` method. This method returns an array of fields and tools available to the resource. To register your resource tool, add your tool to the array of fields returned by this method:

app/Nova/~Resource.php

Copy

Ask AI

```
use Acme\StripeInspector\StripeInspector;
use Laravel\Nova\Http\Requests\NovaRequest;

// ...

/**
 * Get the fields displayed by the resource.
 *
 * @return array<int, \Laravel\Nova\Fields\Field|\Laravel\Nova\ResourceTool>
 */
public function fields(NovaRequest $request): array
{
    return [
        ID::make()->sortable(),

        StripeInspector::make(),
    ];
}
```

### [​](#authorization) Authorization

If you would like to only expose a given tool to certain users, you may invoke the `canSee` method when registering your tool. The `canSee` method accepts a closure which should return `true` or `false`. The closure will receive the incoming HTTP request:

app/Nova/~Resource.php

Copy

Ask AI

```
use Acme\StripeInspector\StripeInspector;
use Laravel\Nova\Http\Requests\NovaRequest;

// ...

/**
 * Get the fields displayed by the resource.
 *
 * @return array<int, \Laravel\Nova\Fields\Field|\Laravel\Nova\ResourceTool>
 */
public function fields(NovaRequest $request): array
{
    return [
        ID::make('ID', 'id')->sortable(),

        StripeInspector::make()->canSee(function ($request) {
            return $request->user()->managesBilling();
        }),
    ];
}
```

### [​](#tool-options) Tool Options

Often, you will need to allow the consumer’s of your tool to customize run-time configuration options on the tool. You may do this by exposing methods on your tool class. These methods may call the tool’s underlying `withMeta` method to add information to the tool’s metadata, which will be available within your `Tool.vue` component. The `withMeta` method accepts an array of key / value options:

nova-components/StripeInspector/src/StripeInspector.php

Copy

Ask AI

```
namespace Acme\StripeInspector;

use Laravel\Nova\ResourceTool;

class StripeInspector extends ResourceTool
{
    // ...

    /**
     * Indicates that the Stripe inspector should allow refunds.
     *
     * @return $this
     */
    public function issuesRefunds()
    {
        return $this->withMeta(['issuesRefunds' => true]);
    }
}
```

#### [​](#accessing-tool-options) Accessing Tool Options

Your resource tool’s `Tool.vue` component receives several Vue `props`: `resourceName`, `resourceId`, and `panel`. The `resourceId` property contains the primary key of the resource the tool is currently attached to. You may use the `resourceId` when making requests to your controllers. The `panel` prop provides access to any tool options that may be available via the `fields`:

Copy

Ask AI

```
const issuesRefunds = this.panel.fields[0].issuesRefunds;
```

#### [​](#dynamic-options) Dynamic Options

Resource tools also offer the ability to dynamically set options on the tool without a setter method by simple calling the desired option as a method when registering the tool. If called with an argument, it will be set as the option’s value:

Copy

Ask AI

```
use Acme\StripeInspector\StripeInspector;
use Laravel\Nova\Http\Requests\NovaRequest;

// ...

/**
 * Get the fields displayed by the resource.
 *
 * @return array<int, \Laravel\Nova\Fields\Field|\Laravel\Nova\ResourceTool>
 */
public function fields(NovaRequest $request): array
{
    return [
        ID::make('ID', 'id')->sortable(),

        StripeInspector::make()->issuesRefunds(),
    ];
}
```

## [​](#building-tools) Building Tools

Each tool generated by Nova includes its own service provider and “tool” class. Using the `stripe-inspector` tool as an example, the tool class will be located at `src/StripeInspector.php`.
The tool’s service provider is also located within the `src` directory of the tool, and is registered within the `extra` section of your tool’s `composer.json` file so that it will be auto-loaded by Laravel.

### [​](#routing) Routing

Often, you will need to define Laravel routes that are called by your tool. When Nova generates your tool, it creates a `routes/api.php` routes file. If needed, you may use this file to define any routes your tool requires.
All routes within this file are automatically defined inside a route group by your tool’s `ToolServiceProvider`. The route group specifies that all routes within the group should receive a `/nova-vendor/tool-name` prefix, where `tool-name` is the “kebab-case” name of your tool. So, for example, `/nova-vendor/stripe-inspector`. You are free to modify this route group definition, but take care to make sure your Nova tool will co-exist with other Nova packages.

When building routes for your tool, you should **always** add authorization to these routes using Laravel gates or policies.

## [​](#assets) Assets

When Nova generates your tool, `resources/js` and `resources/css` directories are generated for you. These directories contain your tool’s JavaScript and CSS. The primary files of interest in these directories are: `resources/js/components/Tool.vue` and `resources/css/tool.css`.
The `Tool.vue` file is a single-file Vue component that contains your tool’s front-end. From this file, you are free to build your tool however you want. Your tool can make HTTP requests using Axios via [Nova.request](./frontend#nova-requests).

### [​](#registering-assets) Registering Assets

Your Nova tool’s service provider registers your tool’s compiled assets so that they will be available to the Nova front-end:

nova-components/StripeInspector/src/ToolServiceProvider.php

Copy

Ask AI

```
use Laravel\Nova\Nova;
use Laravel\Nova\Events\ServingNova;

// ...

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    parent::boot();

    $this->app->booted(function () {
        $this->routes();
    });


*[Content truncated for length]*