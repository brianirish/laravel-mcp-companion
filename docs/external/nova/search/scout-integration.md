# Nova - Search/Scout-Integration

*Source: https://nova.laravel.com/docs/v5/search/scout-integration*

---

- [Laravel Nova home page](https://nova.laravel.com)v5Search...⌘KAsk AI
[Support](/cdn-cgi/l/email-protection#8ee0e1f8efcee2effceff8ebe2a0ede1e3)
- [Platform Status](https://status.laravel.com/)
- [Dashboard](https://nova.laravel.com)
- [Dashboard](https://nova.laravel.com)

Search...NavigationSearchScout Integration[Documentation](/docs/v5/installation)[Knowledge Base](/docs/kb/support)- [Community](https://discord.com/invite/laravel)
- [Blog](https://blog.laravel.com/nova)
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

Search# Scout Integration

Integrate Laravel Scout with your Nova resources.

By default, Nova searches your resources using the resource’s database columns.
However, this can become inefficient and lacks support for robust fuzzy matching capabilities provided by dedicated search engines.

For this reason, Nova integrates seamlessly with [Laravel Scout](https://laravel.com/docs/scout). When the `Laravel\Scout\Searchable` trait is attached to a model associated with a Nova resource, Nova will automatically begin using Scout when performing searches against that resource. There is no other configuration required.

## [​](#customizing-scout-searches)Customizing Scout Searches

If you would like to call methods on the `Laravel\Scout\Builder` instance before it executes your search query against your search engine, you may override the `scoutQuery` method on your resource:

app/Nova/User.phpCopyAsk AI```
namespace App\Nova;

use Laravel\Nova\Http\Requests\NovaRequest;
use Laravel\Scout\Builder as ScoutBuilder;

class User extends Resource 
{
    // ... 

    /**
     * Build a Scout search query for the given resource.
     */
    public static function scoutQuery(NovaRequest $request, ScoutBuilder $query): ScoutBuilder
    {
        return $query;
    }
}

```

### [​](#limiting-scout-search-results)Limiting Scout Search Results

You can customize the amount of search results returned from your Scout search engine by defining the `scoutSearchResults` property on the resource class that is associated with the Scout searchable model:

app/Nova/User.phpCopyAsk AI```
namespace App\Nova;

class User extends Resource 
{
    // ...

    /**
     * The number of results to display when searching the resource using Scout.
     *
     * @var int
     */
    public static $scoutSearchResults = 200;
}

```

## [​](#disabling-scout-search)Disabling Scout Search

You may disable Scout search support for a specific resource by defining a `usesScout` method on the resource class. When Scout search support is disabled, simple database queries will be used to search against the given resource, even if the associated resource model includes the Scout `Searchable` trait:

app/Nova/User.phpCopyAsk AI```
namespace App\Nova;

class User extends Resource 
{
    /**
     * Determine if this resource uses Laravel Scout.
     *
     * @return bool
     */
    public static function usesScout()
    {
        return false;
    }
}

```
Was this page helpful?

YesNo[Global Search](/docs/v5/search/global-search)[Defining Filters](/docs/v5/filters/defining-filters)On this page
- [Customizing Scout Searches](#customizing-scout-searches)
- [Limiting Scout Search Results](#limiting-scout-search-results)
- [Disabling Scout Search](#disabling-scout-search)

[Laravel Nova home page](https://nova.laravel.com)[x](https://x.com/laravelphp)[github](https://github.com/laravel)[discord](https://discord.com/invite/laravel)[linkedin](https://linkedin.com/company/laravel)Platform

[Dashboard](https://nova.laravel.com/)[Status](https://status.laravel.com/)Legal and Compliance

[Term of Service](https://nova.laravel.com/terms)[Privacy Policy](https://nova.laravel.com/privacy)[x](https://x.com/laravelphp)[github](https://github.com/laravel)[discord](https://discord.com/invite/laravel)[linkedin](https://linkedin.com/company/laravel)AssistantResponses are generated using AI and may contain mistakes.