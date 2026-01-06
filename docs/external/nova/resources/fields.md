# Nova - Resources/Fields

*Source: https://nova.laravel.com/docs/v5/resources/fields*

---

[Laravel Nova home page![light logo](https://mintcdn.com/nova-laravel/bY_66OSFONsRO54M/logo/light.svg?fit=max&auto=format&n=bY_66OSFONsRO54M&q=85&s=d7b82e399050ba766ad412155b0dbc7a)![dark logo](https://mintcdn.com/nova-laravel/bY_66OSFONsRO54M/logo/dark.svg?fit=max&auto=format&n=bY_66OSFONsRO54M&q=85&s=a81b28aeb4ce32b7a8afd9ed1f9ce58b)](https://nova.laravel.com)

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

- [Defining Fields](#defining-fields)
- [Field Column Conventions](#field-column-conventions)
- [Showing / Hiding Fields](#showing-%2F-hiding-fields)
- [Showing Fields When Peeking](#showing-fields-when-peeking)
- [Resource Preview Modal](#resource-preview-modal)
- [Dynamic Field Methods](#dynamic-field-methods)
- [Default Values](#default-values)
- [Field Placeholder Text](#field-placeholder-text)
- [Field Hydration](#field-hydration)
- [Sortable Fields](#sortable-fields)
- [Field Types](#field-types)
- [Audio Field](#audio-field)
- [Avatar Field](#avatar-field)
- [Badge Field](#badge-field)
- [Boolean Field](#boolean-field)
- [Customizing True / False Values](#customizing-true-%2F-false-values)
- [Boolean Group Field](#boolean-group-field)
- [Code Field](#code-field)
- [Editing JSON](#editing-json)
- [Syntax Highlighting](#syntax-highlighting)
- [Color Field](#color-field)
- [Country Field](#country-field)
- [Currency Field](#currency-field)
- [Date Field](#date-field)
- [DateTime Field](#datetime-field)
- [Email Field](#email-field)
- [File Field](#file-field)
- [Gravatar Field](#gravatar-field)
- [Heading Field](#heading-field)
- [Hidden Field](#hidden-field)
- [ID Field](#id-field)
- [Image Field](#image-field)
- [KeyValue Field](#keyvalue-field)
- [Customizing KeyValue Labels](#customizing-keyvalue-labels)
- [Markdown Field](#markdown-field)
- [Markdown File Uploads](#markdown-file-uploads)
- [MultiSelect Field](#multiselect-field)
- [Number Field](#number-field)
- [Password Field](#password-field)
- [Password Confirmation Field](#password-confirmation-field)
- [Select Field](#select-field)
- [Using Enum as Options](#using-enum-as-options)
- [Searchable Select Fields](#searchable-select-fields)
- [Slug Field](#slug-field)
- [Sparkline Field](#sparkline-field)
- [Using Trend Metrics](#using-trend-metrics)
- [Customizing the Chart](#customizing-the-chart)
- [Status Field](#status-field)
- [Stack Field](#stack-field)
- [Line Fields](#line-fields)
- [Passing Closures to Line Fields](#passing-closures-to-line-fields)
- [Tag Field](#tag-field)
- [Previewing Tags](#previewing-tags)
- [Displaying Tags as Lists](#displaying-tags-as-lists)
- [Creating New Tags Inline](#creating-new-tags-inline)
- [Adjusting the Inline Creation Modal’s Size](#adjusting-the-inline-creation-modal%E2%80%99s-size)
- [Preloading Available Tags](#preloading-available-tags)
- [Text Field](#text-field)
- [Text Field Suggestions](#text-field-suggestions)
- [Formatting Text as Links](#formatting-text-as-links)
- [Copying Text Field Values to the Clipboard](#copying-text-field-values-to-the-clipboard)
- [Setting maxlength on Text Fields](#setting-maxlength-on-text-fields)
- [Textarea Field](#textarea-field)
- [Setting maxlength on Textarea Fields](#setting-maxlength-on-textarea-fields)
- [Timezone Field](#timezone-field)
- [Trix Field](#trix-field)
- [Trix File Uploads](#trix-file-uploads)
- [UI-Avatar Field](#ui-avatar-field)
- [URL Field](#url-field)
- [Vapor File Field](#vapor-file-field)
- [Vapor Image Field](#vapor-image-field)
- [Validating Vapor Image / File Fields](#validating-vapor-image-%2F-file-fields)
- [Computed Fields](#computed-fields)
- [Customization](#customization)
- [Readonly Fields](#readonly-fields)
- [Immutable Fields](#immutable-fields)
- [Required Fields](#required-fields)
- [Nullable Fields](#nullable-fields)
- [Field Placeholder Text](#field-placeholder-text-2)
- [Field Help Text](#field-help-text)
- [Field Stacking](#field-stacking)
- [Full Width Fields](#full-width-fields)
- [Field Text Alignment](#field-text-alignment)
- [Field Resolution / Formatting](#field-resolution-%2F-formatting)
- [Filterable Fields](#filterable-fields)
- [Extending Fields](#extending-fields)
- [Macro Arguments](#macro-arguments)
- [Macro on Specific Fields](#macro-on-specific-fields)

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

## [​](#showing-/-hiding-fields) Showing / Hiding Fields

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
    return $this->name === 'Taylor Otwell'

*[Content truncated for length]*