Source: https://filamentphp.com/docs/5.x/tables/columns/color.md

# Color column

> Filament 5.x documentation
> Source: https://filamentphp.com/docs/5.x/tables/columns/color.md

## Introduction

The color column allows you to show the color preview from a CSS color definition, typically entered using the [color picker field](https://filamentphp.com/docs/5.x/forms/color-picker.md), in one of the supported formats (HEX, HSL, RGB, RGBA).

```php
use Filament\Tables\Columns\ColorColumn;

ColorColumn::make('color')
```



## Allowing the color to be copied to the clipboard

You may make the color copyable, such that clicking on the preview copies the CSS value to the clipboard, and optionally specify a custom confirmation message and duration in milliseconds. This feature only works when SSL is enabled for the app.

```php
use Filament\Tables\Columns\ColorColumn;

ColorColumn::make('color')
    ->copyable()
    ->copyMessage('Copied!')
    ->copyMessageDuration(1500)
```



Optionally, you may pass a boolean value to control if the text should be copyable or not:

```php
use Filament\Tables\Columns\ColorColumn;

ColorColumn::make('color')
    ->copyable(FeatureFlag::active())
```

As well as allowing static values, the ` copyable() `, ` copyMessage() `, and ` copyMessageDuration() ` methods also accept functions to dynamically calculate them. You can inject various utilities into the function as parameters.

[Utility injection guide](https://filamentphp.com/docs/5.x/tables/columns/overview.md#column-utility-injection)

| Utility | Type | Parameter | Description |
| --- | --- | --- | --- |
| Column | ` Filament\Tables\Columns\Column ` | ` $column ` | The current column instance. |
| Livewire | ` Livewire\Component ` | ` $livewire ` | The Livewire component instance. |
| Eloquent record | ` Illuminate\Database\Eloquent\Model\|array<string, mixed>\|null ` | ` $record ` | The Eloquent record or custom data array for the current table row. |
| Related record | ` Illuminate\Database\Eloquent\Model ` | ` $relatedRecord ` | The current related Eloquent record for the rendered item. |
| Row loop | ` stdClass ` | ` $rowLoop ` | The [row loop](https://laravel.com/docs/blade#the-loop-variable) object for the current table row. |
| State | ` mixed ` | ` $state ` | The current value of the column, based on the current table row. |
| Table | ` Filament\Tables\Table ` | ` $table ` | The current table instance. |


## Wrapping multiple color blocks

Color blocks can be set to wrap if they can't fit on one line, by setting ` wrap() `:

```php
use Filament\Tables\Columns\ColorColumn;

ColorColumn::make('color')
    ->wrap()
```



> **Tip**
>
> The "width" for wrapping is affected by the column label, so you may need to use a shorter or hidden label to wrap more tightly.
