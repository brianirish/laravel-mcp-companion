Source: https://filamentphp.com/docs/5.x/infolists/color-entry.md

# Color entry

> Filament 5.x documentation
> Source: https://filamentphp.com/docs/5.x/infolists/color-entry.md

## Introduction

The color entry allows you to show the color preview from a CSS color definition, typically entered using the [color picker field](https://filamentphp.com/docs/5.x/forms/color-picker.md), in one of the supported formats (HEX, HSL, RGB, RGBA).

```php
use Filament\Infolists\Components\ColorEntry;

ColorEntry::make('color')
```



## Allowing the color to be copied to the clipboard

You may make the color copyable, such that clicking on the preview copies the CSS value to the clipboard, and optionally specify a custom confirmation message and duration in milliseconds. This feature only works when SSL is enabled for the app.

```php
use Filament\Infolists\Components\ColorEntry;

ColorEntry::make('color')
    ->copyable()
    ->copyMessage('Copied!')
    ->copyMessageDuration(1500)
```



Optionally, you may pass a boolean value to control if the color should be copyable or not:

```php
use Filament\Infolists\Components\ColorEntry;

ColorEntry::make('color')
    ->copyable(FeatureFlag::active())
```

As well as allowing static values, the ` copyable() `, ` copyMessage() `, and ` copyMessageDuration() ` methods also accept functions to dynamically calculate them. You can inject various utilities into the function as parameters.

[Utility injection guide](https://filamentphp.com/docs/5.x/infolists/overview.md#entry-utility-injection)

| Utility | Type | Parameter | Description |
| --- | --- | --- | --- |
| Entry | ` Filament\Infolists\Components\Entry ` | ` $component ` | The current entry component instance. |
| Get function | ` Filament\Schemas\Components\Utilities\Get ` | ` $get ` | A function for retrieving values from the current schema data. Validation is not run on form fields. |
| Livewire | ` Livewire\Component ` | ` $livewire ` | The Livewire component instance. |
| Eloquent model FQN | ` ?string<Illuminate\Database\Eloquent\Model> ` | ` $model ` | The Eloquent model FQN for the current schema. |
| Operation | ` string ` | ` $operation ` | The current operation being performed by the schema. Usually ` create `, ` edit `, or ` view `. |
| Parent repeater item index | ` int ` | ` $parentRepeaterItemIndex ` | The zero-based index of the nearest containing repeater item or builder block, or ` 0 ` when neither exists. |
| Record | ` Illuminate\Database\Eloquent\Model\|array<string, mixed>\|null ` | ` $record ` | The Eloquent record or custom data array for the current schema. |
| Related record | ` Illuminate\Database\Eloquent\Model ` | ` $relatedRecord ` | The current related Eloquent record for the rendered item. |
| State | ` mixed ` | ` $state ` | The current value of the entry. |
