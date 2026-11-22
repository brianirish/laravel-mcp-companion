Source: https://filamentphp.com/docs/5.x/forms/color-picker.md

# Color picker

> Filament 5.x documentation
> Source: https://filamentphp.com/docs/5.x/forms/color-picker.md

## Introduction

The color picker component allows you to pick a color in a range of formats.

By default, the component uses HEX format:

```php
use Filament\Forms\Components\ColorPicker;

ColorPicker::make('color')
```



Clicking the color swatch opens a color picker panel where users can visually select a color:



## Setting the color format

While HEX format is used by default, you can choose which color format to use:

```php
use Filament\Forms\Components\ColorPicker;

ColorPicker::make('hsl_color')
    ->hsl()

ColorPicker::make('rgb_color')
    ->rgb()

ColorPicker::make('rgba_color')
    ->rgba()
```



## Customizing the loading placeholder

The color picker displays a loading placeholder while its JavaScript is loaded and initialized. You may customize it using ` loadingPlaceholder() `, passing a Blade view or an ` Htmlable ` instance, such as an ` HtmlString ` containing trusted HTML:

```php
use Filament\Forms\Components\ColorPicker;

ColorPicker::make('color')
    ->loadingPlaceholder(fn () => view('forms.color-picker-loading-placeholder'))
```

As well as allowing a static value, the ` loadingPlaceholder() ` method also accepts a function to dynamically calculate it. You can inject various utilities into the function as parameters.

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


Keep your placeholder HTML decorative and noninteractive. Filament hides it from assistive technologies and supplies an accessible loading status in the surrounding wrapper. If the JavaScript fails to load or initialize, the placeholder remains visible.

To customize the placeholder for all color pickers, use [` ColorPicker::configureUsing() `](https://filamentphp.com/docs/5.x/forms/overview.md#global-settings) in a service provider's ` boot() ` method:

```php
use Filament\Forms\Components\ColorPicker;

ColorPicker::configureUsing(function (ColorPicker $colorPicker): void {
    $colorPicker->loadingPlaceholder(fn () => view('forms.color-picker-loading-placeholder'));
});
```

You may call ` loadingPlaceholder(null) ` on an individual color picker to restore the default loading placeholder.

## Color picker validation

You may use Laravel's validation rules to validate the values of the color picker:

```php
use Filament\Forms\Components\ColorPicker;

ColorPicker::make('hex_color')
    ->regex('/^#([a-fA-F0-9]{6}|[a-fA-F0-9]{3})\b$/')

ColorPicker::make('hsl_color')
    ->hsl()
    ->regex('/^hsl\(\s*(\d+)\s*,\s*(\d*(?:\.\d+)?%)\s*,\s*(\d*(?:\.\d+)?%)\)$/')

ColorPicker::make('rgb_color')
    ->rgb()
    ->regex('/^rgb\((\d{1,3}),\s*(\d{1,3}),\s*(\d{1,3})\)$/')

ColorPicker::make('rgba_color')
    ->rgba()
    ->regex('/^rgba\((\d{1,3}),\s*(\d{1,3}),\s*(\d{1,3}),\s*(\d*(?:\.\d+)?)\)$/')
```
