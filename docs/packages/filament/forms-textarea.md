Source: https://filamentphp.com/docs/5.x/forms/textarea.md

# Textarea

> Filament 5.x documentation
> Source: https://filamentphp.com/docs/5.x/forms/textarea.md

## Introduction

The textarea allows you to interact with a multi-line string:

```php
use Filament\Forms\Components\Textarea;

Textarea::make('description')
```



## Resizing the textarea

You may change the size of the textarea by defining the ` rows() ` and ` cols() ` methods:

```php
use Filament\Forms\Components\Textarea;

Textarea::make('description')
    ->rows(10)
    ->cols(20)
```



As well as allowing static values, the ` rows() ` and ` cols() ` methods also accept functions to dynamically calculate them. You can inject various utilities into the functions as parameters.

[Utility injection guide](https://filamentphp.com/docs/5.x/forms/overview.md#field-utility-injection)

| Utility | Type | Parameter | Description |
| --- | --- | --- | --- |
| Field | ` Filament\Forms\Components\Field ` | ` $component ` | The current field component instance. |
| Get function | ` Filament\Schemas\Components\Utilities\Get ` | ` $get ` | A function for retrieving values from the current form data. Validation is not run. |
| Livewire | ` Livewire\Component ` | ` $livewire ` | The Livewire component instance. |
| Eloquent model FQN | ` ?string<Illuminate\Database\Eloquent\Model> ` | ` $model ` | The Eloquent model FQN for the current schema. |
| Operation | ` string ` | ` $operation ` | The current operation being performed by the schema. Usually ` create `, ` edit `, or ` view `. |
| Parent repeater item index | ` int ` | ` $parentRepeaterItemIndex ` | The zero-based index of the nearest containing repeater item or builder block, or ` 0 ` when neither exists. |
| Raw state | ` mixed ` | ` $rawState ` | The current value of the field, before state casts were applied. Validation is not run. |
| Record | ` Illuminate\Database\Eloquent\Model\|array<string, mixed>\|null ` | ` $record ` | The Eloquent record or custom data array for the current schema. |
| State | ` mixed ` | ` $state ` | The current value of the field. Validation is not run. |


### Autosizing the textarea

You may allow the textarea to automatically resize to fit its content by setting the ` autosize() ` method:

```php
use Filament\Forms\Components\Textarea;

Textarea::make('description')
    ->autosize()
```

Optionally, you may pass a boolean value to control if the textarea should be autosizeable or not:

```php
use Filament\Forms\Components\Textarea;

Textarea::make('description')
    ->autosize(FeatureFlag::active())
```

As well as allowing a static value, the ` autosize() ` method also accepts a function to dynamically calculate it. You can inject various utilities into the function as parameters.

[Utility injection guide](https://filamentphp.com/docs/5.x/forms/overview.md#field-utility-injection)

| Utility | Type | Parameter | Description |
| --- | --- | --- | --- |
| Field | ` Filament\Forms\Components\Field ` | ` $component ` | The current field component instance. |
| Get function | ` Filament\Schemas\Components\Utilities\Get ` | ` $get ` | A function for retrieving values from the current form data. Validation is not run. |
| Livewire | ` Livewire\Component ` | ` $livewire ` | The Livewire component instance. |
| Eloquent model FQN | ` ?string<Illuminate\Database\Eloquent\Model> ` | ` $model ` | The Eloquent model FQN for the current schema. |
| Operation | ` string ` | ` $operation ` | The current operation being performed by the schema. Usually ` create `, ` edit `, or ` view `. |
| Parent repeater item index | ` int ` | ` $parentRepeaterItemIndex ` | The zero-based index of the nearest containing repeater item or builder block, or ` 0 ` when neither exists. |
| Raw state | ` mixed ` | ` $rawState ` | The current value of the field, before state casts were applied. Validation is not run. |
| Record | ` Illuminate\Database\Eloquent\Model\|array<string, mixed>\|null ` | ` $record ` | The Eloquent record or custom data array for the current schema. |
| State | ` mixed ` | ` $state ` | The current value of the field. Validation is not run. |




## Making the field read-only

Not to be confused with [disabling the field](https://filamentphp.com/docs/5.x/forms/overview.md#disabling-a-field), you may make the field "read-only" using the ` readOnly() ` method:

```php
use Filament\Forms\Components\Textarea;

Textarea::make('description')
    ->readOnly()
```

There are a few differences, compared to [` disabled() `](https://filamentphp.com/docs/5.x/forms/overview.md#disabling-a-field):

- When using ` readOnly() `, the field will still be sent to the server when the form is submitted. It can be mutated with the browser console, or via JavaScript. You can use [` saved(false) `](https://filamentphp.com/docs/5.x/forms/overview.md#preventing-a-field-from-being-saved) to prevent this.
- There are no styling changes, such as less opacity, when using ` readOnly() `.
- The field is still focusable when using ` readOnly() `.

Optionally, you may pass a boolean value to control if the field should be read-only or not:

```php
use Filament\Forms\Components\Textarea;

Textarea::make('description')
    ->readOnly(FeatureFlag::active())
```

As well as allowing a static value, the ` readOnly() ` method also accepts a function to dynamically calculate it. You can inject various utilities into the function as parameters.

[Utility injection guide](https://filamentphp.com/docs/5.x/forms/overview.md#field-utility-injection)

| Utility | Type | Parameter | Description |
| --- | --- | --- | --- |
| Field | ` Filament\Forms\Components\Field ` | ` $component ` | The current field component instance. |
| Get function | ` Filament\Schemas\Components\Utilities\Get ` | ` $get ` | A function for retrieving values from the current form data. Validation is not run. |
| Livewire | ` Livewire\Component ` | ` $livewire ` | The Livewire component instance. |
| Eloquent model FQN | ` ?string<Illuminate\Database\Eloquent\Model> ` | ` $model ` | The Eloquent model FQN for the current schema. |
| Operation | ` string ` | ` $operation ` | The current operation being performed by the schema. Usually ` create `, ` edit `, or ` view `. |
| Parent repeater item index | ` int ` | ` $parentRepeaterItemIndex ` | The zero-based index of the nearest containing repeater item or builder block, or ` 0 ` when neither exists. |
| Raw state | ` mixed ` | ` $rawState ` | The current value of the field, before state casts were applied. Validation is not run. |
| Record | ` Illuminate\Database\Eloquent\Model\|array<string, mixed>\|null ` | ` $record ` | The Eloquent record or custom data array for the current schema. |
| State | ` mixed ` | ` $state ` | The current value of the field. Validation is not run. |


## Disabling Grammarly checks

If the user has Grammarly installed and you would like to prevent it from analyzing the contents of the textarea, you can use the ` disableGrammarly() ` method:

```php
use Filament\Forms\Components\Textarea;

Textarea::make('description')
    ->disableGrammarly()
```

Optionally, you may pass a boolean value to control if the field should disable Grammarly checks or not:

```php
use Filament\Forms\Components\Textarea;

Textarea::make('description')
    ->disableGrammarly(FeatureFlag::active())
```

As well as allowing a static value, the ` disableGrammarly() ` method also accepts a function to dynamically calculate it. You can inject various utilities into the function as parameters.

[Utility injection guide](https://filamentphp.com/docs/5.x/forms/overview.md#field-utility-injection)

| Utility | Type | Parameter | Description |
| --- | --- | --- | --- |
| Field | ` Filament\Forms\Components\Field ` | ` $component ` | The current field component instance. |
| Get function | ` Filament\Schemas\Components\Utilities\Get ` | ` $get ` | A function for retrieving values from the current form data. Validation is not run. |
| Livewire | ` Livewire\Component ` | ` $livewire ` | The Livewire component instance. |
| Eloquent model FQN | ` ?string<Illuminate\Database\Eloquent\Model> ` | ` $model ` | The Eloquent model FQN for the current schema. |
| Operation | ` string ` | ` $operation ` | The current operation being performed by the schema. Usually ` create `, ` edit `, or ` view `. |
| Parent repeater item index | ` int ` | ` $parentRepeaterItemIndex ` | The zero-based index of the nearest containing repeater item or builder block, or ` 0 ` when neither exists. |
| Raw state | ` mixed ` | ` $rawState ` | The current value of the field, before state casts were applied. Validation is not run. |
| Record | ` Illuminate\Database\Eloquent\Model\|array<string, mixed>\|null ` | ` $record ` | The Eloquent record or custom data array for the current schema. |
| State | ` mixed ` | ` $state ` | The current value of the field. Validation is not run. |


## Trimming whitespace

You can automatically trim whitespace from the beginning and end of the textarea value using the ` trim() ` method:

```php
use Filament\Forms\Components\Textarea;

Textarea::make('description')
    ->trim()
```

You may want to enable trimming globally for all textareas, similar to Laravel's ` TrimStrings ` middleware. You can do this in a service provider using the ` configureUsing() ` method:

```php
use Filament\Forms\Components\Textarea;

Textarea::configureUsing(function (Textarea $component): void {
    $component->trim();
});
```

## Textarea validation

As well as all rules listed on the [validation](https://filamentphp.com/docs/5.x/forms/validation.md) page, there are additional rules that are specific to textareas.

### Length validation

You may limit the length of the textarea by setting the ` minLength() ` and ` maxLength() ` methods. These methods add both frontend and backend validation:

```php
use Filament\Forms\Components\Textarea;

Textarea::make('description')
    ->minLength(2)
    ->maxLength(1024)
```

You can also specify the exact length of the textarea by setting the ` length() `. This method adds both frontend and backend validation:

```php
use Filament\Forms\Components\Textarea;

Textarea::make('question')
    ->length(100)
```

As well as allowing static values, the ` minLength() `, ` maxLength() ` and ` length() ` methods also accept a function to dynamically calculate them. You can inject various utilities into the function as parameters.

[Utility injection guide](https://filamentphp.com/docs/5.x/forms/overview.md#field-utility-injection)

| Utility | Type | Parameter | Description |
| --- | --- | --- | --- |
| Field | ` Filament\Forms\Components\Field ` | ` $component ` | The current field component instance. |
| Get function | ` Filament\Schemas\Components\Utilities\Get ` | ` $get ` | A function for retrieving values from the current form data. Validation is not run. |
| Livewire | ` Livewire\Component ` | ` $livewire ` | The Livewire component instance. |
| Eloquent model FQN | ` ?string<Illuminate\Database\Eloquent\Model> ` | ` $model ` | The Eloquent model FQN for the current schema. |
| Operation | ` string ` | ` $operation ` | The current operation being performed by the schema. Usually ` create `, ` edit `, or ` view `. |
| Parent repeater item index | ` int ` | ` $parentRepeaterItemIndex ` | The zero-based index of the nearest containing repeater item or builder block, or ` 0 ` when neither exists. |
| Raw state | ` mixed ` | ` $rawState ` | The current value of the field, before state casts were applied. Validation is not run. |
| Record | ` Illuminate\Database\Eloquent\Model\|array<string, mixed>\|null ` | ` $record ` | The Eloquent record or custom data array for the current schema. |
| State | ` mixed ` | ` $state ` | The current value of the field. Validation is not run. |
