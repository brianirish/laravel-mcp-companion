# Nova - Resources/Dependent-Fields

*Source: https://nova.laravel.com/docs/v5/resources/dependent-fields*

---

- [Laravel Nova home page](https://nova.laravel.com)v5Search...⌘KAsk AI
[Support](/cdn-cgi/l/email-protection#98f6f7eef9d8f4f9eaf9eefdf4b6fbf7f5)
- [Platform Status](https://status.laravel.com/)
- [Dashboard](https://nova.laravel.com)
- [Dashboard](https://nova.laravel.com)

Search...NavigationResourcesDependent Fields[Documentation](/docs/v5/installation)[Knowledge Base](/docs/kb/support)- [Community](https://discord.com/invite/laravel)
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

Resources# Dependent Fields

Dependent fields allow you to define fields that have unique configuration depending on the value of other fields.

Dependent fields are created by invoking the `dependsOn` method when defining a field. The `dependsOn` method accepts an `array` of dependent field attributes and a closure that modifies the configuration of the current field instance.

Dependent fields allow advanced customization, such as toggling read-only mode, validation rules, and more based on the state of another field:

CopyAsk AI```
use Laravel\Nova\Fields\FormData;
use Laravel\Nova\Fields\Select;
use Laravel\Nova\Fields\Text;
use Laravel\Nova\Http\Requests\NovaRequest;

// ...

return [
    Select::make('Purchase Type', 'type')
        ->options([
            'personal' => 'Personal',
            'gift' => 'Gift',
        ]),

    // Recipient field configuration is customized based on purchase type...
    Text::make('Recipient')
        ->readonly()
        ->dependsOn(
            ['type'],
            function (Text $field, NovaRequest $request, FormData $formData) {
                if ($formData->type === 'gift') {
                    $field->readonly(false)->rules(['required', 'email']);
                }
            }
        ),
];

```

To define dependent fields separately for creating and updating resources, you may use the `dependsOnCreating` and `dependsOnUpdating` methods.

## [​](#supported-dependent-fields)Supported Dependent Fields

The following field types may depend on other fields:

- Audio

- BelongsTo

- Boolean

- BooleanGroup

- Color

- Code

- Country

- Currency

- Date

- DateTime

- File

- Heading

- Hidden

- Image

- KeyValue

- Markdown

- MorphTo

- Number

- Password

- PasswordConfirmation

- Select

- Status

- Textarea

- Text

- Timezone

- Trix

- URL

- VaporAudio

- VaporFile

- VaporImage

The following field types may not be depended upon by other fields since they do not live-report their changes to Nova:

- Audio

- Code

- File

- Image

- KeyValue

- Status

- Tag

- Trix

- VaporAudio

- VaporFile

- VaporImage

## [​](#toggling-field-visibility-using-dependson)Toggling Field Visibility Using `dependsOn`

One common use-case for dependent fields is toggling field visibility based on the value of another field. You can accomplish this using the `hide` and `show` methods:

CopyAsk AI```
use Laravel\Nova\Fields\Boolean;
use Laravel\Nova\Fields\BelongsTo;
use Laravel\Nova\Fields\FormData;
use Laravel\Nova\Http\Requests\NovaRequest;

// ...

Boolean::make('Anonymous Comment', 'anonymous')
    ->onlyOnForms()
    ->fillUsing(fn () => null)
    ->default(true),

BelongsTo::make('User')
    ->hide()
    ->rules('sometimes')
    ->dependsOn('anonymous', function (BelongsTo $field, NovaRequest $request, FormData $formData) {
        if ($formData->boolean('anonymous') === false) {
            $field->show()->rules('required');
        }
    }),

```

## [​](#setting-a-field%E2%80%99s-value-using-dependson)Setting a Field’s Value Using `dependsOn`

Another common use-case for dependent fields is to set the value of a field based on the value of another field. You can accomplish this using the `setValue` method:

CopyAsk AI```
use Laravel\Nova\Fields\DateTime;
use Laravel\Nova\Fields\FormData;
use Laravel\Nova\Http\Requests\NovaRequest;

// ...

DateTime::make('Created At'),

DateTime::make('Updated At')
    ->dependsOn(['created_at'], function (DateTime $field, NovaRequest $request, FormData $form) {
        $field->setValue(Carbon::parse($form->created_at)->addDays(7));
    }),

```

## [​](#accessing-request-resource-ids)Accessing Request Resource IDs

When interacting with dependent fields, you may retrieve the current resource and related resource IDs via the `resource` method:

CopyAsk AI```
BelongsTo::make(__('Books'), 'books', Book::class),

Currency::make('Price')
    ->dependsOn('books', function (Currency $field, NovaRequest $request, FormData $formData) {
        $bookId = (int) $formData->resource(Book::uriKey(), $formData->books);

        if ($bookId == 1) {
            $field->rules([
                'required', 'numeric', 'min:10', 'max:199'
            ])->help('Price starts from $10-$199');

            return;
        }

        $field->rules([
            'required', 'numeric', 'min:0', 'max:99'
        ])->help('Price starts from $0-$99');
    }),

```
Was this page helpful?

YesNo[Fields](/docs/v5/resources/fields)[Date Fields](/docs/v5/resources/date-fields)On this page
- [Supported Dependent Fields](#supported-dependent-fields)
- [Toggling Field Visibility Using dependsOn](#toggling-field-visibility-using-dependson)
- [Setting a Field’s Value Using dependsOn](#setting-a-field%E2%80%99s-value-using-dependson)
- [Accessing Request Resource IDs](#accessing-request-resource-ids)

[Laravel Nova home page](https://nova.laravel.com)[x](https://x.com/laravelphp)[github](https://github.com/laravel)[discord](https://discord.com/invite/laravel)[linkedin](https://linkedin.com/company/laravel)Platform

[Dashboard](https://nova.laravel.com/)[Status](https://status.laravel.com/)Legal and Compliance

[Term of Service](https://nova.laravel.com/terms)[Privacy Policy](https://nova.laravel.com/privacy)[x](https://x.com/laravelphp)[github](https://github.com/laravel)[discord](https://discord.com/invite/laravel)[linkedin](https://linkedin.com/company/laravel)AssistantResponses are generated using AI and may contain mistakes.