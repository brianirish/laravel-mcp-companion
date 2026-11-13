Source: https://filamentphp.com/docs/5.x/advanced/enums.md

# Enum tricks

> Filament 5.x documentation
> Source: https://filamentphp.com/docs/5.x/advanced/enums.md

## Introduction

Enums are special PHP classes that represent a fixed set of constants. They are useful for modeling concepts that have a limited number of possible values, like days of the week, months in a year, or the suits in a deck of cards.

Since enum "cases" are instances of the enum class, adding interfaces to enums proves to be very useful. Filament provides a collection of interfaces that you can add to enums, which enhance your experience when working with them.

> [!WARNING]
> When using an enum with an attribute on your Eloquent model, please [ensure that it is cast correctly](https://laravel.com/docs/eloquent-mutators#enum-casting).

## Enum labels

The ` HasLabel ` interface transforms an enum instance into a textual label. This is useful for displaying human-readable enum values in your UI.

```php
use Filament\Support\Contracts\HasLabel;
use Illuminate\Contracts\Support\Htmlable;

enum Status: string implements HasLabel
{
    case Draft = 'draft';
    case Reviewing = 'reviewing';
    case Published = 'published';
    case Rejected = 'rejected';
    
    public function getLabel(): string | Htmlable | null
    {
        return $this->name;
        
        // or
    
        return match ($this) {
            self::Draft => 'Draft',
            self::Reviewing => 'Reviewing',
            self::Published => 'Published',
            self::Rejected => 'Rejected',
        };
    }
}
```

### Using the enum label with form field options

The ` HasLabel ` interface can be used to generate an array of options from an enum, where the enum's value is the key and the enum's label is the value. This applies to form fields like [` Select `](https://filamentphp.com/docs/5.x/forms/select.md) and [` CheckboxList `](https://filamentphp.com/docs/5.x/forms/checkbox-list.md), as well as the Table Builder's [` SelectColumn `](https://filamentphp.com/docs/5.x/tables/columns/select.md) and [` SelectFilter `](https://filamentphp.com/docs/5.x/tables/filters/select.md):

```php
use Filament\Forms\Components\CheckboxList;
use Filament\Forms\Components\Radio;
use Filament\Forms\Components\Select;
use Filament\Tables\Columns\SelectColumn;
use Filament\Tables\Filters\SelectFilter;

Select::make('status')
    ->options(Status::class)

CheckboxList::make('status')
    ->options(Status::class)

Radio::make('status')
    ->options(Status::class)

SelectColumn::make('status')
    ->options(Status::class)

SelectFilter::make('status')
    ->options(Status::class)
```

In these examples, ` Status::class ` is the enum class which implements ` HasLabel `, and the options are generated from that:

```php
[
    'draft' => 'Draft',
    'reviewing' => 'Reviewing',
    'published' => 'Published',
    'rejected' => 'Rejected',
]
```

### Using the enum label with a text column in your table

If you use a [` TextColumn `](https://filamentphp.com/docs/5.x/tables/columns/text.md) with the Table Builder, and it is cast to an enum in your Eloquent model, Filament will automatically use the ` HasLabel ` interface to display the enum's label instead of its raw value.

### Using the enum label as a group title in your table

If you use a [grouping](https://filamentphp.com/docs/5.x/tables/grouping.md) with the Table Builder, and it is cast to an enum in your Eloquent model, Filament will automatically use the ` HasLabel ` interface to display the enum's label instead of its raw value. The label will be displayed as the [title of each group](https://filamentphp.com/docs/5.x/tables/grouping.md#setting-a-group-title).

### Using the enum label with a text entry in your infolist

If you use a [` TextEntry `](https://filamentphp.com/docs/5.x/infolists/text-entry.md) in an infolist, and it is cast to an enum in your Eloquent model, Filament will automatically use the ` HasLabel ` interface to display the enum's label instead of its raw value.

## Enum colors

The ` HasColor ` interface transforms an enum instance into a [color](https://filamentphp.com/docs/5.x/styling/colors.md). This is useful for displaying colored enum values in your UI.

```php
use Filament\Support\Contracts\HasColor;

enum Status: string implements HasColor
{
    case Draft = 'draft';
    case Reviewing = 'reviewing';
    case Published = 'published';
    case Rejected = 'rejected';
    
    public function getColor(): string | array | null
    {
        return match ($this) {
            self::Draft => 'gray',
            self::Reviewing => 'warning',
            self::Published => 'success',
            self::Rejected => 'danger',
        };
    }
}
```

### Using the enum color with a text column in your table

If you use a [` TextColumn `](https://filamentphp.com/docs/5.x/tables/columns/text.md) with the Table Builder, and it is cast to an enum in your Eloquent model, Filament will automatically use the ` HasColor ` interface to display the enum label in its color. This works best if you use the [` badge() `](https://filamentphp.com/docs/5.x/tables/columns/text.md#displaying-as-a-badge) method on the column.

### Using the enum color with a text entry in your infolist

If you use a [` TextEntry `](https://filamentphp.com/docs/5.x/infolists/text-entry.md) in an infolist, and it is cast to an enum in your Eloquent model, Filament will automatically use the ` HasColor ` interface to display the enum label in its color. This works best if you use the [` badge() `](https://filamentphp.com/docs/5.x/infolists/text-entry.md#displaying-as-a-badge) method on the entry.

### Using the enum color with a toggle buttons field in your form

If you use a [` ToggleButtons `](https://filamentphp.com/docs/5.x/forms/toggle-buttons.md) form field, and it is set to use an enum for its options, Filament will automatically use the ` HasColor ` interface to display the enum label in its color.

## Enum icons

The ` HasIcon ` interface transforms an enum instance into an [icon](https://filamentphp.com/docs/5.x/styling/icons.md). This is useful for displaying icons alongside enum values in your UI.

```php
use BackedEnum;
use Filament\Support\Contracts\HasIcon;
use Filament\Support\Icons\Heroicon;
use Illuminate\Contracts\Support\Htmlable;

enum Status: string implements HasIcon
{
    case Draft = 'draft';
    case Reviewing = 'reviewing';
    case Published = 'published';
    case Rejected = 'rejected';

    public function getIcon(): string | BackedEnum | Htmlable | null
    {
        return match ($this) {
            self::Draft => Heroicon::Pencil,
            self::Reviewing => Heroicon::Eye,
            self::Published => Heroicon::Check,
            self::Rejected => Heroicon::XMark,
        };
    }
}
```

### Using the enum icon with a text column in your table

If you use a [` TextColumn `](https://filamentphp.com/docs/5.x/tables/columns/text.md) with the Table Builder, and it is cast to an enum in your Eloquent model, Filament will automatically use the ` HasIcon ` interface to display the enum's icon aside its label. This works best if you use the [` badge() `](https://filamentphp.com/docs/5.x/tables/columns/text.md#displaying-as-a-badge) method on the column.

### Using the enum icon with a text entry in your infolist

If you use a [` TextEntry `](https://filamentphp.com/docs/5.x/infolists/text-entry.md) in an infolist, and it is cast to an enum in your Eloquent model, Filament will automatically use the ` HasIcon ` interface to display the enum's icon aside its label. This works best if you use the [` badge() `](https://filamentphp.com/docs/5.x/infolists/text-entry.md#displaying-as-a-badge) method on the entry.

### Using the enum icon with a toggle buttons field in your form

If you use a [` ToggleButtons `](https://filamentphp.com/docs/5.x/forms/toggle-buttons.md) form field, and it is set to use an enum for its options, Filament will automatically use the ` HasIcon ` interface to display the enum's icon aside its label.

## Enum descriptions

The ` HasDescription ` interface transforms an enum instance into a textual description, often displayed under its [label](https://filamentphp.com/docs/5.x/advanced/enums.md#enum-labels). This is useful for displaying human-friendly descriptions in your UI.

```php
use Filament\Support\Contracts\HasDescription;
use Filament\Support\Contracts\HasLabel;
use Illuminate\Contracts\Support\Htmlable;

enum Status: string implements HasLabel, HasDescription
{
    case Draft = 'draft';
    case Reviewing = 'reviewing';
    case Published = 'published';
    case Rejected = 'rejected';
    
    public function getLabel(): string | Htmlable | null
    {
        return $this->name;
    }
    
    public function getDescription(): string | Htmlable | null
    {
        return match ($this) {
            self::Draft => 'This has not finished being written yet.',
            self::Reviewing => 'This is ready for a staff member to read.',
            self::Published => 'This has been approved by a staff member and is public on the website.',
            self::Rejected => 'A staff member has decided this is not appropriate for the website.',
        };
    }
}
```

### Using the enum description with form field descriptions

The ` HasDescription ` interface can be used to generate an array of descriptions from an enum, where the enum's value is the key and the enum's description is the value. This applies to form fields like [` Radio `](https://filamentphp.com/docs/5.x/forms/radio.md#setting-option-descriptions) and [` CheckboxList `](https://filamentphp.com/docs/5.x/forms/checkbox-list.md#setting-option-descriptions):

```php
use Filament\Forms\Components\CheckboxList;
use Filament\Forms\Components\Radio;

Radio::make('status')
    ->options(Status::class)

CheckboxList::make('status')
    ->options(Status::class)
```
