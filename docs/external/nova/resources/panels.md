# Nova - Resources/Panels

*Source: https://nova.laravel.com/docs/v5/resources/panels*

---

- [Laravel Nova home page](https://nova.laravel.com)v5Search...⌘KAsk AI
[Support](/cdn-cgi/l/email-protection#2749485146674b46554651424b0944484a)
- [Platform Status](https://status.laravel.com/)
- [Dashboard](https://nova.laravel.com)
- [Dashboard](https://nova.laravel.com)

Search...NavigationResourcesField Panels[Documentation](/docs/v5/installation)[Knowledge Base](/docs/kb/support)- [Community](https://discord.com/invite/laravel)
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

Resources# Field Panels

If your resource contains many fields, your resource “detail” page can become crowded. For that reason, you may choose to break up groups of fields into their own “panels”:

You may accomplish this by creating a new `Panel` instance within the `fields` method of a resource. Each panel requires a name and an array of fields that belong to that panel:

app/Nova/~Resource.phpCopyAsk AI```
use Laravel\Nova\Panel;
use Laravel\Nova\Fields\Date;
use Laravel\Nova\Fields\ID;
use Laravel\Nova\Fields\Text;
use Laravel\Nova\Http\Requests\NovaRequest;

// ...

/**
 * Get the fields displayed by the resource.
 *
 * @return array<int, \Laravel\Nova\Fields\Field>
 */
public function fields(NovaRequest $request): array
    return [
        ID::make()->sortable(),

        Panel::make('Profile', [
            Text::make('Full Name'),
            Date::make('Date of Birth'),
            Text::make('Place of Birth'),
        ]),
    ];
}

```

### [​](#limiting-displayed-fields)Limiting Displayed Fields

You may limit the amount of fields shown in a panel by default using the `limit` method:

CopyAsk AI```
use Laravel\Nova\Panel;

// ...

Panel::make('Profile', [
    Text::make('Full Name'),
    Date::make('Date of Birth'),
    Text::make('Place of Birth'),
])->limit(1),

```

Panels with a defined field limit will display a **Show All Fields** button in order to allow the user to view all of the defined fields when needed.

### [​](#collapsible-panels)Collapsible Panels

You may allow field panels to be collapsible by invoking the `collapsible` method when defining the panel. This method utilizes JavaScript’s `localStorage` feature to remember the current state of the panel between requests:

CopyAsk AI```
use Laravel\Nova\Panel;

// ...

Panel::make('Profile', [
    Text::make('Full Name'),
    Date::make('Date of Birth'),
    Text::make('Place of Birth'),
])->collapsible(),

```

You may indicate that a panel should always be collapsed by default via the `collapsedByDefault` method:

CopyAsk AI```
use Laravel\Nova\Panel;

// ...

Panel::make('Profile', [
    Text::make('Full Name'),
    Date::make('Date of Birth'),
    Text::make('Place of Birth'),
])->collapsedByDefault(),

```

## [​](#tabs)Tabs

The `Tab` panel allows you to organize resource fields and relationships within tab panels:

To create a tab panel when defining your resource’s fields, provide the tab group title and array of tabs to the `Tab::group` method. Each individual tab may be constructed using `Tab::make` and receives a tab title and array of fields:

app/Nova/Event.phpCopyAsk AI```
use Laravel\Nova\Fields\Currency;
use Laravel\Nova\Fields\HasMany;
use Laravel\Nova\Fields\HasManyThrough;
use Laravel\Nova\Fields\Hidden;
use Laravel\Nova\Fields\ID;
use Laravel\Nova\Http\Requests\NovaRequest;
use Laravel\Nova\Tabs\Tab;

// ...

/**
 * Get the fields displayed by the resource.
 *
 * @return array<int, \Laravel\Nova\Fields\Field|\Laravel\Nova\Panel>
 */
public function fields(NovaRequest $request): array
{
    return [
        ID::make()->sortable(),

        // ...

        Tab::group('Details', [
            Tab::make('Purchases', [
                Currency::make('Price')->asMinorUnits(),
                Number::make('Tickets Available'),
                Number::make('Tickets Sold'),
            ]),

            Tab::make('Registrations', [
                // ...
            ]),

            Tab::make('Event & Venue', [
                // ...
            ]),
        ]),

        Tab::group('Relations', [
            HasMany::make('Orders'),
            HasManyThrough::make('Tickets'),
        ]),
    ]
}

```

### [​](#omitting-tab-group-titles)Omitting Tab Group Titles

Tab group titles may be omitted by simply providing `fields` to the `Tab::group` method:

CopyAsk AI```
use Laravel\Nova\Tabs\Tab;

// ...

Tab::group(fields: [
    HasMany::make('Orders'),
    HasManyThrough::make('Tickets'),
]),

```
Was this page helpful?

YesNo[Repeater Fields](/docs/v5/resources/repeater-fields)[Relationships](/docs/v5/resources/relationships)On this page
- [Limiting Displayed Fields](#limiting-displayed-fields)
- [Collapsible Panels](#collapsible-panels)
- [Tabs](#tabs)
- [Omitting Tab Group Titles](#omitting-tab-group-titles)

[Laravel Nova home page](https://nova.laravel.com)[x](https://x.com/laravelphp)[github](https://github.com/laravel)[discord](https://discord.com/invite/laravel)[linkedin](https://linkedin.com/company/laravel)Platform

[Dashboard](https://nova.laravel.com/)[Status](https://status.laravel.com/)Legal and Compliance

[Term of Service](https://nova.laravel.com/terms)[Privacy Policy](https://nova.laravel.com/privacy)[x](https://x.com/laravelphp)[github](https://github.com/laravel)[discord](https://discord.com/invite/laravel)[linkedin](https://linkedin.com/company/laravel)AssistantResponses are generated using AI and may contain mistakes.