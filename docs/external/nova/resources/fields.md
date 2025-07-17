# Nova - Resources/Fields

*Source: https://nova.laravel.com/docs/v5/resources/fields*

---

[Laravel Nova home page![light logo](https://mintlify.s3.us-west-1.amazonaws.com/nova-laravel/logo/light.svg)![dark logo](https://mintlify.s3.us-west-1.amazonaws.com/nova-laravel/logo/dark.svg)](https://nova.laravel.com)

v5

Search...

⌘KAsk AI

- Support
- [Platform Status](https://status.laravel.com/)
- [Dashboard](https://nova.laravel.com)
- [Dashboard](https://nova.laravel.com)

Search...

Navigation

Resources

Fields

[Documentation](/docs/v5/installation)[Knowledge Base](/docs/kb/support)

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

Resources

# Fields

Nova ships with a variety of fields out of the box, including fields for text inputs, booleans, dates, file uploads, Markdown, and more.

## [​](#defining-fields) Defining Fields

Each Nova resource contains a `fields` method. This method returns an array of fields, which generally extend the `Laravel\Nova\Fields\Field` class. Nova ships with a variety of fields out of the box, including fields for text inputs, booleans, dates, file uploads, Markdown, and more.

To add a field to a resource, you may simply add it to the resource’s `fields` method. Typically, fields may be created using their static `make` method. This method accepts several arguments; however, you usually only need to pass the “human readable” name of the field. Nova will automatically “snake case” this string to determine the underlying database column:

app/Nova/User.php

Copy

Ask AI

```
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
{
    return [
        ID::make()->sortable(),
        Text::make('Name')->sortable(),
    ];
}

```

### [​](#field-column-conventions) Field Column Conventions

As noted above, Nova will “snake case” the displayable name of the field to determine the underlying database column. However, if necessary, you may pass the column name as the second argument to the field’s `make` method:

Copy

Ask AI

```
use Laravel\Nova\Fields\Text;

// ...

Text::make('Name', 'name_column'),

```

If the field has a JSON, `ArrayObject`, or array cast assigned to it, you may use the `->` operator to specify nested properties within the field:

Copy

Ask AI

```
use Laravel\Nova\Fields\Timezone;

// ...

Timezone::make('User Timezone', 'settings->timezone'),

```

## [​](#showing-%2F-hiding-fields) Showing / Hiding Fields

Often, you will only want to display a field in certain situations. For example, there is typically no need to show a `Password` field on a resource index listing. Likewise, you may wish to only display a `Created At` field on the creation / update forms. Nova makes it a breeze to hide / show fields on certain pages.

The following methods may be used to show / hide fields based on the display context:

- `showOnIndex`
- `showOnDetail`
- `showOnCreating`
- `showOnUpdating`
- `showOnPreview`
- `showWhenPeeking`
- `hideFromIndex`
- `hideFromDetail`
- `hideWhenCreating`
- `hideWhenUpdating`
- `onlyOnIndex`
- `onlyOnDetail`
- `onlyOnForms`
- `exceptOnForms`

You may chain any of these methods onto your field’s definition in order to instruct Nova where the field should be displayed:

Copy

Ask AI

```
use Laravel\Nova\Fields\Text;

// ...

Text::make('Name')->hideFromIndex(),

```

Alternatively, you may pass a callback to the following methods.

- `showOnIndex`
- `showOnDetail`
- `showOnCreating`
- `showOnUpdating`
- `showWhenPeeking`
- `hideFromIndex`
- `hideFromDetail`
- `hideWhenCreating`
- `hideWhenUpdating`
- `showOnPreview`
- `onlyOnPreview`

For `show*` methods, the field will be displayed if the given callback returns `true`:

Copy

Ask AI

```
use Laravel\Nova\Fields\Text;

// ...

Text::make('Name')->showOnIndex(function (NovaRequest $request, $resource) {
    return $this->name === 'Taylor Otwell';
}),

```

For `hide*` methods, the field will be hidden if the given callback returns `true`:

Copy

Ask AI

```
use Laravel\Nova\Fields\Text;

// ...

Text::make('Name')->hideFromIndex(function (NovaRequest $request, $resource) {
    return $this->name === 'Taylor Otwell';
}),

```

### [​](#showing-fields-when-peeking) Showing Fields When Peeking

You may allow a field to be visible [when peeking at the resource](./relationships#peeking-at-belongsto-relationships) by invoking the `showWhenPeeking` method when defining the field:

Copy

Ask AI

```
use Laravel\Nova\Fields\Text;

// ...

Text::make('Name')->showWhenPeeking(),

```

### [​](#resource-preview-modal) Resource Preview Modal

You may also define which fields should be included in the resource’s “preview” modal. This modal can be displayed for a given resource by the user when viewing the resource’s index:

Copy

Ask AI

```
use Laravel\Nova\Fields\Markdown;
use Laravel\Nova\Fields\Text;

// ...

Text::make('Title')->showOnPreview(),

Markdown::make('Content')->showOnPreview(),

```

Alternatively, you may pass a callback to the `showOnPreview` method:

Copy

Ask AI

```
use Laravel\Nova\Fields\Markdown;

// ...

Markdown::make('Content')->showOnPreview(function (NovaRequest $request, $resource) {
    return $request->user()->can('previewContent');
}),

```

![Resource Preview](https://mintlify.s3.us-west-1.amazonaws.com/nova-laravel/images/resource-preview.png)

## [​](#dynamic-field-methods) Dynamic Field Methods

If your application requires it, you may specify a separate list of fields for specific display contexts. For example, imagine you have a resource with the following list of fields:

app/Nova/~Resource.php

Copy

Ask AI

```
use Laravel\Nova\Fields\Text;
use Laravel\Nova\Http\Requests\NovaRequest;

// ... 

/**
 * Get the fields displayed by the resource.
 *
 * @return array<int, \Laravel\Nova\Fields\Field>
 */
public function fields(NovaRequest $request): array
{
    return [
        Text::make('First Name'),
        Text::make('Last Name'),
        Text::make('Job Title'),
    ];
}

```

On your detail page, you may wish to show a combined name via a computed field, followed by the job title. In order to do this, you could add a `fieldsForDetail` method to the resource class which returns a separate list of fields that should only be displayed on the resource’s detail page:

app/Nova/~Resource.php

Copy

Ask AI

```
use Laravel\Nova\Fields\Text;
use Laravel\Nova\Http\Requests\NovaRequest;

// ... 

/**
 * Get the fields displayed by the resource on detail page.
 *
 * @return array<int, \Laravel\Nova\Fields\Field>
 */
public function fieldsForDetail(NovaRequest $request): array
{
    return [
        Text::make('Name', function () {
            return sprintf('%s %s', $this->first_name, $this->last_name);
        }),

        Text::make('Job Title'),
    ];
}

```

The available methods that may be defined for individual display contexts are:

- `fieldsForIndex`
- `fieldsForDetail`
- `fieldsForInlineCreate`
- `fieldsForCreate`
- `fieldsForUpdate`
- `fieldsForPreview`

The `fieldsForIndex`, `fieldsForDetail`, `fieldsForInlineCreate`, `fieldsForCreate`,`fieldsForUpdate`, and `fieldsForPreview` methods always take precedence over the `fields` method.

## [​](#default-values) Default Values

There are times you may wish to provide a default value to your fields. Nova offers this functionality via the `default` method, which accepts a value or callback. This value will be used as the field’s default input value on the resource’s creation view:

Copy

Ask AI

```
use Laravel\Nova\Fields\BelongsTo;
use Laravel\Nova\Fields\Text;

// ...

BelongsTo::make('Name')->default($request->user()->getKey()),

Text::make('Uuid')->default(function ($request) {
    return Str::orderedUuid();
}),

```

## [​](#field-placeholder-text) Field Placeholder Text

By default, the placeholder text of a field will be it’s name. You can override the place

*[Content truncated for length]*