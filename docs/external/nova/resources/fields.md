# Nova - Resources/Fields

*Source: https://nova.laravel.com/docs/v5/resources/fields*

---

[Laravel Nova home page](https://nova.laravel.com)
v5
Search...
⌘KAsk AI
- [email protected]
- [Platform Status](https://status.laravel.com/)
- [Dashboard](https://nova.laravel.com)
- [Dashboard](https://nova.laravel.com)
Search...
Navigation
Resources
Fields
[Documentation](/docs/v5/installation)[Knowledge Base](/docs/kb/support)
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
- [Disabled Select Options](#disabled-select-options)
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
By default, the placeholder text of a field will be it’s name. You can override the placeholder text of a field that supports placeholders by using the `placeholder` method:
Copy
Ask AI
```
use Laravel\Nova\Fields\Text;

// ...

Text::make('Name')->placeholder('My New Post'),
```
## [​](#field-hydration) Field Hydration
On every create or update request that Nova receives for a given resource, each field’s corresponding model attribute will automatically be filled before the model is persisted to the database. If necessary, you may customize the hydration behavior of a given field using the `fillUsing` method:
Copy
Ask AI
```
use Illuminate\Support\Str;
use Laravel\Nova\Fields\Text;

// ...

Text::make('Name', 'name')
    ->fillUsing(function ($request, $model, $attribute, $requestAttribute) {
        $model->{$attribute} = Str::title($request->input($attribute));
    }),
```
## [​](#sortable-fields) Sortable Fields
When attaching a field to a resource, you may use the `sortable` method to indicate that the resource index may be sorted by the given field:
Copy
Ask AI
```
use Laravel\Nova\Fields\Text;

// ...

Text::make('Name', 'name_column')->sortable(),
```
## [​](#field-types) Field Types
This portion of the documentation only discusses non-relationship fields. To learn more about relationship fields, [check out their documentation](./relationships).
Nova ships with a variety of field types. So, let’s explore all of the available types and their options:
- [Audio](#audio-field)
- [Avatar](#avatar-field)
- [Badge](#badge-field)
- [Boolean](#boolean-field)
- [Boolean Group](#boolean-group-field)
- [Code](#code-field)
- [Color](#color-field)
- [Country](#country-field)
- [Currency](#currency-field)
- [Date](#date-field)
- [DateTime](#datetime-field)
- [Email](#email-field)
- [File](#file-field)
- [Gravatar](#gravatar-field)
- [Heading](#heading-field)
- [Hidden](#hidden-field)
- [ID](#id-field)
- [Image](#image-field)
- [KeyValue](#keyvalue-field)
- [Markdown](#markdown-field)
- [MultiSelect](#multiselect-field)
- [Number](#number-field)
- [Password](#password-field)
- [Password Confirmation](#password-confirmation-field)
- [Select](#select-field)
- [Slug](#slug-field)
- [Sparkline](#sparkline-field)
- [Status](#status-field)
- [Stack](#stack-field)
- [Tag](#tag-field)
- [Text](#text-field)
- [Textarea](#textarea-field)
- [Timezone](#timezone-field)
- [Trix](#trix-field)
- [UI-Avatar](#ui-avatar-field)
- [URL](#url-field)
- [Vapor File](#vapor-file-field)
- [Vapor Image](#vapor-image-field)
### [​](#audio-field) Audio Field
The `Audio` field extends the [File field](#file-field) and accepts the same options and configurations. The `Audio` field, unlike the `File` field, will display a thumbnail preview of the underlying image when viewing the resource:
Copy
Ask AI
```
use Laravel\Nova\Fields\Audio;

// ...

Audio::make('Theme Song'),
```
By default, the `Audio` field allows the user to download the linked file. To disable downloads, you may use the `disableDownload` method on the field definition:
Copy
Ask AI
```
use Laravel\Nova\Fields\Audio;

// ...

Audio::make('Theme Song')->disableDownload(),
```
You can set the [preload attribute](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/audio#attr-preload) of the field by using the `preload` method:
Copy
Ask AI
```
use Laravel\Nova\Fields\Audio;

// ...

Audio::make('Theme Song')->preload('auto'),

Audio::make('Theme Song')->preload(Audio::PRELOAD_METADATA),
```
To learn more about defining file fields and handling uploads, check out the comprehensive [file field documentation](./file-fields).
### [​](#avatar-field) Avatar Field
The `Avatar` field extends the [Image field](#image-field) and accepts the same options and configuration:
Copy
Ask AI
```
use Laravel\Nova\Fields\Avatar;

// ...

Avatar::make('Avatar'),
```
If a resource contains an `Avatar` field, that field will be displayed next to the resource’s title when the resource is displayed in search results:
You may use the `squared` method to display the image’s thumbnail with squared edges. Additionally, you may use the `rounded` method to display its thumbnails with fully-rounded edges:
Copy
Ask AI
```
use Laravel\Nova\Fields\Avatar;

// ...

Avatar::make('Avatar')->squared(),
```
### [​](#badge-field) Badge Field
The `Badge` field can be used to display the status of a `Resource` in the index and detail views:
Copy
Ask AI
```
use Laravel\Nova\Fields\Badge;

// ...

Badge::make('Status', function () {
    return User::statuses[$this->status];
}),
```
By default, the `Badge` field supports four variations: `info`, `success`, `danger`, and `warning`. You may define your possible field values and their associated badge types using the `map` method:
Copy
Ask AI
```
use Laravel\Nova\Fields\Badge;

// ...

Badge::make('Status')->map([
    'draft' => 'danger',
    'published' => 'success',
]),
```
Alternatively, you may use the `types` method to completely replace the built-in badge types and their associated CSS classes. The CSS classes may be provided as a string or an array:
Copy
Ask AI
```
use Laravel\Nova\Fields\Badge;

// ...

Badge::make('Status')->types([
    'draft' => 'font-medium text-gray-600',
    'published' => ['font-bold', 'text-green-600'],
]),
```
If you only wish to supplement the built-in badge types instead of overwriting all of them, you may use the `addTypes` method:
Copy
Ask AI
```
use Laravel\Nova\Fields\Badge;

// ...

Badge::make('Status')->addTypes([
    'draft' => 'custom classes',
]),
```
By default the `Badge` field is not shown on a resource’s edit or update pages. If you wish to modify the underlying value represented by the `Badge` field on your edit forms, define another field in combination with the `onlyOnForms` field option.
If you’d like to display your badge with an associated icon, you can use the `withIcons` method to direct Nova to display an icon:
Copy
Ask AI
```
use Laravel\Nova\Fields\Badge;

// ...

Badge::make('Status')->map([
    'draft' => 'danger',
    'published' => 'success',
])->withIcons(),
```
If you’d like to customize the icons used when display `Badge` fields you can use the `icons` method:
Copy
Ask AI
```
use Laravel\Nova\Fields\Badge;

// ...

Badge::make('Status')->map([
    'draft' => 'danger',
    'published' => 'success',
])->icons([
    'danger' => 'exclamation-circle',
    'success' => 'check-circle',
]),
```
If you’d like to customize the label that is displayed you can use the `label` method:
Copy
Ask AI
```
use Laravel\Nova\Fields\Badge;

// ...

Badge::make('Status')->map([
    'draft' => 'danger',
    'published' => 'success',
])->label(function ($value) {
    return __($value);
}),
```
You may provide a list of labels using the `labels` method:
Copy
Ask AI
```
use Laravel\Nova\Fields\Badge;

// ...

Badge::make('Status')->map([
    'draft' => 'danger',
    'published' => 'success',
])->labels([
    'draft' => 'Draft',
    'published' => 'Published',
]),
```
### [​](#boolean-field) Boolean Field
The `Boolean` field may be used to represent a boolean / “tiny integer” column in your database. For example, assuming your database has a boolean column named `active`, you may attach a `Boolean` field to your resource like so:
Copy
Ask AI
```
use Laravel\Nova\Fields\Boolean;

// ...

Boolean::make('Active'),
```
#### [​](#customizing-true-/-false-values) Customizing True / False Values
If you are using values other than `true`, `false`, `1`, or `0` to represent “true” and “false”, you may instruct Nova to use the custom values recognized by your application. To accomplish this, chain the `trueValue` and `falseValue` methods onto your field’s definition:
Copy
Ask AI
```
use Laravel\Nova\Fields\Boolean;

// ...

Boolean::make('Active')
    ->trueValue('On')
    ->falseValue('Off'),
```
### [​](#boolean-group-field) Boolean Group Field
The `BooleanGroup` field may be used to group a set of Boolean checkboxes, which are then stored as JSON key-values in the database column they represent. You may create a `BooleanGroup` field by providing a set of keys and labels for each option:
Copy
Ask AI
```
use Laravel\Nova\Fields\BooleanGroup;

// ...

BooleanGroup::make('Permissions')->options([
    'create' => 'Create',
    'read' => 'Read',
    'update' => 'Update',
    'delete' => 'Delete',
]),
```
The user will be presented with a grouped set of checkboxes which, when saved, will be converted to JSON format:
Copy
Ask AI
```
{
  "create": true,
  "read": false,
  "update": false,
  "delete": false
}
```
Before using this field type, you should ensure that the underlying Eloquent attribute is configured to cast to an `array` (or equivalent) within your Eloquent model class:
Copy
Ask AI
```
protected $casts = [
    'permissions' => 'array'
];
```
Sometimes, you may wish to exclude values that are `true` or `false` from display to avoid cluttering the representation of the field. You may accomplish this by invoking the `hideFalseValues` or `hideTrueValues` methods on the field definition:
Copy
Ask AI
```
use Laravel\Nova\Fields\BooleanGroup;

// ...

BooleanGroup::make('Permissions')->options([
    'create' => 'Create',
    'read' => 'Read',
    'update' => 'Update',
    'delete' => 'Delete',
])->hideFalseValues(),

BooleanGroup::make('Permissions')->options([
    'create' => 'Create',
    'read' => 'Read',
    'update' => 'Update',
    'delete' => 'Delete',
])->hideTrueValues(),
```
If the underlying field is empty, Nova will display “No Data”. You may customize this text using the `noValueText` method:
Copy
Ask AI
```
use Laravel\Nova\Fields\BooleanGroup;

// ...

BooleanGroup::make('Permissions')->options([
    'create' => 'Create',
    'read' => 'Read',
    'update' => 'Update',
    'delete' => 'Delete',
])->noValueText('No permissions selected.'),
```
### [​](#code-field) Code Field
The `Code` fields provides a beautiful code editor within your Nova administration panel. Generally, code fields should be attached to `TEXT` database columns:
Copy
Ask AI
```
use Laravel\Nova\Fields\Code;

// ...

Code::make('Snippet'),
```
You may also attach `Code` fields to `JSON` database columns. By default, the field will display the value as a JSON string. You may cast the underlying Eloquent attribute to `array`, `collection`, `object`, or `json` based on your application’s needs:
Copy
Ask AI
```
use Laravel\Nova\Fields\Code;

// ...

Code::make('Options')->json(),
```
By default, Nova will never display a `Code` field on a resource index listing.
#### [​](#editing-json) Editing JSON
If you intend to use a given `Code` field instance to only edit JSON, you may chain the `json` method onto your field definition:
Copy
Ask AI
```
use Laravel\Nova\Fields\Code;

// ...

Code::make('Options')->json(),
```
Nova does not automatically apply the `json` validation rule to `Code` fields. This rule must be manually specified during validation if you wish for it to be applied.
#### [​](#syntax-highlighting) Syntax Highlighting
You may customize the language syntax highlighting of the `Code` field using the `language` method:
Copy
Ask AI
```
use Laravel\Nova\Fields\Code;

// ...

Code::make('Snippet')->language('php'),
```
The `Code` field’s currently supported languages are:
- `dockerfile`
- `htmlmixed`
- `javascript`
- `markdown`
- `nginx`
- `php`
- `ruby`
- `sass`
- `shell`
- `sql`
- `twig`
- `vim`
- `vue`
- `xml`
- `yaml-frontmatter`
- `yaml`
### [​](#color-field) Color Field
The `Color` field generates a color picker using the HTML5 `color` input element:
Copy
Ask AI
```
use Laravel\Nova\Fields\Color;

// ...

Color::make('Color', 'label_color'),
```
### [​](#country-field) Country Field
The `Country` field generates a `Select` field containing a list of the world’s countries. The field will store the country’s corresponding two-letter code:
Copy
Ask AI
```
use Laravel\Nova\Fields\Country;

// ...

Country::make('Country', 'country_code'),
```
### [​](#currency-field) Currency Field
The `Currency` field generates a `Number` field that is automatically formatted using the `brick/money` PHP package. Nova will use `USD` as the default currency; however, this can be changed by modifying the `nova.currency` configuration value:
Copy
Ask AI
```
use Laravel\Nova\Fields\Currency;

// ...

Currency::make('Price'),
```
You may override the currency on a per-field basis using the `currency` method:
Copy
Ask AI
```
use Laravel\Nova\Fields\Currency;

// ...

Currency::make('Price')->currency('EUR'),
```
The `ext-intl` PHP extension is required to display formatted currency. Or, you may install the `symfony/polyfill-intl-icu` Composer package which offers support for the “en” locale.
You may use the `min`, `max`, and `step` methods to set their corresponding attributes on the generated `input` control:
Copy
Ask AI
```
use Laravel\Nova\Fields\Currency;

// ...

Currency::make('price')->min(1)->max(1000)->step(0.01),
```
If you plan to customize the currency “step” amount using the `step` method, you should ensure you always call the `step` method after the `currency`, `asMinorUnits`, and `asMajorUnits` methods. Calling these methods after the `step` method will override the `step` method’s behavior.
The field’s locale will respect the value in your application’s `app.locale` configuration value. You can override this behavior by providing a locale code to the `locale` method:
Copy
Ask AI
```
use Laravel\Nova\Fields\Currency;

// ...

Currency::make('Price')->locale('fr'),
```
### [​](#date-field) Date Field
The `Date` field may be used to store a date value (without time). For more information about dates and timezones within Nova, check out the additional [date / timezone documentation](./date-fields):
Copy
Ask AI
```
use Laravel\Nova\Fields\Date;

// ...

Date::make('Birthday'),
```
### [​](#datetime-field) DateTime Field
The `DateTime` field may be used to store a date-time value. For more information about dates and timezones within Nova, check out the additional [date / timezone documentation](./date-fields):
Copy
Ask AI
```
use Laravel\Nova\Fields\DateTime;

// ...

DateTime::make('Updated At')->hideFromIndex(),
```
### [​](#email-field) Email Field
The `Email` field may be used to display a column with a `mailto:` link on the index and detail views:
Copy
Ask AI
```
use Laravel\Nova\Fields\Email;

// ...

Email::make(),

Email::make('Customer Email', 'customer_email'),
```
### [​](#file-field) File Field
To learn more about defining file fields and handling uploads, please refer to the comprehensive [file field documentation](./file-fields).
Copy
Ask AI
```
use Laravel\Nova\Fields\File;

// ...

File::make('Attachment'),
```
### [​](#gravatar-field) Gravatar Field
The `Gravatar` field does not correspond to any column in your application’s database. Instead, it will display the “Gravatar” image of the model it is associated with.
By default, the Gravatar URL will be generated based on the value of the model’s `email` column. However, if your user’s email addresses are not stored in the `email` column, you may pass a custom column name to the field’s `make` method:
Copy
Ask AI
```
use Laravel\Nova\Fields\Gravatar;

// ...

// Using the "email" column...
Gravatar::make(),

// Using the "email_address" column...
Gravatar::make('Avatar', 'email_address'),
```
You may use the `squared` method to display the image’s thumbnail with squared edges. Additionally, you may use the `rounded` method to display the images with fully-rounded edges:
Copy
Ask AI
```
use Laravel\Nova\Fields\Gravatar;

// ...

Gravatar::make('Avatar', 'email_address')->squared(),
```
### [​](#heading-field) Heading Field
The `Heading` field does not correspond to any column in your application’s database. It is used to display a banner across your forms and can function as a separator for long lists of fields:
Copy
Ask AI
```
use Laravel\Nova\Fields\Heading;

// ...

Heading::make('Meta'),
```
If you need to render HTML content within the `Heading` field, you may invoke the `asHtml` method when defining the field:
Copy
Ask AI
```
use Laravel\Nova\Fields\Heading;

// ...

Heading::make('<p class="text-red-500">* All fields are required.</p>')->asHtml(),
```
`Heading` fields are automatically hidden from the resource index page.
### [​](#hidden-field) Hidden Field
The `Hidden` field may be used to pass any value that doesn’t need to be changed by the user but is required for saving the resource:
Copy
Ask AI
```
use Laravel\Nova\Fields\Hidden;

// ...

Hidden::make('Slug'),

Hidden::make('Slug')->default(Str::random(64)),
```
Combined with [default values](#default-values), `Hidden` fields are useful for passing things like related IDs to your forms:
Copy
Ask AI
```
use Laravel\Nova\Fields\Hidden;

// ...

Hidden::make('User', 'user_id')->default(function ($request) {
    return $request->user()->id;
}),
```
### [​](#id-field) ID Field
The `ID` field represents the primary key of your resource’s database table. Typically, each Nova resource you define should contain an `ID` field. By default, the `ID` field assumes the underlying database column is named `id`; however, you may pass the column name as the second argument to the `make` method if necessary:
Copy
Ask AI
```
use Laravel\Nova\Fields\ID;

// ...

ID::make(),

ID::make('ID', 'id_column'),
```
If your application contains very large integer IDs, you may need to use the `asBigInt` method in order for the Nova client to correctly render the integer:
Copy
Ask AI
```
use Laravel\Nova\Fields\ID;

// ...

ID::make()->asBigInt(),
```
There should only be one `ID` field configured per resource.
### [​](#image-field) Image Field
The `Image` field extends the [File field](#file-field) and accepts the same options and configurations. The `Image` field, unlike the `File` field, will display a thumbnail preview of the underlying image when viewing the resource:
Copy
Ask AI
```
use Laravel\Nova\Fields\Image;

// ...

Image::make('Photo'),
```
By default, the `Image` field allows the user to download the linked file. To disable downloads, you may use the `disableDownload` method on the field definition:
Copy
Ask AI
```
use Laravel\Nova\Fields\Image;

// ...

Image::make('Photo')->disableDownload(),
```
You may use the `squared` method to display the image’s thumbnail with squared edges. Additionally, you may use the `rounded` method to display its thumbnails with fully-rounded edges.
To learn more about defining file fields and handling uploads, check out the comprehensive [file field documentation](./file-fields).
### [​](#keyvalue-field) KeyValue Field
The `KeyValue` field provides a convenient interface to edit flat, key-value data stored inside `JSON` column types. For example, you might store profile information inside a [JSON column type](https://laravel.com/docs/eloquent-mutators#array-and-json-casting) named `meta`:
Copy
Ask AI
```
use Laravel\Nova\Fields\KeyValue;

// ...

KeyValue::make('Meta')->rules('json'),
```
Given the field definition above, the following interface would be rendered by Nova:
#### [​](#customizing-keyvalue-labels) Customizing KeyValue Labels
You can customize the text values used in the component by calling the `keyLabel`, `valueLabel`, and `actionText` methods when defining the field. The `actionText` method customizes the “add row” button text:
Copy
Ask AI
```
use Laravel\Nova\Fields\KeyValue;

// ...

KeyValue::make('Meta')
    ->keyLabel('Item')
    ->valueLabel('Label')
    ->actionText('Add Item'),
```
By default, Nova will never display a `KeyValue` field on a resource index listing.
If you would like to disable the user’s ability to edit the keys of the field, you may use the `disableEditingKeys` method to accomplish this. Disabling editing keys with the `disableEditingKeys` method will automatically disable adding rows as well:
Copy
Ask AI
```
use Laravel\Nova\Fields\KeyValue;

// ...

KeyValue::make('Meta')->disableEditingKeys(),
```
You may also remove the user’s ability to add new rows to the field by chaining the `disableAddingRows` method onto the field’s definition:
Copy
Ask AI
```
use Laravel\Nova\Fields\KeyValue;

// ...

KeyValue::make('Meta')->disableAddingRows(),
```
In addition, you may also wish to remove the user’s ability to delete exisiting rows in the field. You may accomplish this by invoking the `disableDeletingRows` method when defining the field:
Copy
Ask AI
```
use Laravel\Nova\Fields\KeyValue;

// ...

KeyValue::make('Meta')->disableDeletingRows(),
```
### [​](#markdown-field) Markdown Field
The `Markdown` field provides a WYSIWYG Markdown editor for its underlying Eloquent attribute. Typically, this field will correspond to a `TEXT` column in your database. The `Markdown` field will store the raw Markdown text within the associated database column:
Copy
Ask AI
```
use Laravel\Nova\Fields\Markdown;

// ...

Markdown::make('Biography'),
```
By default, Markdown fields will not display their content when viewing a resource’s detail page. Instead, the content will be hidden behind a “Show Content” link that will reveal the field’s content when clicked. You may specify that the Markdown field should always display its content by calling the `alwaysShow` method on the field itself:
Copy
Ask AI
```
use Laravel\Nova\Fields\Markdown;

// ...

Markdown::make('Biography')->alwaysShow(),
```
The Markdown field uses the `league/commonmark` package to parse Markdown content. By default, it uses a parsing strategy similar to GitHub Flavoured Markdown, which does not allow certain HTML within the Markdown content. However, you can change the parsing strategy using the `preset` method. Currently, the following built-in presets are `default`, `commonmark`, and `zero`:
Copy
Ask AI
```
use Laravel\Nova\Fields\Markdown;

// ...

Markdown::make('Biography')->preset('commonmark'),
```
Using the `preset` method, you may register and use custom preset implementations:
Copy
Ask AI
```
use Illuminate\Support\Str;
use Laravel\Nova\Fields\Markdown;
use Laravel\Nova\Fields\Markdown\MarkdownPreset;

// ...

Markdown::make('Biography')->preset('github', new class implements MarkdownPreset {
    /**
     * Convert the given content from markdown to HTML.
     *
     * @param  string  $content
     * @return string
     */
    public function convert(string $content)
    {
        return Str::of($content)->markdown([
            'html_input' => 'strip',
        ]);
    }
}),
```
#### [​](#markdown-file-uploads) Markdown File Uploads
If you would like to allow users to drag-and-drop photos into the `Markdown` field, you may chain the `withFiles` method onto the field’s definition. When calling the `withFiles` method, you should pass the name of the [filesystem disk](https://laravel.com/docs/filesystem) that photos should be stored on:
Copy
Ask AI
```
use Laravel\Nova\Fields\Markdown;

// ...

Markdown::make('Biography')->withFiles('public'),
```
Nova will define two database tables to store pending and persisted `Field` uploads. These two tables will be created automatically when you run Nova’s migrations during installation: `nova_pending_field_attachments` and `nova_field_attachments`.
Finally, in your `routes/console.php` file, you should register a [daily scheduled task](https://laravel.com/docs/scheduling) to prune any stale attachments from the pending attachments table and storage. For convenience, Laravel Nova provides the job implementation needed to accomplish this:
routes/console.php
Copy
Ask AI
```
use Illuminate\Support\Facades\Schedule;
use Laravel\Nova\Fields\Attachments\PruneStaleAttachments;

// ...

Schedule::call(new PruneStaleAttachments)->daily();
```
### [​](#multiselect-field) MultiSelect Field
The `MultiSelect` field provides a `Select` field that allows multiple selection options. This field pairs nicely with model attributes that are cast to `array` or equivalent:
Copy
Ask AI
```
use Laravel\Nova\Fields\MultiSelect;

// ...

MultiSelect::make('Sizes')->options([
    'S' => 'Small',
    'M' => 'Medium',
    'L' => 'Large',
]),
```
On the resource index and detail pages, the `MultiSelect` field’s “key” value will be displayed. If you would like to display the label values instead, you may invoke the `displayUsingLabels` method when defining the field:
Copy
Ask AI
```
use Laravel\Nova\Fields\MultiSelect;

// ...

MultiSelect::make('Size')->options([
    'S' => 'Small',
    'M' => 'Medium',
    'L' => 'Large',
])->displayUsingLabels(),
```
You may also display multi-select options in groups by providing an array structure that contains keys and `label` / `group` pairs:
Copy
Ask AI
```
use Laravel\Nova\Fields\MultiSelect;

// ...

MultiSelect::make('Sizes')->options([
    'MS' => ['label' => 'Small', 'group' => "Men's Sizes"],
    'MM' => ['label' => 'Medium', 'group' => "Men's Sizes"],
    'WS' => ['label' => 'Small', 'group' => "Women's Sizes"],
    'WM' => ['label' => 'Medium', 'group' => "Women's Sizes"],
])->displayUsingLabels(),
```
### [​](#number-field) Number Field
The `Number` field provides an `input` control with a `type` attribute of `number`:
Copy
Ask AI
```
use Laravel\Nova\Fields\Number;

// ...

Number::make('price'),
```
You may use the `min`, `max`, and `step` methods to set the corresponding HTML attributes on the generated `input` control:
Copy
Ask AI
```
use Laravel\Nova\Fields\Number;

// ...

Number::make('price')->min(1)->max(1000)->step(0.01),
```
You may also allow arbitrary-precision decimal values:
Copy
Ask AI
```
use Laravel\Nova\Fields\Number;

// ...

Number::make('price')->min(1)->max(1000)->step('any'),
```
### [​](#password-field) Password Field
The `Password` field provides an `input` control with a `type` attribute of `password`:
Copy
Ask AI
```
use Laravel\Nova\Fields\Password;

// ...

Password::make('Password'),
```
The `Password` field will automatically preserve the password that is currently stored in the database if the incoming password field is empty. Therefore, a typical password field definition might look like the following:
Copy
Ask AI
```
use Illuminate\Validation\Rules;
use Laravel\Nova\Fields\Password;

// ...

Password::make('Password')
    ->onlyOnForms()
    ->creationRules('required', Rules\Password::defaults())
    ->updateRules('nullable', Rules\Password::defaults()),
```
### [​](#password-confirmation-field) Password Confirmation Field
The `PasswordConfirmation` field provides an input that can be used for confirming another `Password` field. This field will only be shown on forms and will not attempt to hydrate an underlying attribute on the Eloquent model:
Copy
Ask AI
```
use Laravel\Nova\Fields\PasswordConfirmation;

// ...

PasswordConfirmation::make('Password Confirmation'),
```
When using this field, you should define the appropriate validation rules on the corresponding `Password` field:
Copy
Ask AI
```
use Illuminate\Validation\Rules;
use Laravel\Nova\Fields\Password;
use Laravel\Nova\Fields\PasswordConfirmation;

// ...

Password::make('Password')
    ->onlyOnForms()
    ->creationRules('required', Rules\Password::defaults(), 'confirmed')
    ->updateRules('nullable', Rules\Password::defaults(), 'confirmed'),

PasswordConfirmation::make('Password Confirmation'),
```
### [​](#select-field) Select Field
The `Select` field may be used to generate a drop-down select menu. The `Select` menu’s options may be defined using the `options` method:
Copy
Ask AI
```
use Laravel\Nova\Fields\Select;

// ...

Select::make('Size')->options([
    'S' => 'Small',
    'M' => 'Medium',
    'L' => 'Large',
]),
```
On the resource index and detail pages, the `Select` field’s “key” value will be displayed. If you would like to display the labels instead, you may use the `displayUsingLabels` method:
Copy
Ask AI
```
use Laravel\Nova\Fields\Select;

// ...

Select::make('Size')->options([
    'S' => 'Small',
    'M' => 'Medium',
    'L' => 'Large',
])->displayUsingLabels(),
```
You may also display `Select` options in groups by providing an array structure that contains keys and `label` / `group` pairs:
Copy
Ask AI
```
use Laravel\Nova\Fields\Select;

// ...

Select::make('Size')->options([
    'MS' => ['label' => 'Small', 'group' => 'Men Sizes'],
    'MM' => ['label' => 'Medium', 'group' => 'Men Sizes'],
    'WS' => ['label' => 'Small', 'group' => 'Women Sizes'],
    'WM' => ['label' => 'Medium', 'group' => 'Women Sizes'],
])->displayUsingLabels(),
```
If you need more control over the generation of the `Select` field’s options, you may provide a closure to the `options` method:
Copy
Ask AI
```
use App\Value\Size;
use Laravel\Nova\Fields\Select;

// ...

Select::make('Size')->options(fn () => [
    Size::SMALL => 'Small',
    Size::MEDIUM => 'Medium',
    Size::LARGE => 'Large',
])),
```
#### [​](#disabled-select-options) Disabled Select Options
You may disable specific options in a `Select` field by providing an array of options with `label` and `disabled` keys within the option definition:
Copy
Ask AI
```
use App\Value\Size;
use Laravel\Nova\Fields\Select;

// ...

Select::make('Size')
    ->options([
        Size::SMALL => [
            'label => 'Small',
            'disabled' => true,
        ],
        Size::MEDIUM => [
            'label => 'Medium',
            'disabled' => false,
        ],
        Size::LARGE => [
            'label => 'Large',
            'disabled' => false,
        ],
    ])
    ->displayUsingLabels(),
```
#### [​](#using-enum-as-options) Using Enum as Options
Furthermore, you can also provide an enum to the `options` method:
Copy
Ask AI
```
use App\Enums\Size;
use Laravel\Nova\Fields\Select;

// ...

Select::make('Size')
    ->options(Size::class),
```
As example, here’s the `App\Enums\Size` enum definition, The case key will be used as `label` and case value as `value`:
app/Enums/Size.php
Copy
Ask AI
```
namespace App\Enums;

enum Size: string {
    case SMALL = 'small';
    case MEDIUM = 'medium';
    case LARGE = 'large';
}
```
To allow customizing the `label` you can define `name()` or `label()` method within the enum:
app/Enums/Size.php
Copy
Ask AI
```
namespace App\Enums;

use Laravel\Nova\Nova;

enum Size: string {
    case SMALL = 'small';
    case MEDIUM = 'medium';
    case LARGE = 'large';

    public function name(): string 
    {
        return match ($this) {
            self::SMALL => (string) Nova::__('Small Size'),
            self::MEDIUM => (string) Nova::__('Medium Size'),
            self::LARGE => (string) Nova::__('Large Size'),
        };
    }
}
```
#### [​](#searchable-select-fields) Searchable Select Fields
At times it’s convenient to be able to search or filter the list of options available in a `Select` field. You can enable this by invoking the `searchable` method on the field:
Copy
Ask AI
```
use Laravel\Nova\Fields\Select;

// ...

Select::make('Size')
    ->searchable()
    ->options([
        'S' => 'Small',
        'M' => 'Medium',
        'L' => 'Large',
    ])->displayUsingLabels(),
```
After marking a select field as `searchable`, Nova will display an `input` field which allows you to filter the list of options based on its label:
### [​](#slug-field) Slug Field
Sometimes you may need to generate a unique, human-readable identifier based on the contents of another field, such as when generating a “slug” for a blog post title. You can automatically generate these “slugs” using the `Slug` field:
Copy
Ask AI
```
use Laravel\Nova\Fields\Slug;

// ...

Slug::make('Slug')->from('Title'),
```
By default, the field will convert a string like ‘My Blog Post’ to a slug like ‘my-blog-post’. If you would like the field to use underscores instead of dashes, you may use the `separator` method to define your own custom “separator”:
Copy
Ask AI
```
use Laravel\Nova\Fields\Slug;

// ...

Slug::make('Slug')->from('Title')->separator('_'),
```
### [​](#sparkline-field) Sparkline Field
The `Sparkline` field may be used to display a small line chart on a resource’s index or detail page. The data provided to a `Sparkline` may be provided via an `array`, a `callable` (which returns an array), or an instance of a `Trend` metric class:
Copy
Ask AI
```
use Laravel\Nova\Fields\Sparkline;

// ...

// Using an array...
Sparkline::make('Post Views')->data([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]),

// Using a callable...
Sparkline::make('Post Views')->data(function () {
    return json_decode($this->views_data);
}),
```
#### [​](#using-trend-metrics) Using Trend Metrics
If the data needed by your `Sparkline` field requires complicated database queries to compute, you may wish to encapsulate the data retrieval within a [trend metric](./../metrics/defining-metrics) which can then be provided to the `Sparkline` field:
Copy
Ask AI
```
use App\Nova\Metrics\PostViewsOverTime;
use Laravel\Nova\Fields\Sparkline;

// ...

Sparkline::make('Post Views')->data(new PostViewsOverTime($this->id)),
```
In the example above, we’re providing the post’s `id` to the metric’s constructor. This value will become the `resourceId` property of the request that is available within the trend metric. For example, within the metric, we could access this post ID via `$request->resourceId`:
Copy
Ask AI
```
use App\Models\PostView;

// ...

return $this->countByDays(
    $request,
    PostView::where('post_id', '=', $request->resourceId)
);
```
When providing data to a `Sparkline` field via a trend metric, the `Sparkline` field will always use the first range defined in the `ranges` method of the metric.
#### [​](#customizing-the-chart) Customizing the Chart
If a bar chart better suits your data, you may invoke the `asBarChart` method when defining the field:
Copy
Ask AI
```
use Laravel\Nova\Fields\Sparkline;

// ...

Sparkline::make('Post Views')
           ->data([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
           ->asBarChart(),
```
By default, a `Sparkline` will appear on a resource’s detail page. You can customize the dimensions of the chart using the `height` and `width` methods:
Copy
Ask AI
```
use Laravel\Nova\Fields\Sparkline;

// ...

Sparkline::make('Post Views')
           ->data([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
           ->height(200)
           ->width(600),
```
### [​](#status-field) Status Field
The `Status` field may be used to display a “progress state” column. Internally, Nova uses the `Status` field to indicate the current state (waiting, running, or finished) of queued actions. However, you are free to use this field for your own purposes as needed:
The `loadingWhen` and `failedWhen` methods may be used to instruct the field which words indicate a “loading” state and which words indicate a “failed” state. In this example, we will indicate that database column values of `waiting` or `running` should display a “loading” indicator:
Copy
Ask AI
```
use Laravel\Nova\Fields\Status;

// ...

Status::make('Status')
    ->loadingWhen(['waiting', 'running'])
    ->failedWhen(['failed']),
```
### [​](#stack-field) Stack Field
As your resource classes grow, you may find it useful to be able to group fields together to simplify your index and detail views. A `Stack` field allows you to display fields like `BelongsTo`, `Text`, and others in a vertical orientation:
Copy
Ask AI
```
use Illuminate\Support\Str;
use Laravel\Nova\Fields\Stack;
use Laravel\Nova\Fields\Text;

// ...

Stack::make('Details', [
    Text::make('Name'),
    Text::make('Slug')->resolveUsing(function () {
        return Str::slug(optional($this->resource)->name);
    }),
]),
```
Stack fields are not shown on forms, and are only intended for stacking lines of text on the index and detail resource views.
#### [​](#line-fields) Line Fields
To gain more control over how the individual fields in a `Stack` are displayed, you may use the `Line` field, which provides methods for controlling the display of the line’s text. `Line` fields offer the following presentational methods:
- `asHeading`
- `asSubTitle`
- `asSmall`
- `asBase`
In addition to the `Line` field’s presentational methods, you may also pass any additional Tailwind classes to the field to customize the appearance of the `Line`:
Copy
Ask AI
```
use Laravel\Nova\Fields\Stack;

// ...

Stack::make('Details', [
    Line::make('Title')->extraClasses('italic font-medium text-80'),
]),
```
#### [​](#passing-closures-to-line-fields) Passing Closures to Line Fields
In addition to passing `BelongsTo`, `Text`, and `Line` fields to the `Stack` field, you may also pass a closure. The result of the closure will automatically be converted to a `Line` instance:
Copy
Ask AI
```
use Laravel\Nova\Fields\Stack;

// ...

Stack::make('Details', [
    Line::make('Name')->asHeading(),
    fn () => optional($this->resource)->position
]),
```
### [​](#tag-field) Tag Field
The `Tag` field all

*[Content truncated for length]*