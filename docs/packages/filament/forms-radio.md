Source: https://filamentphp.com/docs/5.x/forms/radio.md

# Radio

> Filament 5.x documentation
> Source: https://filamentphp.com/docs/5.x/forms/radio.md

## Introduction

The radio input provides a radio button group for selecting a single value from a list of predefined options:

```php
use Filament\Forms\Components\Radio;

Radio::make('status')
    ->options([
        'draft' => 'Draft',
        'scheduled' => 'Scheduled',
        'published' => 'Published'
    ])
```

As well as allowing a static array, the ` options() ` method also accepts a function to dynamically calculate it. You can inject various utilities into the function as parameters.

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




## Setting option descriptions

You can optionally provide descriptions to each option using the ` descriptions() ` method:

```php
use Filament\Forms\Components\Radio;

Radio::make('status')
    ->options([
        'draft' => 'Draft',
        'scheduled' => 'Scheduled',
        'published' => 'Published'
    ])
    ->descriptions([
        'draft' => 'Is not visible.',
        'scheduled' => 'Will be visible.',
        'published' => 'Is visible.'
    ])
```

As well as allowing a static array, the ` descriptions() ` method also accepts a function to dynamically calculate it. You can inject various utilities into the function as parameters.

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




> [!NOTE]
> Be sure to use the same ` key ` in the descriptions array as the ` key ` in the option array so the right description matches the right option.

## Positioning the options inline with each other

You may wish to display the options ` inline() ` with each other:

```php
use Filament\Forms\Components\Radio;

Radio::make('feedback')
    ->label('Like this post?')
    ->boolean()
    ->inline()
```



Optionally, you may pass a boolean value to control if the options should be inline or not:

```php
use Filament\Forms\Components\Radio;

Radio::make('feedback')
    ->label('Like this post?')
    ->boolean()
    ->inline(FeatureFlag::active())
```

As well as allowing a static value, the ` inline() ` method also accepts a function to dynamically calculate it. You can inject various utilities into the function as parameters.

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


## Disabling specific options

You can disable specific options using the ` disableOptionWhen() ` method. It accepts a closure, in which you can check if the option with a specific ` $value ` should be disabled:

```php
use Filament\Forms\Components\Radio;

Radio::make('status')
    ->options([
        'draft' => 'Draft',
        'scheduled' => 'Scheduled',
        'published' => 'Published',
    ])
    ->disableOptionWhen(fn (string $value): bool => $value === 'published')
```

You can inject various utilities into the function as parameters.

[Utility injection guide](https://filamentphp.com/docs/5.x/forms/overview.md#field-utility-injection)

| Utility | Type | Parameter | Description |
| --- | --- | --- | --- |
| Field | ` Filament\Forms\Components\Field ` | ` $component ` | The current field component instance. |
| Get function | ` Filament\Schemas\Components\Utilities\Get ` | ` $get ` | A function for retrieving values from the current form data. Validation is not run. |
| Option label | ` string \| Illuminate\Contracts\Support\Htmlable ` | ` $label ` | The label of the option to disable. |
| Livewire | ` Livewire\Component ` | ` $livewire ` | The Livewire component instance. |
| Eloquent model FQN | ` ?string<Illuminate\Database\Eloquent\Model> ` | ` $model ` | The Eloquent model FQN for the current schema. |
| Operation | ` string ` | ` $operation ` | The current operation being performed by the schema. Usually ` create `, ` edit `, or ` view `. |
| Parent repeater item index | ` int ` | ` $parentRepeaterItemIndex ` | The zero-based index of the nearest containing repeater item or builder block, or ` 0 ` when neither exists. |
| Raw state | ` mixed ` | ` $rawState ` | The current value of the field, before state casts were applied. Validation is not run. |
| Record | ` Illuminate\Database\Eloquent\Model\|array<string, mixed>\|null ` | ` $record ` | The Eloquent record or custom data array for the current schema. |
| State | ` mixed ` | ` $state ` | The current value of the field. Validation is not run. |
| Option value | ` mixed ` | ` $value ` | The value of the option to disable. |




If you want to retrieve the options that have not been disabled, e.g. for validation purposes, you can do so using ` getEnabledOptions() `:

```php
use Filament\Forms\Components\Radio;

Radio::make('status')
    ->options([
        'draft' => 'Draft',
        'scheduled' => 'Scheduled',
        'published' => 'Published',
    ])
    ->disableOptionWhen(fn (string $value): bool => $value === 'published')
    ->in(fn (Radio $component): array => array_keys($component->getEnabledOptions()))
```

For more information about the ` in() ` function, please see the [Validation documentation](https://filamentphp.com/docs/5.x/forms/validation.md#in).

## Boolean options

If you want a simple boolean radio button group, with "Yes" and "No" options, you can use the ` boolean() ` method:

```php
use Filament\Forms\Components\Radio;

Radio::make('feedback')
    ->label('Like this post?')
    ->boolean()
```



To customize the "Yes" label, you can use the ` trueLabel ` argument on the ` boolean() ` method:

```php
use Filament\Forms\Components\Radio;

Radio::make('feedback')
    ->label('Like this post?')
    ->boolean(trueLabel: 'Absolutely!')
```

To customize the "No" label, you can use the ` falseLabel ` argument on the ` boolean() ` method:

```php
use Filament\Forms\Components\Radio;

Radio::make('feedback')
    ->label('Like this post?')
    ->boolean(falseLabel: 'Not at all!')
```
