Source: https://filamentphp.com/docs/5.x/infolists/icon-entry.md

# Icon entry

> Filament 5.x documentation
> Source: https://filamentphp.com/docs/5.x/infolists/icon-entry.md

## Introduction

Icon entries render an [icon](https://filamentphp.com/docs/5.x/styling/icons.md) representing the state of the entry:

```php
use Filament\Infolists\Components\IconEntry;
use Filament\Support\Icons\Heroicon;

IconEntry::make('status')
    ->icon(fn (string $state): Heroicon => match ($state) {
        'draft' => Heroicon::OutlinedPencil,
        'reviewing' => Heroicon::OutlinedClock,
        'published' => Heroicon::OutlinedCheckCircle,
    })
```

The ` icon() ` method can inject various utilities into the function as parameters.

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




## Customizing the color

You may change the [color](https://filamentphp.com/docs/5.x/styling/colors.md) of the icon, using the ` color() ` method:

```php
use Filament\Infolists\Components\IconEntry;

IconEntry::make('status')
    ->color('success')
```

By passing a function to ` color() `, you can customize the color based on the state of the entry:

```php
use Filament\Infolists\Components\IconEntry;

IconEntry::make('status')
    ->color(fn (string $state): string => match ($state) {
        'draft' => 'info',
        'reviewing' => 'warning',
        'published' => 'success',
        default => 'gray',
    })
```

The ` color() ` method can inject various utilities into the function as parameters.

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




## Customizing the size

The default icon size is ` IconSize::Large `, but you may customize the size to be either ` IconSize::ExtraSmall `, ` IconSize::Small `, ` IconSize::Medium `, ` IconSize::ExtraLarge ` or ` IconSize::TwoExtraLarge `:

```php
use Filament\Infolists\Components\IconEntry;
use Filament\Support\Enums\IconSize;

IconEntry::make('status')
    ->size(IconSize::Medium)
```

As well as allowing a static value, the ` size() ` method also accepts a function to dynamically calculate it. You can inject various utilities into the function as parameters.

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




## Handling booleans

Icon entries can display a check or "X" icon based on the state of the entry, either true or false, using the ` boolean() ` method:

```php
use Filament\Infolists\Components\IconEntry;

IconEntry::make('is_featured')
    ->boolean()
```

> If this attribute in the model class is already cast as a ` bool ` or ` boolean `, Filament is able to detect this, and you do not need to use ` boolean() ` manually.



Optionally, you may pass a boolean value to control if the icon should be boolean or not:

```php
use Filament\Infolists\Components\IconEntry;

IconEntry::make('is_featured')
    ->boolean(FeatureFlag::active())
```

As well as allowing a static value, the ` boolean() ` method also accepts a function to dynamically calculate it. You can inject various utilities into the function as parameters.

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


### Customizing the boolean icons

You may customize the [icon](https://filamentphp.com/docs/5.x/styling/icons.md) representing each state:

```php
use Filament\Infolists\Components\IconEntry;
use Filament\Support\Icons\Heroicon;

IconEntry::make('is_featured')
    ->boolean()
    ->trueIcon(Heroicon::OutlinedCheckBadge)
    ->falseIcon(Heroicon::OutlinedXMark)
```

As well as allowing static values, the ` trueIcon() ` and ` falseIcon() ` methods also accept functions to dynamically calculate them. You can inject various utilities into the functions as parameters.

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




### Customizing the boolean colors

You may customize the icon [color](https://filamentphp.com/docs/5.x/styling/colors.md) representing each state:

```php
use Filament\Infolists\Components\IconEntry;

IconEntry::make('is_featured')
    ->boolean()
    ->trueColor('info')
    ->falseColor('warning')
```

As well as allowing static values, the ` trueColor() ` and ` falseColor() ` methods also accept functions to dynamically calculate them. You can inject various utilities into the functions as parameters.

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
