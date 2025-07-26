# Nova - Releases

*Source: https://nova.laravel.com/docs/v5/releases*

---

- [Community](https://discord.com/invite/laravel)
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

On this page

- [Modernizing Dependencies](#modernizing-dependencies)
- [Tab Panels](#tab-panels)
- [Fields & Filters Improvements](#fields-%26-filters-improvements)
- [New Dependent Computed Field via Field::computed() method](#new-dependent-computed-field-via-field%3A%3Acomputed-method)
- [New Field::immutable() method](#new-field%3A%3Aimmutable-method)
- [Other Field Improvements](#other-field-improvements)
- [Separate Policy Classes for Nova Resources](#separate-policy-classes-for-nova-resources)

Get Started

# Release Notes

Laravel Nova Release Notes

Nova 5 continues the improvements made in Nova 4.x by introducing support for tab panels, searchable select filters, dependent field improvements, third party component improvements, and dependency modernization with support for Inertia.js 2.x.

## [​](#modernizing-dependencies) Modernizing Dependencies

Nova 5 removes support for Laravel 8.x and 9.x, while also requiring PHP 8.1+. This dependency upgrade allows for deeper integration with the Laravel ecosystem, including Fortify, Prompts, and Pennant.
Furthermore, Nova’s frontend code has been updated to utilize Vue 3.5, Heroicons 2.x, and Inertia.js 2.x. Please refer to the Nova [upgrade guide](./upgrade#dependency-upgrades) for a detailed description of these changes and how they affect your application.

## [​](#tab-panels) Tab Panels

Nova 5 further improves the resource UI with the introduction of **Tabs Panels** on the resource detail and form pages:

app/Nova/Event.php

Copy

Ask AI

```
use Laravel\Nova\Fields\HasMany;
use Laravel\Nova\Fields\HasManyThrough;
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
        // ...

        Tab::group('Details', [
            Tab::make('Purchases', [ /* List of fields */ ]),
            Tab::make('Registrations', [ /* List of fields */ ]),
            Tab::make('Event & Venue', [ /* List of fields */ ]),
        ]),

        Tab::group(attribute: 'Relations', fields: [
            HasMany::make('Orders', 'orders', Order::class),
            HasManyThrough::make('Tickets', 'tickets', Ticket::class),
        ]),
    ];
}

```

For example, the code snippet above will generate the following tabs:

![Tab Panel](https://mintlify.s3.us-west-1.amazonaws.com/nova-laravel/images/tab-panel.png)

To learn more about adding tab panels to your Nova resources, check out the [tab documentation](./resources/panels#tabs).

## [​](#fields-%26-filters-improvements) Fields & Filters Improvements

### [​](#new-dependent-computed-field-via-field%3A%3Acomputed-method) New Dependent Computed Field via `Field::computed()` method

Nova 5 introduces an enhanced `computed` method that builds upon the previous computed fields feature. While computed fields have always been valuable for displaying additional resource information, they previously lacked a unique `$attribute` identifier, which limited their use as dependent fields. This limitation has been resolved in Nova 5:

Copy

Ask AI

```
use Laravel\Nova\Fields\Boolean;
use Laravel\Nova\Fields\FormData;
use Laravel\Nova\Fields\Text;
use Laravel\Nova\Http\Requests\NovaRequest;

// ... 

Boolean::make('Would you like to leave a comment?', 'comment_boolean')
    ->computed(),

Text::make('Comment')
    ->hidden()
    ->dependsOn('comment_boolean', function (Text $field, NovaRequest $request, FormData $formData) {
        if ($formData->boolean('comment_boolean') === true) {
            $field->show();
        }
    }),

```

More information on computed fields can be found within the [computed field documentation](./resources/dependent-fields#dependable-computed-fields).

### [​](#new-field%3A%3Aimmutable-method) New `Field::immutable()` method

While [readonly fields](./resources/fields#readonly-fields) disable a field’s input and prevent form submission of its value, immutable fields offer more flexibility. By invoking the `immutable` method on a field, you can prevent users from modifying the field’s value while still allowing it to be submitted with the form.
You may also pass a boolean argument to the `immutable` method to dynamically control whether a field should be immutable:

Copy

Ask AI

```
use Laravel\Nova\Fields\Text;

// ...

Text::make('Name')->immutable(),

```

Further reading is available on the [documentation](./resources/fields#immutable-fields).

### [​](#other-field-improvements) Other Field Improvements

- [Enums may now be used as `Select::options()`](./resources/fields#using-enum-as-options)
- [Searchable select filters are now supported](./filters/registering-filters#searchable-select-filter)
- JSON `Repeater` fields are now displayed on the resource detail page

## [​](#separate-policy-classes-for-nova-resources) Separate Policy Classes for Nova Resources

In previous Nova releases, Nova resources shared authorization policies with your user-facing application. This approach to authorization can present problems if your application’s authorization logic differs from how resource authorization should be handled for Nova operations.
In Nova 5, you may now create a separate policy class that is only used for operations that are triggered via Nova:

Copy

Ask AI

```
php artisan nova:policy

```

![Create UserPolicy class](https://mintlify.s3.us-west-1.amazonaws.com/nova-laravel/images/make-policy-command.png)

To enable the new policy you need to add the following code:

app/Nova/User.php

Copy

Ask AI

```
namespace App\Nova;

class User extends Resource
{
    /**
     * The policy the resource corresponds to.
     *
     * @var class-string
     */
    public static $policy = Policies\UserPolicy::class;
}

```

Further reading is available on the [Authorization](./resources/authorization#using-separate-policy-class-for-nova-resource) documentation.

Was this page helpful?

YesNo

[Installation](/docs/v5/installation)[Upgrade Guide](/docs/v5/upgrade)

Assistant

Responses are generated using AI and may contain mistakes.