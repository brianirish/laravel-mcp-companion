Source: https://filamentphp.com/docs/5.x/tables/columns/icon.md

# Icon column

> Filament 5.x documentation
> Source: https://filamentphp.com/docs/5.x/tables/columns/icon.md

## Introduction

Icon columns render an [icon](https://filamentphp.com/docs/5.x/styling/icons.md) representing the state of the column:

```php
use Filament\Tables\Columns\IconColumn;
use Filament\Support\Icons\Heroicon;

IconColumn::make('status')
    ->icon(fn (string $state): Heroicon => match ($state) {
        'draft' => Heroicon::OutlinedPencil,
        'reviewing' => Heroicon::OutlinedClock,
        'published' => Heroicon::OutlinedCheckCircle,
    })
```

The ` icon() ` method can inject various utilities into the function as parameters.

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




## Customizing the color

You may change the [color](https://filamentphp.com/docs/5.x/styling/colors.md) of the icon, using the ` color() ` method:

```php
use Filament\Tables\Columns\IconColumn;

IconColumn::make('status')
    ->color('success')
```

By passing a function to ` color() `, you can customize the color based on the state of the column:

```php
use Filament\Tables\Columns\IconColumn;

IconColumn::make('status')
    ->color(fn (string $state): string => match ($state) {
        'draft' => 'info',
        'reviewing' => 'warning',
        'published' => 'success',
        default => 'gray',
    })
```

The ` color() ` method can inject various utilities into the function as parameters.

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




## Customizing the size

The default icon size is ` IconSize::Large `, but you may customize the size to be either ` IconSize::ExtraSmall `, ` IconSize::Small `, ` IconSize::Medium `, ` IconSize::ExtraLarge ` or ` IconSize::TwoExtraLarge `:

```php
use Filament\Tables\Columns\IconColumn;
use Filament\Support\Enums\IconSize;

IconColumn::make('status')
    ->size(IconSize::Medium)
```

As well as allowing a static value, the ` size() ` method also accepts a function to dynamically calculate it. You can inject various utilities into the function as parameters.

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




## Handling booleans

Icon columns can display a check or "X" icon based on the state of the column, either true or false, using the ` boolean() ` method:

```php
use Filament\Tables\Columns\IconColumn;

IconColumn::make('is_featured')
    ->boolean()
```

> If this attribute in the model class is already cast as a ` bool ` or ` boolean `, Filament is able to detect this, and you do not need to use ` boolean() ` manually.



Optionally, you may pass a boolean value to control if the icon should be boolean or not:

```php
use Filament\Tables\Columns\IconColumn;

IconColumn::make('is_featured')
    ->boolean(FeatureFlag::active())
```

As well as allowing a static value, the ` boolean() ` method also accepts a function to dynamically calculate it. You can inject various utilities into the function as parameters.

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


### Customizing the boolean icons

You may customize the [icon](https://filamentphp.com/docs/5.x/styling/icons.md) representing each state:

```php
use Filament\Tables\Columns\IconColumn;
use Filament\Support\Icons\Heroicon;

IconColumn::make('is_featured')
    ->boolean()
    ->trueIcon(Heroicon::OutlinedCheckBadge)
    ->falseIcon(Heroicon::OutlinedXMark)
```

As well as allowing static values, the ` trueIcon() ` and ` falseIcon() ` methods also accept functions to dynamically calculate them. You can inject various utilities into the functions as parameters.

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




### Customizing the boolean colors

You may customize the icon [color](https://filamentphp.com/docs/5.x/styling/colors.md) representing each state:

```php
use Filament\Tables\Columns\IconColumn;

IconColumn::make('is_featured')
    ->boolean()
    ->trueColor('info')
    ->falseColor('warning')
```

As well as allowing static values, the ` trueColor() ` and ` falseColor() ` methods also accept functions to dynamically calculate them. You can inject various utilities into the functions as parameters.

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




## Wrapping multiple icons

When displaying multiple icons, they can be set to wrap if they can't fit on one line, using ` wrap() `:

```php
use Filament\Tables\Columns\IconColumn;

IconColumn::make('icon')
    ->wrap()
```



> **Tip**
>
> The "width" for wrapping is affected by the column label, so you may need to use a shorter or hidden label to wrap more tightly.
