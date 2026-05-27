# Nova - Resources/Dependent-Fields

*Source: https://nova.laravel.com/docs/v5/resources/dependent-fields*

---

## On this page
- [Supported Dependent Fields](#supported-dependent-fields)
- [Toggling Field Visibility Using dependsOn](#toggling-field-visibility-using-dependson)
- [Setting a Field’s Value Using dependsOn](#setting-a-field%E2%80%99s-value-using-dependson)
- [Accessing Request Resource IDs](#accessing-request-resource-ids)
Resources
# Dependent Fields
Dependent fields allow you to define fields that have unique configuration depending on the value of other fields.
> ## Documentation Index
>
> Fetch the complete documentation index at: <https://nova.laravel.com/docs/llms.txt>
>
> Use this file to discover all available pages before exploring further.
Dependent fields are created by invoking the `dependsOn` method when defining a field. The `dependsOn` method accepts an `array` of dependent field attributes and a closure that modifies the configuration of the current field instance.
Dependent fields allow advanced customization, such as toggling read-only mode, validation rules, and more based on the state of another field:
```
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
## [​](#supported-dependent-fields) Supported Dependent Fields
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
## [​](#toggling-field-visibility-using-dependson) Toggling Field Visibility Using `dependsOn`
One common use-case for dependent fields is toggling field visibility based on the value of another field. You can accomplish this using the `hide` and `show` methods:
```
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
## [​](#setting-a-field’s-value-using-dependson) Setting a Field’s Value Using `dependsOn`
Another common use-case for dependent fields is to set the value of a field based on the value of another field. You can accomplish this using the `setValue` method:
```
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
## [​](#accessing-request-resource-ids) Accessing Request Resource IDs
When interacting with dependent fields, you may retrieve the current resource and related resource IDs via the `resource` method:
```
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
YesNo
[Fields](/docs/v5/resources/fields)[Date Fields](/docs/v5/resources/date-fields)
⌘I